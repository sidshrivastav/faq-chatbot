# Security Review — FAQ Knowledge Assistant

**Review date:** 2026-05-20
**Reviewer:** AI-assisted (Claude), Stage 7 QA
**Status:** All findings recorded. Two medium-severity items require follow-up before production.

---

## Checklist Results

| Item | Result | Finding ID |
|---|---|---|
| Admin-only routes require `require_admin` | Pass | — |
| Authenticated routes require `get_current_user` | Pass | — |
| Unauthenticated → 401 | Pass | — |
| End-user → 403 on admin routes | Pass | — |
| Cross-user chat session access prevention | **Fail** | S-01 |
| Cross-user feedback access prevention | **Fail** | S-02 |
| Input validation via Pydantic schemas | Pass | — |
| No real secrets in code/tests/fixtures | Pass | — |
| `.env.example` free of real secrets | Pass (no `.env` exists — not yet needed) | — |
| Dependency vulnerability scan | **Not run** | S-03 |
| CORS configuration reviewed | Informational | S-04 |
| OWASP API1 (BOLA) | **Fail** | S-01, S-02 |
| OWASP API2 (Broken Authentication) | Pass (local-dev model; see S-05) | S-05 |
| OWASP API5 (Broken Function Level Authorization) | Pass | — |
| OWASP API8 (Security Misconfiguration) | Informational | S-04 |
| Prompt injection risk | Informational | S-06 |
| LLM data leakage | Pass | — |
| Sensitive data logged | Pass (logging not wired — see observability) | — |

---

## Findings

### S-01 — BOLA: User can attach to another user's conversation
**Status:** AI-found
**Severity:** Medium
**File:** `backend/app/repositories/chat.py:72–75`

`ensure_conversation` accepts a caller-supplied `conversation_id` and re-opens the conversation without verifying that `conversation.user_id == requesting_user_id`. A user who discovers another user's `conversation_id` can submit questions into that conversation and read its context indirectly through retrieved entries.

```python
# chat.py:72–75 — no ownership check
if conversation_id and conversation_id in self.conversations:
    conversation = self.conversations[conversation_id]
    conversation.updated_at = now
    return conversation
```

**Evidence:** No ownership assertion exists in `ensure_conversation`. No test covers cross-user `conversation_id` injection. `test_role_authorization.py` tests role-based access but not object-level ownership.

**Recommended fix:** Before returning an existing conversation, assert `conversation.user_id == user_id` and raise a 403 if they differ.

---

### S-02 — BOLA: User can submit feedback on any answer
**Status:** AI-found
**Severity:** Medium
**File:** `backend/app/services/feedback_service.py:33–35`

`submit_feedback` verifies the `answer_id` exists in `chat_repository.answers` but does not check that the answer belongs to a conversation owned by `user_id`. Any authenticated user who knows an `answer_id` can submit feedback on another user's answer.

```python
# feedback_service.py:33–35 — existence check only, no ownership check
answer = self.chat_repository.answers.get(answer_id)
if answer is None:
    raise AnswerNotFoundError(answer_id)
```

**Evidence:** `test_feedback_api.py` tests duplicate feedback and not-found, but no test attempts cross-user feedback submission. The `AnswerRecord` dataclass does not store `user_id` so ownership cannot be verified without tracing back through `question → conversation → user_id`.

**Recommended fix:** Add `question_id` → `QuestionRecord` → `conversation_id` → `ConversationRecord.user_id` lookup; raise 403 if `conversation.user_id != user_id`.

---

### S-03 — Dependency vulnerability scan not run
**Status:** Not run
**Severity:** Low
**Reason:** `pip-audit` and `safety` are not installed in the backend virtualenv. The requirements file pins three direct dependencies (`fastapi>=0.115`, `pydantic>=2.8`, `uvicorn>=0.30`). No known CVEs exist against these version ranges as of the review date, but this has not been programmatically verified.

**Recommended fix:** Add `pip-audit` to `requirements-dev.txt` and run `pip-audit` in CI.

---

### S-04 — CORS allows credentials from localhost origins
**Status:** Informational (accepted risk for local dev)
**Severity:** Low
**File:** `backend/app/main.py:29–35`

```python
CORSMiddleware(
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

`allow_credentials=True` with explicit localhost origins is safe for local development. This configuration must be replaced with an environment-variable-driven allowlist before any production deployment.

**Recommended action:** Document this as a pre-production task. No code change required now.

---

### S-05 — Auth uses trust-on-header model (no JWT)
**Status:** Informational (accepted risk for local dev)
**Severity:** Low
**File:** `backend/app/auth/dependencies.py:17–39`

Authentication is based entirely on `x-user-id`, `x-user-email`, and `x-user-role` headers sent by the client. Any client can claim any identity. This is intentional for the local-dev assessment context but would be a critical vulnerability in a networked deployment.

**Recommended action:** Document this as a pre-production requirement. Gate real user sessions behind a JWT/session-cookie layer before exposing to a network.

---

### S-06 — Raw question text reaches LLM prompt
**Status:** Informational (accepted risk)
**Severity:** Low
**File:** `backend/app/llm/prompt_builder.py:28–36`

`question_text` from the user is included verbatim in `AnswerPrompt`. The current `FakeLLMProvider` never sends this to a real model, so there is no active prompt injection risk. When a real provider is wired, the prompt should clearly delimit user-supplied content from system context (e.g., via role-separated messages in the Chat Completions API).

**Recommended action:** When implementing a real LLM provider, use system/user message separation and document the injection boundary.
