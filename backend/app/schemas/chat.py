from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import AnswerState
from app.schemas.faq_source import FaqEntry


class QuestionCreate(BaseModel):
    conversation_id: str | None = None
    use_case_id: str = Field(min_length=1)
    question_text: str = Field(min_length=1)


class ChatAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: str
    answer_id: str
    answer_state: AnswerState
    message: str
    use_case_id: str
    source_id: str | None = None
    source_name: str | None = None
    retrieved_entries: list[FaqEntry] = Field(default_factory=list)
    feedback_allowed: bool

