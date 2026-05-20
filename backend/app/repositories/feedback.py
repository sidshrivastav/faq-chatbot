from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.domain.enums import FeedbackRating, FeedbackReason
from app.schemas.faq_source import utc_now


@dataclass(slots=True)
class FeedbackRecord:
    id: str
    answer_id: str
    question_id: str
    use_case_id: str
    faq_source_id_at_time: str | None
    user_id: str
    rating: FeedbackRating
    reason: FeedbackReason | None
    comment: str | None
    created_at: datetime


class InMemoryFeedbackRepository:
    def __init__(self) -> None:
        self._records: dict[str, FeedbackRecord] = {}

    def find_by_answer_and_user(self, *, answer_id: str, user_id: str) -> FeedbackRecord | None:
        for record in self._records.values():
            if record.answer_id == answer_id and record.user_id == user_id:
                return record
        return None

    def save(
        self,
        *,
        answer_id: str,
        question_id: str,
        use_case_id: str,
        faq_source_id_at_time: str | None,
        user_id: str,
        rating: FeedbackRating,
        reason: FeedbackReason | None,
        comment: str | None,
    ) -> FeedbackRecord:
        record = FeedbackRecord(
            id=f"feedback_{uuid4().hex}",
            answer_id=answer_id,
            question_id=question_id,
            use_case_id=use_case_id,
            faq_source_id_at_time=faq_source_id_at_time,
            user_id=user_id,
            rating=rating,
            reason=reason,
            comment=comment,
            created_at=utc_now(),
        )
        self._records[record.id] = record
        return record

    def clear(self) -> None:
        self._records.clear()
