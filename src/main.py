"""CLI for the Week 1 LLM task router assignment solution."""

import json
from typing import Any

from src.config import get_settings
from src.llm_client import Message, chat
from src.router import build_openai_client, route_task
from src.schemas import RouteDecision, TaskType, ToolCall
from src.tools import TOOL_DEFINITIONS, call_tool


SYSTEM_PROMPT = "You are a concise assistant for an AI agent bootcamp."
SUMMARIZE_PROMPT = "Summarize the user's text clearly and concisely."
TRANSLATE_PROMPT = (
    "Translate the text requested by the user. If the target language or text is missing, "
    "ask one brief clarification question."
)
TOOL_PROMPT = (
    "Use one local tool when it helps answer the request. "
    "Do not answer directly if one of the provided tools can solve it."
)


def print_route(decision: RouteDecision) -> None:
    """Print the structured route decision for debugging."""

    print(f"Route: {decision.task_type} ({decision.confidence:.2f})")
    print(f"Reason: {decision.reason}")


def respond_to_chat(user_input: str, messages: list[Message]) -> str:
    """Handle the chat route with the existing chat client."""

    messages.append({"role": "user", "content": user_input})
    assistant_response = chat(messages)
    messages.append({"role": "assistant", "content": assistant_response})
    return assistant_response


def respond_with_prompt(user_input: str, instructions: str) -> str:
    """Handle one-off LLM tasks that do not need conversation history."""

    return chat(
        [
            {"role": "developer", "content": instructions},
            {"role": "user", "content": user_input},
        ]
    )


def select_tool_call(user_input: str, client: Any | None = None) -> ToolCall:
    """Ask the model to select a local tool and provide arguments."""

    settings = get_settings()
    active_client = client or build_openai_client(settings)
    response = active_client.responses.create(
        model=settings.model,
        input=user_input,
        instructions=TOOL_PROMPT,
        tools=TOOL_DEFINITIONS,
        temperature=0.1,
        max_output_tokens=300,
    )
    function_calls = [item for item in response.output if item.type == "function_call"]
    if not function_calls:
        raise ValueError("The model did not select a local tool.")

    call = function_calls[0]
    return ToolCall(name=call.name, arguments=json.loads(call.arguments))


def respond_with_tool(user_input: str) -> str:
    """Select and execute one local tool for the user request."""

    tool_call = select_tool_call(user_input)
    result = call_tool(tool_call.name, **tool_call.arguments)
    return f"Tool: {tool_call.name}\nResult: {result}"


def handle_routed_request(user_input: str, messages: list[Message]) -> str:
    """Route one user request and return a response string."""

    decision = route_task(user_input)
    print_route(decision)

    if decision.task_type == TaskType.CHAT:
        return respond_to_chat(user_input, messages)

    if decision.task_type == TaskType.SUMMARIZE:
        return respond_with_prompt(user_input, SUMMARIZE_PROMPT)

    if decision.task_type == TaskType.TRANSLATE:
        return respond_with_prompt(user_input, TRANSLATE_PROMPT)

    if decision.task_type == TaskType.TOOL_CALL:
        return respond_with_tool(user_input)

    raise ValueError(f"Unsupported task type: {decision.task_type}")


def run_chatbot() -> None:
    """Start the task router CLI in the terminal."""

    messages: list[Message] = [{"role": "developer", "content": SYSTEM_PROMPT}]
    print("LLM Task Router CLI. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        response = handle_routed_request(user_input, messages)
        print(f"Bot: {response}")


if __name__ == "__main__":
    run_chatbot()
