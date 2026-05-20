from __future__ import annotations

from dataclasses import dataclass

from app.schemas.faq_source import FaqEntry, FaqSourceDetail
from app.schemas.chat import QuestionCreate


@dataclass(slots=True)
class AnswerPrompt:
    question_id: str
    user_id: str
    use_case_id: str
    question_text: str
    source_id: str
    source_name: str
    retrieved_entries: list[FaqEntry]


def build_answer_prompt(
    *,
    question_id: str,
    user_id: str,
    payload: QuestionCreate,
    source: FaqSourceDetail,
    retrieved_entries: list[FaqEntry],
) -> AnswerPrompt:
    return AnswerPrompt(
        question_id=question_id,
        user_id=user_id,
        use_case_id=payload.use_case_id,
        question_text=payload.question_text,
        source_id=source.id,
        source_name=source.name,
        retrieved_entries=retrieved_entries,
    )

