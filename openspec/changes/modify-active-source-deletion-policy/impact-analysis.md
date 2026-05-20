# Impact Analysis: modify-active-source-deletion-policy

## Backend

### `backend/app/services/source_service.py`
- Add `ActiveSourceDeletionError(source_id: str)` exception class (alongside existing `SourceNotFoundError`, `SourceNotReadyError`, etc.)
- Add active-source guard in `delete_source()` before calling `self.repository.delete_source()`:
  ```python
  source = self.repository.get_source(source_id)
  if source is None:
      raise SourceNotFoundError(source_id)
  if source.is_active:
      raise ActiveSourceDeletionError(source_id)
  ```
- **Risk**: Low — purely additive guard; no change to success path.

### `backend/app/api/faq_sources.py`
- Import `ActiveSourceDeletionError` from service.
- Add `except ActiveSourceDeletionError` branch in the DELETE route handler, returning 409 via the existing `_conflict()` helper (same pattern as `SourceNotReadyError` → 409 in `activate_source`).
- **Risk**: Low — mirrors existing 409 pattern exactly.

### `backend/tests/api/test_faq_sources_api.py`
- Add test: delete active source → 409, body has `code == "source_active"`.
- Add test: delete inactive source → 204 (verifies guard only fires on active).
- Existing test `test_admin_can_create_list_update_detail_and_delete_source` deletes a non-activated source — it must remain green without modification.
- **Risk**: None — additive tests only.

## Frontend

No frontend changes. The Chat page already handles network errors; a 409 from DELETE will surface as an error state in any admin UI that calls delete. No new component work is required for this change.

## OpenAPI Contract

`specs/001-faq-knowledge-assistant/contracts/openapi.yaml` — add `"409": $ref: "#/components/responses/Conflict"` to the DELETE `/admin/faq-sources/{source_id}` path. The `Conflict` response component is already defined.

## Regression Surface

| Area | Risk | Note |
|---|---|---|
| Existing delete tests | None | They use non-active sources; the guard does not fire |
| Activate/deactivate/archive | None | Unrelated endpoints; no code changes in those paths |
| Chat pipeline | None | Deletion is an admin operation; chat reads active sources only |
| Auth checks | None | `require_admin` dependency applied before service call; unchanged |

## Effort Estimate

| Task | Estimate |
|---|---|
| Failing tests | 1h |
| Service error + guard | 0.5h |
| API route handler | 0.5h |
| OpenAPI spec | 0.25h |
| **Total** | **~2.25h** |
