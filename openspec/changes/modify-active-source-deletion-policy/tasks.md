# Tasks: modify-active-source-deletion-policy

Change ID: `modify-active-source-deletion-policy`
Type: Modify existing behavior
Verification: `pytest backend/tests/api/test_faq_sources_api.py --no-cov -v` and `pytest --no-cov -q`

---

## Test Tasks

- [x] TC01 Update `backend/tests/api/test_faq_sources_api.py` — add failing cases:
  - Delete active source → 409, `code == "source_active"`
  - Delete inactive source → 204 (regression guard: ensures non-active deletion still works)
  - (Est: 1h; test scenario: TC01 409 case fails before `ActiveSourceDeletionError` is raised)

---

## Backend Tasks

- [x] TC02 Add `ActiveSourceDeletionError` and active-source guard to `backend/app/services/source_service.py`
  - New exception: `ActiveSourceDeletionError(source_id: str)`
  - Guard in `delete_source()`: fetch source first; if `is_active`, raise `ActiveSourceDeletionError`
  - (Est: 0.5h; test scenario: TC01 service-layer cases fail before this is added)

- [x] TC03 Update `backend/app/api/faq_sources.py` DELETE route
  - Import `ActiveSourceDeletionError`
  - Add `except ActiveSourceDeletionError` → 409 via `_conflict()` helper
  - (Est: 0.5h; test scenario: TC01 API 409 case passes after this is added)

---

## Documentation Tasks

- [x] TC04 Update `specs/001-faq-knowledge-assistant/contracts/openapi.yaml`
  - Add `"409": $ref: "#/components/responses/Conflict"` to `DELETE /admin/faq-sources/{source_id}`
  - (Est: 0.25h; test scenario: YAML is valid and paths match implementation)

---

## Verification Commands

```bash
# Focused
cd backend && pytest tests/api/test_faq_sources_api.py --no-cov -v

# Full backend regression
cd backend && pytest --no-cov -q

# Full frontend regression (smoke check — no frontend changes)
cd frontend && npm run test
```

---

## Completion Checklist

- [x] TC01 new API test cases written and passing
- [x] TC02 `ActiveSourceDeletionError` added, guard in `delete_source()`
- [x] TC03 API route catches `ActiveSourceDeletionError` → 409
- [x] TC04 OpenAPI spec updated with 409 on DELETE
- [x] All existing FAQ source tests still pass
- [x] Full backend test suite passes
