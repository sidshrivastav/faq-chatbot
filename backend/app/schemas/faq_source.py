from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SourceStatus = Literal["draft", "ready", "active", "inactive", "invalid", "archived"]
ReadinessState = Literal["not_checked", "ready", "invalid", "warning"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class FaqEntryInput(BaseModel):
    question_text: str = Field(min_length=1)
    answer_text: str = Field(min_length=1)
    keywords: list[str] = Field(default_factory=list)


class FaqEntry(FaqEntryInput):
    id: str
    faq_source_id: str
    is_valid: bool = True
    validation_message: str | None = None


class FaqSourceCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    use_case_id: str = Field(min_length=1)
    entries: list[FaqEntryInput] = Field(default_factory=list)


class FaqSourceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    entries: list[FaqEntryInput] | None = None


class FaqSource(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None = None
    use_case_id: str
    use_case_name: str | None = None
    status: SourceStatus
    is_active: bool
    readiness_state: ReadinessState
    readiness_message: str | None = None
    version: int = 1
    created_by_user_id: str | None = None
    updated_by_user_id: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    activated_at: datetime | None = None
    archived_at: datetime | None = None


class FaqSourceDetail(FaqSource):
    entries: list[FaqEntry] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class FaqSourceListResponse(BaseModel):
    items: list[FaqSource]
