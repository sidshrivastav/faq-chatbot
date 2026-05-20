# Archive: modify-active-source-deletion-policy

## Date Archived
2026-05-20

## Change ID
`modify-active-source-deletion-policy`

## Change Type
Modify existing behavior

## Summary of Implemented Behavior
`DELETE /admin/faq-sources/{source_id}` now returns 409 Conflict with error code `source_active` when the target source is currently active (`is_active = true`). Deletion of sources in any non-active state (draft, ready, inactive, invalid, archived) continues to return 204 unchanged. The guard is enforced in the service layer via a new `ActiveSourceDeletionError` exception. No frontend changes were required.

---

## Artifact Completion

| Artifact | Completed |
|---|---|
| `proposal.md` | Yes |
| `spec-diff.md` | Yes |
| `tasks.md` | Yes — all 4 tasks marked complete |
| `impact-analysis.md` | Yes |

---

## Tests Run

### Focused (change-scoped)

```bash
cd backend && python -m pytest tests/api/test_faq_sources_api.py --no-cov -v
# 5 passed
```

### Full regression

```bash
cd backend && python -m pytest --no-cov -q
# 82 passed
```

_(No frontend changes; frontend test suite not re-run.)_

---

## Verification Result

**PASSED.** All acceptance criteria from the proposal are met:

| Criterion | Status |
|---|---|
| AC1: DELETE active source → 409, code `source_active` | Pass |
| AC2: DELETE inactive/draft/ready/invalid/archived source → 204 | Pass |
| AC3: 409 body uses shared `ErrorResponse` schema | Pass |
| AC4: Admin auth unchanged — unauthenticated → 401, end_user → 403 | Pass |
| AC5: `SourceService.delete_source()` raises `ActiveSourceDeletionError` when active | Pass |
| AC6: API route catches `ActiveSourceDeletionError` → 409 | Pass |

---

## Files Changed

### New
_(none)_

### Modified

| File | Change |
|---|---|
| `backend/app/services/source_service.py` | Added `ActiveSourceDeletionError` exception; added active-source guard in `delete_source()` — fetches source first, raises if `is_active` |
| `backend/app/api/faq_sources.py` | Imported `ActiveSourceDeletionError`; added `except ActiveSourceDeletionError` branch in DELETE route → HTTP 409 with `code: source_active` |
| `backend/tests/api/test_faq_sources_api.py` | Added `test_delete_active_source_returns_409` and `test_delete_inactive_source_returns_204` |
| `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` | Added `"409": $ref: "#/components/responses/Conflict"` to DELETE `/admin/faq-sources/{source_id}` |
| `openspec/changes/modify-active-source-deletion-policy/tasks.md` | Marked all 4 tasks complete |

---

## Commits

| Hash | Message |
|---|---|
| `4e2f23f` | `change:modify-active-source-deletion-policy document change case` |
| `9ce16df` | `change:modify-active-source-deletion-policy implement active-source deletion guard` |
| _(this commit)_ | `change:modify-active-source-deletion-policy archive completed change` |

---

## Deviations from Proposal

| Item | Detail |
|---|---|
| No `_conflict()` helper used in DELETE route | The proposal referenced using a `_conflict()` helper (by analogy with `_not_found()`). No such helper exists in `faq_sources.py` — the activate endpoint raises `HTTPException` directly. The DELETE route follows the same direct pattern for consistency. |

---

## Remaining Risks

| Risk | Severity | Note |
|---|---|---|
| SQLite migration will need a data read before delete | Low | The in-memory guard reads the source then deletes it. When SQLite is wired, this becomes two queries. An index on `id` keeps it O(1); no correctness risk. |
| Race condition on concurrent activate + delete | Low | In-memory repository has no locking. A concurrent activate immediately before a delete could slip past the guard. Not relevant for current single-process dev server; will need a database-level advisory lock or transaction when persistence is added. |

---

## Rollback Note

1. Remove `ActiveSourceDeletionError` from `backend/app/services/source_service.py`.
2. Remove the active-source guard (the `get_source` + `is_active` check) from `delete_source()`.
3. Remove the `except ActiveSourceDeletionError` block from the DELETE route in `backend/app/api/faq_sources.py`.
4. Remove the `ActiveSourceDeletionError` import from `faq_sources.py`.
5. Remove `test_delete_active_source_returns_409` and `test_delete_inactive_source_returns_204` from `test_faq_sources_api.py`.
6. Remove `"409": $ref: "#/components/responses/Conflict"` from the DELETE path in `openapi.yaml`.

---

## Final Status

**Applied and archived.** All 4 tasks complete. All acceptance criteria verified. 82 backend tests passing.
