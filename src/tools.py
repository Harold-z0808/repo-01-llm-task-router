"""Lesson 2: function calling tools."""

from collections.abc import Callable


def get_word_count(text: str) -> int:
    """Count whitespace-delimited words."""

    return len(text.split())


def uppercase(text: str) -> str:
    """Return uppercase text."""

    return text.upper()


# Assignment TODO:
# Add at least one more local tool, then register it in TOOLS.
# Example idea: reverse_text(text: str) -> str


TOOLS: dict[str, Callable[..., object]] = {
    "get_word_count": get_word_count,
    "uppercase": uppercase,
}


def call_tool(name: str, **arguments: object) -> object:
    """Call a registered local tool by name."""

    try:
        tool = TOOLS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown tool: {name}") from exc
    return tool(**arguments)
