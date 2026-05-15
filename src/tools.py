"""Lesson 2: function calling tools."""

from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field


class TextToolArgs(BaseModel):
    """Arguments shared by the simple text tools."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(description="The input text for the tool.")


class ToolSpec(BaseModel):
    """Local tool metadata used to build OpenAI function definitions."""

    name: str
    description: str
    function: Callable[..., object]
    args_model: type[BaseModel]

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_word_count(text: str) -> int:
    """Count whitespace-delimited words."""

    return len(text.split())


def uppercase(text: str) -> str:
    """Return uppercase text."""

    return text.upper()


def reverse_text(text: str) -> str:
    """Return text with its characters in reverse order."""

    return text[::-1]


TOOL_SPECS: dict[str, ToolSpec] = {
    "get_word_count": ToolSpec(
        name="get_word_count",
        description="Count the number of whitespace-delimited words in a text string.",
        function=get_word_count,
        args_model=TextToolArgs,
    ),
    "uppercase": ToolSpec(
        name="uppercase",
        description="Convert text to uppercase.",
        function=uppercase,
        args_model=TextToolArgs,
    ),
    "reverse_text": ToolSpec(
        name="reverse_text",
        description="Reverse the characters in a text string.",
        function=reverse_text,
        args_model=TextToolArgs,
    ),
}

TOOLS: dict[str, Callable[..., object]] = {
    name: spec.function for name, spec in TOOL_SPECS.items()
}


def build_tool_definition(spec: ToolSpec) -> dict[str, object]:
    """Convert local tool metadata into an OpenAI function definition."""

    return {
        "type": "function",
        "name": spec.name,
        "description": spec.description,
        "parameters": spec.args_model.model_json_schema(),
    }


TOOL_DEFINITIONS = [build_tool_definition(spec) for spec in TOOL_SPECS.values()]


def call_tool(name: str, **arguments: object) -> object:
    """Call a registered local tool by name."""

    try:
        tool = TOOLS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown tool: {name}") from exc
    return tool(**arguments)
