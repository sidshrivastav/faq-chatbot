# AGENTS.md

Guidance for Codex and other AI agents implementing the Configurable FAQ Knowledge Assistant.

<!-- SPECKIT START -->
Primary implementation context lives in:

- `specs/001-faq-knowledge-assistant/spec.md`
- `specs/001-faq-knowledge-assistant/plan.md`
- `specs/001-faq-knowledge-assistant/tasks.md`
- `specs/001-faq-knowledge-assistant/data-model.md`
- `specs/001-faq-knowledge-assistant/contracts/openapi.yaml`
- `docs/design/`
- `docs/architecture.md`
<!-- SPECKIT END -->

Note: Older prompt references may mention `specs/faq-assistant/*`. In this repository, use `specs/001-faq-knowledge-assistant/*`.

## 1. Project Purpose

Build a configurable FAQ knowledge assistant for multiple use cases such as HR, IT support, product support, and admissions.

Admins manage FAQ sources, activate one source per use case, review unanswered questions, and inspect analytics. End users ask natural-language questions and receive grounded answers based only on the active FAQ source for the selected use case. Users can provide helpful or unhelpful feedback on answers and unanswered responses.

## 2. Repository Structure

Planned implementation structure:

```text
backend/
├── app/
│   ├── api/
│   ├── auth/
│   ├── domain/
│   ├── llm/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
└── tests/
    ├── api/
    ├── integration/
    ├── services/
    └── unit/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── styles/
│   └── App.tsx
└── tests/

docs/
├── architecture.md
├── design/
└── harness-traces/
```

Spec Kit artifacts are under `specs/001-faq-knowledge-assistant/`.

