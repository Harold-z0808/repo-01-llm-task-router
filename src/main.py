"""Starter CLI for the Week 1 LLM task router assignment."""

from src.llm_client import Message, chat
from src.router import route_task
from src.schemas import RouteDecision, TaskType


SYSTEM_PROMPT = "You are a concise assistant for an AI agent bootcamp."


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


def handle_routed_request(user_input: str, messages: list[Message]) -> str:
    """Route one user request and return a response string.

    Assignment TODO:
    - Fill in summarize and translate behavior.
    - Fill in tool_call behavior by selecting and calling a local tool.
    - Decide how to handle low-confidence or unsupported requests.
    """

    decision = route_task(user_input)
    print_route(decision)

    if decision.task_type == TaskType.CHAT:
        return respond_to_chat(user_input, messages)

    if decision.task_type == TaskType.SUMMARIZE:
        return "TODO: summarize this request with the LLM."

    if decision.task_type == TaskType.TRANSLATE:
        return "TODO: translate this request with the LLM."

    if decision.task_type == TaskType.TOOL_CALL:
        return "TODO: call a registered local tool."

    raise ValueError(f"Unsupported task type: {decision.task_type}")


def run_chatbot() -> None:
    """Start the task router CLI in the terminal."""

    messages: list[Message] = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("LLM Task Router CLI. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        try:
            response = handle_routed_request(user_input, messages)
        except NotImplementedError as exc:
            response = f"Starter TODO: {exc}"

        print(f"Bot: {response}")


if __name__ == "__main__":
    run_chatbot()
