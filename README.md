# Configurable FAQ Knowledge Assistant

AI Application Engineer assessment submission — full-stack FAQ chatbot platform with role-based access, structured change management, and systematic QA review.

---

## 1. Project Overview

The Configurable FAQ Knowledge Assistant is a multi-use-case chatbot platform. Admins upload and manage FAQ sources for different use cases (HR, IT support, product support, etc.). End users ask natural-language questions and receive answers grounded exclusively in the active FAQ source for the selected use case.

Key capabilities:

- **Role-based access** — admin and end-user roles enforced at every API route
- **FAQ source lifecycle** — create, validate, activate, deactivate, archive, delete
- **Grounded chat** — deterministic retrieval + LLM provider boundary; no hallucination outside FAQ content
- **Answer feedback** — helpful/unhelpful ratings with structured reason selection
- **Structured change management** — OpenSpec-style propose → apply → archive lifecycle (Stage 6)
- **Systematic QA review** — performance, security, code quality, and observability audit (Stage 7)

---

## 2. Key Features

| Feature | Detail |
|---|---|
| Admin role | FAQ source management, activation, analytics, unanswered review |
| End-user role | Chat question submission, feedback |
| FAQ source lifecycle | draft → ready → active → inactive → archived; invalid state for bad entries |
| Active-source guard | Only one source may be active per use case; active sources cannot be deleted |
| Grounded chat | Deterministic keyword/entry scoring retrieval → LLM boundary → grounded answer |
| Fake LLM provider | `FakeLLMProvider` used in all automated tests — no real API calls |
| Answer feedback | Helpful / unhelpful ratings; unhelpful supports structured reason (5 values) |
| Unanswered tracking | Unsupported and no-active-source responses recorded for admin review |
| Stage 6 changes | Two OpenSpec change cases with full artifact trail |
| Stage 7 QA | AI-assisted review across 6 areas; 23 findings documented |
| Health check | `GET /health` → `{"status": "ok"}` |
| Observability | Structured log infrastructure (`services/logging.py`); wiring follow-up documented |

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Pydantic v2 |
| Frontend | React, Tailwind CSS, Vite |
| Database | SQLite (infrastructure in place; repositories currently in-memory for assessment) |
| LLM | `LLMProvider` Protocol boundary; `FakeLLMProvider` for tests |
| Testing | pytest, pytest-cov, httpx, vitest |
| AI workflow | Claude / Codex, AGENTS.md, Spec Kit-style artifacts, custom skills, OpenSpec change management |

---

## 4. Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Windows:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend

```bash
cd frontend
npm install
```

### Environment files

Example files are provided for documentation. Local defaults are sufficient for assessment mode — no real API keys are required.

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

---

## 5. Running Locally

### Backend

The app uses a factory function (`create_app()`). Start the server with:

```bash
cd backend
uvicorn app.main:app --reload
```

> **Note:** `app.main` exports a top-level `app = create_app()` instance, so the above command is correct. If you need the factory form: `uvicorn app.main:create_app --factory --reload`.

### Frontend

```bash
cd frontend
npm run dev
```

### Expected local URLs

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Frontend | http://localhost:5173 |
| Health check | http://localhost:8000/health |
| API docs (FastAPI) | http://localhost:8000/docs |

---

## 6. Running Tests

### Backend

```bash
cd backend
pytest
```

With coverage report:

