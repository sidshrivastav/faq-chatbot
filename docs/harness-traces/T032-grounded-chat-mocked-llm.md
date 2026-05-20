# Harness Trace: T032 Grounded Chat with Mocked LLM Integration

## Task

T032 [US2] Harness trace task: write failing service tests for deterministic retrieval and mocked LLM boundary in `backend/tests/services/test_answer_service.py`.

## Phase / User Story

Phase 4, User Story 2: Ask Grounded Questions.

## Brainstorm

- Put the retrieval and LLM boundary behind a small answer service so the tests can assert call order and grounding separately.
- Keep a fake provider with call tracking so the tests can prove no external LLM is used.
- Store unanswered question records for unsupported and no-active-source paths so later admin review tasks have context.

## Selected Approach

Use a single answer service backed by a deterministic retrieval service, an in-memory chat repository, and a fake LLM provider. The service returns grounded answers when retrieval finds an active-source match, skips the provider when retrieval is insufficient, and records unanswered cases.

## Plan

1. Write failing backend service tests for:
   - grounded answer path
   - unsupported question path
   - no active source path
   - provider failure path
2. Add chat schemas, retrieval service, fake provider, answer service, and chat repository.
3. Run the focused backend tests, then the full backend and frontend verification.

## Test Plan

- Happy path: a covered HR question calls the fake provider with retrieved entries from the active HR source.
- Cross-use-case exclusion: an active IT source is ignored for an HR question.
- No active source: the service returns `no_active_source`, skips the provider, and records the unanswered question.
- LLM failure: the fake provider raises and the service returns a safe `error` state.

## Failing Test Evidence

Initial failures were expected and confirmed before implementation:

```text
ModuleNotFoundError: No module named 'app.llm'
```

```text
Failed to load url ../src/pages/chat/ChatPage
Failed to load url ../../src/services/chat
```

Those failures showed the chat service stack and frontend chat imports were still missing.

## Implementation Summary

- Added `backend/app/schemas/chat.py` for question and chat response models.
- Added `backend/app/llm/` with the provider protocol, prompt builder, and fake provider.
- Added `backend/app/repositories/chat.py` for in-memory conversation, question, answer, and unanswered records.
- Added `backend/app/services/retrieval_service.py` with deterministic lexical matching and active-source filtering.
- Added `backend/app/services/answer_service.py` to orchestrate retrieval, fake LLM generation, unsupported handling, and no-active-source handling.
- Added `backend/app/api/chat.py` and registered it in `backend/app/main.py`.
- Added frontend chat service adapters and the static chat screen.

## Verification Commands

- `backend/.venv/bin/pytest backend/tests/services/test_answer_service.py backend/tests/api/test_chat_api.py`
- `backend/.venv/bin/pytest`
- `npm run test -- ChatPage.test.tsx services/chat.test.ts`
- `npm run test`
- `npm run build`
- `python3 -m compileall backend/app`

## Final Result

The chat story is implemented and verified. Grounded answers use deterministic retrieval first, unsupported and no-active-source paths skip the LLM, and the fake provider is used in tests only.

## AI Mistake or Risk Found

The first retrieval pass matched on common words like `how`, `do`, and `i`, which made unsupported questions look grounded. The unanswered-question repository was also keyed by unanswered record ID instead of question ID, which did not match the test expectation.

## Human Correction or Judgment

I tightened the retrieval matcher by dropping stopwords and keyed unanswered records by question ID so the chat tests reflect the intended behavior and later review flows have a stable lookup path.

## Files Changed

- `backend/app/schemas/chat.py`
- `backend/app/llm/__init__.py`
- `backend/app/llm/provider.py`
- `backend/app/llm/prompt_builder.py`
- `backend/app/llm/fake_provider.py`
- `backend/app/repositories/chat.py`
- `backend/app/services/retrieval_service.py`
- `backend/app/services/answer_service.py`
- `backend/app/api/chat.py`
- `backend/app/main.py`
- `frontend/src/services/chat.ts`
- `frontend/src/services/useCases.ts`
- `frontend/src/pages/chat/ChatPage.tsx`
- `backend/tests/services/test_answer_service.py`
- `backend/tests/api/test_chat_api.py`
- `frontend/tests/ChatPage.test.tsx`
- `frontend/tests/services/chat.test.ts`

## Suggested Commit Message

`Add grounded chat workflow`
