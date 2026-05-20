# Tasks: add-feedback-reasons

Change ID: `add-feedback-reasons`
Type: Add feature
Verification: `pytest backend/tests/api/test_feedback_api.py backend/tests/services/test_feedback_service.py --no-cov` and `npm run test -- AnswerFeedback`

---

## Test Tasks

- [x] TC01 Update `backend/tests/api/test_feedback_api.py` — add failing cases:
  - unhelpful + valid reason → 201, reason in response
  - unhelpful + no reason → 201, reason is null (regression: existing behavior)
  - helpful + reason → 422
  - invalid reason string → 422
  - (Est: 1h; test scenario: new 422 case fails before schema cross-field validator is added)

- [x] TC02 Update `backend/tests/services/test_feedback_service.py` — add failing cases:
  - reason stored on `FeedbackRecord` when submitted with unhelpful rating
  - reason is `None` on `FeedbackRecord` when not submitted
  - (Est: 1h; test scenario: tests fail before `reason` field added to record and `save()`)

- [x] TC03 Update `frontend/tests/AnswerFeedback.test.tsx` — add failing cases:
  - reason selector visible after user clicks Unhelpful
  - reason selector hidden when state is idle or saved with helpful rating
  - each reason option renders with accessible text label
  - (Est: 1h; test scenario: tests fail before reason selector added to component)

---

## Backend Tasks

- [x] TC04 Add `FeedbackReason` StrEnum to `backend/app/domain/enums.py`
  - Values: `incorrect_answer`, `not_specific_enough`, `missing_from_faq`, `confusing_response`, `outdated_source`
  - (Est: 0.5h; test scenario: `python -m compileall backend/app` succeeds)

- [x] TC05 Update `backend/app/schemas/feedback.py`
  - Add `reason: FeedbackReason | None = None` to `FeedbackCreate`
  - Add `model_validator` (or `field_validator`) rejecting `reason` when `rating == helpful`
  - Add `reason: FeedbackReason | None` to `FeedbackResponse`
  - (Est: 1h; test scenario: TC01 validation cases pass)

- [x] TC06 Update `backend/app/repositories/feedback.py`
  - Add `reason: FeedbackReason | None` to `FeedbackRecord` dataclass
  - Add `reason` parameter to `InMemoryFeedbackRepository.save()`
  - (Est: 0.5h; test scenario: TC02 record storage cases pass)

- [x] TC07 Update `backend/app/services/feedback_service.py`
  - Pass `payload.reason` through to `feedback_repository.save()`
  - (Est: 0.5h; test scenario: TC02 service tests pass end-to-end)

- [x] TC08 Update `backend/app/api/feedback.py`
  - Pass `record.reason` into `FeedbackResponse`
  - (Est: 0.5h; test scenario: TC01 API tests pass end-to-end)

---

## Frontend Tasks

- [x] TC09 Update `frontend/src/services/feedback.ts`
  - Add `reason?: FeedbackReason | null` to `FeedbackPayload` type
  - Add `FeedbackReason` type export matching the five enum values
  - (Est: 0.5h; test scenario: TypeScript build succeeds)

- [ ] TC10 Update `frontend/src/components/feedback/AnswerFeedback.tsx`
  - Add `reason` prop and `selectedReason` to component state/props
  - Show reason selector (radio group or select) after user clicks Unhelpful
  - Hide reason selector when state is idle before selection, or after Helpful is chosen
  - Render each of the five options with visible text label and `aria-label`
  - Pass selected reason to submission handler
  - (Est: 2h; test scenario: TC03 frontend tests pass)

---

## Documentation Tasks

- [ ] TC11 Update `specs/001-faq-knowledge-assistant/contracts/openapi.yaml`
  - Add `FeedbackReason` enum schema
  - Add `reason` field to feedback request and response schemas
  - Add 422 description for reason-with-helpful-rating case
  - (Est: 0.5h; test scenario: `openapi.yaml` is valid YAML and paths match implementation)

---

## Verification Commands

```bash
# Backend
cd backend && pytest tests/api/test_feedback_api.py tests/services/test_feedback_service.py --no-cov -v

# Full backend regression
cd backend && pytest --no-cov -q

# Frontend
cd frontend && npm run test -- AnswerFeedback

# Full frontend regression
cd frontend && npm run test

# Build check
cd frontend && npm run build
```

---

## Completion Checklist

- [x] TC01 new API test cases written and passing
- [x] TC02 new service test cases written and passing
- [x] TC03 new frontend test cases written and passing
- [x] TC04 `FeedbackReason` enum added
- [x] TC05 `FeedbackCreate` cross-field validation and `FeedbackResponse` updated
- [x] TC06 `FeedbackRecord` and repository `save()` updated
- [x] TC07 service passes reason through
- [x] TC08 API route passes reason into response
- [x] TC09 frontend service type updated
- [ ] TC10 `AnswerFeedback` component shows reason selector on unhelpful click
- [ ] TC11 OpenAPI contract updated
- [ ] All existing feedback tests still pass
- [ ] Full backend test suite passes
- [ ] Full frontend test suite passes
- [ ] Frontend build passes
