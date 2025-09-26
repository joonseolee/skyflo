"""Tests for main.py module."""

import pytest
from unittest.mock import patch, MagicMock
from main import main


class TestMain:
    """Test cases for main function."""

    @patch('main.mcp')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_sse_transport(self, mock_parse_args, mock_mcp):
        """Test main function with SSE transport."""
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.sse = True
        mock_args.port = 9999
        mock_args.host = "127.0.0.1"
        mock_parse_args.return_value = mock_args

        # Mock mcp settings and run method
        mock_mcp.settings.port = 8888
        mock_mcp.settings.host = "0.0.0.0"
        mock_mcp.run = MagicMock()

        main()

        # Verify mcp settings were updated
        assert mock_mcp.settings.port == 9999
        assert mock_mcp.settings.host == "127.0.0.1"
        
        # Verify mcp.run was called with SSE transport
        mock_mcp.run.assert_called_once_with(transport="sse")

    @patch('main.mcp')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_http_transport(self, mock_parse_args, mock_mcp):
        """Test main function with HTTP transport (default)."""
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.sse = False
        mock_args.port = 8080
        mock_args.host = "0.0.0.0"
        mock_parse_args.return_value = mock_args

        # Mock mcp settings and run method
        mock_mcp.settings.port = 8888
        mock_mcp.settings.host = "0.0.0.0"
        mock_mcp.run = MagicMock()

        main()

        # Verify mcp settings were updated
        assert mock_mcp.settings.port == 8080
        assert mock_mcp.settings.host == "0.0.0.0"
        
        # Verify mcp.run was called without transport parameter (default HTTP)
        mock_mcp.run.assert_called_once_with()

    @patch('main.mcp')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_default_values(self, mock_parse_args, mock_mcp):
        """Test main function with default argument values."""
        # Mock command line arguments with defaults
        mock_args = MagicMock()
        mock_args.sse = False
        mock_args.port = 8888  # default
        mock_args.host = "0.0.0.0"  # default
        mock_parse_args.return_value = mock_args

        # Mock mcp settings and run method
        mock_mcp.settings.port = 8888
        mock_mcp.settings.host = "0.0.0.0"
        mock_mcp.run = MagicMock()

        main()

        # Verify mcp settings were updated
        assert mock_mcp.settings.port == 8888
        assert mock_mcp.settings.host == "0.0.0.0"
        
        # Verify mcp.run was called without transport parameter
        mock_mcp.run.assert_called_once_with()

    @patch('main.mcp')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_custom_host_port(self, mock_parse_args, mock_mcp):
        """Test main function with custom host and port."""
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.sse = False
        mock_args.port = 3000
        mock_args.host = "192.168.1.100"
        mock_parse_args.return_value = mock_args

        # Mock mcp settings and run method
        mock_mcp.settings.port = 8888
        mock_mcp.settings.host = "0.0.0.0"
        mock_mcp.run = MagicMock()

        main()

        # Verify mcp settings were updated
        assert mock_mcp.settings.port == 3000
        assert mock_mcp.settings.host == "192.168.1.100"
        
        # Verify mcp.run was called without transport parameter
        mock_mcp.run.assert_called_once_with()

    @patch('main.mcp')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_sse_with_custom_values(self, mock_parse_args, mock_mcp):
        """Test main function with SSE transport and custom values."""
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.sse = True
        mock_args.port = 5000
        mock_args.host = "10.0.0.1"
        mock_parse_args.return_value = mock_args

        # Mock mcp settings and run method
        mock_mcp.settings.port = 8888
        mock_mcp.settings.host = "0.0.0.0"
        mock_mcp.run = MagicMock()

        main()

        # Verify mcp settings were updated
        assert mock_mcp.settings.port == 5000
        assert mock_mcp.settings.host == "10.0.0.1"
        
        # Verify mcp.run was called with SSE transport
        mock_mcp.run.assert_called_once_with(transport="sse")