```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

Current result: **82 passed, 94.45% coverage** (target ≥ 70%).

### Frontend

```bash
cd frontend
npm run test     # 35 tests across 8 files
npm run build    # production build check
```

> Automated tests never call real LLM APIs. All tests use `FakeLLMProvider`.

---

## 7. Demo Flow (Reviewer Walkthrough)

1. Start the backend (`uvicorn app.main:app --reload`)
2. Start the frontend (`npm run dev`)
3. Open http://localhost:5173 — select **Admin** role on the login screen
4. Navigate to FAQ Sources → create a source with at least one entry
5. Activate the source
6. Switch to **End User** role (sign out, re-select End User)
7. Navigate to Ask a Question → submit a question covered by the FAQ
8. Submit a question not covered — observe "unsupported" state
9. Submit helpful or unhelpful feedback; on unhelpful, select a reason
10. Sign out and attempt to access an admin route directly — observe 403
11. Review `openspec/changes/` for Stage 6 change artifacts
12. Review `docs/qa-summary.md` for Stage 7 QA findings

---

## 8. Assessment Stage Map

| Stage | Requirement | What I Used | Main Artifacts |
|---|---|---|---|
| 1 — Requirements | Define the product | Spec Kit-style `/specify` with Codex | `specs/001-faq-knowledge-assistant/spec.md` |
| 2 — UI / Design | Interaction design | Codex-generated design artifacts | `docs/design/`, `docs/design/prototype/` |
| 3 — Technical Plan | Plan + task breakdown | Spec Kit `/plan` and `/tasks` with Codex | `specs/001-faq-knowledge-assistant/plan.md`, `tasks.md`, `docs/architecture.md`, `specs/.../data-model.md`, `specs/.../contracts/openapi.yaml` |
| 4 — AI Tool Rules | Agent guidance | `AGENTS.md` + 6 custom skills | `AGENTS.md`, `docs/skills/` |
| 5 — TDD Implementation | Build the system | `task-runner` + `test-writer` skills, Brainstorm→Plan→Tests→Implement→Verify | `backend/`, `frontend/`, `docs/harness-traces/` |
| 6 — Change Management | Managed changes | OpenSpec propose→apply→archive flow | `openspec/changes/` |
| 7 — QA Review | Systematic QA | `qa-reviewer` skill, AI-assisted audit | `docs/performance.md`, `docs/security.md`, `docs/code-review.md`, `docs/qa-summary.md` |

---

## 9. Custom Skills

All skills live under `docs/skills/`. They are instruction documents given to the AI agent to constrain and structure its behavior for a specific task type.

### `test-writer`

**When:** Before any backend or frontend implementation task.  
**Purpose:** Generates a test plan and writes failing tests before production code is written.  
**Typical prompt:**
```
Use docs/skills/test-writer.md for task T032. Create the test plan and failing tests before implementation.
```

### `task-runner`

**When:** For normal task IDs or ranges from `specs/001-faq-knowledge-assistant/tasks.md`.  
**Purpose:** Executes tasks sequentially with scope control, TDD, and harness trace preservation.  
**Typical prompts:**
```
Use task-runner to implement T001.
Use task-runner to continue with T060-T065 only.
```
> This skill is for task-list IDs only. For Stage 6 changes, use the OpenSpec skills.

### `openspec-proposer`

**When:** Stage 6 — beginning a new change case.  
**Purpose:** Creates `proposal.md`, `spec-diff.md`, `tasks.md`, and `impact-analysis.md`. No implementation.  
**Typical prompt:**
```
propose change add-feedback-reasons. Type: add feature. Behavior: ...
```

### `openspec-applier`

**When:** Stage 6 — after proposal artifacts exist.  
**Purpose:** Applies the proposed change using TDD. Writes failing tests first, then implements.  
**Typical prompt:**
```
apply change add-feedback-reasons.
```

### `openspec-archiver`

**When:** Stage 6 — after apply is verified.  
**Purpose:** Creates `archive.md` with tests run, files changed, verification result, risks, and rollback note.  
**Typical prompt:**
```
archive change add-feedback-reasons.
```

### `qa-reviewer`

**When:** Stage 7 — after implementation and change management are complete.  
**Purpose:** Systematic AI-assisted review across performance, security, code quality, observability, test coverage, and documentation consistency.  
**Typical prompt:**
```
Use docs/skills/qa-reviewer.md to perform Stage 7 Quality Assurance.
```
**Outputs:** `docs/performance.md`, `docs/security.md`, `docs/code-review.md`, `docs/qa-summary.md`

---

## 10. Harness-Driven AI Workflow

This project did not use freeform AI chat. The AI agent was constrained by:

- **`AGENTS.md`** — project rules, conventions, testing requirements, FastAPI and Pydantic v2 idioms
- **`specs/` artifacts** — spec, plan, tasks, data model, OpenAPI contract
- **`task-runner`** — scope-controlled task execution (one task or range at a time)
- **`test-writer`** — failing tests always written before implementation
- **OpenSpec skills** — structured propose → apply → archive lifecycle for changes
- **`qa-reviewer`** — systematic post-implementation audit
- **Local verification commands** — pytest and npm test run at every task boundary
- **Harness traces** — implementation decisions and test results preserved under `docs/harness-traces/`

**Cycle per task:**

```
Brainstorm → Plan → Tests First → Implement → Verify → Trace
```

---

## 11. Stage 6 Change Cases

| Change ID | Type | Summary | Artifacts |
|---|---|---|---|
| `add-feedback-reasons` | Add feature | Adds five structured reason values to unhelpful feedback; cross-field validation rejects reason on helpful rating | `openspec/changes/add-feedback-reasons/` |
| `modify-active-source-deletion-policy` | Modify behavior | Prevents direct deletion of an active FAQ source; 409 returned; admin must deactivate or archive first | `openspec/changes/modify-active-source-deletion-policy/` |

Each change includes: `proposal.md`, `spec-diff.md`, `tasks.md`, `impact-analysis.md`, `archive.md`.

---

## 12. Stage 7 QA Summary

Full findings are in `docs/qa-summary.md`. 23 findings across 6 areas.

| Area | Result | Key finding |
|---|---|---|
| Security | Conditional pass | Two BOLA gaps (cross-user conversation + feedback ownership); accepted risks for local-dev auth model |
| Performance | Conditional pass | No pagination on source list; no load baseline (requires real LLM + SQLite first) |
| Code quality | Pass | Architecture sound; `FakeLLMProvider` hardcoded at module level (no path to real provider yet) |
| Observability | Fail | Structured logging infrastructure defined but never called in production code |
| Test coverage | Pass | 94.45% backend; 35/35 frontend; two cross-user ownership tests missing |
| Documentation | Pass | OpenAPI, task log, change archives all consistent |

AI-found and human-confirmed issues are clearly separated in each QA document.

---

## 13. Known Limitations

- **Auth model:** Authentication uses trusted request headers (`x-user-id`, `x-user-role`). Suitable for local assessment; a JWT or session layer is required before any network exposure.
- **Persistence:** All repositories are currently in-memory. SQLite infrastructure (`repositories/sqlite.py`) is implemented but not yet wired.
- **Retrieval:** Deterministic keyword scoring is used. Vector/semantic search is a documented future improvement.
- **LLM provider:** `FakeLLMProvider` is active in the production server. A provider factory with environment-variable selection is needed to wire a real model.
- **Observability:** Structured log helper (`services/logging.py`) is implemented and unit-tested but not yet called from production routes or services.
- **Production readiness:** A production deployment would additionally require hardened auth, rate limiting, monitoring, database migrations, LLM timeout/retry handling, secrets management, and CORS origin restriction.

---

## 14. Repository Structure

```text
project-root/
├── AGENTS.md                          # AI agent rules and conventions
├── README.md                          # This file
│
├── backend/
│   ├── app/
│   │   ├── api/                       # FastAPI route handlers (thin)
│   │   ├── auth/                      # Auth dependencies and models
│   │   ├── domain/                    # StrEnum domain types
│   │   ├── llm/                       # LLM provider boundary + fake provider
│   │   ├── repositories/              # In-memory repositories + SQLite base
│   │   ├── schemas/                   # Pydantic v2 request/response schemas
│   │   ├── services/                  # Business logic
│   │   └── main.py                    # FastAPI app factory
│   ├── tests/
│   │   ├── api/                       # API integration tests
│   │   ├── services/                  # Service unit tests
│   │   └── unit/                      # Unit tests (logging, etc.)
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/                # Shared UI components
│   │   ├── pages/                     # Page-level components (Chat, Admin)
│   │   └── services/                  # API client and typed service adapters
│   └── tests/                         # Vitest test files
│
├── specs/
│   └── 001-faq-knowledge-assistant/
│       ├── spec.md                    # Stage 1 requirements
│       ├── plan.md                    # Stage 3 technical plan
│       ├── tasks.md                   # Stage 3 task breakdown
│       ├── data-model.md              # Data model
│       └── contracts/
│           └── openapi.yaml           # OpenAPI contract (source of truth)
│
├── docs/
│   ├── architecture.md                # System architecture
│   ├── design/                        # Stage 2 design artifacts + prototype
│   ├── skills/                        # Custom AI skill instruction files
│   │   ├── test-writer.md
│   │   ├── task-runner.md
│   │   ├── openspec-proposer.md
│   │   ├── openspec-applier.md
│   │   ├── openspec-archiver.md
│   │   └── qa-reviewer.md
│   ├── harness-traces/                # Implementation traces per task range
│   │   ├── T001-T008.md
│   │   ├── T009-T020.md
│   │   ├── T021-T031.md
│   │   ├── T032-grounded-chat-mocked-llm.md
│   │   ├── T060-role-authorization.md
│   │   └── task-log.md
│   ├── performance.md                 # Stage 7 performance review
│   ├── security.md                    # Stage 7 security review
│   ├── code-review.md                 # Stage 7 code quality review
│   └── qa-summary.md                  # Stage 7 QA rollup
│
└── openspec/
    └── changes/
        ├── add-feedback-reasons/       # Stage 6 change 1
        └── modify-active-source-deletion-policy/  # Stage 6 change 2
