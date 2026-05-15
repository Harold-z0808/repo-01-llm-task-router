from src.config import Settings
from src.llm_client import MockProvider, build_provider, chat


def test_mock_provider_echoes_last_user_message():
    """MockProvider should return a deterministic response for tests."""

    provider = MockProvider()

    response = chat(
        [
            {"role": "system", "content": "Be brief."},
            {"role": "user", "content": "hello"},
        ],
        provider=provider,
    )

    assert response == "Mock response: hello"


def test_build_provider_uses_mock_provider():
    """build_provider should select MockProvider for mock settings."""

    provider = build_provider(Settings(provider="mock"))

    assert isinstance(provider, MockProvider)
