# Impact Analysis: add-feedback-reasons

## Risk
**Low.** This is a purely additive change. All new fields are optional. Existing API callers, tests, and frontend behavior are unaffected if they do not supply or read `reason`. The cross-field validation (reason only valid with unhelpful rating) is the only new enforcement path.

---

## Backend Impact

### `backend/app/domain/enums.py`
- Add `FeedbackReason` StrEnum with five values: `incorrect_answer`, `not_specific_enough`, `missing_from_faq`, `confusing_response`, `outdated_source`.

### `backend/app/schemas/feedback.py`
- Add `reason: FeedbackReason | None = None` to `FeedbackCreate`.
- Add cross-field validator: raise `ValueError` if `rating == helpful` and `reason` is not `None`.
- Add `reason: FeedbackReason | None` to `FeedbackResponse`.

### `backend/app/repositories/feedback.py`
- Add `reason: FeedbackReason | None` field to `FeedbackRecord` dataclass.
- Update `InMemoryFeedbackRepository.save()` to accept and store `reason`.

### `backend/app/services/feedback_service.py`
- Pass `reason` from `FeedbackCreate` through to `feedback_repository.save()`.

### `backend/app/api/feedback.py`
- Pass `reason` from the saved `FeedbackRecord` into `FeedbackResponse`.

No route signature changes. No new routes. No auth changes.

---

## Frontend Impact

### `frontend/src/components/feedback/AnswerFeedback.tsx`
- After user clicks Unhelpful, show a reason selector (radio buttons or select) with the five options.
- Reason selector is hidden when user clicks Helpful or before any rating is selected.
- Reason selection is optional — user can submit unhelpful feedback without selecting a reason.
- Each option must be labelled with text, not color alone.
- Selector must be keyboard-accessible.

### `frontend/src/services/feedback.ts`
- Add optional `reason` field to `FeedbackPayload` type.
- Pass `reason` in the request body when present.

### `frontend/src/pages/chat/ChatPage.tsx`
- No structural changes needed — `AnswerFeedback` is already integrated; the reason selector is internal to the component.

---

## Data / Model Impact
- `FeedbackReason` is a new bounded enum — five valid values, easily extensible.
- `FeedbackRecord` gains one nullable field. No records are invalidated by absence of a reason.
- In-memory repository: field added to dataclass and `save()` signature.
- SQLite persistence (when implemented): one `ALTER TABLE feedback ADD COLUMN reason TEXT DEFAULT NULL` is sufficient with no data loss.

---

## API Impact
- `POST /answers/{answer_id}/feedback` request body gains optional `reason` field.
- `FeedbackResponse` gains `reason` field.
- New 422 case: `reason` provided with `helpful` rating.
- All existing valid request shapes remain valid — no breaking change.
- `contracts/openapi.yaml` must be updated to reflect the new enum, request field, and response field.

---

## Test Impact

### Files to add or update

| File | Change |
|---|---|
| `backend/tests/api/test_feedback_api.py` | Add: unhelpful + valid reason → 201; helpful + reason → 422; invalid reason value → 422; reason null on helpful → still 201 |
| `backend/tests/services/test_feedback_service.py` | Add: reason stored on record; helpful + reason raises validation error at schema level |
| `frontend/tests/AnswerFeedback.test.tsx` | Add: reason selector visible after clicking Unhelpful; reason selector hidden after clicking Helpful; each reason option has accessible label |

### Existing tests
All existing feedback tests continue to pass — reason defaults to `null` and existing requests do not supply it.

---

## Security Impact
None. The `reason` field is a bounded enum validated by Pydantic — no free-text injection surface is introduced. The cross-field validation is enforced in the schema layer before it reaches service or persistence code.

---

## Performance Impact
Negligible. One nullable enum field added to the feedback record. No indexing or query changes needed.

---

## Observability Impact
- The structured log event for feedback submission (already planned in `services/logging.py`) should include `reason` alongside `rating` and `answer_id`.
- No new log events required.

---

## Rollback Impact
- Remove `FeedbackReason` from `domain/enums.py`.
- Remove `reason` from `FeedbackCreate`, `FeedbackResponse`, and `FeedbackRecord`.
- Revert `feedback_repository.save()` signature.
- Revert `AnswerFeedback` component to version without reason selector.
- Stored `reason` values become orphaned in any persistent store but do not affect correctness.
- All tests return to green without the new test cases.
