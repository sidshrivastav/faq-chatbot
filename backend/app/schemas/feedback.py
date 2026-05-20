from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.domain.enums import FeedbackRating


class FeedbackCreate(BaseModel):
    rating: FeedbackRating
    comment: str | None = None


class FeedbackResponse(BaseModel):
    id: str
    answer_id: str
    question_id: str
    use_case_id: str
    faq_source_id_at_time: str | None
    rating: FeedbackRating
    comment: str | None
    created_at: datetime
