# Development Notes

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
pytest --cov=app --cov-report=term-missing
pytest tests/api/test_health_and_errors.py
pytest tests/unit/test_foundation_models.py tests/unit/test_sqlite_repository.py tests/unit/test_auth_dependencies.py tests/unit/test_logging_events.py
```

Backend API coverage target: 70%+.

## Frontend

```bash
cd frontend
npm install
npm run build
npm run test
npm run test -- services/apiClient.test.ts components/commonStates.test.tsx
```

## LLM Test Rule

Do not call real LLM APIs in automated tests. Use a fake or mocked LLM provider for all unit, service, and API tests.

## Harness Traces

Representative implementation traces belong under `docs/harness-traces/`.
