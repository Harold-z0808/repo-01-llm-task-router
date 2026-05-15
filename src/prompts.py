"""Lesson 2: prompt templates."""

ROUTER_INSTRUCTIONS = """You classify user requests into one of:
- chat
- summarize
- translate
- tool_call

Return only structured output matching the RouteDecision schema.
"""

# Backwards-compatible name for students who have already read the starter code.
ROUTER_SYSTEM_PROMPT = ROUTER_INSTRUCTIONS


def build_router_prompt(user_request: str) -> str:
    """Create the router prompt body for a user request."""

    return f"Classify this request:\n\n{user_request}"
