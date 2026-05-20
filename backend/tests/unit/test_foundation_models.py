from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.domain.enums import (
    AnswerState,
    FaqSourceStatus,
    FeedbackRating,
    ReadinessState,
    Role,
    UnansweredReason,
)
from app.schemas.common import ErrorResponse


def test_domain_enums_reject_unsupported_values() -> None:
    assert Role.ADMIN == "admin"
    assert Role.END_USER == "end_user"
    assert FaqSourceStatus.ACTIVE == "active"
    assert ReadinessState.READY == "ready"
    assert AnswerState.UNSUPPORTED == "unsupported"
    assert FeedbackRating.HELPFUL == "helpful"
    assert UnansweredReason.NO_ACTIVE_SOURCE == "no_active_source"

    with pytest.raises(ValueError):
        Role("owner")


def test_error_response_requires_code_and_message() -> None:
    response = ErrorResponse(code="not_found", message="Resource not found")

    assert response.model_dump() == {
        "code": "not_found",
        "message": "Resource not found",
        "details": None,
    }

    with pytest.raises(ValidationError):
        ErrorResponse(code="", message="")
