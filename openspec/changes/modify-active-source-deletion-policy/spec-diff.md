# Spec Diff: modify-active-source-deletion-policy

## Functional Requirement Change

**FR-DELETE-01 (modified)**

| | Before | After |
|---|---|---|
| Precondition | Source exists | Source exists **and is not active** |
| Success | 204 No Content | 204 No Content |
| Active guard | _(none)_ | 409 Conflict — `source_active` |

## New Domain Error

```
ActiveSourceDeletionError(source_id: str)
  → HTTP 409
  → code: "source_active"
  → message: "Source {source_id} is currently active and cannot be deleted. Deactivate or archive it first."
```

## OpenAPI Contract Change

### `DELETE /admin/faq-sources/{source_id}` — add 409 response

```yaml
# Before
responses:
  "204":
    description: Deleted
  "403":
    $ref: "#/components/responses/Forbidden"
  "404":
    $ref: "#/components/responses/NotFound"

# After
responses:
  "204":
    description: Deleted
  "403":
    $ref: "#/components/responses/Forbidden"
  "404":
    $ref: "#/components/responses/NotFound"
  "409":
    $ref: "#/components/responses/Conflict"
```

The existing `Conflict` shared response is already defined and used by the activate endpoint. No new schema required.

## No Schema Changes

`FaqSource`, `FaqSourceCreate`, `FaqSourceUpdate`, `ErrorResponse` — all unchanged.

## Unchanged Endpoints

All other FAQ source endpoints and the chat/feedback/analytics endpoints are unaffected.
