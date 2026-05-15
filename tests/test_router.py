import pytest
from pydantic import ValidationError

from src.router import parse_route_decision, route_decision_schema
from src.schemas import TaskType


def test_route_decision_schema_disallows_extra_fields():
    """route_decision_schema should match the strict schema pattern from notebook 02."""

    schema = route_decision_schema()

    assert schema["additionalProperties"] is False


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


# Assignment TODO:
# Add tests for route_task by monkeypatching or injecting a fake LLM response.
# Tests should not call the real OpenAI API.