## 3. Setup Commands

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
pytest --cov=app --cov-report=term-missing
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm run test
```

Use the actual commands added during implementation if package scripts differ. Keep `docs/development.md` and `specs/001-faq-knowledge-assistant/quickstart.md` in sync with working commands.

## 4. Backend Conventions

- Use Python 3.11+.
- Use FastAPI for API routing.
- Use Pydantic v2 for request and response schemas.
- Use SQLite for local development persistence.
- Keep business logic in `backend/app/services/`, not route handlers.
- Keep persistence access in `backend/app/repositories/`.
- Keep domain enums and state-transition helpers in `backend/app/domain/`.
- Keep route handlers thin: validate input, enforce auth dependency, call a service, return a schema.
- Preserve source-at-time context for questions, answers, feedback, and analytics.
- Implement deterministic retrieval before any LLM boundary call.

## 5. Frontend Conventions

- Use React + Tailwind CSS.
- Follow Stage 2 design docs and prototype under `docs/design/`.
- Keep API calls in `frontend/src/services/`.
- Keep shared UI states in `frontend/src/components/common/`.
- Keep feedback controls in `frontend/src/components/feedback/`.
- Keep page-level workflows under `frontend/src/pages/`.
- All active, invalid, helpful, unhelpful, loading, empty, and error states must be conveyed with text, not color alone.
- Preserve typed response handling for API success and error responses.

## 6. Testing Requirements

- Backend tests use pytest.
- Backend API test coverage target: 70%+.
- Include tests for source management, grounded chat, feedback, analytics, unanswered review, and role authorization.
- Do not call real LLM APIs in automated tests.
- Mock or fake the LLM client in all tests.
- Test both success and failure states.
- Test admin and end-user role behavior.
- Test that users cannot access other users' chat sessions.
- Test that inactive, invalid, archived, or different-use-case FAQ sources are excluded from answers.

## 7. TDD Workflow

Tests come before implementation.

For each task:

1. Write the smallest meaningful failing test.
2. Run the focused test and confirm it fails for the expected reason.
3. Implement the minimum code needed to pass.
4. Run the focused test again.
5. Run the relevant broader test set.
6. Refactor only after tests pass.
7. Update docs or contracts if behavior changes.

Do not skip the failing-test step for backend behavior, role checks, retrieval, LLM boundary behavior, or source state transitions.

## 8. FastAPI-Specific Rules

- Use routers grouped by domain: health, me, use cases, FAQ sources, chat, feedback, analytics, unanswered questions.
- Use FastAPI dependencies for authentication and role checks.
- Private endpoints require authentication.
- Admin-only endpoints require admin role checks.
- Use consistent error response schemas.
- Do not embed business rules in route handlers.
- Register shared exception handlers in `backend/app/main.py`.
- Return Pydantic response models for public API contracts.
- Keep request and response models explicit.

## 9. Pydantic v2 Rules

- Use Pydantic v2 APIs and idioms.
- Prefer `BaseModel` schemas for request/response contracts.
- Use `field_validator` or `model_validator` where validation is schema-level.
- Keep domain state-transition validation in services/domain helpers when it depends on persisted state.
- Avoid accepting arbitrary dictionaries when a typed schema is possible.
- Ensure error messages are safe for users and do not expose secrets or internal stack traces.

## 10. LLM Integration Rules

- The LLM is accessed only through `backend/app/llm/`.
- Route handlers must never call LLM providers directly.
- Retrieval must happen before LLM generation.
- The LLM must receive only retrieved entries from the active FAQ source for the selected use case.
- If no relevant FAQ source content exists, return a safe fallback and record the unanswered question.
- If no active source exists, return a no-active-source response and record the unanswered question.
- Automated tests must use a fake provider.
- Do not import or configure real provider clients in unit/API tests.
- Treat LLM output as untrusted; validate answer state and grounding before persistence.
- Vector search is a future improvement, not part of the first implementation.

## 11. Security Rules

- Do not commit secrets.
- Do not store API keys in code, tests, fixtures, or docs.
- Keep `.env.example` free of real secret values.
- Enforce backend role checks even if frontend navigation hides pages.
- Admin-only endpoints include FAQ source management, activation/deactivation/archive/delete, analytics, and unanswered question review.
- End-user allowed endpoints include use case listing, chat question submission, and feedback submission.
- Users must not access other users' chat sessions.
- Answers must be grounded in active FAQ sources only.
- Inactive, archived, invalid, or different-use-case sources must not be used for answer generation.
- Unauthorized and forbidden responses must use safe user-facing messages.

## 12. Observability Rules

Use structured logs for:

- Request route, method, role, and correlation/request id when available
- Authorization failures
- FAQ source create/update/activate/deactivate/archive/delete
- FAQ source readiness validation
- Chat question submission
- Retrieval result and unsupported reason
- LLM boundary called, skipped, failed, or fake-provider used
- Answer persisted with answer state
- Feedback submitted with rating
- Analytics requested with filters
- Unanswered questions listed or reviewed

Avoid logging unnecessary full question/answer content. Never log secrets.

## 13. AI Collaboration Conventions

- Read the relevant spec, plan, tasks, and design docs before editing.
- Prefer the task order in `specs/001-faq-knowledge-assistant/tasks.md`.
- Use the custom `test-writer` skill before implementing any backend or frontend feature.
- Keep edits scoped to the task.
- Do not refactor unrelated files.
- Do not alter contracts casually; update tests, docs, and dependent code together when contract changes are required.
- Preserve existing user changes.
- Use clear commit boundaries around completed logical work.
- If a requested path does not exist, verify the active Spec Kit feature path before proceeding.

## Custom Skill: test-writer

Use `docs/skills/test-writer.md` before implementation tasks that touch backend or frontend behavior.

The `test-writer` skill requires Codex to:

- Produce a test plan before implementation.
- Write failing tests before production code.
- Include backend tests when backend behavior changes.
- Include frontend tests when UI behavior changes.
- Mock or fake LLM behavior in all automated tests.
- Cover authorization, validation, not-found, cross-user access, LLM failure, no-relevant-source, feedback, analytics, and regression cases where applicable.
- Record representative harness traces under `docs/harness-traces/` for risky or assessment-representative tasks.

## 14. Harness Workflow: Brainstorm -> Plan -> Implement -> Verify

Use this workflow for meaningful implementation work:

1. **Brainstorm**: Identify the user story, acceptance criteria, affected modules, risks, and test cases.
2. **Plan**: Select the next task from `tasks.md`, define files to edit, and identify the verification command.
3. **Implement**: Write failing tests first, implement the code, and keep business logic in services.
4. **Verify**: Run focused tests, then broader tests where useful. Record results and unresolved gaps.

Representative harness trace areas:

- Role-based authorization
- FAQ source management
- Grounded chat with mocked LLM integration

## 15. Harness Trace Preservation

Preserve implementation traces under:

```text
docs/harness-traces/
```

For representative or risky tasks, create a concise trace file named:

```text
docs/harness-traces/TASK-ID-short-name.md
```

Each trace should include:

- Task ID and title
- Brainstorm notes
- Plan and files touched
- Tests written before implementation
- Implementation summary
- Verification commands and outcomes
- Any deviations or follow-up risks

Do not include secrets, real tokens, private user data, or full LLM prompts containing sensitive content in harness traces.
