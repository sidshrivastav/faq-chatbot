from __future__ import annotations

import pytest

from app.repositories.faq_sources import InMemoryFaqSourceRepository
from app.schemas.faq_source import FaqEntryInput, FaqSourceCreate
from app.services.source_service import SourceNotFoundError, SourceNotReadyError, SourceService


def make_service() -> SourceService:
    return SourceService(InMemoryFaqSourceRepository())


def test_create_source_marks_valid_entries_ready() -> None:
    service = make_service()

    source = service.create_source(
        FaqSourceCreate(
            name="Employee handbook FAQ",
            use_case_id="hr",
            entries=[
                FaqEntryInput(
                    question_text="How do I update tax declarations?",
                    answer_text="Use payroll self-service.",
                )
            ],
        ),
        user_id="admin-1",
    )

    assert source.status == "ready"
    assert source.readiness_state == "ready"
    assert source.readiness_message == "Source is ready for Q&A"


def test_create_source_marks_empty_entries_invalid() -> None:
    service = make_service()

    source = service.create_source(
        FaqSourceCreate(name="Empty FAQ", use_case_id="hr", entries=[]),
        user_id="admin-1",
    )

    assert source.status == "invalid"
    assert source.readiness_state == "invalid"
    assert "At least one valid FAQ entry is required" in source.readiness_message


def test_duplicate_questions_create_warning_readiness() -> None:
    service = make_service()

    source = service.create_source(
        FaqSourceCreate(
            name="Duplicate FAQ",
            use_case_id="hr",
            entries=[
                FaqEntryInput(question_text="Reset password?", answer_text="Use portal."),
                FaqEntryInput(question_text="Reset password?", answer_text="Contact IT."),
            ],
        ),
        user_id="admin-1",
    )

    assert source.status == "ready"
    assert source.readiness_state == "warning"
    assert "Duplicate FAQ questions detected" in source.readiness_message


def test_activation_transitions_only_ready_sources() -> None:
    service = make_service()
    ready = service.create_source(
        FaqSourceCreate(
            name="Ready FAQ",
            use_case_id="hr",
            entries=[FaqEntryInput(question_text="Question?", answer_text="Answer.")],
        ),
        user_id="admin-1",
    )
    invalid = service.create_source(
        FaqSourceCreate(name="Invalid FAQ", use_case_id="hr", entries=[]),
        user_id="admin-1",
    )

    activated = service.activate_source(ready.id)
    assert activated.status == "active"
    assert activated.is_active is True

    with pytest.raises(SourceNotReadyError):
        service.activate_source(invalid.id)


def test_missing_source_raises_not_found() -> None:
    service = make_service()

    with pytest.raises(SourceNotFoundError):
        service.get_source("missing")
