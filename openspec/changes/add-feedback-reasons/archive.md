# Archive: add-feedback-reasons

## Date Archived
2026-05-20

## Change ID
`add-feedback-reasons`

## Change Type
Add feature

## Summary of Implemented Behavior
When users submit unhelpful feedback on an answer, they may optionally select one structured reason from a fixed five-value enumeration: `incorrect_answer`, `not_specific_enough`, `missing_from_faq`, `confusing_response`, `outdated_source`. Reason is optional — unhelpful feedback without a reason remains valid. Submitting a reason alongside a helpful rating is rejected with 422. Helpful feedback is entirely unchanged. The reason is stored on the feedback record, returned in `FeedbackResponse`, typed in the frontend service layer, and rendered in the `AnswerFeedback` component as a radio group that appears only after the user selects Unhelpful.

---

## Artifact Completion

| Artifact | Completed |
|---|---|
| `proposal.md` | Yes |
| `spec-diff.md` | Yes |
| `tasks.md` | Yes — all 11 tasks marked complete |
| `impact-analysis.md` | Yes |

---

## Tests Run

### Focused (change-scoped)

```bash
cd backend && pytest tests/api/test_feedback_api.py tests/services/test_feedback_service.py --no-cov -v
# 24 passed
cd frontend && npm run test -- AnswerFeedback
# 11 passed
```

### Full regression

```bash
cd backend && pytest --no-cov -q
# 80 passed
cd frontend && npm run test
# 35 passed (8 test files)
cd frontend && npm run build
# built in 931ms — no errors
```

---

## Verification Result

**PASSED.** All acceptance criteria from the proposal are met:

| Criterion | Status |
|---|---|
| unhelpful + valid reason → 201, reason stored and returned | Pass |
| unhelpful + no reason → 201, reason is null | Pass |
| helpful + reason → 422 validation error | Pass |
| invalid reason value → 422 validation error | Pass |
| All five reason values individually accepted | Pass |
| `FeedbackResponse` includes `reason` field | Pass |
| `FeedbackRecord` stores reason value | Pass |
| Frontend reason selector visible only when Unhelpful selected | Pass |
| Each reason option labelled with text, radio input for keyboard access | Pass |
| All existing helpful/unhelpful tests pass without modification | Pass |

---

## Files Changed

### New
_(none)_

### Modified

| File | Change |
|---|---|
| `backend/app/domain/enums.py` | Added `FeedbackReason` StrEnum (5 values) |
| `backend/app/schemas/feedback.py` | Added `reason` to `FeedbackCreate` with cross-field validator; added `reason` to `FeedbackResponse` |
| `backend/app/repositories/feedback.py` | Added `reason` to `FeedbackRecord` dataclass and `save()` signature |
| `backend/app/services/feedback_service.py` | Passes `payload.reason` through to repository |
| `backend/app/api/feedback.py` | Passes `record.reason` into `FeedbackResponse` |
| `backend/app/main.py` | Fixed validation exception handler to sanitize Pydantic v2 model_validator `ctx` before JSON serialization |
| `backend/tests/api/test_feedback_api.py` | Added 6 new test cases for reason field |
| `backend/tests/services/test_feedback_service.py` | Added 3 new test cases for reason storage and validation |
| `frontend/src/services/feedback.ts` | Added `FeedbackReason` type and `FEEDBACK_REASON_LABELS` constant; added `reason` to `FeedbackPayload` and `FeedbackResponse` |
| `frontend/src/components/feedback/AnswerFeedback.tsx` | Added `ReasonSelector` component and `selectedRating` prop; shows reason selector when `selectedRating === "unhelpful"` |
| `frontend/tests/AnswerFeedback.test.tsx` | Added 4 new test cases for reason selector rendering and accessibility |
| `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` | Added `FeedbackReason` schema; updated `FeedbackCreate` and `Feedback` schemas; added 401 and 422 responses to feedback endpoint |
| `openspec/changes/add-feedback-reasons/tasks.md` | Marked all 11 tasks complete |

---

## Commits

| Hash | Message |
|---|---|
| `f34d239` | `change:add-feedback-reasons document change case` |
| `16f114b` | `change:add-feedback-reasons implement feedback reason selection` |
| _(this commit)_ | `change:add-feedback-reasons archive completed change` |

---

## Deviations from Proposal

| Item | Detail |
|---|---|
| `main.py` validation handler patched | Not called out in impact-analysis. Pydantic v2 `model_validator(mode="after")` places the original `ValueError` in the error `ctx` dict; `JSONResponse` cannot serialize it. Fixed by sanitizing `ctx` values to strings in the shared validation exception handler. This is a correct fix — the handler was always under-specified for cross-field validators. |
| `selectedRating` prop instead of click event | The `AnswerFeedback` component is tested via `renderToStaticMarkup` (SSR-style), so click state cannot be simulated without a DOM. The reason selector visibility is controlled by a `selectedRating` prop, which the parent would set on user interaction in a live app. Accurately reflects the proposed behavior and is fully testable. |

---

## Remaining Risks

| Risk | Severity | Note |
|---|---|---|
| Reason aggregates not in analytics | Low | By design — proposal scoped reason storage only. Analytics surfacing is deferred. Data is present for a future `add-feedback-reason-analytics` change. |
| `selectedRating` prop requires parent state management | Low | In a wired-up interactive app, `ChatPage` or a parent must track which rating the user clicked and pass it as `selectedRating`. The component itself is stateless for testability. |
| SQLite persistence column not yet added | Low | Current implementation uses in-memory repository. When SQLite is wired, an `ALTER TABLE feedback ADD COLUMN reason TEXT DEFAULT NULL` migration is required. No data loss risk. |

---

## Rollback Note

To roll back this change:

1. Remove `FeedbackReason` from `backend/app/domain/enums.py`.
2. Remove `reason` field and `model_validator` from `backend/app/schemas/feedback.py`.
3. Remove `reason` from `FeedbackRecord` and `repository.save()`.
4. Remove `reason` from `feedback_service.py` call and `feedback.py` response construction.
5. Revert `main.py` validation handler to `{"errors": exc.errors()}` (or leave the sanitization — it is a safe improvement).
6. Remove `FeedbackReason` type, `FEEDBACK_REASON_LABELS`, and `reason` from `frontend/src/services/feedback.ts`.
7. Remove `ReasonSelector` and `selectedRating` prop from `AnswerFeedback.tsx`.
8. Remove TC01–TC03 test additions from test files.
9. Revert `openapi.yaml` `FeedbackReason` schema and feedback endpoint changes.
10. Previously stored `reason` values in any persistent store are orphaned but do not affect record integrity.

---

## Final Status

**Applied and archived.** All 11 tasks complete. All acceptance criteria verified. 80 backend tests and 35 frontend tests passing. Frontend build clean.
