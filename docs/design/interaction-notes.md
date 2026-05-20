# Interaction Notes

## Purpose

This document records UI behavior, states, accessibility considerations, and interaction rules for the Configurable FAQ Knowledge Assistant.

Source requirements: `specs/001-faq-knowledge-assistant/spec.md`

## Global Interaction Principles

- Keep use case context visible wherever answers, sources, or analytics are shown.
- Make active versus inactive FAQ source state explicit in text.
- Never imply that unsupported answers are available when the active FAQ source cannot answer.
- Keep admin workflows task-focused and dense enough for repeated management work.
- Keep end-user chat simple, with feedback controls close to the related answer.

## Grounded Answer Behavior

### Answer Available

When the active FAQ source contains enough information:

- Show the answer in the conversation.
- Keep the selected use case visible.
- Attach feedback controls to the answer.
- Avoid exposing unrelated or inactive source content in the answer experience.

### Answer Not Available

When the active FAQ source cannot answer:

- Show a plain-language unanswered message.
- Avoid speculative wording.
- Keep feedback controls available.
- Ensure the unanswered state can be reviewed by admins later.

### No Active Source

When the selected use case has no active FAQ source:

- Show a clear no-active-source message.
- Disable or constrain question submission for that use case.
- Offer use case switching when other answerable use cases exist.

## FAQ Source Management Interactions

### Add Source

- Admin selects Add Source from the FAQ Sources list.
- Required fields should be clearly marked.
- Save should be unavailable until minimum required information is present.
- Readiness status should appear after content is provided.

### Edit or Replace Source

- Admin opens a source detail or edit screen.
- Existing content and source context should remain visible.
- Saving should preserve entered changes if an error occurs.
- Any change that affects end-user answers should be confirmed.

### Activate Source

- Activation should show the use case affected.
- If another source is active, the confirmation should explain that the new source becomes the answer source for future questions.
- Activation should not hide historical analytics tied to previous sources.

### Deactivate Source

- Deactivation should warn when it leaves a use case without an active source.
- The warning should describe the end-user impact: questions for that use case cannot receive grounded answers.

### Delete or Archive Source

- Destructive actions require confirmation.
- Archive should be preferred where historical interpretation matters.
- The confirmation copy should name the source and use case.

## Chat Interactions

### Composer

- Empty or whitespace-only questions cannot be sent.
- While an answer is loading, the latest submitted question remains visible.
- Users should not lose typed text after recoverable errors.

### Conversation

- Messages appear in chronological order.
- User questions and assistant responses should be visually distinct.
- The current conversation history remains visible during the session.
- The most recent answer should be easy to locate after loading completes.

### Follow-Up Questions

- Follow-up questions still use the active FAQ source for the selected use case.
- If a follow-up relies on missing context, the assistant should ask for a clearer question or mark the answer unsupported.

## Feedback Interactions

### Helpful Feedback

- User selects helpful.
- Inline confirmation appears.
- The selected state remains visible.
- Optional comment can be offered but should not be required.

### Unhelpful Feedback

- User selects unhelpful.
- Optional comment input appears immediately.
- User can submit the rating with or without a comment.
- Confirmation appears after submission.

### Feedback Error

- Keep the selected rating and comment text.
- Show an inline error near the feedback controls.
- Provide a retry action.

## Analytics Interactions

### Filters

- Filters include use case, FAQ source, and time period.
- Filter selections should remain visible while data is loading.
- If a filter combination has no results, show a no-results state rather than blank metrics.

### Metrics

- Question volume, answered count, unanswered count, helpful feedback, and unhelpful feedback should be readable as standalone values.
- Metric labels must be unambiguous.
- Metric drill-downs should preserve selected filters where possible.

### Unanswered Question Review

- Unanswered question lists should support scanning by question text, use case, source, and time.
- Opening a question should show the full question and the source context at the time it was asked.
- Returning to the list should preserve filters and scroll position where practical.

## Loading States

- Use case list: show loading state in the selection area.
- Chat answer: show a response-in-progress state attached to the latest question.
- FAQ source list: show row or card placeholders.
- Source save: disable conflicting actions and show save progress.
- Analytics: show metric-level loading indicators without removing filters.
- Unanswered questions: show list-level loading state.

## Empty States

- No FAQ sources: prompt admin to add a source.
- No active source: explain that end-user answers are unavailable for the use case.
- No chat history: invite the user to ask the first question.
- No analytics: explain that metrics appear after questions and feedback exist.
- No unanswered questions: state that no unanswered questions match the current view.
- No feedback: explain that feedback appears after users rate answers.

## Error States

- Invalid FAQ source: explain what prevents readiness and how admin can correct it.
- Unauthorized access: state that the current role cannot access the requested admin area.
- Failed answer: explain that the answer could not be prepared and allow retry.
- Unsupported answer: state that the active FAQ source does not contain enough information.
- Failed feedback submission: preserve input and allow retry.
- Failed analytics load: keep filters visible and allow retry.

## Accessibility Notes

- Use semantic headings that match page hierarchy.
- All controls must have accessible names.
- Do not communicate active, invalid, helpful, or unhelpful states with color alone.
- Keyboard users must be able to reach navigation, filters, chat input, send action, source actions, feedback controls, and dialogs.
- Focus should move predictably after opening dialogs, submitting forms, and closing confirmations.
- Confirmation and error messages should be announced to assistive technologies.
- Chat updates should be announced without moving focus unexpectedly.
- Tables or list-based analytics must expose labels for metrics, filters, and row actions.
- Touch targets for feedback, source actions, and filters should be large enough for comfortable selection.

## Copy Tone

- Use direct, specific language.
- For unsupported questions, say that the answer is not available in the active FAQ source.
- For invalid sources, describe the admin action needed rather than technical failure details.
- For access denial, explain the role limitation without exposing admin-only details.
