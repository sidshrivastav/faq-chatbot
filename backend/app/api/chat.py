from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.models import CurrentUser
from app.api.faq_sources import get_source_service
from app.llm.fake_provider import FakeLLMProvider
from app.repositories.chat import InMemoryChatRepository
from app.schemas.chat import ChatAnswerResponse, QuestionCreate
from app.services.answer_service import AnswerService

router = APIRouter(prefix="/chat", tags=["Chat"])

_repository = InMemoryChatRepository()
_llm_provider = FakeLLMProvider()


def get_chat_service() -> AnswerService:
    return AnswerService(
        source_service=get_source_service(),
        chat_repository=_repository,
        llm_provider=_llm_provider,
    )


def reset_chat_repository() -> None:
    _repository.clear()


@router.post("/questions", response_model=ChatAnswerResponse)
def submit_question(
    payload: QuestionCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: AnswerService = Depends(get_chat_service),
) -> ChatAnswerResponse:
    return service.ask_question(user_id=current_user.id, payload=payload)