```

---

## 15. Final Verification Commands

```bash
# Backend — all tests
cd backend && pytest

# Backend — tests with coverage
cd backend && pytest --cov=app --cov-report=term-missing

# Frontend — all tests
cd frontend && npm run test

# Frontend — production build
cd frontend && npm run build
```

Expected: 82 backend tests passing, 94.45% coverage, 35 frontend tests passing, clean build.

---

## 16. Interview Navigation Guide

Open these files in order to walk through the project:

| File | Why |
|---|---|
| `README.md` | Start here — full project map |
| `AGENTS.md` | AI agent rules, conventions, skill registry |
| `specs/001-faq-knowledge-assistant/spec.md` | Stage 1 requirements |
| `specs/001-faq-knowledge-assistant/plan.md` | Stage 3 technical plan |
| `specs/001-faq-knowledge-assistant/tasks.md` | Full task breakdown |
| `docs/architecture.md` | System architecture decisions |
| `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` | API contract |
| `docs/harness-traces/T032-grounded-chat-mocked-llm.md` | Stage 5 TDD trace (chat) |
| `docs/harness-traces/T060-role-authorization.md` | Stage 5 TDD trace (auth) |
| `docs/harness-traces/task-log.md` | All task log entries |
| `openspec/changes/` | Stage 6 change cases |
| `docs/qa-summary.md` | Stage 7 QA rollup — 23 findings |
| `docs/security.md` | Stage 7 security findings |
| `docs/code-review.md` | Stage 7 code quality findings |
| `docs/performance.md` | Stage 7 performance findings |
