from __future__ import annotations

from pydantic import BaseModel

from app.domain.enums import Role


class CurrentUser(BaseModel):
    id: str
    email: str
    display_name: str | None = None
    role: Role
