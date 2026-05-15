import pytest

from src.tools import call_tool, get_word_count, uppercase


def test_get_word_count_counts_whitespace_delimited_words():
    """get_word_count should count words separated by whitespace."""

    assert get_word_count("structured output is useful") == 4


def test_uppercase_converts_text():
    """uppercase should convert all alphabetic characters to uppercase."""

    assert uppercase("hello agent") == "HELLO AGENT"


def test_call_tool_dispatches_registered_tool():
    """call_tool should dispatch calls to registered tool functions."""

    assert call_tool("get_word_count", text="route this request") == 3


def test_call_tool_rejects_unknown_tool():
    """call_tool should raise a clear error for unregistered tools."""

    with pytest.raises(ValueError, match="Unknown tool"):
        call_tool("missing_tool", text="hello")

