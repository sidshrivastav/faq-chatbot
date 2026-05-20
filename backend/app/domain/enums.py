from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    END_USER = "end_user"


class FaqSourceStatus(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    ACTIVE = "active"
    INACTIVE = "inactive"
    INVALID = "invalid"
    ARCHIVED = "archived"


class ReadinessState(StrEnum):
    NOT_CHECKED = "not_checked"
    READY = "ready"
    INVALID = "invalid"
    WARNING = "warning"


class AnswerState(StrEnum):
    ANSWERED = "answered"
    UNSUPPORTED = "unsupported"
    NO_ACTIVE_SOURCE = "no_active_source"
    ERROR = "error"


class FeedbackRating(StrEnum):
    HELPFUL = "helpful"
    UNHELPFUL = "unhelpful"


class UnansweredReason(StrEnum):
    NO_ACTIVE_SOURCE = "no_active_source"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    AMBIGUOUS_QUESTION = "ambiguous_question"
    SOURCE_NOT_READY = "source_not_ready"
