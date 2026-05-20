# Screens

## Purpose

This document describes key screens, layout intent, content priorities, states, and interactions for the Configurable FAQ Knowledge Assistant.

Source requirements: `specs/001-faq-knowledge-assistant/spec.md`

## Screen: End-User Use Case Selection

### Purpose

Help users choose the business context that controls which active FAQ source will be used for answers.

### Layout Intent

- Primary content: list or selector of available use cases.
- Supporting content: short status for whether a use case has an active FAQ source.
- Primary action: continue to chat.

### States

- **Default**: Use cases are available and at least one has an active FAQ source.
- **Loading**: Use case options are being prepared.
- **Empty**: No use cases are available.
- **No active source**: A use case is visible but marked as not currently answerable.
- **Error**: Use cases cannot be loaded; provide a retry action.

### Interaction Notes

- The selected use case must remain visible after entering chat.
- If a selected use case has no active FAQ source, users should see the limitation before asking a question.

## Screen: End-User Chat

### Purpose

Allow users to ask questions and receive grounded answers or clear unanswered messages.

### Layout Intent

- Header: selected use case and active-source availability state.
- Main area: chronological conversation with user questions and assistant responses.
- Composer: question input and send action.
- Response controls: feedback options attached to each assistant response.

### States

- **Empty conversation**: Prompt area is ready for the first question.
- **Loading answer**: The latest question shows a response-in-progress state.
- **Answered**: Assistant response appears with feedback controls.
- **Unanswered**: Assistant explains that the active source does not contain enough information.
- **No active source**: Chat explains that answers are unavailable for the selected use case.
- **Error**: A response could not be prepared; user can retry.

### Interaction Notes

- Sending should be disabled for empty questions.
- The latest response should be easy to distinguish from earlier responses.
- Feedback should stay attached to the answer it refers to.
- Chat history should remain visible during the current conversation.

## Screen: Admin Overview

### Purpose

Give admins a quick operational summary across FAQ sources, answer coverage, feedback, and unanswered questions.

### Layout Intent

- Top summary metrics: active sources, total questions, answered count, unanswered count, helpful and unhelpful feedback.
- Middle section: use case health summary.
- Lower section: recent unanswered questions and sources needing attention.

### States

- **Default**: Metrics and recent activity are populated.
- **Loading**: Metric cards and lists show loading indicators.
- **Empty**: No sources or questions exist yet.
- **Partial data**: Sources exist but no questions or feedback have been recorded.
- **Error**: Overview data cannot be shown; preserve navigation and provide retry.

### Interaction Notes

- Metric cards should link to filtered analytics where useful.
- Source warnings should link to the relevant FAQ source detail.
- Recent unanswered questions should link to unanswered question detail or filtered list.

## Screen: FAQ Sources List

### Purpose

Allow admins to find, compare, and manage FAQ sources by use case and status.

### Layout Intent

- Header: page title and Add Source action.
- Filters: use case, status, active state.
- Source list: source name, use case, active state, readiness, last updated, and actions.

### States

- **Default**: Sources are listed with filter controls.
- **Loading**: List rows or source cards show loading placeholders.
- **Empty**: No sources exist; primary action prompts admin to add one.
- **No filter results**: Explain that no sources match the filters.
- **Error**: Source list cannot be loaded; provide retry.

### Interaction Notes

- Active source should be visually prominent and text-labeled.
- Invalid or unreadable sources should show issue summaries in the list.
- Destructive actions should require confirmation.

## Screen: Add or Edit FAQ Source

### Purpose

Allow admins to add new FAQ content or update an existing source.

### Layout Intent

- Source identity: name and assigned use case.
- Content area: source content entry or upload affordance.
- Readiness panel: status, warnings, and blockers.
- Actions: save, activate when ready, archive, deactivate, delete where applicable.

### States

- **New source**: Required fields are empty.
- **Editing source**: Existing details are loaded.
- **Saving**: Actions are disabled and progress is shown.
- **Ready**: Source can be activated.
- **Invalid**: Source cannot be activated until issues are resolved.
- **Activation conflict**: Another source is active for the use case.
- **Error**: Changes could not be saved; preserve entered content.

### Interaction Notes

- Admins should see the consequence of activating a source before confirmation.
- Deactivating the only active source should warn that end users will not receive answers for that use case.
- Invalid content messages should explain the user-facing problem, not technical causes.

## Screen: FAQ Source Detail

### Purpose

Show source status, assigned use case, active state, readiness, and available management actions.

### Layout Intent

- Summary area: source name, use case, active state, readiness, last updated.
- Content preview or summary: enough for admin review.
- Related performance: basic usage and feedback for that source.
- Management actions: edit, activate, deactivate, archive, delete.

### States

- **Active source**: Shows that this source currently grounds answers.
- **Inactive source**: Shows it is available but not used for answers.
- **Invalid source**: Shows blockers and edit or replace action.
- **Archived source**: Shows limited actions and historical context.

### Interaction Notes

- Active-source status must be text-visible near the title.
- Historical analytics should remain understandable even after updates or replacement.

## Screen: Analytics

### Purpose

Help admins evaluate usage, answer coverage, feedback, and content gaps.

### Layout Intent

- Filters: time period, use case, FAQ source.
- Metrics: question volume, answered count, unanswered count, helpful feedback, unhelpful feedback.
- Trends or comparisons: simple visual summaries.
- Drill-down links: unanswered question list and feedback examples.

### States

- **Default**: Metrics reflect current filters.
- **Loading filters**: Metrics show progress while retaining selected filters.
- **No data yet**: Explain that analytics will appear after questions and feedback exist.
- **No matching results**: Explain that no records match current filters.
- **Error**: Analytics cannot load; provide retry and keep filters visible.

### Interaction Notes

- Filter changes should visibly update all metrics.
- Metrics should be labeled clearly enough to stand without chart interpretation.
- Empty analytics should not be presented as a failure.

## Screen: Unanswered Questions

### Purpose

Allow admins to review questions the active FAQ source could not answer.

### Layout Intent

- Filters: use case, FAQ source, time period.
- List: question text, use case, source at time asked, date, and feedback indicator.
- Detail area or page: full question, unanswered message, feedback, and source context.

### States

- **Default**: Unanswered questions are listed.
- **Loading**: List shows loading state.
- **Empty**: No unanswered questions exist.
- **No filter results**: No unanswered questions match filters.
- **Error**: List cannot load; provide retry.

### Interaction Notes

- Long questions should be scannable without hiding the main context.
- Opening a question should preserve filter context when returning to the list.

## Screen: Feedback Review

### Purpose

Let admins interpret helpful and unhelpful feedback in context.

### Layout Intent

- Filters: rating, use case, source, time period.
- List: rating, optional comment preview, related question, and source.
- Detail: full feedback, answer, question, and source context.

### States

- **Default**: Feedback entries are visible.
- **No feedback yet**: Explain that feedback will appear after users rate answers.
- **No matching results**: No feedback matches selected filters.
- **Error**: Feedback cannot load; provide retry.

### Interaction Notes

- Unhelpful feedback should be easy to find from analytics.
- Optional comments should remain associated with the exact answer they describe.
