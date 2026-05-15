"""Lesson 2: prompt templates."""

ROUTER_SYSTEM_PROMPT = """You classify user requests into one of:
- chat
- summarize
- translate
- tool_call

Return only structured output matching the RouteDecision schema.
"""


def build_router_prompt(user_request: str) -> str:
    """Create the router prompt body for a user request."""

    return f"Classify this request:\n\n{user_request}"
