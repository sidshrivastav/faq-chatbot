# QA Summary — FAQ Knowledge Assistant

**Review date:** 2026-05-20
**Reviewer:** AI-assisted (Claude), Stage 7 QA
**Branch:** `001-faq-knowledge-assistant`
**Scope:** Full backend + frontend after all Stage 1–6 changes applied and archived.

---

## Test Suite Results (run in this session)

| Suite | Command | Result |
|---|---|---|
| Backend (all tests + coverage) | `pytest --cov=app --cov-report=term-missing --no-header -q` | **82 passed**, 5 warnings |
| Frontend (all tests) | `npm run test` | **35 passed** (8 test files) |
| Frontend build | `npm run build` | **Clean** — 917 ms, no errors |

Backend coverage: **94.45%** (target ≥ 70% ✅)

---

## Finding Index

| ID | Area | Severity | Status | Summary |
|---|---|---|---|---|
| S-01 | Security | Medium | AI-found | BOLA: user can join another user's conversation via `conversation_id` |
| S-02 | Security | Medium | AI-found | BOLA: user can submit feedback on any answer regardless of ownership |
| S-03 | Security | Low | Not run | Dependency vulnerability scan (`pip-audit`) not executed |
| S-04 | Security | Low | Accepted risk | CORS `allow_credentials=True` from localhost — local dev only |
| S-05 | Security | Low | Accepted risk | Trust-on-header auth model — local dev only, no JWT |
| S-06 | Security | Low | Accepted risk | Raw question text in LLM prompt — injection boundary not delimited |
| P-01 | Performance | Low | Not run | No load-test baseline; requires SQLite + real LLM provider first |
| P-02 | Performance | Low | Informational | Chat endpoint LLM call will dominate; retrieval is O(entries), negligible |
| P-03 | Performance | Medium | AI-found | `GET /admin/faq-sources` has no pagination — unbounded list |
| P-04 | Performance | Low | AI-found | `find_by_answer_and_user` is O(n) scan; needs index at SQLite layer |
| P-05 | Performance | Low | AI-found | `list_sources(active=True)` is O(n) scan; needs index at SQLite layer |
| P-06 | Performance | Low | Informational | Retrieval scoring O(entries × tokens) — acceptable at FAQ scale |
| CR-01 | Code quality | Low | AI-found | Dead branch: identical both sides of conditional in `answer_service.py:151` |
| CR-02 | Code quality | Medium | AI-found | `FakeLLMProvider` hardcoded at module level — no path to wire real provider |
| CR-03 | Code quality | Low | AI-found | `AnswerService` concretely typed to `InMemoryChatRepository` |
| CR-04 | Code quality | Low | AI-found | `use_case_name` is stub (`.upper()` of ID) |
| CR-05 | Code quality | Low | Informational | SQLite infrastructure exists but not wired (all repos in-memory) |
| OB-01 | Observability | High | AI-found | `log_event`/`get_logger` never called in production code — zero structured logs emitted |
| OB-02 | Observability | Medium | AI-found | No request logging middleware — routes, methods, roles not logged |
| OB-03 | Observability | Low | AI-found | LLM error at `answer_service.py:129` swallowed silently — not logged |
| TC-01 | Test coverage | Medium | AI-found | No test for cross-user conversation ownership (BOLA gap S-01) |
| TC-02 | Test coverage | Medium | AI-found | No test for cross-user feedback ownership (BOLA gap S-02) |
| TC-03 | Test coverage | Low | AI-found | `app/llm/provider.py` — 0% coverage (Protocol-only; acceptable) |
| DC-01 | Docs | Low | AI-found | `AGENTS.md` says "Use SQLite" but all repos are in-memory |

---

## Observability Findings (detail)

These did not appear in `docs/security.md` or `docs/code-review.md` and are recorded here.

### OB-01 — Structured logging infrastructure defined but never called
**Status:** AI-found
**Severity:** High
**Evidence:** `Grep` for `log_event|get_logger` across `backend/app/**` — only matched `app/services/logging.py` (definition) and `tests/unit/test_logging_events.py` (test). No production call site exists.

No lifecycle events (source create/activate/delete, question received, LLM called, feedback submitted) are currently logged. The logging infrastructure is complete and tested in isolation but has zero production wiring.

**Recommended fix:** Add `log_event(logger, "source_created", source_id=..., user_id=...)` calls to `source_service.py`, `answer_service.py`, `feedback_service.py`, and `auth/dependencies.py` for auth failures. This is the single highest-value observability improvement.

