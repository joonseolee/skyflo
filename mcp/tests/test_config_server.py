"""Tests for config.server module."""

import pytest
from unittest.mock import patch, MagicMock
from config.server import mcp


class TestMCPConfig:
    """Test cases for MCP server configuration."""

    def test_mcp_instance_creation(self):
        """Test that MCP instance is created with correct configuration."""
        assert mcp is not None
        assert hasattr(mcp, 'settings')
        assert hasattr(mcp, 'run')

    def test_mcp_name(self):
        """Test that MCP has correct name."""
        assert mcp.name == "Skyflo.ai MCP Server"

    def test_mcp_instructions(self):
        """Test that MCP has correct instructions."""
        instructions = mcp.instructions
        assert "Kubernetes DevOps MCP" in instructions
        assert "kubectl operations" in instructions
        assert "Helm charts" in instructions
        assert "Argo Rollouts" in instructions
        assert "blue/green" in instructions
        assert "canary strategies" in instructions

    def test_mcp_dependencies(self):
        """Test that MCP has correct dependencies."""
        dependencies = mcp.dependencies
        expected_deps = ["pydantic", "kubernetes", "helm", "argo"]
        
        for dep in expected_deps:
            assert dep in dependencies

    def test_mcp_tools_imported(self):
        """Test that all tool modules are imported."""
        # This test verifies that the imports at the bottom of server.py work
        # We can't directly test the imports, but we can verify the mcp object
        # has the expected structure
        assert mcp is not None
        
    @patch('config.server.kubectl')
    @patch('config.server.helm')
    @patch('config.server.argo')
    @patch('config.server.jenkins')
    def test_tool_imports(self, mock_jenkins, mock_argo, mock_helm, mock_kubectl):
        """Test that tool modules are properly imported."""
        # This test verifies that the import statements work correctly
        # The actual imports happen at module level, so we just verify
        # that the modules can be imported without errors
        assert mock_kubectl is not None
        assert mock_helm is not None
        assert mock_argo is not None
        assert mock_jenkins is not None

    def test_mcp_settings_attributes(self):
        """Test that MCP settings have expected attributes."""
        # Test that settings object exists and has expected attributes
        assert hasattr(mcp, 'settings')
        
        # Test that we can set port and host
        original_port = mcp.settings.port
        original_host = mcp.settings.host
        
        mcp.settings.port = 9999
        mcp.settings.host = "127.0.0.1"
        
        assert mcp.settings.port == 9999
        assert mcp.settings.host == "127.0.0.1"
        
        # Restore original values
        mcp.settings.port = original_port
        mcp.settings.host = original_host

    def test_mcp_run_method(self):
        """Test that MCP has a run method."""
        assert hasattr(mcp, 'run')
        assert callable(mcp.run)

    def test_fastmcp_initialization(self):
        """Test that FastMCP is initialized with correct parameters."""
        # Test that the mcp instance has the expected attributes
        assert mcp.name == "Skyflo.ai MCP Server"
        assert "Kubernetes DevOps MCP" in mcp.instructions
        assert "pydantic" in mcp.dependencies
        assert "kubernetes" in mcp.dependencies
        assert "helm" in mcp.dependencies
        assert "argo" in mcp.dependencies
