"""Starter code for the Week 1 task router assignment.

This file is where Lesson 1 API-call knowledge meets Lesson 2 structured
output. The plain chat helper in llm_client.py remains useful for normal chat
responses, but routing needs a stricter JSON schema response.
"""

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


def route_task(user_request: str) -> RouteDecision:
    """Classify a request using a real LLM structured-output call.

    Assignment TODO:
    - Build an OpenAI client from the project settings.
    - Call client.responses.create(...) with ROUTER_INSTRUCTIONS.
    - Request JSON schema structured output using route_decision_schema().
    - Validate response.output_text with parse_route_decision(...).

    Follow the structured-output pattern from
    notebooks/02_structured_output_and_tools.ipynb:

        response = client.responses.create(
            model=MODEL,
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

    This function intentionally uses the Responses API structured-output shape
    directly instead of llm_client.chat(), because chat() returns plain text for
    normal assistant responses.

    Do not replace this with local keyword rules. The point of this assignment is
    to let the LLM make the route decision.
    """

    prompt = build_router_prompt(user_request)
    raise NotImplementedError(
        "TODO: use a real LLM structured-output call to route this request. "
        f"Router prompt prepared with instructions {ROUTER_INSTRUCTIONS!r} "
        f"and user prompt {prompt!r}."
    )
