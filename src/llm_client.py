"""Lesson 1: provider abstraction and plain-text chat().

This module intentionally handles normal assistant text responses only.
Lesson 2 structured output for routing belongs in src/router.py, where students
can apply the notebook 02 JSON schema pattern directly.
"""

from typing import Protocol

from openai import OpenAI

try:
    from src.config import Settings, get_settings
except ModuleNotFoundError:
    from config import Settings, get_settings


Message = dict[str, str]


class ChatProvider(Protocol):
    """Common interface for chat providers."""

    def chat(self, messages: list[Message]) -> str:
        """Return the assistant response for a message list."""


class MockProvider:
    """Deterministic provider used for local development and tests."""

    def chat(self, messages: list[Message]) -> str:
        """Return a predictable response based on the latest user message."""

        last_user_message = next(
            (message["content"] for message in reversed(messages) if message["role"] == "user"),
            "",
        )
        return f"Mock response: {last_user_message}"


class OpenAIProvider:
    """OpenAI plain-text chat provider."""

    def __init__(self, settings: Settings):
        """Initialize an OpenAI provider from runtime settings."""

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.model

    def chat(self, messages: list[Message]) -> str:
        """Send chat messages to the OpenAI Responses API.

        This helper returns response.output_text for regular chat. It does not
        request json_schema output; route_task does that separately for routing.
        """

        response = self._client.responses.create(
            model=self._model,
            input=messages,
        )
        return response.output_text


class LLMClient:
    """Small lesson-friendly client wrapper used by notebooks and the CLI."""

    def __init__(
        self,
        provider: str = "mock",
        model: str = "gpt-5.4-mini",
        api_key: str | None = None,
    ):
        """Create an LLM client with an explicit provider configuration."""

        settings = Settings(provider=provider, model=model, openai_api_key=api_key)
        self._provider = build_provider(settings)

    def chat(self, messages: list[Message]) -> str:
        """Return one assistant message for a chat history."""

        return self._provider.chat(messages)


def build_provider(settings: Settings | None = None) -> ChatProvider:
    """Create a provider from settings."""

    active_settings = settings or get_settings()
    provider = active_settings.provider.lower()
    if provider == "mock":
        return MockProvider()
    if provider == "openai":
        return OpenAIProvider(active_settings)
    raise ValueError(f"Unsupported LLM_PROVIDER: {active_settings.provider}")


def chat(messages: list[Message], provider: ChatProvider | None = None) -> str:
    """Convenience wrapper around the active provider."""

    active_provider = provider or build_provider()
    return active_provider.chat(messages)
