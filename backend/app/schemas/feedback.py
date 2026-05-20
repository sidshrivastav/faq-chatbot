from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, model_validator

from app.domain.enums import FeedbackRating, FeedbackReason


class FeedbackCreate(BaseModel):
    rating: FeedbackRating
    comment: str | None = None
    reason: FeedbackReason | None = None

    @model_validator(mode="after")
    def reason_only_on_unhelpful(self) -> "FeedbackCreate":
        if self.reason is not None and self.rating == FeedbackRating.HELPFUL:
            raise ValueError("reason may only be provided when rating is unhelpful")
        return self


class FeedbackResponse(BaseModel):
    id: str
    answer_id: str
    question_id: str
    use_case_id: str
    faq_source_id_at_time: str | None
    rating: FeedbackRating
    reason: FeedbackReason | None
    comment: str | None
    created_at: datetime
