# Development Notes

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
pytest --cov=app --cov-report=term-missing
```

Backend API coverage target: 70%+.

## Frontend

```bash
cd frontend
npm install
npm run build
npm run test
```

## LLM Test Rule

Do not call real LLM APIs in automated tests. Use a fake or mocked LLM provider for all unit, service, and API tests.

## Harness Traces

Representative implementation traces belong under `docs/harness-traces/`.
