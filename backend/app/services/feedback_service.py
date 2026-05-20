from __future__ import annotations

from app.repositories.chat import InMemoryChatRepository
from app.repositories.feedback import FeedbackRecord, InMemoryFeedbackRepository
from app.schemas.feedback import FeedbackCreate


class AnswerNotFoundError(Exception):
    pass


class DuplicateFeedbackError(Exception):
    pass


class FeedbackService:
    def __init__(
        self,
        *,
        chat_repository: InMemoryChatRepository,
        feedback_repository: InMemoryFeedbackRepository,
    ) -> None:
        self.chat_repository = chat_repository
        self.feedback_repository = feedback_repository

    def submit_feedback(
        self,
        *,
        answer_id: str,
        user_id: str,
        payload: FeedbackCreate,
    ) -> FeedbackRecord:
        answer = self.chat_repository.answers.get(answer_id)
        if answer is None:
            raise AnswerNotFoundError(answer_id)

        existing = self.feedback_repository.find_by_answer_and_user(
            answer_id=answer_id, user_id=user_id
        )
        if existing is not None:
            raise DuplicateFeedbackError(answer_id)

        return self.feedback_repository.save(
            answer_id=answer_id,
            question_id=answer.question_id,
            use_case_id=answer.use_case_id,
            faq_source_id_at_time=answer.faq_source_id_at_time,
            user_id=user_id,
            rating=payload.rating,
            comment=payload.comment,
        )
