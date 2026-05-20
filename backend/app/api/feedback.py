from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.chat import get_chat_service, reset_chat_repository
from app.auth.dependencies import get_current_user
from app.auth.models import CurrentUser
from app.repositories.feedback import InMemoryFeedbackRepository
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import AnswerNotFoundError, DuplicateFeedbackError, FeedbackService

router = APIRouter(tags=["Feedback"])

_feedback_repository = InMemoryFeedbackRepository()


def get_feedback_service() -> FeedbackService:
    chat_service = get_chat_service()
    return FeedbackService(
        chat_repository=chat_service.chat_repository,
        feedback_repository=_feedback_repository,
    )


def reset_feedback_repository() -> None:
    _feedback_repository.clear()


@router.post("/answers/{answer_id}/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    answer_id: str,
    payload: FeedbackCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    try:
        record = service.submit_feedback(
            answer_id=answer_id,
            user_id=current_user.id,
            payload=payload,
        )
    except AnswerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": "Answer not found", "details": None},
        ) from exc
    except DuplicateFeedbackError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "conflict", "message": "Feedback already submitted for this answer", "details": None},
        ) from exc

    return FeedbackResponse(
        id=record.id,
        answer_id=record.answer_id,
        question_id=record.question_id,
        use_case_id=record.use_case_id,
        faq_source_id_at_time=record.faq_source_id_at_time,
        rating=record.rating,
        comment=record.comment,
        created_at=record.created_at,
    )
