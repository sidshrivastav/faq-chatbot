# User Flows

## Purpose

This document describes the major admin and end-user journeys for the Configurable FAQ Knowledge Assistant. It focuses on user intent, decision points, screen transitions, and states.

Source requirements: `specs/001-faq-knowledge-assistant/spec.md`

## Admin Flow

### Goal

Allow admins to prepare FAQ content, control active sources, monitor usage, and identify unanswered questions.

### Primary Path

1. Admin opens the admin area.
2. Admin reviews overview cards for active sources, unanswered questions, and feedback health.
3. Admin opens FAQ Sources.
4. Admin adds or selects a FAQ source.
5. Admin assigns the source to a use case.
6. Admin reviews readiness status.
7. Admin activates the source for that use case.
8. Admin returns to overview or analytics to monitor behavior.

### Decision Points

- If the source is ready, admin can activate it.
- If the source is invalid, empty, unreadable, or conflicting, admin sees the issue and cannot rely on it for end-user answers.
- If another source is already active for the use case, admin must confirm the active-source change.
- If analytics show many unanswered questions, admin can open the unanswered question list to inspect gaps.

### Key States

- Loading overview metrics
- Empty admin workspace with no FAQ sources
- Source added but not active
- Source active and available for end-user Q&A
- Source invalid or not ready
- Analytics unavailable because no questions exist yet

## FAQ Source Management Flow

### Goal

Allow admins to manage the lifecycle of FAQ sources for use cases such as HR, IT support, product support, and admissions.

### Primary Path

1. Admin opens FAQ Sources.
2. Admin filters or scans sources by use case and status.
3. Admin selects Add Source.
4. Admin provides source name and use case.
5. Admin adds FAQ content.
6. System evaluates whether the source is ready for Q&A.
7. Admin reviews source summary and readiness messages.
8. Admin activates the source if it is ready.

### Update Path

1. Admin opens an existing source.
2. Admin reviews source details and current active state.
3. Admin updates, replaces, archives, deactivates, or deletes the source.
4. Admin confirms changes that affect active end-user answers.
5. Source list and status indicators update.

### Error and Edge Paths

- Empty source: show source as not ready and explain that content is required.
- Duplicate or conflicting entries: show a warning and let admin review before activation.
- Unreadable source: show a clear failure state and ask admin to replace or edit the source.
- Deactivating the only active source: warn that end users will receive a no-active-source message for that use case.

## End-User Chat Flow

### Goal

Allow end users to ask natural-language questions and receive grounded answers based only on the active FAQ source for the selected use case.

### Primary Path

1. End user opens the assistant.
2. User selects or confirms a use case context.
3. Chat screen shows the active context.
4. User enters a natural-language question.
5. Chat shows a loading or thinking state.
6. If the active FAQ source contains enough information, chat shows a grounded answer.
7. User can ask a follow-up question or provide feedback.

### Unsupported Question Path

1. User asks a question that is not covered by the active FAQ source.
2. Chat shows that the assistant cannot answer from the active source.
3. The question is treated as unanswered for admin review.
4. User can submit feedback or ask a different question.

### No Active Source Path

1. User selects a use case with no active FAQ source.
2. Chat input is disabled or clearly constrained.
3. The screen explains that no active FAQ source is available for that use case.
4. User can choose another use case when available.

### Ambiguous Question Path

1. User asks a broad, unclear, or multi-part question.
2. If the active source cannot support a complete answer, chat explains what cannot be answered from the source.
3. When appropriate, chat can ask the user to narrow the question without inventing unsupported content.

## Feedback Flow

### Goal

Allow users to rate answer usefulness and optionally provide comments for admin review.

### Primary Path

1. User receives an answer or unanswered message.
2. Feedback controls appear with helpful and unhelpful options.
3. User selects a rating.
4. Confirmation appears inline.
5. Optional comment input is offered, especially for unhelpful feedback.
6. Submitted feedback remains visibly associated with the answer.

### Error Path

1. User submits feedback.
2. Submission fails.
3. Inline error appears near the feedback controls.
4. User can retry without losing the selected rating or typed comment.

### Interaction Rules

- Feedback should be lightweight and not interrupt chat.
- Users should understand whether feedback has been saved.
- Users should be able to leave a rating without writing a comment.
- Feedback on unanswered messages should be supported.

## Analytics Review Flow

### Goal

Allow admins to understand usage, answer coverage, feedback trends, and content gaps.

### Primary Path

1. Admin opens Analytics.
2. Default view shows a selected time period and all use cases.
3. Admin reviews question volume, answered count, unanswered count, helpful feedback, and unhelpful feedback.
4. Admin filters by use case, FAQ source, or time period.
5. Admin opens unanswered question details when needed.

### Unanswered Question Review Path

1. Admin opens Unanswered Questions from Analytics or primary navigation.
2. Admin filters by use case, FAQ source, and time period.
3. Admin scans unanswered question list.
4. Admin opens a question detail.
5. Admin reviews question text, context, timing, and related active FAQ source.

### Empty and Loading States

- Before questions exist, metrics show zero values with explanatory text.
- While filters are applying, metric areas show loading states without clearing the surrounding context.
- When no results match filters, the screen states that no questions or feedback match the selected filters.
