import pytest
from pydantic import ValidationError

from src.router import parse_route_decision, route_decision_schema, route_task
from src.schemas import TaskType


class FakeResponses:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs

        class Response:
            output_text = """
            {
              "task_type": "translate",
              "confidence": 0.94,
              "reason": "The user asks to translate text."
            }
            """

        return Response()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_route_decision_schema_disallows_extra_fields():
    """route_decision_schema should match the strict schema pattern from notebook 02."""

    schema = route_decision_schema()

    assert schema["additionalProperties"] is False


def test_route_task_uses_strict_json_schema_response():
    """route_task should follow the notebook 02 structured-output call shape."""

    client = FakeClient()

    decision = route_task("translate good morning into Chinese", client=client)

    assert decision.task_type == TaskType.TRANSLATE
    assert decision.confidence == 0.94
    assert client.responses.kwargs["text"]["format"]["type"] == "json_schema"
    assert client.responses.kwargs["text"]["format"]["name"] == "route_decision"
    assert client.responses.kwargs["text"]["format"]["strict"] is True
    assert client.responses.kwargs["temperature"] == 0.1


def test_parse_route_decision_accepts_valid_json():
    """parse_route_decision should validate a well-formed router response."""

    decision = parse_route_decision(
        """
        {
          "task_type": "summarize",
          "confidence": 0.91,
          "reason": "The user asks for a summary."
        }
        """
    )

    assert decision.task_type == TaskType.SUMMARIZE
    assert decision.confidence == 0.91
    assert decision.reason == "The user asks for a summary."


def test_parse_route_decision_rejects_invalid_task_type():
    """parse_route_decision should reject task types outside the schema."""

    with pytest.raises(ValidationError):
        parse_route_decision(
            """
            {
              "task_type": "calendar",
              "confidence": 0.9,
              "reason": "Unsupported route."
            }
            """
        )


def test_parse_route_decision_rejects_invalid_confidence():
    """parse_route_decision should reject confidence values outside 0 to 1."""

    with pytest.raises(ValidationError):
        parse_route_decision(
            """
            {
              "task_type": "chat",
              "confidence": 1.5,
              "reason": "Confidence must stay in range."
            }
            """
        )
