from __future__ import annotations

from app.domain.enums import AnswerState, UnansweredReason
from app.llm.fake_provider import FakeLLMProvider
from app.repositories.chat import InMemoryChatRepository
from app.repositories.faq_sources import InMemoryFaqSourceRepository
from app.schemas.chat import QuestionCreate
from app.schemas.faq_source import FaqEntryInput, FaqSourceCreate
from app.services.answer_service import AnswerService
from app.services.source_service import SourceService


def create_active_source(
    source_service: SourceService,
    *,
    name: str,
    use_case_id: str,
    question_text: str,
    answer_text: str,
) -> str:
    source = source_service.create_source(
        FaqSourceCreate(
            name=name,
            use_case_id=use_case_id,
            entries=[
                FaqEntryInput(
                    question_text=question_text,
                    answer_text=answer_text,
                    keywords=["policy"],
                )
            ],
        ),
        user_id="admin-1",
    )
    source_service.activate_source(source.id)
    return source.id


def test_answer_service_returns_grounded_answer_and_calls_llm_with_retrieved_entries() -> None:
    source_service = SourceService(InMemoryFaqSourceRepository())
    source_id = create_active_source(
        source_service,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I request parental leave?",
        answer_text="Submit the request in Workday.",
    )
    provider = FakeLLMProvider()
    chat_repository = InMemoryChatRepository()
    service = AnswerService(
        source_service=source_service,
        chat_repository=chat_repository,
        llm_provider=provider,
    )

    result = service.ask_question(
        user_id="user-1",
        payload=QuestionCreate(
            use_case_id="hr",
            question_text="What is the process for parental leave?",
        ),
    )

    assert result.answer_state == AnswerState.ANSWERED
    assert result.source_id == source_id
    assert result.source_name == "HR handbook"
    assert result.message == "Submit the request in Workday."
    assert len(result.retrieved_entries) == 1
    assert provider.calls[0].use_case_id == "hr"
    assert provider.calls[0].retrieved_entries[0].question_text == "How do I request parental leave?"
    assert chat_repository.answers[result.answer_id].answer_state == AnswerState.ANSWERED


def test_answer_service_skips_inactive_or_other_use_case_sources_and_returns_unsupported() -> None:
    source_service = SourceService(InMemoryFaqSourceRepository())
    create_active_source(
        source_service,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I book time off?",
        answer_text="Use the time-off portal.",
    )
    create_active_source(
        source_service,
        name="IT support",
        use_case_id="it",
        question_text="How do I reset my password?",
        answer_text="Use the password reset link.",
    )
    provider = FakeLLMProvider()
    chat_repository = InMemoryChatRepository()
    service = AnswerService(
        source_service=source_service,
        chat_repository=chat_repository,
        llm_provider=provider,
    )

    result = service.ask_question(
        user_id="user-1",
        payload=QuestionCreate(
            use_case_id="hr",
            question_text="How do I reset my password?",
        ),
    )

    assert result.answer_state == AnswerState.UNSUPPORTED
    assert result.source_name == "HR handbook"
    assert result.retrieved_entries == []
    assert provider.calls == []
    assert chat_repository.unanswered_questions[result.question_id].reason == UnansweredReason.INSUFFICIENT_CONTEXT


def test_answer_service_returns_no_active_source_when_no_active_source_exists() -> None:
    source_service = SourceService(InMemoryFaqSourceRepository())
    provider = FakeLLMProvider()
    chat_repository = InMemoryChatRepository()
    service = AnswerService(
        source_service=source_service,
        chat_repository=chat_repository,
        llm_provider=provider,
    )

    result = service.ask_question(
        user_id="user-1",
        payload=QuestionCreate(
            use_case_id="hr",
            question_text="Where do I submit expenses?",
        ),
    )

    assert result.answer_state == AnswerState.NO_ACTIVE_SOURCE
    assert "No active FAQ source" in result.message
    assert provider.calls == []
    assert chat_repository.unanswered_questions[result.question_id].reason == UnansweredReason.NO_ACTIVE_SOURCE


def test_answer_service_returns_error_state_when_provider_fails() -> None:
    source_service = SourceService(InMemoryFaqSourceRepository())
    create_active_source(
        source_service,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I request parental leave?",
        answer_text="Submit the request in Workday.",
    )
    provider = FakeLLMProvider(raise_on_generate=True)
    chat_repository = InMemoryChatRepository()
    service = AnswerService(
        source_service=source_service,
        chat_repository=chat_repository,
        llm_provider=provider,
    )

    result = service.ask_question(
        user_id="user-1",
        payload=QuestionCreate(
            use_case_id="hr",
            question_text="What is the process for parental leave?",
        ),
    )

    assert result.answer_state == AnswerState.ERROR
    assert "temporarily unavailable" in result.message.lower()
    assert len(provider.calls) == 1
