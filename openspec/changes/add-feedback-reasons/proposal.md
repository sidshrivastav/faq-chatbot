# Change Proposal: add-feedback-reasons

## Change ID
`add-feedback-reasons`

## Type
Add feature

## Problem Statement
When users mark an answer as unhelpful, there is no structured way for them to communicate why the answer was poor. Admins reviewing feedback in analytics can see that a response was rated unhelpful but cannot distinguish between an answer that was factually wrong versus one that was simply incomplete or drawn from an outdated source. This makes targeted FAQ improvement difficult.

## Current Behavior
- `POST /answers/{answer_id}/feedback` accepts `rating` (helpful | unhelpful) and an optional free-text `comment`.
- No structured reason field exists.
- `FeedbackCreate` schema: `{ rating, comment? }`.
- `FeedbackRecord` and `FeedbackResponse` do not include a reason field.
- The `AnswerFeedback` frontend component presents Helpful / Unhelpful buttons and an optional comment textarea but no structured reason selector.

## Proposed Behavior
- When a user submits unhelpful feedback, they may optionally select one structured reason from a fixed enumeration:
  - `incorrect_answer` — the answer contained wrong information
  - `not_specific_enough` — the answer was too vague or high-level
  - `missing_from_faq` — the question is not covered by the FAQ source
  - `confusing_response` — the answer was unclear or hard to follow
  - `outdated_source` — the answer appears to reference outdated content
- Reason selection is **optional** — unhelpful feedback without a reason remains valid.
- Reason is **only accepted when `rating` is `unhelpful`** — submitting a reason with a helpful rating is a validation error.
- Helpful feedback continues to work exactly as before.
- The reason is stored on the feedback record and returned in `FeedbackResponse`.
- The frontend `AnswerFeedback` component shows the reason selector only after the user clicks Unhelpful.

## User Impact
- End users can communicate structured reasons for dissatisfaction in one click rather than writing free text.
- Admins gain a machine-readable signal for FAQ improvement decisions (e.g., if `missing_from_faq` appears frequently for a use case, new FAQ entries are needed).

## Business / Product Value
- Improves actionability of feedback for FAQ content maintenance.
- Provides a signal for use-case-level source quality without requiring analytics queries on free text.
- Aligns with FR-015 (optional comments) by adding a complementary structured path.

## Acceptance Criteria

1. `POST /answers/{answer_id}/feedback` with `rating: unhelpful` and a valid `reason` → 201, reason stored and returned.
2. `POST /answers/{answer_id}/feedback` with `rating: unhelpful` and no reason → 201, reason is `null`, existing behavior preserved.
3. `POST /answers/{answer_id}/feedback` with `rating: helpful` and a reason → 422 validation error.
4. `POST /answers/{answer_id}/feedback` with an invalid reason value → 422 validation error.
5. `FeedbackResponse` includes `reason` field (`null` or a valid enum value).
6. `FeedbackRecord` stores the reason value.
7. `AnswerFeedback` frontend component shows the reason selector when the user clicks Unhelpful and hides it when the user clicks Helpful.
8. Reason selector renders each option as text (not color alone) and is keyboard-accessible.
9. All existing helpful/unhelpful tests continue to pass without modification.

## Out of Scope
- Making reason mandatory for unhelpful feedback.
- Adding reasons for helpful feedback.
- Surfacing reason aggregates in analytics (Phase 6 work; data is stored for future use).
- Free-text "other" reason — only the five enumerated values are valid.
- Changing or removing the free-text `comment` field.

## Rollback Plan
If rolled back:
- Remove `reason` field from `FeedbackCreate`, `FeedbackResponse`, and `FeedbackRecord`.
- Remove `FeedbackReason` enum from `domain/enums.py`.
- Revert `AnswerFeedback` component to idle state without reason selector.
- Previously stored `reason` values in the database become orphaned but do not affect correctness of other records.
- Existing tests continue to pass as reason was always optional.
