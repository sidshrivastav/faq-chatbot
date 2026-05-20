from __future__ import annotations

from app.llm.prompt_builder import AnswerPrompt


class FakeLLMProvider:
    def __init__(self, *, response_text: str | None = None, raise_on_generate: bool = False) -> None:
        self.response_text = response_text
        self.raise_on_generate = raise_on_generate
        self.calls: list[AnswerPrompt] = []

    def generate(self, prompt: AnswerPrompt) -> str:
        self.calls.append(prompt)
        if self.raise_on_generate:
            raise RuntimeError("Fake LLM failure")
        if self.response_text is not None:
            return self.response_text
        if prompt.retrieved_entries:
            return prompt.retrieved_entries[0].answer_text
        return "I couldn't find an answer in the active FAQ source."

