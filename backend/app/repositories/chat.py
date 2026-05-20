from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.domain.enums import AnswerState, UnansweredReason
from app.schemas.faq_source import FaqEntry, utc_now


@dataclass(slots=True)
class ConversationRecord:
    id: str
    user_id: str
    use_case_id: str
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class QuestionRecord:
    id: str
    conversation_id: str
    user_id: str
    use_case_id: str
    question_text: str
    active_source_id_at_time: str | None
    created_at: datetime


@dataclass(slots=True)
class AnswerRecord:
    id: str
    question_id: str
    use_case_id: str
    faq_source_id_at_time: str | None
    answer_text: str
    answer_state: AnswerState
    grounding_summary: str
    retrieved_entry_ids: list[str]
    created_at: datetime


@dataclass(slots=True)
class UnansweredQuestionRecord:
    id: str
    question_id: str
    user_id: str
    use_case_id: str
    question_text: str
    active_source_id_at_time: str | None
    source_name_at_time: str | None
    reason: UnansweredReason
    created_at: datetime


class InMemoryChatRepository:
    def __init__(self) -> None:
        self.conversations: dict[str, ConversationRecord] = {}
        self.questions: dict[str, QuestionRecord] = {}
        self.answers: dict[str, AnswerRecord] = {}
        self.unanswered_questions: dict[str, UnansweredQuestionRecord] = {}

    def ensure_conversation(
        self,
        *,
        user_id: str,
        use_case_id: str,
        conversation_id: str | None = None,
    ) -> ConversationRecord:
        now = utc_now()
        if conversation_id and conversation_id in self.conversations:
            conversation = self.conversations[conversation_id]
            conversation.updated_at = now
            return conversation

        conversation = ConversationRecord(
            id=conversation_id or f"conv_{uuid4().hex}",
            user_id=user_id,
            use_case_id=use_case_id,
            created_at=now,
            updated_at=now,
        )
        self.conversations[conversation.id] = conversation
        return conversation

    def save_question(
        self,
        *,
        conversation_id: str,
        user_id: str,
        use_case_id: str,
        question_text: str,
        active_source_id_at_time: str | None,
    ) -> QuestionRecord:
        question = QuestionRecord(
            id=f"question_{uuid4().hex}",
            conversation_id=conversation_id,
            user_id=user_id,
            use_case_id=use_case_id,
            question_text=question_text,
            active_source_id_at_time=active_source_id_at_time,
            created_at=utc_now(),
        )
        self.questions[question.id] = question
        return question

    def save_answer(
        self,
        *,
        question_id: str,
        use_case_id: str,
        faq_source_id_at_time: str | None,
        answer_text: str,
        answer_state: AnswerState,
        grounding_summary: str,
        retrieved_entries: list[FaqEntry],
    ) -> AnswerRecord:
        answer = AnswerRecord(
            id=f"answer_{uuid4().hex}",
            question_id=question_id,
            use_case_id=use_case_id,
            faq_source_id_at_time=faq_source_id_at_time,
            answer_text=answer_text,
            answer_state=answer_state,
            grounding_summary=grounding_summary,
            retrieved_entry_ids=[entry.id for entry in retrieved_entries],
            created_at=utc_now(),
        )
        self.answers[answer.id] = answer
        return answer

    def save_unanswered_question(
        self,
        *,
        question_id: str,
        user_id: str,
        use_case_id: str,
        question_text: str,
        active_source_id_at_time: str | None,
        source_name_at_time: str | None,
        reason: UnansweredReason,
    ) -> UnansweredQuestionRecord:
        unanswered = UnansweredQuestionRecord(
            id=f"unanswered_{uuid4().hex}",
            question_id=question_id,
            user_id=user_id,
            use_case_id=use_case_id,
            question_text=question_text,
            active_source_id_at_time=active_source_id_at_time,
            source_name_at_time=source_name_at_time,
            reason=reason,
            created_at=utc_now(),
        )
        self.unanswered_questions[question_id] = unanswered
        return unanswered

    def clear(self) -> None:
        self.conversations.clear()
        self.questions.clear()
        self.answers.clear()
        self.unanswered_questions.clear()
