"""Tests for utils.types module."""

import pytest
from utils.types import ToolOutput


class TestToolOutput:
    """Test cases for ToolOutput TypedDict."""

    def test_tool_output_creation(self):
        """Test creating ToolOutput with valid data."""
        output = ToolOutput(output="test output", error=False)
        
        assert output["output"] == "test output"
        assert output["error"] is False

    def test_tool_output_error_case(self):
        """Test creating ToolOutput with error case."""
        output = ToolOutput(output="error message", error=True)
        
        assert output["output"] == "error message"
        assert output["error"] is True

    def test_tool_output_empty_string(self):
        """Test creating ToolOutput with empty string."""
        output = ToolOutput(output="", error=False)
        
        assert output["output"] == ""
        assert output["error"] is False

    def test_tool_output_type_validation(self):
        """Test that ToolOutput enforces correct types."""
        # This should work
        output = ToolOutput(output="string", error=True)
        assert isinstance(output["output"], str)
        assert isinstance(output["error"], bool)

    def test_tool_output_required_fields(self):
        """Test that ToolOutput requires both fields."""
        # This should work
        output = ToolOutput(output="test", error=False)
        assert "output" in output
        assert "error" in output
