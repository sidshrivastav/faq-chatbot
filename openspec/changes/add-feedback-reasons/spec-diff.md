# Spec Diff: add-feedback-reasons

## Requirements Changed

### FR-014 (unchanged)
> Users MUST be able to provide positive or negative feedback on answers.

No change — still satisfied.

### FR-015 (extended)
**Before:**
> Users MUST be able to add optional comments when giving feedback.

**After (extended, not replaced):**
> Users MUST be able to add optional comments when giving feedback. When feedback is unhelpful, users MAY additionally select one structured reason from a fixed enumeration.

### FR-016 (extended)
**Before:**
> The system MUST associate feedback with the related question, answer, use case, and FAQ source.

**After (extended):**
> The system MUST associate feedback with the related question, answer, use case, and FAQ source. When a structured reason is provided, it MUST be stored as part of the feedback record.

### New implicit requirement
> The system MUST reject a structured reason when the feedback rating is `helpful`. Reason is only valid with `unhelpful` rating.

---

## New Acceptance Criteria

Added to User Story 3 (Provide Answer Feedback):

- **Given** a user marks an answer as unhelpful and selects a structured reason, **When** the feedback is submitted, **Then** the reason is stored and returned in the feedback response.
- **Given** a user marks an answer as unhelpful and does not select a reason, **When** the feedback is submitted, **Then** the feedback is accepted and `reason` is `null`.
- **Given** a user marks an answer as helpful and provides a reason, **When** the feedback is submitted, **Then** the request is rejected with a validation error.

---

## Data Model Changes

### `FeedbackReason` enum (new)
Added to `backend/app/domain/enums.py`:

```python
class FeedbackReason(StrEnum):
    INCORRECT_ANSWER = "incorrect_answer"
    NOT_SPECIFIC_ENOUGH = "not_specific_enough"
    MISSING_FROM_FAQ = "missing_from_faq"
    CONFUSING_RESPONSE = "confusing_response"
    OUTDATED_SOURCE = "outdated_source"
```

### `FeedbackCreate` schema (modified)
**Before:** `{ rating: FeedbackRating, comment: str | None }`
**After:** `{ rating: FeedbackRating, comment: str | None, reason: FeedbackReason | None }`

Cross-field validation: if `rating == helpful` and `reason` is not `None` → 422.

### `FeedbackResponse` schema (modified)
**Before:** `{ id, answer_id, question_id, use_case_id, faq_source_id_at_time, rating, comment, created_at }`
**After:** adds `reason: FeedbackReason | None`

### `FeedbackRecord` dataclass (modified)
**Before:** `{ ..., rating, comment, created_at }`
**After:** adds `reason: FeedbackReason | None`

### `InMemoryFeedbackRepository.save()` (modified)
Accepts and stores `reason` alongside existing fields.

---

## API Contract Changes

### `POST /answers/{answer_id}/feedback`

**Request body — before:**
```json
{ "rating": "helpful" | "unhelpful", "comment": "string?" }
```

**Request body — after:**
```json
{
  "rating": "helpful" | "unhelpful",
  "comment": "string?",
  "reason": "incorrect_answer" | "not_specific_enough" | "missing_from_faq" | "confusing_response" | "outdated_source" | null
}
```

**Response body — before:**
```json
{ "id": "...", "answer_id": "...", ..., "rating": "...", "comment": "..." }
```

**Response body — after:** adds `"reason": "..." | null`

**New validation rule:** `reason` is non-null only when `rating` is `unhelpful`. Supplying `reason` with `helpful` returns 422.

---

## Deprecated or Removed Behavior
None — all existing feedback behavior is preserved. This is an additive change.

---

## Compatibility Notes
- Existing API callers that omit `reason` continue to work — field is optional and defaults to `null`.
- Existing `FeedbackResponse` consumers must handle the new `reason` field; they may ignore it if unused.
- The `comment` field is unchanged.
- No database migration is required for the in-memory repository; for SQLite persistence, a column addition with `DEFAULT NULL` is sufficient.
