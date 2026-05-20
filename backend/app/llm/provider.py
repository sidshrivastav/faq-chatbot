from __future__ import annotations

from typing import Protocol

from app.llm.prompt_builder import AnswerPrompt


class LLMProvider(Protocol):
    def generate(self, prompt: AnswerPrompt) -> str: ...

