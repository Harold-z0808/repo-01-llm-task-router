"""Lesson 2: Pydantic schemas."""

from enum import StrEnum

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    """Supported task categories."""

    CHAT = "chat"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    TOOL_CALL = "tool_call"


class RouteDecision(BaseModel):
    """Structured router output."""

    task_type: TaskType
    confidence: float = Field(ge=0, le=1)
    reason: str


class ToolCall(BaseModel):
    """A simple function calling request."""

    name: str
    arguments: dict[str, str | int | float | bool]
