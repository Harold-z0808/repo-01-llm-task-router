"""Starter code for the Week 1 task router assignment.

This file is where Lesson 1 API-call knowledge meets Lesson 2 structured
output. The plain chat helper in llm_client.py remains useful for normal chat
responses, but routing needs a stricter JSON schema response.
"""

from typing import Any

from openai import OpenAI

from src.config import Settings, get_settings
from src.prompts import ROUTER_INSTRUCTIONS, build_router_prompt
from src.schemas import RouteDecision


def route_decision_schema() -> dict[str, object]:
    """Return the strict JSON schema used for router structured output.

    This mirrors the pattern in notebook 02:
    - start from the Pydantic model schema
    - disallow fields the program does not know how to handle
    - pass this schema to Responses API text.format.json_schema
    """

    schema = RouteDecision.model_json_schema()
    schema["additionalProperties"] = False
    return schema


def parse_route_decision(raw_json: str) -> RouteDecision:
    """Validate raw router JSON as a RouteDecision."""

    return RouteDecision.model_validate_json(raw_json)


def build_openai_client(settings: Settings) -> OpenAI:
    """Create the OpenAI client used for real Responses API calls."""

    if settings.provider.lower() != "openai":
        raise ValueError("LLM_PROVIDER=openai is required for real LLM calls.")
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")
    return OpenAI(api_key=settings.openai_api_key)


def route_task(user_request: str, client: Any | None = None) -> RouteDecision:
    """Classify a request using a real LLM structured-output call.

    This function intentionally uses the Responses API structured-output shape
    directly instead of llm_client.chat(), because chat() returns plain text for
    normal assistant responses.
    """

    settings = get_settings()
    active_client = client or build_openai_client(settings)
    prompt = build_router_prompt(user_request)

    response = active_client.responses.create(
        model=settings.model,
        input=prompt,
        instructions=ROUTER_INSTRUCTIONS,
        text={
            "format": {
                "type": "json_schema",
                "name": "route_decision",
                "schema": route_decision_schema(),
                "strict": True,
            }
        },
        temperature=0.1,
        max_output_tokens=300,
    )
    return parse_route_decision(response.output_text)
