# test-writer Skill

## Purpose

The `test-writer` skill helps Codex follow TDD during implementation of the Configurable FAQ Knowledge Assistant. It generates a focused test plan and failing tests before implementation begins.

Use this skill to translate an implementation task into concrete backend and frontend test scenarios, including authorization, validation, LLM mocking, grounded-answer behavior, and regression coverage. The expected output is a set of deterministic tests that fail for the intended reason before production code is written.

## When to Use

Use before each implementation task from `specs/001-faq-knowledge-assistant/tasks.md`.

Older prompts may refer to `specs/faq-assistant/tasks.md`; in this repository, use `specs/001-faq-knowledge-assistant/tasks.md`.

Use especially before tasks involving:

- Role-based authorization
- FAQ source management
- Grounded chat and retrieval
- LLM integration boundaries
- Answer feedback
- Admin analytics
- Unanswered-question tracking
- Frontend loading, empty, error, and feedback states

## Inputs

Provide these inputs before writing tests:

- Task ID
- Task description
- Related acceptance criteria
- Related spec or plan section
- Existing code files
- Expected behavior
- Known edge cases

If any input is missing, inspect the relevant artifact first:

- `specs/001-faq-knowledge-assistant/spec.md`
- `specs/001-faq-knowledge-assistant/plan.md`
- `specs/001-faq-knowledge-assistant/tasks.md`
- `specs/001-faq-knowledge-assistant/contracts/openapi.yaml`
- `docs/architecture.md`
- `docs/design/`

## Outputs

Produce these outputs before implementation:

- Test plan
- Backend tests when applicable
- Frontend tests when applicable
- Mocking strategy
- Authorization test cases
- Validation test cases
- Edge cases
- Verification commands

The test plan should state:

- What behavior is being protected
- Which acceptance criteria are covered
- Which files will receive tests
- Which tests should fail before implementation
- Which command verifies the work

## Required Test Categories

Include relevant cases from this list for each task:

1. Happy path
2. Validation failures
3. Authentication failures
4. Authorization failures
5. Not-found cases
6. Cross-user access prevention
7. LLM failure behavior
8. No relevant FAQ source behavior
9. Feedback and analytics behavior where applicable
10. Regression cases for previous bugs

If a category does not apply, say why in the test plan rather than silently omitting it.

## LLM Testing Rules

- Never call real LLM APIs in automated tests.
- Mock the LLM client/service.
- Test fallback behavior when the LLM fails.
- Test that answers are only generated after FAQ retrieval.
- Test that no unsupported answer is returned when no relevant FAQ source exists.
- Test that no LLM call is made when there is no active source or retrieval returns insufficient context.
- Test that the LLM receives only retrieved entries from the active FAQ source for the selected use case.

## FastAPI Testing Rules

- Use pytest.
- Use FastAPI TestClient or async test client as appropriate.
- Test status codes and response bodies.
- Test request validation errors.
- Test authenticated and unauthenticated requests.
- Test admin-only endpoints with both admin and end-user accounts.
- Test private endpoints without authentication.
- Test stable error codes and safe user-facing messages.
- Keep route tests focused on API behavior; put business-rule permutations in service tests.

## Frontend Testing Rules

- Test main user flows.
- Test loading states.
- Test error states.
- Test empty states.
- Test feedback interactions.
- Mock API calls.
- Test role-aware navigation and unauthorized states where applicable.
- Test that active, invalid, helpful, unhelpful, and unsupported states are represented with text, not color alone.
- Test that user input is preserved after recoverable errors where the design requires it.

## Test Quality Checklist

Before implementation starts, confirm:

- Tests are deterministic.
- Tests do not depend on external services.
- Tests map to acceptance criteria.
- Tests fail before implementation.
- Tests cover important edge cases.
- Tests are readable and maintainable.
- LLM behavior is mocked or faked.
- Tests do not require secrets.
- Backend API coverage impact supports the 70%+ target.

## Example Invocation

Task: Grounded chat with mocked LLM integration

Input:

```text
Task ID: T032
Task description: Harness trace task: write failing service tests for deterministic retrieval and mocked LLM boundary in backend/tests/services/test_answer_service.py
Related acceptance criteria:
- Covered questions receive grounded answers from the active FAQ source.
- Unsupported questions do not invent answers and are recorded as unanswered.
- Inactive or different-use-case sources are excluded.
Related plan section:
- LLM Integration Boundary
- Retrieval Strategy
Existing files:
- backend/app/services/answer_service.py
- backend/app/services/retrieval_service.py
- backend/app/llm/fake_provider.py
Expected behavior:
- Retrieval runs before generation.
- Fake LLM is called only when retrieval returns sufficient active-source context.
- Unsupported and no-active-source paths skip the LLM.
Known edge cases:
- No active source
- Active source has no matching entries
- Matching entry belongs to another use case
- LLM provider raises an error
```

Codex should first produce a test plan:

```text
Test plan:
1. Happy path: active HR source has matching FAQ entry; answer service calls fake LLM once with retrieved entry.
2. No relevant source: active HR source has no matching entry; answer state is unsupported and fake LLM is not called.
3. No active source: answer state is no_active_source and unanswered record is created.
4. Cross-source isolation: IT source entry is not used for HR question.
5. LLM failure: fake provider raises; service returns safe error/fallback behavior and records answer state.

Test file:
- backend/tests/services/test_answer_service.py

Verification command:
- pytest backend/tests/services/test_answer_service.py
```

Then Codex should write failing tests only. After confirming the tests fail for the expected reason, Codex may proceed to implementation in a separate step or task. The implementation step must not call real LLM APIs.
