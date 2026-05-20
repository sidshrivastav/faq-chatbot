"""
T043 – Service tests for feedback association rules.

Covers:
- Feedback stores rating, optional comment, answer_id, question_id, use_case_id, source_at_time
- Helpful and unhelpful ratings are accepted
- Comment is optional
- Missing answer raises AnswerNotFoundError
- Duplicate feedback raises DuplicateFeedbackError
"""
from __future__ import annotations

import pytest

from app.domain.enums import AnswerState, FeedbackRating, UnansweredReason
from app.repositories.chat import AnswerRecord, InMemoryChatRepository
from app.repositories.feedback import InMemoryFeedbackRepository
from app.schemas.feedback import FeedbackCreate
from app.services.feedback_service import AnswerNotFoundError, DuplicateFeedbackError, FeedbackService
from app.schemas.faq_source import utc_now


def _make_answer(
    answer_id: str = "ans-1",
    question_id: str = "q-1",
    use_case_id: str = "hr",
    faq_source_id_at_time: str | None = "src-1",
    answer_state: AnswerState = AnswerState.ANSWERED,
) -> AnswerRecord:
    return AnswerRecord(
        id=answer_id,
        question_id=question_id,
        use_case_id=use_case_id,
        faq_source_id_at_time=faq_source_id_at_time,
        answer_text="Test answer.",
        answer_state=answer_state,
        grounding_summary="HR handbook",
        retrieved_entry_ids=["entry-1"],
        created_at=utc_now(),
    )


@pytest.fixture()
def chat_repo() -> InMemoryChatRepository:
    repo = InMemoryChatRepository()
    repo.answers["ans-1"] = _make_answer()
    return repo


@pytest.fixture()
def feedback_repo() -> InMemoryFeedbackRepository:
    return InMemoryFeedbackRepository()


@pytest.fixture()
def service(chat_repo: InMemoryChatRepository, feedback_repo: InMemoryFeedbackRepository) -> FeedbackService:
    return FeedbackService(chat_repository=chat_repo, feedback_repository=feedback_repo)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_helpful_feedback_is_persisted(service: FeedbackService) -> None:
    record = service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.HELPFUL),
    )
    assert record.rating == FeedbackRating.HELPFUL
    assert record.answer_id == "ans-1"
    assert record.question_id == "q-1"
    assert record.use_case_id == "hr"
    assert record.faq_source_id_at_time == "src-1"
    assert record.comment is None


def test_unhelpful_feedback_with_comment(service: FeedbackService) -> None:
    record = service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.UNHELPFUL, comment="Too vague."),
    )
    assert record.rating == FeedbackRating.UNHELPFUL
    assert record.comment == "Too vague."


def test_feedback_on_no_active_source_answer(
    chat_repo: InMemoryChatRepository,
    feedback_repo: InMemoryFeedbackRepository,
) -> None:
    chat_repo.answers["ans-unanswered"] = _make_answer(
        answer_id="ans-unanswered",
        faq_source_id_at_time=None,
        answer_state=AnswerState.NO_ACTIVE_SOURCE,
    )
    svc = FeedbackService(chat_repository=chat_repo, feedback_repository=feedback_repo)
    record = svc.submit_feedback(
        answer_id="ans-unanswered",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.UNHELPFUL),
    )
    assert record.faq_source_id_at_time is None
    assert record.rating == FeedbackRating.UNHELPFUL


def test_feedback_record_has_unique_id(service: FeedbackService) -> None:
    r1 = service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.HELPFUL),
    )
    # A second answer so we can get a second feedback id
    service.chat_repository.answers["ans-2"] = _make_answer(answer_id="ans-2", question_id="q-2")
    r2 = service.submit_feedback(
        answer_id="ans-2",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.HELPFUL),
    )
    assert r1.id != r2.id


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

def test_feedback_on_missing_answer_raises(service: FeedbackService) -> None:
    with pytest.raises(AnswerNotFoundError):
        service.submit_feedback(
            answer_id="nonexistent",
            user_id="user-1",
            payload=FeedbackCreate(rating=FeedbackRating.HELPFUL),
        )


# ---------------------------------------------------------------------------
# TC02 – add-feedback-reasons: reason stored on record
# ---------------------------------------------------------------------------

def test_reason_stored_on_unhelpful_feedback_record(service: FeedbackService) -> None:
    from app.domain.enums import FeedbackReason
    record = service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.UNHELPFUL, reason=FeedbackReason.NOT_SPECIFIC_ENOUGH),
    )
    assert record.reason == FeedbackReason.NOT_SPECIFIC_ENOUGH


def test_reason_is_none_when_not_provided(service: FeedbackService) -> None:
    record = service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.UNHELPFUL),
    )
    assert record.reason is None


def test_helpful_feedback_with_reason_raises_validation_error() -> None:
    from pydantic import ValidationError
    from app.domain.enums import FeedbackReason
    with pytest.raises(ValidationError):
        FeedbackCreate(rating=FeedbackRating.HELPFUL, reason=FeedbackReason.OUTDATED_SOURCE)


def test_duplicate_feedback_raises(service: FeedbackService) -> None:
    service.submit_feedback(
        answer_id="ans-1",
        user_id="user-1",
        payload=FeedbackCreate(rating=FeedbackRating.HELPFUL),
    )
    with pytest.raises(DuplicateFeedbackError):
        service.submit_feedback(
            answer_id="ans-1",
            user_id="user-1",
            payload=FeedbackCreate(rating=FeedbackRating.UNHELPFUL),
        )
