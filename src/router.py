"""Starter code for the Week 1 task router assignment."""

from src.prompts import ROUTER_SYSTEM_PROMPT, build_router_prompt
from src.schemas import RouteDecision


def parse_route_decision(raw_json: str) -> RouteDecision:
    """Validate raw router JSON as a RouteDecision."""

    return RouteDecision.model_validate_json(raw_json)


def route_task(user_request: str) -> RouteDecision:
    """Classify a request using a real LLM structured-output call.

    Assignment TODO:
    - Build an OpenAI client from the project settings.
    - Call client.responses.create(...) with ROUTER_SYSTEM_PROMPT.
    - Request JSON schema structured output using RouteDecision.model_json_schema().
    - Validate response.output_text with parse_route_decision(...).

    Do not replace this with local keyword rules. The point of this assignment is
    to let the LLM make the route decision.
    """

    prompt = build_router_prompt(user_request)
    raise NotImplementedError(
        "TODO: use a real LLM structured-output call to route this request. "
        f"Router prompt prepared with system prompt {ROUTER_SYSTEM_PROMPT!r} "
        f"and user prompt {prompt!r}."
    )
