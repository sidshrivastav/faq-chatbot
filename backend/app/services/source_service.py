from __future__ import annotations

from collections import Counter
from uuid import uuid4

from app.schemas.faq_source import (
    FaqEntry,
    FaqEntryInput,
    FaqSourceCreate,
    FaqSourceDetail,
    FaqSourceUpdate,
    utc_now,
)


class SourceNotFoundError(Exception):
    pass


class SourceNotReadyError(Exception):
    pass


class ActiveSourceDeletionError(Exception):
    pass


class SourceService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_sources(
        self,
        *,
        use_case_id: str | None = None,
        status: str | None = None,
        active: bool | None = None,
    ) -> list[FaqSourceDetail]:
        return self.repository.list_sources(use_case_id=use_case_id, status=status, active=active)

    def get_source(self, source_id: str) -> FaqSourceDetail:
        source = self.repository.get_source(source_id)
        if source is None:
            raise SourceNotFoundError(source_id)
        return source

    def create_source(self, payload: FaqSourceCreate, *, user_id: str) -> FaqSourceDetail:
        source_id = f"src_{uuid4().hex}"
        entries = self._build_entries(source_id, payload.entries)
        readiness_state, readiness_message, warnings = self._evaluate_readiness(payload.entries)
        status = "invalid" if readiness_state == "invalid" else "ready"
        now = utc_now()
        source = FaqSourceDetail(
            id=source_id,
            name=payload.name,
            description=payload.description,
            use_case_id=payload.use_case_id,
            use_case_name=payload.use_case_id.upper(),
            status=status,
            is_active=False,
            readiness_state=readiness_state,
            readiness_message=readiness_message,
            created_by_user_id=user_id,
            updated_by_user_id=user_id,
            created_at=now,
            updated_at=now,
            entries=entries,
            warnings=warnings,
        )
        return self.repository.save_source(source)

    def update_source(self, source_id: str, payload: FaqSourceUpdate, *, user_id: str) -> FaqSourceDetail:
        source = self.get_source(source_id)
        if payload.name is not None:
            source.name = payload.name
        if payload.description is not None:
            source.description = payload.description
        if payload.entries is not None:
            source.entries = self._build_entries(source.id, payload.entries)
            readiness_state, readiness_message, warnings = self._evaluate_readiness(payload.entries)
            source.readiness_state = readiness_state
            source.readiness_message = readiness_message
            source.warnings = warnings
            if source.status != "archived":
                source.status = "invalid" if readiness_state == "invalid" else ("active" if source.is_active else "ready")
        source.updated_by_user_id = user_id
        source.updated_at = utc_now()
        source.version += 1
        return self.repository.save_source(source)

    def activate_source(self, source_id: str) -> FaqSourceDetail:
        source = self.get_source(source_id)
        if source.readiness_state == "invalid" or source.status in {"invalid", "archived"}:
            raise SourceNotReadyError(source_id)

        now = utc_now()
        for existing in self.repository.list_by_use_case(source.use_case_id):
            if existing.id != source.id and existing.is_active:
                existing.is_active = False
                existing.status = "inactive"
                existing.updated_at = now
                self.repository.save_source(existing)

        source.is_active = True
        source.status = "active"
        source.activated_at = now
        source.updated_at = now
        return self.repository.save_source(source)

    def deactivate_source(self, source_id: str) -> FaqSourceDetail:
        source = self.get_source(source_id)
        source.is_active = False
        if source.status != "archived":
            source.status = "inactive"
        source.updated_at = utc_now()
        return self.repository.save_source(source)

    def archive_source(self, source_id: str) -> FaqSourceDetail:
        source = self.get_source(source_id)
        now = utc_now()
        source.is_active = False
        source.status = "archived"
        source.archived_at = now
        source.updated_at = now
        return self.repository.save_source(source)

    def delete_source(self, source_id: str) -> None:
        source = self.repository.get_source(source_id)
        if source is None:
            raise SourceNotFoundError(source_id)
        if source.is_active:
            raise ActiveSourceDeletionError(source_id)
        if not self.repository.delete_source(source_id):
            raise SourceNotFoundError(source_id)

    def _build_entries(self, source_id: str, entries: list[FaqEntryInput]) -> list[FaqEntry]:
        return [
            FaqEntry(
                id=f"entry_{uuid4().hex}",
                faq_source_id=source_id,
                question_text=entry.question_text,
                answer_text=entry.answer_text,
                keywords=entry.keywords,
                is_valid=True,
            )
            for entry in entries
        ]

    def _evaluate_readiness(self, entries: list[FaqEntryInput]) -> tuple[str, str, list[str]]:
        if not entries:
            return "invalid", "At least one valid FAQ entry is required", []

        normalized_questions = [entry.question_text.strip().casefold() for entry in entries]
        duplicates = [question for question, count in Counter(normalized_questions).items() if count > 1]
        if duplicates:
            message = "Duplicate FAQ questions detected; review before activation"
            return "warning", message, [message]

        return "ready", "Source is ready for Q&A", []
