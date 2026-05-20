# Implementation Plan: Configurable FAQ Knowledge Assistant

**Branch**: `001-faq-knowledge-assistant` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-faq-knowledge-assistant/spec.md`; Stage 2 design artifacts from `docs/design/`.

## Summary

Build a role-aware FAQ knowledge assistant with admin FAQ source management, chat-based grounded Q&A, answer feedback, unanswered question review, and basic analytics. The implementation will use a FastAPI backend with Pydantic v2 schemas, SQLite for local development, React + Tailwind CSS for the UI, deterministic FAQ retrieval before any LLM call, and an explicit LLM provider boundary that can be replaced with fakes in automated tests.

## Technical Context

**Language/Version**: Python 3.11+ for backend; TypeScript-compatible React frontend.

**Primary Dependencies**: FastAPI, Pydantic v2, pytest, React, Tailwind CSS, SQLite driver/ORM layer selected during implementation, LLM provider adapter interface.

**Storage**: SQLite for local development with relational tables for users, use cases, FAQ sources, FAQ entries, conversations, questions, answers, feedback, and audit-like source events.

**Testing**: pytest for backend unit, service, and API tests; frontend component and flow tests may be added with the React test tooling selected during implementation. Backend API coverage target is 70%+.

**Target Platform**: Local web application running a Python backend service and browser-based React frontend.

**Project Type**: Web application with separate backend and frontend packages.

**Performance Goals**: Admins complete FAQ source add/activate/update/deactivate flow in under 5 minutes; end users receive an answer or unsupported-answer message in under 30 seconds under normal local-development conditions; analytics for common filters render within 2 seconds for local sample-sized datasets.

**Constraints**: No real LLM API calls in automated tests; deterministic retrieval must run before LLM generation; vector search is deferred as a future improvement; answers must be grounded only in the active FAQ source for the selected use case; backend API tests target 70%+ coverage.

**Scale/Scope**: Initial local-development scope for a small-to-medium FAQ corpus across HR, IT support, product support, admissions, and similar use cases. Basic analytics cover question volume, answered/unanswered counts, feedback totals, filtering, and unanswered question review.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The current constitution file contains placeholder principle text only and defines no enforceable gates. Plan proceeds under the explicit user constraints and feature requirements.

Initial gate result: PASS, no constitution violations identified.

Post-design gate result: PASS, generated design artifacts preserve the selected constraints and introduce no constitution conflicts.

## Architecture Overview

The application is split into a backend API and frontend UI.

- **Frontend** renders the admin and end-user experiences defined in Stage 2: login shell, admin dashboard, FAQ source list/detail, chat, feedback states, unanswered review, and analytics dashboard.
- **Backend API** owns role checks, FAQ source lifecycle, deterministic retrieval, LLM boundary invocation, answer persistence, feedback persistence, and analytics aggregation.
- **Retrieval service** selects the active FAQ source for the requested use case, normalizes the question, scores FAQ entries deterministically, and returns grounded snippets or an unsupported-answer result.
- **LLM service boundary** receives only retrieved FAQ context and the user question. It returns an answer constrained to that context. Automated tests use a fake provider and must not call external LLM APIs.
- **Persistence layer** stores source state, source entries, conversations, questions, answers, feedback, and analytics inputs in SQLite for local development.

## Major Backend Modules

- `backend/app/main.py`: FastAPI application setup, router registration, health endpoint, error handlers.
- `backend/app/api/`: Route modules for auth/session preview, use cases, FAQ sources, chat, feedback, unanswered questions, analytics.
- `backend/app/schemas/`: Pydantic v2 request/response models and shared error models.
- `backend/app/domain/`: Domain models, enums, validation rules, state transition helpers.
- `backend/app/services/source_service.py`: FAQ source create/update/archive/delete/activate/deactivate workflows.
- `backend/app/services/retrieval_service.py`: Deterministic FAQ matching and source grounding decisions.
- `backend/app/services/answer_service.py`: Chat orchestration, unsupported-answer handling, answer persistence.
- `backend/app/services/feedback_service.py`: Feedback validation and persistence.
- `backend/app/services/analytics_service.py`: Aggregations for dashboard metrics, filters, and unanswered lists.
- `backend/app/llm/`: Provider interface, prompt builder, response validation, fake provider for tests.
- `backend/app/auth/`: Role extraction, admin/end-user authorization dependencies, local-development session handling.
- `backend/app/repositories/`: SQLite persistence access, query helpers, transaction boundaries.
- `backend/tests/`: Unit, service, API, authorization, and fake-LLM tests.

## Major Frontend Modules

- `frontend/src/App.tsx`: App shell, route layout, role-aware navigation.
- `frontend/src/pages/LoginPage.tsx`: Static login/role entry for local development.
- `frontend/src/pages/admin/AdminDashboard.tsx`: Admin overview cards, health summary, recent unanswered questions.
- `frontend/src/pages/admin/FaqSourcesList.tsx`: Source filters, source table/list, empty/loading/error states.
- `frontend/src/pages/admin/FaqSourceDetail.tsx`: Source status, content preview/editor area, activation/deactivation actions.
- `frontend/src/pages/admin/UnansweredQuestions.tsx`: Filtered unanswered list and detail view.
- `frontend/src/pages/admin/AnalyticsDashboard.tsx`: Metrics, filters, drill-down links.
- `frontend/src/pages/chat/ChatPage.tsx`: Use case context, conversation view, composer, answer states.
- `frontend/src/components/feedback/AnswerFeedback.tsx`: Helpful/unhelpful controls, optional comment, saved/error states.
- `frontend/src/components/common/`: Buttons, badges, status messages, loading skeletons, empty states, error banners.
- `frontend/src/services/`: API client functions and typed response adapters.

## Data Model

Detailed fields and state transitions are defined in [data-model.md](./data-model.md). Core entities:

- User
- UseCase
- FaqSource
- FaqEntry
- Conversation
- Question
- Answer
- Feedback
- UnansweredQuestion
- AnalyticsSummary

Important model rules:

- A use case may have zero or one active FAQ source at a time.
- Inactive, archived, invalid, or different-use-case sources are excluded from retrieval.
- Answers retain the source and source version used at the time of answer generation.
- Unsupported questions are persisted for admin review.
- Feedback is tied to the exact question/answer context.

## API Design

Detailed contracts are defined in [contracts/openapi.yaml](./contracts/openapi.yaml).

Primary API groups:

- `GET /health`
- `GET /me`
- `GET /use-cases`
- `GET /admin/faq-sources`
- `POST /admin/faq-sources`
- `GET /admin/faq-sources/{source_id}`
- `PATCH /admin/faq-sources/{source_id}`
- `POST /admin/faq-sources/{source_id}/activate`
- `POST /admin/faq-sources/{source_id}/deactivate`
- `POST /admin/faq-sources/{source_id}/archive`
- `DELETE /admin/faq-sources/{source_id}`
- `POST /chat/questions`
- `POST /answers/{answer_id}/feedback`
- `GET /admin/unanswered-questions`
- `GET /admin/analytics/summary`

API behavior is driven by Stage 2 UI needs:

- List endpoints support filters used in admin tables and dashboards.
- Chat response includes answer state, source context, and feedback eligibility for inline chat rendering.
- Source endpoints expose readiness, active status, and warnings for list/detail screens.
- Analytics endpoints return already-labeled metrics for dashboard cards and drill-downs.
- Error responses include user-facing messages suitable for empty/error states.

## LLM Integration Boundary

The LLM boundary is a service interface, not direct calls from route handlers.

Inputs:

- User question
- Use case context
- Retrieved FAQ entries from the active FAQ source
- Source metadata required for traceability

Outputs:

- Answer text
- Grounding metadata
- Refusal/unsupported signal when context is insufficient

Rules:

- Retrieval must happen before LLM invocation.
- LLM receives only active-source retrieved context, never inactive or unrelated source content.
- If deterministic retrieval returns insufficient context, no LLM generation is attempted.
- Automated tests use fake providers and fixtures; real LLM APIs are not called in tests.
- LLM output is validated before persistence to ensure it maps to the requested answer state.

## Retrieval Strategy

Initial retrieval is deterministic:

1. Resolve selected use case.
2. Find active FAQ source for that use case.
3. Reject if no active source or source is not ready.
4. Normalize question and FAQ entry questions/answers.
5. Score entries using lexical matching, keyword overlap, exact phrase matching, and configurable thresholds.
6. Return top matched entries when score meets threshold.
7. Mark unsupported when no match meets threshold or only partial/ambiguous matches exist.

Vector search is explicitly deferred as a future improvement. The data model keeps FAQ entries addressable and versioned so vector indexing can be added later without changing user-facing workflows.

## Authentication and Authorization

Initial implementation should support local-development login/session behavior sufficient to exercise role-based flows.

Authorization rules:

- Admin-only: FAQ source management, activation/deactivation, analytics, unanswered question review.
- End-user allowed: use case listing, chat questions, feedback submission.
- Admins may also use chat, but chat answers follow the same active-source grounding rules.
- Unauthorized access returns a consistent error with a user-facing message.

Production-grade identity provider integration is out of scope for the initial implementation plan unless added in a later feature.

## Error Handling

Backend error categories:

- Validation errors for malformed requests or missing required fields.
- Authorization errors for admin-only actions.
- Not-found errors for missing sources, use cases, questions, or answers.
- Conflict errors for invalid source state transitions or activation conflicts.
- Unsupported-answer results for insufficient active FAQ source context.
- Service errors for LLM provider failures or persistence failures.

Frontend error states:

- Preserve user input where possible.
- Show inline errors near the failed action for feedback and source edits.
- Keep selected filters visible for analytics errors.
- Show clear no-active-source and unsupported-answer messages in chat.

## Observability

Backend should emit structured logs for:

- Source create/update/activate/deactivate/archive/delete events.
- Chat question submitted, retrieval result, answer state, unsupported state.
- Feedback submitted.
- Analytics requested with filter dimensions.
- Authorization failures and validation failures.
- LLM provider call attempted/skipped/fake-provider used.

Metrics should be derived from stored records for the initial implementation. Request IDs or correlation IDs should be included in logs where practical to connect chat questions, answers, feedback, and errors.

## Testing Strategy

Backend:

- Unit tests for source state transitions, deterministic retrieval scoring, validation rules, analytics aggregation, and authorization helpers.
- API tests for source management, activation conflict, chat answered/unsupported/no-active-source flows, feedback, unanswered list, analytics filters, and role restrictions.
- Fake LLM provider tests proving real LLM APIs are not called.
- Coverage target: backend API test coverage 70%+.

Frontend:

- Component tests for chat answer states, feedback states, source status badges, empty/loading/error states, and admin filters.
- Flow tests for admin source management, end-user chat, feedback, unanswered review, and analytics filtering when frontend tooling is available.

Manual verification:

- Follow [quickstart.md](./quickstart.md) to run local backend/frontend and exercise Stage 2 prototype-aligned screens.

## Security Considerations

- Enforce role checks on backend endpoints, not only in frontend navigation.
- Never use inactive or unrelated FAQ source content for answer generation.
- Validate FAQ source input size, required fields, and readiness before activation.
- Treat LLM output as untrusted; validate answer state and grounding before returning/persisting.
- Avoid storing secrets in code or tests.
- Do not expose admin-only analytics or source details to end users.
- Preserve historical answer/source context without allowing deleted or archived content to be used for new answers.

## Performance Considerations

- Deterministic retrieval should operate on the active source only, keeping local matching fast for initial corpus sizes.
- Use pagination for FAQ source lists, unanswered question lists, and feedback/analytics drill-downs.
- Precompute or cache simple analytics summaries only if direct aggregate queries become slow.
- Keep chat response path short by skipping LLM calls when retrieval is insufficient.
- Defer vector search and indexing work until corpus size or matching quality justifies it.

## Stage 2 Design Influence on API and Data Model

Stage 2 design directly shaped the implementation plan:

- Persistent use case context in chat requires `use_case_id` on questions and answer responses.
- Active-source badges and readiness states require explicit source status, active state, readiness, and warnings in the FAQ source model and API.
- Feedback controls attached to each answer require feedback to reference answer, question, use case, and source context.
- Unanswered review screens require unsupported questions to be stored with question text, use case, source-at-time, answer state, feedback, and timestamps.
- Analytics filters require records to retain use case, FAQ source, answer state, feedback rating, and creation time.
- Loading, empty, and error state designs require consistent response envelopes and user-facing error messages.
- Admin source activation confirmations require state transition endpoints that can report conflicts and consequences.

## Project Structure

### Documentation (this feature)

```text
specs/001-faq-knowledge-assistant/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md
```

### Source Code (repository root)

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
```

**Structure Decision**: Use a two-package web application structure with `backend/` and `frontend/` at repository root. This matches the user constraints and keeps API/domain concerns separate from React/Tailwind UI implementation.

## Complexity Tracking

No constitution violations or avoidable complexity exceptions are identified.
