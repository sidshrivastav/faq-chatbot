# Performance Review — FAQ Knowledge Assistant

**Review date:** 2026-05-20
**Reviewer:** AI-assisted (Claude), Stage 7 QA
**Status:** No load-testing tool installed; baseline metrics not captured. Architectural findings recorded.

---

## Baseline Metrics

**Status: Not run.**
**Reason:** No load-testing tool (`locust`, `hey`, `ab`) is installed, and the in-memory repositories reset on each `create_app()` call, making steady-state load measurement impractical without a persistent backend. All performance findings below are derived from static code analysis.

---

## Checklist Results

| Item | Result | Finding ID |
|---|---|---|
| P50/P95/P99 latency captured | Not run | P-01 |
| Chat answer endpoint bottleneck identified | Analytical | P-02 |
| FAQ source list pagination | **Fail** | P-03 |
| Feedback submission synchronous only | Pass | — |
| Analytics endpoint implemented | No — deferred | — |
| `find_by_answer_and_user` index | **Fail** | P-04 |
| `list_sources(active=True)` index | **Fail** | P-05 |
| Retrieval scoring complexity | Acceptable | P-06 |

---

## Findings

### P-01 — No load test baseline
**Status:** Not run
**Severity:** Low (accepted for this stage)

No tool installed to capture P50/P95/P99 latency. Given the in-memory repositories and `FakeLLMProvider`, response times will be sub-millisecond and not representative of production. Baseline measurements should be taken after SQLite persistence and a real LLM provider are wired.

**Recommended action:** Add `locust` or `hey` to dev tooling. Capture baselines before and after each optimization. Target: chat endpoint P95 < 2 s end-to-end (retrieval + LLM).

---

### P-02 — Chat endpoint: LLM call is the expected bottleneck
**Status:** AI-found (analytical)
**Severity:** Low
**File:** `backend/app/services/answer_service.py:124–133`

With a real LLM provider, `llm_provider.generate(prompt)` will dominate latency (typically 0.5–5 s for cloud APIs). Retrieval scoring (`RetrievalService._score_entry`) is O(entries × tokens) and will be negligible at FAQ scale (< 1000 entries). No optimization is needed in the retrieval layer before profiling with a real provider.

The `except Exception` bare catch at line 129 swallows the error and returns a graceful fallback — correct behavior, but the error is not logged (see observability review).

---

### P-03 — No pagination on `GET /admin/faq-sources`
**Status:** AI-found
**Severity:** Medium
**File:** `backend/app/api/faq_sources.py:31–39`

```python
@router.get("", response_model=FaqSourceListResponse)
def list_sources(...) -> FaqSourceListResponse:
    return FaqSourceListResponse(items=service.list_sources(...))
```

`list_sources` returns all matching sources in a single response with no `limit`/`offset` or cursor. For an admin managing hundreds of FAQ sources, this will produce large payloads and slow serialization.

**Recommended fix:** Add `limit: int = 50` and `offset: int = 0` query parameters; pass through to repository filter. Document the plan in a future `add-faq-source-pagination` OpenSpec change.

---

### P-04 — `find_by_answer_and_user` is O(n) linear scan
**Status:** AI-found
**Severity:** Low
**File:** `backend/app/repositories/feedback.py:29–33`

```python
def find_by_answer_and_user(self, *, answer_id: str, user_id: str) -> FeedbackRecord | None:
    for record in self._records.values():
        if record.answer_id == answer_id and record.user_id == user_id:
            return record
    return None
```

The in-memory feedback store is a flat dict. Duplicate-feedback detection scans all records on every submission. This will degrade as feedback volume grows.

**Recommended fix:** When SQLite is wired, add a unique index on `(answer_id, user_id)`. For the current in-memory store, add a secondary dict keyed by `(answer_id, user_id)` if performance profiling shows this as a hotspot.

---

### P-05 — `list_sources(active=True)` is O(n) linear scan
**Status:** AI-found
**Severity:** Low
**File:** `backend/app/repositories/faq_sources.py`

The in-memory source repository filters by `active=True` by iterating all stored sources. With a small number of FAQ sources (the expected scale for a single deployment), this is negligible. When SQLite is wired, add an index on `is_active`.

---

### P-06 — Retrieval scoring: O(entries × tokens), acceptable
**Status:** Informational
**File:** `backend/app/services/retrieval_service.py:56–71`

Each question causes a score to be computed for every valid entry in the active source. For a typical FAQ source of up to 200 entries and questions of up to 50 tokens, this is O(10,000) token comparisons — sub-millisecond in Python. No optimization required at current scale.

The `[:3]` cap on retrieved entries correctly limits LLM context size.
