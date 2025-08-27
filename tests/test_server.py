"""
Tests for the MCP server tools
"""
import sys
import os
from unittest.mock import patch, Mock

import pytest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


class TestMCPServerTools:
    """Test cases for the MCP server tools."""
    
    @patch('server.GoogleSearch')
    def test_search_posts_found(self, mock_google_search):
        """Test searching posts with matches found using SerpApi."""
        from server import search_posts
        
        # Mock SerpApi response
        mock_search_instance = Mock()
        mock_google_search.return_value = mock_search_instance
        mock_search_instance.get_dict.return_value = {
            "search_metadata": {"status": "Success"},
            "organic_results": [
                {
                    "title": "Python Tips and Tricks",
                    "link": "https://jtemporal.com/python-tips",
                    "snippet": "Learn advanced Python techniques..."
                },
                {
                    "title": "Django for Beginners",
                    "link": "https://jtemporal.com/django-beginners",
                    "snippet": "Start your Django journey..."
                }
            ]
        }
        
        result = search_posts('python')
        
        assert 'Found 2 post(s) matching' in result
        assert 'Python Tips and Tricks' in result
        assert 'Django for Beginners' in result
        assert 'https://jtemporal.com/python-tips' in result
    
    @patch('server.GoogleSearch')
    def test_search_posts_not_found(self, mock_google_search):
        """Test searching posts with no matches."""
        from server import search_posts
        
        # Mock SerpApi response with no results
        mock_search_instance = Mock()
        mock_google_search.return_value = mock_search_instance
        mock_search_instance.get_dict.return_value = {
            "search_metadata": {"status": "Success"},
            "organic_results": []
        }
        
        result = search_posts('nonexistent')
        
        assert 'No posts found matching' in result
        assert 'nonexistent' in result
    
    @patch('server.GoogleSearch')
    def test_search_posts_api_failure(self, mock_google_search):
        """Test handling of SerpApi failure."""
        from server import search_posts
        
        # Mock SerpApi response with failure
        mock_search_instance = Mock()
        mock_google_search.return_value = mock_search_instance
        mock_search_instance.get_dict.return_value = {
            "search_metadata": {"status": "Error"}
        }
        
        result = search_posts('python')
        
        assert 'No posts found matching' in result
    
    @patch('server.requests.get')
    def test_get_post_content_found(self, mock_get):
        """Test getting specific post content by title."""
        from server import get_post_content
        
        # Mock llms.txt response
        llms_content = """# LLM Feed for jtemporal.com
_Generated: Wed, 27 Aug 2025 01:32:38 +0000_

## All posts
The links below take you to the raw Markdown content.

- [Python Tips and Tricks](https://raw.githubusercontent.com/jtemporal/jtemporal.github.io/refs/heads/main/_posts/2024-01-01-python-tips.md)
- [Django for Beginners](https://raw.githubusercontent.com/jtemporal/jtemporal.github.io/refs/heads/main/_posts/2024-01-02-django-beginners.md)
"""
        
        # Mock markdown content response
        markdown_content = """---
title: 'Python Tips and Tricks'
layout: post
date: 2024-01-01T04:00:00.000+00:00
tags:
- python
- tutorial
---

# Python Tips and Tricks

Here are some useful Python tips...
"""
        
        # Configure mock responses
        mock_responses = [
            Mock(status_code=200, text=llms_content),  # llms.txt response
            Mock(status_code=200, text=markdown_content)  # markdown content response
        ]
        mock_get.side_effect = mock_responses
        for response in mock_responses:
            response.raise_for_status = Mock()
        
        result = get_post_content('Python Tips and Tricks')
        
        assert 'Python Tips and Tricks' in result
        assert 'Here are some useful Python tips' in result
        assert 'layout: post' in result
    
    @patch('server.requests.get')
    def test_get_post_content_not_found(self, mock_get):
        """Test getting post content when post doesn't exist."""
        from server import get_post_content
        
        # Mock llms.txt response without the requested post
        llms_content = """# LLM Feed for jtemporal.com
_Generated: Wed, 27 Aug 2025 01:32:38 +0000_

## All posts
The links below take you to the raw Markdown content.

- [Python Tips and Tricks](https://raw.githubusercontent.com/jtemporal/jtemporal.github.io/refs/heads/main/_posts/2024-01-01-python-tips.md)
"""
        
        mock_response = Mock(status_code=200, text=llms_content)
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_post_content('Nonexistent Post')
        
        assert 'Post with title' in result
        assert 'not found in llm.txt' in result
    
    @patch('server.requests.get')
    def test_get_post_content_llms_txt_not_found(self, mock_get):
        """Test handling when llms.txt is not available."""
        from server import get_post_content
        
        # Mock 404 response for llms.txt
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")
        mock_get.return_value = mock_response
        
        result = get_post_content('Some Title')
        
        assert 'Error processing content' in result
    
    @patch('server.requests.get')
    def test_get_post_content_github_content_not_found(self, mock_get):
        """Test handling when GitHub content is not available."""
        from server import get_post_content
        
        # Mock llms.txt response
        llms_content = """# LLM Feed for jtemporal.com
_Generated: Wed, 27 Aug 2025 01:32:38 +0000_

## All posts
The links below take you to the raw Markdown content.

- [Python Tips and Tricks](https://raw.githubusercontent.com/jtemporal/jtemporal.github.io/refs/heads/main/_posts/2024-01-01-python-tips.md)
"""
        
        # Configure mock responses: first successful, second fails
        llms_response = Mock(status_code=200, text=llms_content)
        llms_response.raise_for_status = Mock()
        
        github_response = Mock()
        github_response.raise_for_status.side_effect = Exception("404 Client Error")
        
        mock_get.side_effect = [llms_response, github_response]
        
        result = get_post_content('Python Tips and Tricks')
        
        assert 'Error processing content' in result
    
    @patch('server.requests.get')
    def test_get_post_content_partial_title_match(self, mock_get):
        """Test getting post content with partial title match."""
        from server import get_post_content
        
        # Mock llms.txt response
        llms_content = """# LLM Feed for jtemporal.com
_Generated: Wed, 27 Aug 2025 01:32:38 +0000_

## All posts
The links below take you to the raw Markdown content.

- [Python Tips and Tricks](https://raw.githubusercontent.com/jtemporal/jtemporal.github.io/refs/heads/main/_posts/2024-01-01-python-tips.md)
"""
        
        # Mock markdown content response
        markdown_content = """---
title: 'Python Tips and Tricks'
layout: post
---

# Python Tips and Tricks

Content here...
"""
        
        # Configure mock responses
        mock_responses = [
            Mock(status_code=200, text=llms_content),
            Mock(status_code=200, text=markdown_content)
        ]
        mock_get.side_effect = mock_responses
        for response in mock_responses:
            response.raise_for_status = Mock()
        
        # Test partial match
        result = get_post_content('Python Tips')  # Partial title
        
        assert 'Python Tips and Tricks' in result
        assert 'Content here' in result
    
    def test_mcp_server_exists(self):
        """Test that the MCP server instance exists."""
        from server import mcp
        
        assert mcp is not None
        assert hasattr(mcp, 'tool')  # Should have the tool decorator method
    
    def test_server_tools_are_registered(self):
        """Test that all tools are properly registered with the MCP server."""
        import server
        
        # Check that the module has the expected tool functions
        assert hasattr(server, 'search_posts')
        assert hasattr(server, 'get_post_content')
        
        # Check that they are callable
        assert callable(server.search_posts)
        assert callable(server.get_post_content)
    
    @patch('server.GoogleSearch')
    def test_search_posts_constructs_correct_query(self, mock_google_search):
        """Test that search_posts constructs the correct site-specific query."""
        from server import search_posts
        
        mock_search_instance = Mock()
        mock_google_search.return_value = mock_search_instance
        mock_search_instance.get_dict.return_value = {
            "search_metadata": {"status": "Success"},
            "organic_results": []
        }
        
        search_posts('python tutorials')
        
        # Verify GoogleSearch was called with the correct parameters
        mock_google_search.assert_called_once()
        call_args = mock_google_search.call_args[0][0]
        assert 'site:jtemporal.com python tutorials' in call_args['q']
        assert 'api_key' in call_args


if __name__ == '__main__':
    pytest.main([__file__])