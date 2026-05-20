from __future__ import annotations

from pydantic import BaseModel


class UseCaseSummary(BaseModel):
    id: str
    name: str
    description: str | None = None
    has_active_source: bool
    active_source_name: str | None = None


class UseCaseListResponse(BaseModel):
    items: list[UseCaseSummary]
