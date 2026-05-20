# Information Architecture

## Purpose

This document defines the UI-level structure for the Configurable FAQ Knowledge Assistant. It focuses on navigation, content grouping, role-based access, and the relationship between admin and end-user experiences.

Source requirements: `specs/001-faq-knowledge-assistant/spec.md`

## Roles

### Admin

Admins manage FAQ sources, control which source is active for each use case, review answer quality, and inspect unanswered questions.

Primary admin tasks:

- Manage FAQ sources by use case
- Activate or deactivate FAQ sources
- Review source readiness and status
- View analytics by use case, source, and time period
- Review unanswered questions and feedback

### End User

End users ask questions in a use case context and provide feedback on answers.

Primary end-user tasks:

- Select or confirm the active use case context
- Ask natural-language questions
- Review grounded answers or unanswered messages
- Provide helpful or unhelpful feedback
- Add optional feedback comments

## Top-Level Product Areas

### End-User Area

- **Use Case Selection**: Entry point for choosing HR, IT support, product support, admissions, or another available use case.
- **Chat**: Primary Q&A workspace for asking questions and reviewing answers.
- **Answer Feedback**: Lightweight interaction attached to each answer or unanswered response.

### Admin Area

- **Overview**: At-a-glance state across use cases, active FAQ sources, answer coverage, and recent unanswered questions.
- **FAQ Sources**: Manage sources, readiness, active status, and source details.
- **Analytics**: Review question volume, answered versus unanswered counts, and feedback trends.
- **Unanswered Questions**: Inspect content gaps by use case, source, and time period.

## Navigation Model

### Admin Navigation

Recommended primary navigation:

1. Overview
2. FAQ Sources
3. Analytics
4. Unanswered Questions

Admin navigation should remain persistent across admin screens so admins can move quickly between content management and performance review.

### End-User Navigation

Recommended end-user structure:

1. Use case context selector
2. Chat conversation
3. Feedback controls within responses

The end-user experience should minimize navigation. Chat is the main workspace; use case context should be visible and changeable when allowed.

## Content Hierarchy

### Use Case

Use case is the primary organizing concept. It determines which FAQ source is active for answers and how analytics are filtered.

Displayed attributes:

- Use case name
- Active FAQ source status
- Last updated state
- Answer coverage indicators in admin views

### FAQ Source

FAQ source is the admin-managed content unit.

Displayed attributes:

- Source name
- Assigned use case
- Active or inactive state
- Readiness state
- Last updated information
- High-level source health messages

### Question and Answer

Question and answer records appear in chat, analytics, feedback review, and unanswered question review.

Displayed attributes:

- Question text
- Answer or unanswered state
- Use case
- Related active FAQ source at time asked
- Feedback state when available

### Feedback

Feedback is attached to answers or unanswered questions.

Displayed attributes:

- Helpful or unhelpful rating
- Optional comment
- Related question and answer
- Use case and FAQ source context

## Role-Based Access

### Admin-Only Areas

- FAQ source management
- FAQ source activation and deactivation
- Analytics
- Unanswered question review

### End-User Areas

- Use case selection
- Chat-based Q&A
- Answer feedback

### Shared Behavior

Admins may ask questions using the same grounded-answer behavior as end users. When acting in the chat experience, answers must follow the active-source rules.

## Empty State Strategy

### No FAQ Sources

Admin area should explain that answers cannot be served until a FAQ source is added and activated for a use case. Primary action: add FAQ source.

### No Active FAQ Source

End-user chat should show a clear message that no active FAQ source is available for the selected use case. Admin area should show the use case as needing activation.

### No Questions Yet

Analytics should show zero states without implying a failure. Primary guidance: analytics will populate after users ask questions.

### No Unanswered Questions

Unanswered question review should state that no content gaps have been recorded for the current filters.

## State Model for UI

### FAQ Source States

- Draft or newly added
- Ready
- Active
- Inactive
- Invalid or unreadable
- Archived

### Answer States

- Waiting for user question
- Finding answer
- Answered from active source
- Not answerable from active source
- No active source available
- Error while preparing response

### Feedback States

- Not submitted
- Helpful submitted
- Unhelpful submitted
- Comment added
- Feedback submission failed

## Accessibility Notes

- Navigation labels must be explicit and text-based, not icon-only.
- Active use case and active source state must be conveyed with text, not color alone.
- Chat messages should preserve reading order for screen readers.
- Status changes such as loading, answer ready, feedback submitted, and errors should be announced to assistive technologies.
- Tables and metric groups should use clear labels and summaries so admins can understand analytics without relying on visual layout alone.
