"""
Test fixtures for the MCP blog search server
"""
import json
import os
import pytest
from unittest.mock import Mock, MagicMock


def load_fixture(filename):
    """Load a fixture from the fixtures directory."""
    fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    with open(os.path.join(fixtures_dir, filename), 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_blog_posts():
    """Mock blog post data for testing."""
    return load_fixture('blog_posts.json')


@pytest.fixture
def mock_github_repo():
    """Mock GitHub repository object."""
    mock_repo = Mock()
    
    # Load blog posts from fixture
    blog_posts = load_fixture('blog_posts.json')
    
    # Mock file objects
    mock_files = []
    for post in blog_posts:
        mock_file = Mock()
        mock_file.name = post['name']
        mock_file.decoded_content.decode.return_value = post['content']
        mock_files.append(mock_file)
    
    mock_repo.get_contents.return_value = mock_files
    return mock_repo


@pytest.fixture
def mock_github_client(mock_github_repo):
    """Mock GitHub client with mocked repository."""
    mock_client = Mock()
    mock_client.get_repo.return_value = mock_github_repo
    return mock_client


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return load_fixture('config.json')


@pytest.fixture
def mock_serpapi_success_response():
    """Mock SerpApi successful search response."""
    return load_fixture('serpapi_success_response.json')


@pytest.fixture
def mock_serpapi_no_results():
    """Mock SerpApi response with no results."""
    return load_fixture('serpapi_no_results.json')


@pytest.fixture
def mock_llms_txt_content():
    """Mock llms.txt content for testing."""
    return load_fixture('llms_txt_content.json')['content']