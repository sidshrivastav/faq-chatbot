from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from app.domain.enums import UnansweredReason
from app.schemas.faq_source import FaqEntry, FaqSourceDetail
from app.services.source_service import SourceService


@dataclass(slots=True)
class RetrievalResult:
    source: FaqSourceDetail | None
    retrieved_entries: list[FaqEntry]
    reason: UnansweredReason | None


class RetrievalService:
    STOP_WORDS = {
        "a",
        "an",
        "and",
        "can",
        "do",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "it",
        "my",
        "of",
        "on",
        "or",
        "the",
        "to",
        "what",
        "when",
        "where",
        "who",
        "why",
        "you",
    }

    def __init__(self, source_service: SourceService) -> None:
        self.source_service = source_service

    def retrieve(self, *, question_text: str, use_case_id: str) -> RetrievalResult:
        active_sources = self.source_service.list_sources(use_case_id=use_case_id, active=True)
        if not active_sources:
            return RetrievalResult(source=None, retrieved_entries=[], reason=UnansweredReason.NO_ACTIVE_SOURCE)

        source = active_sources[0]
        scored_entries = [
            (self._score_entry(question_text, entry), entry)
            for entry in source.entries
            if entry.is_valid
        ]
        scored_entries.sort(key=lambda item: (-item[0], item[1].question_text.lower()))

        retrieved_entries = [entry for score, entry in scored_entries if score >= 2][:3]
        if not retrieved_entries:
            return RetrievalResult(
                source=source,
                retrieved_entries=[],
                reason=UnansweredReason.INSUFFICIENT_CONTEXT,
            )

        return RetrievalResult(source=source, retrieved_entries=retrieved_entries, reason=None)

    def _score_entry(self, question_text: str, entry: FaqEntry) -> int:
        question_tokens = set(self._tokenize(question_text))
        entry_tokens = set(self._tokenize(entry.question_text))
        entry_tokens.update(self._tokenize(entry.answer_text))
        entry_tokens.update(self._tokenize(" ".join(entry.keywords)))

        score = len(question_tokens & entry_tokens)
        normalized_question = question_text.casefold()
        normalized_entry_question = entry.question_text.casefold()
        if normalized_entry_question in normalized_question or normalized_question in normalized_entry_question:
            score += 2
        if any(keyword.casefold() in normalized_question for keyword in entry.keywords):
            score += 1
        return score

    def _tokenize(self, text: str) -> Iterable[str]:
        return [token for token in re.findall(r"[a-z0-9]+", text.casefold()) if token not in self.STOP_WORDS]
