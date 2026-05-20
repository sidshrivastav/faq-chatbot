from __future__ import annotations

from dataclasses import dataclass

from app.domain.enums import AnswerState, UnansweredReason
from app.llm.prompt_builder import build_answer_prompt
from app.repositories.chat import InMemoryChatRepository
from app.schemas.chat import ChatAnswerResponse, QuestionCreate
from app.services.retrieval_service import RetrievalService
from app.services.source_service import SourceService


@dataclass(slots=True)
class AnswerServiceDependencies:
    source_service: SourceService
    chat_repository: InMemoryChatRepository
    llm_provider: object


class AnswerService:
    def __init__(
        self,
        *,
        source_service: SourceService,
        chat_repository: InMemoryChatRepository,
        llm_provider: object,
        retrieval_service: RetrievalService | None = None,
    ) -> None:
        self.source_service = source_service
        self.chat_repository = chat_repository
        self.llm_provider = llm_provider
        self.retrieval_service = retrieval_service or RetrievalService(source_service)

    def ask_question(self, *, user_id: str, payload: QuestionCreate) -> ChatAnswerResponse:
        conversation = self.chat_repository.ensure_conversation(
            user_id=user_id,
            use_case_id=payload.use_case_id,
            conversation_id=payload.conversation_id,
        )
        retrieval = self.retrieval_service.retrieve(
            question_text=payload.question_text,
            use_case_id=payload.use_case_id,
        )
        source = retrieval.source
        question = self.chat_repository.save_question(
            conversation_id=conversation.id,
            user_id=user_id,
            use_case_id=payload.use_case_id,
            question_text=payload.question_text,
            active_source_id_at_time=source.id if source else None,
        )

        if retrieval.reason == UnansweredReason.NO_ACTIVE_SOURCE:
            answer_state = AnswerState.NO_ACTIVE_SOURCE
            message = "No active FAQ source is available for this use case."
            answer = self.chat_repository.save_answer(
                question_id=question.id,
                use_case_id=payload.use_case_id,
                faq_source_id_at_time=None,
                answer_text=message,
                answer_state=answer_state,
                grounding_summary=message,
                retrieved_entries=[],
            )
            self.chat_repository.save_unanswered_question(
                question_id=question.id,
                user_id=user_id,
                use_case_id=payload.use_case_id,
                question_text=payload.question_text,
                active_source_id_at_time=None,
                source_name_at_time=None,
                reason=UnansweredReason.NO_ACTIVE_SOURCE,
            )
            return self._build_response(
                question_id=question.id,
                answer=answer,
                use_case_id=payload.use_case_id,
                source_id=None,
                source_name=None,
                message=message,
                retrieved_entries=[],
                feedback_allowed=True,
            )

        if not source or not retrieval.retrieved_entries:
            message = "I couldn't find an answer in the active FAQ source."
            answer = self.chat_repository.save_answer(
                question_id=question.id,
                use_case_id=payload.use_case_id,
                faq_source_id_at_time=source.id if source else None,
                answer_text=message,
                answer_state=AnswerState.UNSUPPORTED,
                grounding_summary=message,
                retrieved_entries=[],
            )
            self.chat_repository.save_unanswered_question(
                question_id=question.id,
                user_id=user_id,
                use_case_id=payload.use_case_id,
                question_text=payload.question_text,
                active_source_id_at_time=source.id if source else None,
                source_name_at_time=source.name if source else None,
                reason=UnansweredReason.INSUFFICIENT_CONTEXT,
            )
            return self._build_response(
                question_id=question.id,
                answer=answer,
                use_case_id=payload.use_case_id,
                source_id=source.id if source else None,
                source_name=source.name if source else None,
                message=message,
                retrieved_entries=[],
                feedback_allowed=True,
            )

        prompt = build_answer_prompt(
            question_id=question.id,
            user_id=user_id,
            payload=payload,
            source=source,
            retrieved_entries=retrieval.retrieved_entries,
        )

        try:
            message = self.llm_provider.generate(prompt)
            answer_state = AnswerState.ANSWERED
            feedback_allowed = True
            response_entries = retrieval.retrieved_entries
        except Exception:
            message = "The assistant is temporarily unavailable. Please try again."
            answer_state = AnswerState.ERROR
            feedback_allowed = False
            response_entries = retrieval.retrieved_entries

        answer = self.chat_repository.save_answer(
            question_id=question.id,
            use_case_id=payload.use_case_id,
            faq_source_id_at_time=source.id,
            answer_text=message,
            answer_state=answer_state,
            grounding_summary=source.name,
            retrieved_entries=retrieval.retrieved_entries,
        )
        return self._build_response(
            question_id=question.id,
            answer=answer,
            use_case_id=payload.use_case_id,
            source_id=source.id,
            source_name=source.name,
            message=message,
            retrieved_entries=response_entries if answer_state == AnswerState.ANSWERED else response_entries,
            feedback_allowed=feedback_allowed,
        )

    def _build_response(
        self,
        *,
        question_id: str,
        answer,
        use_case_id: str,
        source_id: str | None,
        source_name: str | None,
        message: str,
        retrieved_entries,
        feedback_allowed: bool,
    ) -> ChatAnswerResponse:
        return ChatAnswerResponse(
            question_id=question_id,
            answer_id=answer.id,
            answer_state=answer.answer_state,
            message=message,
            use_case_id=use_case_id,
            source_id=source_id,
            source_name=source_name,
            retrieved_entries=retrieved_entries,
            feedback_allowed=feedback_allowed,
        )

