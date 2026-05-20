# Quickstart: Configurable FAQ Knowledge Assistant

## Prerequisites

- Python 3.11+
- Node.js and npm compatible with the selected React tooling
- SQLite available locally

## Backend Setup

From repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run backend tests:

```bash
pytest
```

Coverage target:

```bash
pytest --cov=app --cov-report=term-missing
```

Expected backend API coverage target: 70%+.

Run backend locally:

```bash
uvicorn app.main:app --reload
```

## Frontend Setup

From repository root:

```bash
cd frontend
npm install
npm run dev
```

## Local Verification Flow

1. Sign in or select a local-development role as admin.
2. Create use cases for HR, IT support, product support, and admissions.
3. Add an HR FAQ source with at least two valid FAQ entries.
4. Activate the HR FAQ source.
5. Open the chat experience as an end user.
6. Select HR and ask a question covered by the source.
7. Confirm the answer is grounded in the active source.
8. Ask a question not covered by the source.
9. Confirm the answer is marked unsupported and appears in unanswered review.
10. Submit helpful and unhelpful feedback.
11. Open analytics and confirm question, answered, unanswered, and feedback counts update.

## LLM Test Rule

Automated tests must use a fake LLM provider. Real LLM APIs must not be called by unit, service, or API tests.

## Design References

- `docs/design/information-architecture.md`
- `docs/design/user-flows.md`
- `docs/design/screens.md`
- `docs/design/interaction-notes.md`
- `docs/design/prototype/`
