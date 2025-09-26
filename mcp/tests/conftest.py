"""Pytest configuration and fixtures for MCP tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from utils.types import ToolOutput


@pytest.fixture
def mock_tool_output():
    """Mock ToolOutput for testing."""
    return {
        "output": "test output",
        "error": False
    }


@pytest.fixture
def mock_error_output():
    """Mock error ToolOutput for testing."""
    return {
        "output": "test error",
        "error": True
    }


@pytest.fixture
def mock_run_command():
    """Mock run_command function."""
    return AsyncMock(return_value={
        "output": "mocked command output",
        "error": False
    })


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for command execution."""
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate = AsyncMock(return_value=(b"stdout", b"stderr"))
    return mock_proc
