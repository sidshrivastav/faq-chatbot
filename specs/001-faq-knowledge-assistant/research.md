# Research: Configurable FAQ Knowledge Assistant

## Decision: FastAPI backend with Pydantic v2 schemas

**Rationale**: The user explicitly constrained the backend to Python 3.11+, FastAPI, Pydantic v2, and pytest. FastAPI maps cleanly to typed request/response contracts, role-aware dependencies, and automated API tests.

**Alternatives considered**: Flask was rejected because it was outside the requested stack. Django was rejected because the feature scope does not require a full framework and the user explicitly requested FastAPI.

## Decision: React + Tailwind CSS frontend

**Rationale**: The user explicitly constrained the frontend to React + Tailwind CSS. The Stage 2 design artifacts define dashboard, table, detail, chat, feedback, empty/loading/error, and analytics screens that fit a component-based React UI.

**Alternatives considered**: Server-rendered templates and other frontend frameworks were rejected because they do not match the requested frontend constraint.

## Decision: SQLite for local development

**Rationale**: The user explicitly requested SQLite for local development. The data is relational: users, use cases, sources, entries, questions, answers, feedback, and analytics inputs all have clear relationships and filter needs.

**Alternatives considered**: PostgreSQL was rejected for initial local development because the user specified SQLite. File-only storage was rejected because analytics and relationship queries would become fragile.

## Decision: Deterministic retrieval before LLM generation

**Rationale**: Requirements demand grounded answers based only on the active FAQ source. Deterministic retrieval provides auditable inclusion/exclusion before any generated answer and supports reliable unsupported-answer behavior.

**Alternatives considered**: Direct LLM answer generation was rejected because it risks unsupported answers. Vector search was deferred because the user explicitly set it as a future improvement.

## Decision: LLM provider behind a testable boundary

**Rationale**: The application needs LLM integration for grounded answer generation, but tests must never call real LLM APIs. A provider interface allows production and fake implementations while keeping route handlers deterministic in tests.

**Alternatives considered**: Direct SDK calls in API routes were rejected because they are difficult to test safely. A global mock-only approach was rejected because it hides the integration boundary.

## Decision: One active FAQ source per use case

**Rationale**: The feature spec assumes at most one active source for each use case so end-user answers have a clear grounding source and admins can understand source impact.

**Alternatives considered**: Multiple active sources per use case were rejected for initial scope because they complicate answer provenance, activation UX, and analytics interpretation.

## Decision: Store unsupported questions as first-class review records

**Rationale**: Stage 2 includes an unanswered question review screen and analytics drill-down. Persisting unsupported questions with use case and source-at-time makes content gaps reviewable.

**Alternatives considered**: Inferring unanswered questions from logs was rejected because logs are not a product data source and would weaken admin workflows.

## Decision: Backend-enforced role authorization

**Rationale**: Stage 2 navigation separates admin and end-user areas, but security requires backend enforcement. Admin-only routes must reject end users regardless of frontend state.

**Alternatives considered**: Frontend-only role hiding was rejected because it would not protect source management or analytics.

## Decision: API responses include user-facing state messages

**Rationale**: The design artifacts require clear empty, loading, unsupported, no-active-source, invalid-source, and unauthorized messages. Backend responses should expose stable state codes and safe display messages.

**Alternatives considered**: Free-form exception text was rejected because it is inconsistent and unsuitable for UI states.