### OB-02 — No request logging middleware
**Status:** AI-found
**Severity:** Medium
**Evidence:** `backend/app/main.py` — no `@app.middleware("http")` block. Route, method, status code, and response time are not logged per request.

**Recommended fix:** Add a lightweight middleware that logs `{method, path, status_code, duration_ms}` at INFO level for every request.

### OB-03 — LLM error silently swallowed
**Status:** AI-found
**Severity:** Low
**File:** `backend/app/services/answer_service.py:129`

```python
except Exception:
    message = "The assistant is temporarily unavailable. Please try again."
    answer_state = AnswerState.ERROR
    ...
```

The exception is caught and the user receives a safe message, which is correct. However, the error is never logged, so LLM failures are invisible to operators.

**Recommended fix:** Add `log_event(logger, "llm_error", exc=str(exc), question_id=..., use_case_id=...)` inside the except block before proceeding to the fallback.

---

## Test Coverage Findings (detail)

### TC-01 — No cross-user conversation ownership test
**Status:** AI-found
**Severity:** Medium

No test in `test_chat_api.py` or `test_role_authorization.py` submits a question with a `conversation_id` owned by a different user and verifies a 403 response. This gap corresponds directly to S-01.

**Test to add (failing before fix):**
```python
def test_user_cannot_join_another_users_conversation() -> None:
    # user-1 creates a conversation, user-2 supplies conversation_id → 403
```

### TC-02 — No cross-user feedback ownership test
**Status:** AI-found
**Severity:** Medium

No test attempts feedback submission where the `answer_id` belongs to a different user's question. This gap corresponds directly to S-02.

### TC-03 — `app/llm/provider.py` at 0% coverage
**Status:** Informational (accepted)
**Reason:** `LLMProvider` is a `Protocol` with a single `generate` method stub. It exists for type-checking only. `FakeLLMProvider` is tested via `test_answer_service.py` and all chat API tests. No production implementation exists yet to test. Accepted.

---

## Documentation Consistency Findings

### DC-01 — `AGENTS.md` SQLite guidance does not match implementation
**Status:** AI-found
**Severity:** Low
**File:** `AGENTS.md:93` — "Use SQLite for local development persistence"

All three active repositories (`InMemoryFaqSourceRepository`, `InMemoryChatRepository`, `InMemoryFeedbackRepository`) are in-memory. `sqlite.py` and `base.py` exist but are not wired. The spec guidance is aspirational, not current.

**Recommended fix:** Update `AGENTS.md` to reflect current state: "Repositories currently use in-memory storage. SQLite wiring is a planned future stage."

Other documentation items passed:
- OpenAPI spec matches all implemented routes and schemas ✅
- Task log has entries for all task IDs (T032–T065) and all Stage 6 changes ✅
- Archive documents exist for `add-feedback-reasons` and `modify-active-source-deletion-policy` ✅
- Harness traces do not contain secrets or sensitive data ✅

---

## Area Pass/Fail Summary

| Area | Pass/Fail | Blocking? | Notes |
|---|---|---|---|
| Security | **Conditional pass** | Yes (before production) | S-01/S-02 are medium-severity BOLA gaps |
| Performance | **Conditional pass** | No (local dev only) | No pagination (P-03); baselines not captured |
| Code quality | **Pass** | No | CR-01/CR-02 are low/medium; architecture sound |
| Observability | **Fail** | No (local dev) | OB-01 is high severity — logging never fires in production |
| Test coverage | **Pass** | No | 94.45% backend, 35/35 frontend; TC-01/TC-02 are gaps |
| Documentation | **Pass** | No | DC-01 is minor wording inconsistency |

---

## Priority Action List

| Priority | Action | Finding |
|---|---|---|
| 1 | Wire `log_event` into services and auth dependency | OB-01 |
| 2 | Add ownership check in `ensure_conversation` + test | S-01, TC-01 |
| 3 | Add ownership check in `submit_feedback` + test | S-02, TC-02 |
| 4 | Add LLM provider factory with env-var selection | CR-02 |
| 5 | Add request logging middleware | OB-02 |
| 6 | Log LLM errors in the except block | OB-03 |
| 7 | Add pagination to `GET /admin/faq-sources` | P-03 |
| 8 | Remove dead conditional in `answer_service.py:151` | CR-01 |
| 9 | Add `pip-audit` to dev requirements and CI | S-03 |
| 10 | Update `AGENTS.md` SQLite guidance | DC-01 |
