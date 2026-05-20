# Proposal: modify-active-source-deletion-policy

## Change ID
`modify-active-source-deletion-policy`

## Change Type
Modify existing behavior

## Problem Statement

Admins can currently delete any FAQ source regardless of its activation state. Deleting an active source silently breaks the chat pipeline for all end users on that use case — in-flight chat requests that looked up the now-deleted source will encounter dangling references, and the use case will have no active source until a new one is explicitly activated. There is no guard preventing this.

## Current Behavior

`DELETE /admin/faq-sources/{source_id}` returns 204 for any existing source, including sources that are currently active (`is_active = true`). The service layer raises only `SourceNotFoundError` (→ 404).

## Proposed Behavior

`DELETE /admin/faq-sources/{source_id}` returns **409 Conflict** when the target source is currently active (`is_active = true`). The admin must first deactivate (`POST /admin/faq-sources/{source_id}/deactivate`) or archive (`POST /admin/faq-sources/{source_id}/archive`) the source before deletion is permitted.

Deletion of sources in any non-active state (draft, ready, inactive, invalid, archived) continues to return 204 unchanged.

## Acceptance Criteria

| # | Criterion |
|---|---|
| AC1 | `DELETE` on an active source → 409, error code `source_active`, descriptive message |
| AC2 | `DELETE` on an inactive/draft/ready/invalid/archived source → 204 (regression) |
| AC3 | 409 response body uses the shared `ErrorResponse` schema (`code`, `message`) |
| AC4 | Admin authentication requirement is unchanged — unauthenticated → 401, end_user → 403 |
| AC5 | `SourceService.delete_source()` raises a new `ActiveSourceDeletionError` when the source is active |
| AC6 | The API route catches `ActiveSourceDeletionError` and returns 409 |

## Out of Scope

- Changing the behavior of `archive_source()` — it already forces `is_active = False` before storing, so it acts as a valid pre-deletion step with no change needed.
- Changing the behavior of `deactivate_source()` — already returns the source with `is_active = False`.
- Any UI changes — the frontend DELETE call will simply surface the existing error-state pattern on 409.
- Cascade deletion or soft-delete mechanics.

## Rollback

1. Remove `ActiveSourceDeletionError` from `source_service.py`.
2. Remove the active-source guard in `delete_source()`.
3. Remove the `except ActiveSourceDeletionError` block from `faq_sources.py`.
4. Remove the 409 response from the OpenAPI spec DELETE path.
5. Remove the new test cases for active-source deletion.
