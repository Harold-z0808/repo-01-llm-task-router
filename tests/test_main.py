from src.main import handle_routed_request, respond_with_tool, select_tool_call
from src.schemas import RouteDecision, TaskType, ToolCall


class FakeFunctionCall:
    type = "function_call"
    name = "get_word_count"
    arguments = '{"text": "structured output is useful"}'


class FakeResponses:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs

        class Response:
            output = [FakeFunctionCall()]

        return Response()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_handle_routed_request_uses_chat_branch(monkeypatch):
    """The chat route should use the normal chat helper with conversation history."""

    monkeypatch.setattr(
        "src.main.route_task",
        lambda user_input: RouteDecision(
            task_type=TaskType.CHAT,
            confidence=0.9,
            reason="General question.",
        ),
    )
    monkeypatch.setattr("src.main.chat", lambda messages: "chat response")
    messages = [{"role": "developer", "content": "Be concise."}]

    response = handle_routed_request("What is Python?", messages)

    assert response == "chat response"
    assert messages[-1] == {"role": "assistant", "content": "chat response"}


def test_handle_routed_request_uses_summarize_branch(monkeypatch):
    """The summarize route should send a one-off summarization prompt."""

    monkeypatch.setattr(
        "src.main.route_task",
        lambda user_input: RouteDecision(
            task_type=TaskType.SUMMARIZE,
            confidence=0.9,
            reason="Summary requested.",
        ),
    )
    monkeypatch.setattr("src.main.chat", lambda messages: "summary response")

    response = handle_routed_request("Summarize this paragraph.", [])

    assert response == "summary response"


def test_select_tool_call_uses_function_call_shape():
    """Tool selection should follow the notebook 02 function-calling pattern."""

    client = FakeClient()

    tool_call = select_tool_call("Count words in structured output is useful", client=client)

    assert tool_call == ToolCall(
        name="get_word_count",
        arguments={"text": "structured output is useful"},
    )
    assert client.responses.kwargs["tools"]
    assert client.responses.kwargs["temperature"] == 0.1


def test_respond_with_tool_executes_selected_tool(monkeypatch):
    """The tool branch should execute the registered Python function."""

    monkeypatch.setattr(
        "src.main.select_tool_call",
        lambda user_input: ToolCall(
            name="get_word_count",
            arguments={"text": "route this request"},
        ),
    )

    response = respond_with_tool("Count words in route this request")

    assert response == "Tool: get_word_count\nResult: 3"
