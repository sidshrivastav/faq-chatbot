# Data Model: Configurable FAQ Knowledge Assistant

## User

Represents a person using the assistant.

Fields:

- `id`: unique identifier
- `email`: unique email or local-development identity label
- `display_name`: user-facing name
- `role`: `admin` or `end_user`
- `created_at`
- `updated_at`

Validation:

- Role must be one of the supported roles.
- Admin-only actions require `role = admin`.

Relationships:

- User creates questions and feedback.
- Admin users may create and update FAQ sources.

## UseCase

Represents a business context such as HR, IT support, product support, or admissions.

Fields:

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

Validation:

- Name is required and unique.
- Inactive use cases are not offered for new chat questions unless explicitly shown as unavailable.

Relationships:

- Has many FAQ sources.
- Has zero or one active FAQ source.
- Has many questions, answers, feedback records, and analytics records through related activity.

## FaqSource

Represents an admin-managed FAQ content collection assigned to a use case.

Fields:

- `id`
- `use_case_id`
- `name`
- `description`
- `status`: `draft`, `ready`, `active`, `inactive`, `invalid`, `archived`
- `is_active`
- `version`
- `readiness_state`: `not_checked`, `ready`, `invalid`, `warning`
- `readiness_message`
- `created_by_user_id`
- `updated_by_user_id`
- `created_at`
- `updated_at`
- `activated_at`
- `archived_at`

Validation:

- Name and use case are required.
- A source cannot be activated unless readiness permits Q&A.
- At most one active FAQ source may exist per use case.
- Archived or invalid sources cannot be active.

State transitions:

- `draft` -> `ready` after valid content is present.
- `ready` -> `active` when admin activates it.
- Existing active source for the same use case -> `inactive` when another source is activated.
- `active` -> `inactive` when admin deactivates it.
- Any non-deleted source -> `archived` when archived.
- `draft` or `ready` -> `invalid` when content is empty, unreadable, or unusable.

Relationships:

- Belongs to a UseCase.
- Has many FaqEntries.
- Referenced by Questions and Answers as source-at-time.

## FaqEntry

Represents one searchable FAQ item inside a source.

Fields:

- `id`
- `faq_source_id`
- `question_text`
- `answer_text`
- `keywords`
- `sort_order`
- `is_valid`
- `validation_message`
- `created_at`
- `updated_at`

Validation:

- Question text and answer text are required for valid entries.
- Invalid entries are excluded from retrieval.
- Duplicate or conflicting entries create warnings on the parent source.

Relationships:

- Belongs to a FaqSource.
- May be cited as retrieved context for an Answer.

## Conversation

Represents a current chat session context.

Fields:

- `id`
- `user_id`
- `use_case_id`
- `created_at`
- `updated_at`

Validation:

- Use case is required for chat questions.

Relationships:

- Belongs to User and UseCase.
- Has many Questions.

## Question

Represents a natural-language user question.

Fields:

- `id`
- `conversation_id`
- `user_id`
- `use_case_id`
- `question_text`
- `active_source_id_at_time`
- `created_at`

Validation:

- Question text must not be empty or whitespace-only.
- Use case is required.

Relationships:

- Has zero or one Answer.
- May produce an UnansweredQuestion record.

## Answer

Represents an assistant response or unsupported-answer message.

Fields:

- `id`
- `question_id`
- `use_case_id`
- `faq_source_id_at_time`
- `answer_text`
- `answer_state`: `answered`, `unsupported`, `no_active_source`, `error`
- `grounding_summary`
- `retrieved_entry_ids`
- `created_at`

Validation:

- `answered` requires source context and at least one retrieved valid FAQ entry.
- `unsupported` and `no_active_source` must use clear user-facing messages and cannot include unsupported factual claims.
- Answer source must match the active source at question time.

Relationships:

- Belongs to Question.
- Has zero or many Feedback records.

## Feedback

Represents a user rating and optional comment on an answer or unanswered state.

Fields:

- `id`
- `answer_id`
- `question_id`
- `user_id`
- `use_case_id`
- `faq_source_id_at_time`
- `rating`: `helpful` or `unhelpful`
- `comment`
- `created_at`

Validation:

- Rating is required.
- Comment is optional.
- Feedback must attach to an existing answer or unanswered response.

Relationships:

- Belongs to Answer, Question, User, UseCase, and source-at-time.

## UnansweredQuestion

Represents a question the active FAQ source could not answer sufficiently.

Fields:

- `id`
- `question_id`
- `use_case_id`
- `faq_source_id_at_time`
- `reason`: `no_active_source`, `insufficient_context`, `ambiguous_question`, `source_not_ready`
- `review_status`: `new`, `reviewed`, `dismissed`
- `created_at`
- `reviewed_at`

Validation:

- Must reference a question.
- Reason is required.

Relationships:

- Belongs to Question and UseCase.
- May reference the source active at the time, if one existed.
- May have related Feedback through the Answer.

## AnalyticsSummary

Represents aggregated values returned to admin screens. It may be computed on demand for initial implementation.

Fields:

- `time_period_start`
- `time_period_end`
- `use_case_id`
- `faq_source_id`
- `question_count`
- `answered_count`
- `unanswered_count`
- `helpful_feedback_count`
- `unhelpful_feedback_count`

Validation:

- Counts must be non-negative.
- Filters must align to existing use cases and sources when provided.
