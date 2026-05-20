# Tasks: Configurable FAQ Knowledge Assistant

**Input**: Design documents from `specs/001-faq-knowledge-assistant/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: TDD is required for this task set. Write the listed test tasks first, verify they fail, then implement. Do not call real LLM APIs in automated tests.

**Task sizing**: Each task is scoped to 1-4 hours.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks in the same phase after dependencies are met
- **[Story]**: User story label for story phases only
- **Harness trace task**: Representative task that should be captured in implementation traces
- **Test scenario**: Included in every task description

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize backend, frontend, tooling, and shared documentation structure.

- [x] T001 Create backend project skeleton in `backend/app/main.py`, `backend/app/api/__init__.py`, `backend/app/schemas/__init__.py`, `backend/app/services/__init__.py`, and `backend/tests/conftest.py` (Est: 2h; test scenario: `python -m compileall backend/app` succeeds)
- [x] T002 Create backend dependency files in `backend/requirements.txt` and `backend/requirements-dev.txt` for FastAPI, Pydantic v2, pytest, coverage, and SQLite support (Est: 1h; test scenario: dependency install command can resolve all packages)
- [x] T003 [P] Create frontend React/Tailwind project skeleton in `frontend/src/App.tsx`, `frontend/src/main.tsx`, `frontend/src/styles/index.css`, and `frontend/package.json` (Est: 3h; test scenario: `npm run build` reaches the expected missing-implementation boundary or succeeds after dependencies install)
- [x] T004 [P] Configure backend pytest and coverage defaults in `backend/pyproject.toml` with 70%+ API coverage target documented (Est: 1h; test scenario: `pytest --collect-only` discovers tests without import errors)
- [x] T005 [P] Configure frontend lint/build scripts in `frontend/package.json` and Tailwind config in `frontend/tailwind.config.js` (Est: 2h; test scenario: `npm run build` uses Tailwind entrypoint without CSS import errors)
- [x] T006 [P] Create local environment example files in `backend/.env.example` and `frontend/.env.example` without real secrets (Est: 1h; test scenario: app startup documents required variables without secret values)
- [x] T007 [P] Create developer command notes in `docs/development.md` for backend tests, frontend build, local run, and no-real-LLM-test rule (Est: 2h; test scenario: commands listed match `quickstart.md`)
- [x] T008 Create root-level ignore and placeholder directories in `.gitignore`, `backend/tests/api/.gitkeep`, `backend/tests/services/.gitkeep`, `frontend/tests/.gitkeep` (Est: 1h; test scenario: generated caches and SQLite files are ignored)

**Checkpoint**: Project skeleton and tooling conventions are ready.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend/frontend contracts, persistence, auth shell, error handling, logging, and API client foundations required before any user story implementation.

**Critical**: No user story work should start until this phase is complete.

- [x] T009 Write failing backend smoke API tests in `backend/tests/api/test_health_and_errors.py` for `GET /health` and shared error response shape (Est: 1h; test scenario: tests fail before route/error handler implementation)
- [x] T010 Implement FastAPI app factory, health route, CORS setup, and shared exception handlers in `backend/app/main.py` and `backend/app/api/health.py` (Est: 2h; test scenario: T009 passes with `pytest backend/tests/api/test_health_and_errors.py`)
- [x] T011 [P] Define shared domain enums in `backend/app/domain/enums.py` for roles, FAQ source status, readiness state, answer state, feedback rating, and unanswered reason (Est: 1h; test scenario: enum unit tests reject unsupported values)
- [x] T012 [P] Define base Pydantic schemas and error schema in `backend/app/schemas/common.py` (Est: 2h; test scenario: schema tests validate required `code` and `message` fields)
- [x] T013 Write failing repository tests in `backend/tests/unit/test_sqlite_repository.py` for SQLite connection lifecycle and transaction rollback (Est: 2h; test scenario: rollback test fails before repository implementation)
- [x] T014 Implement SQLite repository/session helpers in `backend/app/repositories/sqlite.py` and `backend/app/repositories/base.py` (Est: 3h; test scenario: T013 passes against a temporary SQLite database)
- [x] T015 [P] Write failing auth dependency tests in `backend/tests/unit/test_auth_dependencies.py` for admin, end-user, and unauthorized role cases (Est: 2h; test scenario: tests fail before auth dependency implementation)
- [x] T016 Implement local-development auth dependencies in `backend/app/auth/dependencies.py` and `backend/app/auth/models.py` (Est: 2h; test scenario: T015 passes and unauthorized access returns consistent error shape)
- [x] T017 [P] Create frontend API client foundation in `frontend/src/services/apiClient.ts` with typed success/error handling (Est: 2h; test scenario: client unit test covers success and error response adaptation)
- [x] T018 [P] Create shared frontend UI primitives in `frontend/src/components/common/StatusBadge.tsx`, `EmptyState.tsx`, `ErrorState.tsx`, and `LoadingState.tsx` (Est: 3h; test scenario: component tests render accessible labels for each state)
- [x] T019 [P] Configure structured logging helpers in `backend/app/services/logging.py` for source, chat, feedback, analytics, and authorization events (Est: 2h; test scenario: unit test captures structured log fields)
- [x] T020 Document foundation verification commands in `docs/development.md` for `pytest`, coverage, and frontend build (Est: 1h; test scenario: commands align with generated project paths)

**Checkpoint**: Foundation ready; user story implementation can start.

---

## Phase 3: User Story 1 - Manage FAQ Sources (Priority: P1) MVP

**Goal**: Admins can create, upload/edit, review, activate, deactivate, archive, delete, and list FAQ sources by use case.

**Independent Test**: As an admin, add a valid HR source, activate it, update it, deactivate it, and confirm the source list/detail state reflects each change.

### Tests for User Story 1

- [x] T021 [P] [US1] Write failing API contract tests for FAQ source list/create/detail/update/delete in `backend/tests/api/test_faq_sources_api.py` (Est: 3h; test scenario: admin succeeds and end user receives 403 for admin source routes)
- [x] T022 [P] [US1] Harness trace task: write failing API tests for FAQ source activation/deactivation conflict handling in `backend/tests/api/test_faq_source_activation.py` (Est: 3h; test scenario: activating a ready source makes it active and deactivates any previous active source for that use case)
- [x] T023 [P] [US1] Write failing service tests for source readiness and invalid entries in `backend/tests/services/test_source_service.py` (Est: 2h; test scenario: empty, duplicate, and unreadable-like entries produce invalid or warning readiness)
- [x] T024 [P] [US1] Write failing frontend tests for source list states in `frontend/tests/FaqSourcesList.test.tsx` (Est: 2h; test scenario: default, empty, loading, invalid-source, and error states render)

### Implementation for User Story 1

- [x] T025 [P] [US1] Implement FAQ source and FAQ entry schemas in `backend/app/schemas/faq_source.py` (Est: 2h; test scenario: schema rejects missing source name, use case, and entry answer text)
- [x] T026 [US1] Implement FAQ source repository operations in `backend/app/repositories/faq_sources.py` (Est: 3h; test scenario: repository persists source, entries, active flag, readiness, and timestamps)
- [x] T027 [US1] Implement FAQ source service state transitions in `backend/app/services/source_service.py` (Est: 4h; test scenario: T023 passes for create/update/activate/deactivate/archive/delete transitions)
- [x] T028 [US1] Implement admin FAQ source routes in `backend/app/api/faq_sources.py` and register them in `backend/app/main.py` (Est: 3h; test scenario: T021 and T022 pass with admin role and reject end-user role)
- [x] T029 [P] [US1] Implement FAQ Sources List screen in `frontend/src/pages/admin/FaqSourcesList.tsx` using Stage 2 filters and states (Est: 3h; test scenario: T024 passes and source status text is not color-only)
- [x] T030 [P] [US1] Implement FAQ Source Detail screen in `frontend/src/pages/admin/FaqSourceDetail.tsx` with readiness, warnings, activation, deactivation, archive, and delete affordances (Est: 4h; test scenario: component test renders active, invalid, archived, and activation-conflict states)
- [x] T031 [US1] Wire frontend source API functions in `frontend/src/services/faqSources.ts` to list/detail/create/update/activate/deactivate/archive/delete contracts (Est: 2h; test scenario: mocked client calls use the paths in `contracts/openapi.yaml`)

**Verification commands**: `pytest backend/tests/api/test_faq_sources_api.py backend/tests/api/test_faq_source_activation.py backend/tests/services/test_source_service.py`; `npm run test -- FaqSourcesList`

**Checkpoint**: US1 is independently functional and demoable as MVP.

---

## Phase 4: User Story 2 - Ask Grounded Questions (Priority: P1)

**Goal**: End users can ask natural-language questions in a selected use case and receive grounded answers, unsupported messages, or no-active-source messages.

**Independent Test**: Activate a known FAQ source, ask covered and unsupported questions, and verify only the active source is used.

### Tests for User Story 2

- [ ] T032 [P] [US2] Harness trace task: write failing service tests for deterministic retrieval and mocked LLM boundary in `backend/tests/services/test_answer_service.py` (Est: 3h; test scenario: covered question calls fake LLM with active-source entries and unsupported question skips LLM)
- [ ] T033 [P] [US2] Write failing API tests for `POST /chat/questions` in `backend/tests/api/test_chat_api.py` (Est: 3h; test scenario: answered, unsupported, no-active-source, and inactive-source exclusion responses match contract)
- [ ] T034 [P] [US2] Write failing frontend chat tests in `frontend/tests/ChatPage.test.tsx` (Est: 3h; test scenario: use case chip, answer loading, grounded answer, unsupported answer, and no-active-source states render)

### Implementation for User Story 2

- [ ] T035 [P] [US2] Implement question, answer, and conversation schemas in `backend/app/schemas/chat.py` (Est: 2h; test scenario: schema rejects empty question text and missing use case)
- [ ] T036 [US2] Implement deterministic retrieval in `backend/app/services/retrieval_service.py` with normalization, lexical scoring, thresholds, and active-source filtering (Est: 4h; test scenario: T032 retrieval cases pass without LLM provider calls)
- [ ] T037 [US2] Implement LLM provider boundary and fake provider in `backend/app/llm/provider.py`, `backend/app/llm/fake_provider.py`, and `backend/app/llm/prompt_builder.py` (Est: 3h; test scenario: fake provider is used in tests and no external API client is imported)
- [ ] T038 [US2] Implement answer orchestration in `backend/app/services/answer_service.py` for answered, unsupported, no-active-source, and error states (Est: 4h; test scenario: T032 passes and unsupported answers contain no fabricated source facts)
- [ ] T039 [US2] Implement chat API route in `backend/app/api/chat.py` and persistence calls in `backend/app/repositories/chat.py` (Est: 3h; test scenario: T033 passes and saved answer records retain source-at-time)
- [ ] T040 [P] [US2] Implement Chat screen in `frontend/src/pages/chat/ChatPage.tsx` with use case context, conversation list, composer, loading, grounded, unsupported, and no-active-source states (Est: 4h; test scenario: T034 passes with keyboard-accessible composer)
- [ ] T041 [US2] Wire chat and use-case frontend API functions in `frontend/src/services/chat.ts` and `frontend/src/services/useCases.ts` (Est: 2h; test scenario: mocked calls submit `use_case_id` and render response `answer_state`)

**Verification commands**: `pytest backend/tests/services/test_answer_service.py backend/tests/api/test_chat_api.py`; `npm run test -- ChatPage`

**Checkpoint**: US2 works independently after at least one FAQ source exists.

---

## Phase 5: User Story 3 - Provide Answer Feedback (Priority: P2)

**Goal**: Users can mark answers helpful or unhelpful and optionally add comments, including for unanswered responses.

**Independent Test**: Submit helpful and unhelpful feedback after an answer and confirm the feedback is associated with the related question, answer, use case, and source.

### Tests for User Story 3

- [ ] T042 [P] [US3] Write failing API tests for `POST /answers/{answer_id}/feedback` in `backend/tests/api/test_feedback_api.py` (Est: 2h; test scenario: helpful, unhelpful with comment, unanswered feedback, and missing answer cases are covered)
- [ ] T043 [P] [US3] Write failing service tests for feedback association rules in `backend/tests/services/test_feedback_service.py` (Est: 2h; test scenario: feedback stores answer, question, use case, source-at-time, rating, and optional comment)
- [ ] T044 [P] [US3] Write failing frontend feedback component tests in `frontend/tests/AnswerFeedback.test.tsx` (Est: 2h; test scenario: saved state, optional comment, retry-preserves-comment error state render)

### Implementation for User Story 3

- [ ] T045 [P] [US3] Implement feedback schemas in `backend/app/schemas/feedback.py` (Est: 1h; test scenario: schema accepts only helpful/unhelpful ratings and optional comment)
- [ ] T046 [US3] Implement feedback repository and service in `backend/app/repositories/feedback.py` and `backend/app/services/feedback_service.py` (Est: 3h; test scenario: T043 passes and duplicate handling is explicit)
- [ ] T047 [US3] Implement feedback API route in `backend/app/api/feedback.py` (Est: 2h; test scenario: T042 passes and feedback on unsupported answer is accepted)
- [ ] T048 [P] [US3] Implement AnswerFeedback UI component in `frontend/src/components/feedback/AnswerFeedback.tsx` (Est: 3h; test scenario: T044 passes and buttons have accessible names)
- [ ] T049 [US3] Integrate feedback component into `frontend/src/pages/chat/ChatPage.tsx` and service calls in `frontend/src/services/feedback.ts` (Est: 2h; test scenario: mocked feedback submission preserves selected rating and comment on error)

**Verification commands**: `pytest backend/tests/api/test_feedback_api.py backend/tests/services/test_feedback_service.py`; `npm run test -- AnswerFeedback`

**Checkpoint**: US3 feedback loop works with answered and unanswered responses.

---

## Phase 6: User Story 4 - Review Analytics and Unanswered Questions (Priority: P2)

**Goal**: Admins can view basic analytics and review unanswered questions by use case, source, and time period.

**Independent Test**: Generate questions, answers, unsupported answers, and feedback, then confirm analytics counts and unanswered question filters reflect the data.

### Tests for User Story 4

- [ ] T050 [P] [US4] Write failing analytics API tests in `backend/tests/api/test_analytics_api.py` (Est: 3h; test scenario: question volume, answered, unanswered, helpful, unhelpful counts filter by use case, source, and dates)
- [ ] T051 [P] [US4] Write failing unanswered question API tests in `backend/tests/api/test_unanswered_questions_api.py` (Est: 2h; test scenario: admin sees unsupported questions with source-at-time and end user receives 403)
- [ ] T052 [P] [US4] Write failing frontend analytics tests in `frontend/tests/AnalyticsDashboard.test.tsx` (Est: 2h; test scenario: metrics, loading, empty, no-results, and error states render)
- [ ] T053 [P] [US4] Write failing frontend unanswered review tests in `frontend/tests/UnansweredQuestions.test.tsx` (Est: 2h; test scenario: filtered list, detail panel, empty, and error states render)

### Implementation for User Story 4

- [ ] T054 [US4] Implement analytics repository queries in `backend/app/repositories/analytics.py` (Est: 3h; test scenario: aggregate counts are non-negative and honor filters)
- [ ] T055 [US4] Implement analytics and unanswered services in `backend/app/services/analytics_service.py` and `backend/app/services/unanswered_service.py` (Est: 3h; test scenario: T050 and T051 service setup returns expected counts and top unanswered rows)
- [ ] T056 [US4] Implement admin analytics and unanswered routes in `backend/app/api/analytics.py` and `backend/app/api/unanswered.py` (Est: 3h; test scenario: T050 and T051 pass with admin role restrictions)
- [ ] T057 [P] [US4] Implement Analytics Dashboard in `frontend/src/pages/admin/AnalyticsDashboard.tsx` with filters, metrics, drill-down links, and states (Est: 4h; test scenario: T052 passes and filters remain visible during loading/error)
- [ ] T058 [P] [US4] Implement Unanswered Questions Review screen in `frontend/src/pages/admin/UnansweredQuestions.tsx` with list/detail and source-at-time context (Est: 4h; test scenario: T053 passes and returning from detail preserves filter context)
- [ ] T059 [US4] Wire analytics frontend services in `frontend/src/services/analytics.ts` and `frontend/src/services/unanswered.ts` (Est: 2h; test scenario: mocked calls include use case, source, and time period query params)

**Verification commands**: `pytest backend/tests/api/test_analytics_api.py backend/tests/api/test_unanswered_questions_api.py`; `npm run test -- AnalyticsDashboard UnansweredQuestions`

**Checkpoint**: US4 admin review workflows are independently functional.

---

## Phase 7: User Story 5 - Enforce Admin and End-User Roles (Priority: P3)

**Goal**: Admin capabilities are restricted to admins while end users can ask questions and provide feedback.

**Independent Test**: Act as admin and end user, then verify source management and analytics are admin-only while chat and feedback remain available to end users.

### Tests for User Story 5

- [ ] T060 [P] [US5] Harness trace task: write failing role-based authorization API tests in `backend/tests/api/test_role_authorization.py` (Est: 3h; test scenario: end user receives 403 for admin routes and can access chat/feedback routes)
- [ ] T061 [P] [US5] Write failing frontend navigation tests in `frontend/tests/RoleNavigation.test.tsx` (Est: 2h; test scenario: admin sees admin nav and end user sees chat-focused navigation without admin links)

### Implementation for User Story 5

- [ ] T062 [US5] Apply admin authorization dependency to all admin routers in `backend/app/api/faq_sources.py`, `backend/app/api/analytics.py`, and `backend/app/api/unanswered.py` (Est: 2h; test scenario: T060 passes for every admin route)
- [ ] T063 [US5] Implement current-user endpoint and local role selector support in `backend/app/api/me.py` and `backend/app/auth/dependencies.py` (Est: 2h; test scenario: admin/end-user identities are returned with stable role values)
- [ ] T064 [US5] Implement role-aware app shell and navigation in `frontend/src/App.tsx` and `frontend/src/pages/LoginPage.tsx` (Est: 3h; test scenario: T061 passes and direct admin navigation displays unauthorized state for end user)
- [ ] T065 [US5] Add unauthorized frontend state in `frontend/src/components/common/UnauthorizedState.tsx` and use it in admin pages (Est: 2h; test scenario: unauthorized message explains role limitation without exposing admin details)

**Verification commands**: `pytest backend/tests/api/test_role_authorization.py`; `npm run test -- RoleNavigation`

**Checkpoint**: US5 role boundaries are enforced in both backend and frontend.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Verification, documentation, accessibility, observability, and coverage hardening across all stories.

- [ ] T066 [P] Add backend observability tests in `backend/tests/unit/test_logging_events.py` for source, chat, feedback, analytics, authorization, and fake-LLM events (Est: 2h; test scenario: each event includes request or correlation context where available)
- [ ] T067 Implement structured log calls across `backend/app/services/source_service.py`, `backend/app/services/answer_service.py`, `backend/app/services/feedback_service.py`, and `backend/app/services/analytics_service.py` (Est: 3h; test scenario: T066 passes and no question/answer content is logged unnecessarily)
- [ ] T068 [P] Add accessibility review notes and fixes for frontend states in `frontend/src/components/common/` and `docs/accessibility-checklist.md` (Est: 3h; test scenario: keyboard path covers navigation, filters, chat input, feedback controls, and dialogs)
- [ ] T069 [P] Update implementation documentation in `README.md`, `docs/development.md`, and `specs/001-faq-knowledge-assistant/quickstart.md` with final commands and no-real-LLM-test rule (Est: 2h; test scenario: commands match actual package scripts and pytest paths)
- [ ] T070 Run and document backend coverage verification in `docs/test-results.md` using `pytest --cov=app --cov-report=term-missing` from `backend/` (Est: 2h; test scenario: backend API coverage is 70%+ or gaps are listed)
- [ ] T071 Run and document frontend build/test verification in `docs/test-results.md` using `npm run build` and available frontend test command from `frontend/` (Est: 2h; test scenario: build succeeds and known static UI states are covered)
- [ ] T072 [P] Review `contracts/openapi.yaml` against implemented routes and update `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` for any naming drift (Est: 2h; test scenario: contract paths match backend router paths exactly)
- [ ] T073 Perform end-to-end manual quickstart verification and record results in `docs/test-results.md` (Est: 3h; test scenario: admin source management, grounded chat with fake LLM, feedback, analytics, unanswered review, and role checks all pass)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1.
- **Phase 3 US1 Manage FAQ Sources**: Depends on Phase 2.
- **Phase 4 US2 Ask Grounded Questions**: Depends on Phase 2 and needs at least one active source from US1 for full demo; service tests can proceed with fixtures.
- **Phase 5 US3 Provide Answer Feedback**: Depends on Phase 2 and answer records from US2 fixtures.
- **Phase 6 US4 Analytics and Unanswered Review**: Depends on Phase 2 and question/answer/feedback records from US2/US3 fixtures.
- **Phase 7 US5 Role Enforcement**: Depends on Phase 2; should be applied before production-like demo of US1-US4.
- **Phase 8 Polish**: Depends on completed target stories.

### User Story Dependencies

- **US1 (P1)**: Foundation only; MVP scope.
- **US2 (P1)**: Foundation plus active-source fixture; complements US1.
- **US3 (P2)**: Requires answer/unanswered records from US2 or fixtures.
- **US4 (P2)**: Requires source, question, answer, unanswered, and feedback records from earlier stories or fixtures.
- **US5 (P3)**: Cross-cuts US1-US4 but can be developed after foundation with route/page fixtures.

### Within Each User Story

- Write tests first and verify failure.
- Implement schemas before repositories/services.
- Implement repositories before services when persistence is required.
- Implement services before API routes.
- Implement frontend service adapters before page integration where useful.
- Verify each story independently before moving to the next priority.

---

## Parallel Opportunities

- Setup tasks T003-T007 can run in parallel after T001/T002 ownership is clear.
- Foundational tasks T011, T012, T015, T017, T018, and T019 can run in parallel.
- US1 test tasks T021-T024 can run in parallel; frontend work T029/T030 can proceed after API contract shape is stable.
- US2 test tasks T032-T034 can run in parallel; LLM boundary T037 can proceed alongside retrieval T036 after schemas T035.
- US3 test tasks T042-T044 can run in parallel; frontend feedback T048 can proceed from contract mocks.
- US4 test tasks T050-T053 can run in parallel; Analytics and Unanswered frontend screens T057/T058 can proceed from mocked service responses.
- US5 backend and frontend tests T060/T061 can run in parallel.

## Parallel Example: User Story 1

```text
Task: "T021 [US1] Write failing API contract tests for FAQ source list/create/detail/update/delete in backend/tests/api/test_faq_sources_api.py"
Task: "T022 [US1] Harness trace task: write failing API tests for FAQ source activation/deactivation conflict handling in backend/tests/api/test_faq_source_activation.py"
Task: "T024 [US1] Write failing frontend tests for source list states in frontend/tests/FaqSourcesList.test.tsx"
```

## Parallel Example: User Story 2

```text
Task: "T032 [US2] Harness trace task: write failing service tests for deterministic retrieval and mocked LLM boundary in backend/tests/services/test_answer_service.py"
Task: "T033 [US2] Write failing API tests for POST /chat/questions in backend/tests/api/test_chat_api.py"
Task: "T034 [US2] Write failing frontend chat tests in frontend/tests/ChatPage.test.tsx"
```

## Parallel Example: User Story 4

```text
Task: "T050 [US4] Write failing analytics API tests in backend/tests/api/test_analytics_api.py"
Task: "T051 [US4] Write failing unanswered question API tests in backend/tests/api/test_unanswered_questions_api.py"
Task: "T052 [US4] Write failing frontend analytics tests in frontend/tests/AnalyticsDashboard.test.tsx"
Task: "T053 [US4] Write failing frontend unanswered review tests in frontend/tests/UnansweredQuestions.test.tsx"
```

---

## Representative Harness Trace Tasks

1. **Role-based authorization**: T060 in `backend/tests/api/test_role_authorization.py`
2. **FAQ source management**: T022 in `backend/tests/api/test_faq_source_activation.py`
3. **Grounded chat with mocked LLM integration**: T032 in `backend/tests/services/test_answer_service.py`

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 US1 so admins can manage active FAQ sources.
3. Validate US1 with its API/service/frontend tests.
4. Add Phase 4 US2 for grounded chat once source management is stable.

### Incremental Delivery

1. Deliver US1 source management.
2. Deliver US2 grounded chat.
3. Deliver US3 feedback.
4. Deliver US4 analytics and unanswered review.
5. Deliver US5 role enforcement hardening before broader demo.

### Verification Command Set

```bash
cd backend && pytest
cd backend && pytest --cov=app --cov-report=term-missing
cd frontend && npm run build
cd frontend && npm run test
```

### TDD Expectations

- Every story phase starts with failing tests.
- Automated tests must use fake LLM providers only.
- Backend API coverage target is 70%+.
- Do not merge implementation work for a story until its independent test criteria pass.
