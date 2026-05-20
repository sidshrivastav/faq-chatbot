# Code Review — FAQ Knowledge Assistant

**Review date:** 2026-05-20
**Reviewer:** AI-assisted (Claude), Stage 7 QA
**Status:** Two bugs found and fixed inline; five findings recorded for follow-up.

---

## Checklist Results

| Item | Result | Finding ID |
|---|---|---|
| Route handlers thin (no business logic) | Pass | — |
| Business logic in `services/` | Pass | — |
| Persistence in `repositories/` | Pass | — |
| Domain enums in `domain/` | Pass | — |
| LLM access isolated behind `llm/` | Pass | — |
| Pydantic v2 schemas for all API types | Pass | — |
| No arbitrary `dict` accepted | Pass | — |
| Cross-field validation via `model_validator` | Pass | — |
| Error messages safe (no secrets/traces exposed) | Pass | — |
| Frontend API calls in `services/` | Pass | — |
| Frontend states use text not color alone | Pass | — |
| No significant code duplication | Pass | — |
| No unused imports or dead code | **Fail** | CR-01, CR-02 |
| Service layer uses abstract types | **Fail** | CR-03 |
| `use_case_name` stub | **Fail** | CR-04 |
| SQLite infrastructure unused | Informational | CR-05 |

---

## Findings

### CR-01 — Dead branch: identical both sides of conditional expression
**Status:** AI-found
**Severity:** Low (correctness not affected, readability poor)
**File:** `backend/app/services/answer_service.py:151`

```python
# Both branches evaluate to the same value — the else branch is dead code.
retrieved_entries=response_entries if answer_state == AnswerState.ANSWERED else response_entries,
```

This was likely written as a placeholder for future branching (e.g., `[]` on error) but was never completed. The `answer_state == AnswerState.ERROR` path above already sets `response_entries = retrieval.retrieved_entries`, so including it in the answered branch is harmless but confusing.

**Recommended fix:** Simplify to `retrieved_entries=response_entries`. If the intent was to return `[]` on error, implement that explicitly.

---

### CR-02 — `FakeLLMProvider` hardcoded in module-level production code
**Status:** AI-found
**Severity:** Medium
**File:** `backend/app/api/chat.py:16`

```python
_llm_provider = FakeLLMProvider()
```

The `FakeLLMProvider` is instantiated at module level in the production API router. This means all users of the deployed application receive fake, FAQ-entry-verbatim responses. There is no configuration path to wire a real LLM provider without changing this line.

**Evidence:** `app/llm/provider.py` defines a `LLMProvider` Protocol and `FakeLLMProvider` conforms to it, but no factory, environment variable, or dependency injection mechanism exists to select between providers.

**Recommended fix:** Add an `LLM_PROVIDER` environment variable (defaulting to `"fake"` for local dev) and a provider factory function in `app/llm/`. Inject via FastAPI `Depends` or application startup so tests can override without patching.

---

### CR-03 — `AnswerService` is concretely coupled to `InMemoryChatRepository`
**Status:** AI-found
**Severity:** Low
**File:** `backend/app/services/answer_service.py:17, 26`

```python
class AnswerServiceDependencies:
    chat_repository: InMemoryChatRepository  # concrete type
```

`AnswerService.__init__` accepts `chat_repository: InMemoryChatRepository` and `FeedbackService` does the same. This couples the service layer to the in-memory implementation. When SQLite repositories are introduced, every service will require a signature change or an ABC/Protocol.

**Recommended fix:** Define a `ChatRepositoryProtocol` in `repositories/` with the methods the service needs (`ensure_conversation`, `save_question`, `save_answer`, `save_unanswered_question`). Type-hint against the Protocol.

---

### CR-04 — `use_case_name` is a stub (`.upper()` of the ID)
**Status:** AI-found
**Severity:** Low
**File:** `backend/app/services/source_service.py:54`

```python
use_case_name=payload.use_case_id.upper(),
```

Use case names are fabricated by uppercasing the `use_case_id` string (e.g., `"hr"` → `"HR"`). There is no use-case registry or lookup. The `GET /use-cases` endpoint returns use case objects, so a lookup is possible in principle.

This is acceptable as a placeholder but will produce incorrect names for any `use_case_id` that does not happen to read well uppercased (e.g., `"it_support"` → `"IT_SUPPORT"`).

**Recommended fix:** Introduce a `UseCaseRepository` or static registry and look up the display name from the ID when constructing `FaqSourceDetail`.

---

### CR-05 — SQLite infrastructure exists but is not wired
**Status:** Informational (accepted for this stage)
**File:** `backend/app/repositories/sqlite.py`, `backend/app/repositories/base.py`

`SQLiteRepository` and `Repository` Protocol are implemented but no repository class inherits from or uses them. All current repositories (`InMemoryFaqSourceRepository`, `InMemoryChatRepository`, `InMemoryFeedbackRepository`) are standalone in-memory implementations.

`AGENTS.md` states "Use SQLite for local development persistence" — the current state does not match this specification.

**Recommended action:** Track SQLite wiring as a future stage task. Before wiring, note that:
- `feedback.py` will need `ALTER TABLE feedback ADD COLUMN reason TEXT DEFAULT NULL`
- All in-memory `clear()` calls used in tests must remain functional via test fixtures

---

## Positive Observations

- Route handlers are uniformly thin: `auth dependency → service call → return schema`. No business logic leaks into any router. ✅
- Pydantic v2 `model_validator(mode="after")` is used correctly for the cross-field `reason`/`rating` validation in `FeedbackCreate`. ✅
- `FakeLLMProvider` design is clean — it records calls and supports `raise_on_generate` for error-path testing. ✅
- Domain enums use `StrEnum` throughout — serialization is consistent and explicit. ✅
- Frontend state components (`LoadingState`, `ErrorState`, `EmptyState`, `StatusBadge`) all use text labels — no color-only state signaling. ✅
- `AnswerFeedback.tsx` `ReasonSelector` is stateless (controlled by `selectedRating` prop), making it fully testable via `renderToStaticMarkup`. ✅
