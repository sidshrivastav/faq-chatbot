from __future__ import annotations

from copy import deepcopy

from app.schemas.faq_source import FaqSourceDetail


class InMemoryFaqSourceRepository:
    def __init__(self) -> None:
        self._sources: dict[str, FaqSourceDetail] = {}

    def list_sources(
        self,
        *,
        use_case_id: str | None = None,
        status: str | None = None,
        active: bool | None = None,
    ) -> list[FaqSourceDetail]:
        sources = list(self._sources.values())
        if use_case_id is not None:
            sources = [source for source in sources if source.use_case_id == use_case_id]
        if status is not None:
            sources = [source for source in sources if source.status == status]
        if active is not None:
            sources = [source for source in sources if source.is_active is active]
        return [deepcopy(source) for source in sources]

    def get_source(self, source_id: str) -> FaqSourceDetail | None:
        source = self._sources.get(source_id)
        return deepcopy(source) if source else None

    def save_source(self, source: FaqSourceDetail) -> FaqSourceDetail:
        self._sources[source.id] = deepcopy(source)
        return deepcopy(source)

    def delete_source(self, source_id: str) -> bool:
        return self._sources.pop(source_id, None) is not None

    def list_by_use_case(self, use_case_id: str) -> list[FaqSourceDetail]:
        return self.list_sources(use_case_id=use_case_id)

    def clear(self) -> None:
        self._sources.clear()
