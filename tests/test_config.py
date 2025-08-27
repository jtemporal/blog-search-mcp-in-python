"""
Tests for the config.py module
"""
import sys
import os
from unittest.mock import patch

import pytest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


class TestConfigModule:
    """Test cases for the config.py module."""
    
    def test_default_config_values(self):
        """Test that default configuration values are properly set."""
        from config import load_config
        
        with patch('config.os.path.exists', return_value=False):
            with patch.dict('os.environ', {}, clear=True):
                result = load_config('dev')
        
        expected_keys = [
            "blog_base_url", "server_name", "log_level", "serpapi_key"
        ]
        
        for key in expected_keys:
            assert key in result
            assert result[key] is not None
            assert isinstance(result[key], str)
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('config.os.path.exists')
    def test_load_config_no_file_no_env(self, mock_exists):
        """Test loading config when no .config file exists and no env vars are set."""
        mock_exists.return_value = False
        
        from config import load_config
        result = load_config('dev')
        
        # Should return default values
        assert result['blog_base_url'] == 'https://yourblog.com'
        assert result['server_name'] == 'Blog Search Server'
        assert result['log_level'] == 'INFO'
        assert result['serpapi_key'] == 'your-serpapi-key'
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('config.os.path.exists')
    @patch('config.ConfigParser')
    def test_load_config_from_example_file(self, mock_config_parser, mock_exists):
        """Test loading config from .config.example when .config doesn't exist."""
        # .config doesn't exist, but .config.example does
        mock_exists.side_effect = lambda path: path.endswith('.config.example')
        
        # Mock the ConfigParser
        mock_parser = mock_config_parser.return_value
        mock_parser.__contains__ = lambda self, key: key == 'MCP_SERVER'
        mock_parser.__getitem__ = lambda self, key: {
            'blog_base_url': 'https://example.com',
            'server_name': 'Example Server',
            'serpapi_key': 'example-api-key'
        }
        
        from config import load_config
        result = load_config('dev')
        
        # Should use values from .config.example
        assert result['blog_base_url'] == 'https://example.com'
        assert result['server_name'] == 'Example Server'
        assert result['serpapi_key'] == 'example-api-key'
    
    @patch.dict('os.environ', {
        'BLOG_BASE_URL': 'https://test-blog.com',
        'SERVER_NAME': 'Test Server',
        'SERPAPI_KEY': 'test-api-key-123'
    }, clear=True)
    @patch('config.os.path.exists')
    def test_load_config_from_environment(self, mock_exists):
        """Test loading config from environment variables."""
        mock_exists.return_value = False
        
        from config import load_config
        result = load_config('dev')
        
        # Should use environment values
        assert result['blog_base_url'] == 'https://test-blog.com'
        assert result['server_name'] == 'Test Server'
        assert result['serpapi_key'] == 'test-api-key-123'
    
    @patch('config.os.path.exists')
    @patch('config.ConfigParser')
    def test_load_config_from_file(self, mock_config_parser, mock_exists):
        """Test loading config from .config file."""
        # .config exists
        mock_exists.side_effect = lambda path: path.endswith('.config')
        
        # Mock the ConfigParser
        mock_parser = mock_config_parser.return_value
        mock_parser.__contains__ = lambda self, key: key == 'MCP_SERVER'
        mock_parser.__getitem__ = lambda self, key: {
            'blog_base_url': 'https://file-blog.com',
            'server_name': 'File Server',
            'serpapi_key': 'file-api-key'
        }
        
        # Clear environment to test file loading
        with patch.dict('os.environ', {}, clear=True):
            from config import load_config
            result = load_config('dev')
        
            # Should use values from file
            assert result['blog_base_url'] == 'https://file-blog.com'
            assert result['server_name'] == 'File Server'
            assert result['serpapi_key'] == 'file-api-key'
    
    @patch.dict('os.environ', {'ENV': 'production'}, clear=True)
    @patch('config.os.path.exists')
    def test_load_config_production_environment(self, mock_exists):
        """Test loading config for production environment."""
        mock_exists.return_value = False
        
        from config import load_config
        result = load_config('production')
        
        # Should set production-specific defaults
        assert result['log_level'] == 'WARNING'
    
    @patch('config.os.path.exists')
    @patch('config.ConfigParser')
    def test_load_config_file_read_error(self, mock_config_parser, mock_exists, caplog):
        """Test handling of config file read errors."""
        mock_exists.return_value = True
        mock_config_parser.return_value.read.side_effect = Exception("File read error")
        
        # Clear environment to test error handling
        with patch.dict('os.environ', {}, clear=True):
            from config import load_config
            result = load_config('dev')
        
            # Should fall back to defaults
            assert result['blog_base_url'] == 'https://yourblog.com'
            assert result['server_name'] == 'Blog Search Server'
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('config.os.path.exists')
    def test_load_config_serpapi_key_priority(self, mock_exists):
        """Test that SERPAPI_KEY environment variable takes priority."""
        mock_exists.return_value = False
        
        with patch.dict('os.environ', {'SERPAPI_KEY': 'env-serpapi-key'}):
            from config import load_config
            result = load_config('dev')
            assert result['serpapi_key'] == 'env-serpapi-key'
    
    def test_config_exports_correct_values(self):
        """Test that config module exports the expected constants."""
        from config import (
            BLOG_BASE_URL, SERVER_NAME, LOG_LEVEL, SERPAPI_KEY
        )
        
        # Should all be strings or None (for SERPAPI_KEY if not set)
        assert isinstance(BLOG_BASE_URL, str)
        assert isinstance(SERVER_NAME, str)
        assert isinstance(LOG_LEVEL, str)
        # SERPAPI_KEY can be None if not set
        assert SERPAPI_KEY is None or isinstance(SERPAPI_KEY, str)
    
    @patch('config.os.path.dirname')
    @patch('config.os.path.abspath')
    def test_config_file_path_construction(self, mock_abspath, mock_dirname):
        """Test that config file path is constructed correctly."""
        mock_abspath.return_value = '/fake/path/to/src/config.py'
        mock_dirname.side_effect = ['/fake/path/to/src', '/fake/path/to']
        
        with patch('config.os.path.exists') as mock_exists:
            mock_exists.return_value = False  # Neither .config nor .config.example exist
            from config import load_config
            load_config('dev')
            
            # Should check for .config file first, then .config.example
            expected_config_path = '/fake/path/to/.config'
            expected_example_path = '/fake/path/to/.config.example'
            
            # Verify both paths were checked
            calls = mock_exists.call_args_list
            assert any(call[0][0] == expected_config_path for call in calls), f"Expected {expected_config_path} to be checked"
            assert any(call[0][0] == expected_example_path for call in calls), f"Expected {expected_example_path} to be checked"


if __name__ == '__main__':
    pytest.main([__file__])