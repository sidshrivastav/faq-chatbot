from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.models import CurrentUser
from app.schemas.me import CurrentUserResponse

router = APIRouter(tags=["Me"])


@router.get("/me", response_model=CurrentUserResponse)
def get_me(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        role=current_user.role,
    )
