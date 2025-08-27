#!/usr/bin/env python3
"""
Integration tests for the Blog Search MCP Server
These tests make real API calls to SerpApi and GitHub (for content) and should be run sparingly.
Run with: pytest tests/test_integration.py -v -m integration
"""

import sys
import os
import pytest

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

pytestmark = pytest.mark.integration  # Mark all tests in this file as integration tests


class TestIntegration:
    """Integration tests that make real API calls to SerpApi and GitHub."""
    
    def test_real_serpapi_connection(self):
        """Test that we can connect to the real SerpApi."""
        try:
            from server import search_posts
            from config import SERPAPI_KEY, BLOG_BASE_URL
            
            print(f"\n🔗 Testing SerpApi connection for {BLOG_BASE_URL}")
            
            if not SERPAPI_KEY or SERPAPI_KEY == 'your-serpapi-key':
                pytest.skip("No valid SerpApi key configured")
            
            # This makes a real API call to SerpApi
            result = search_posts('python')
            
            # Basic validation
            assert isinstance(result, str), "search_posts should return a string"
            assert len(result) > 0, "Search result should not be empty"
            
            # Check for expected patterns in the response
            if 'Found' in result and 'post(s) matching' in result:
                print(f"✅ Successfully searched blog posts via SerpApi")
                print(f"Result preview: {result[:200]}...")
            elif 'No posts found' in result:
                print("⚠️  No blog posts found for search term 'python'")
            else:
                print(f"⚠️  Unexpected response format: {result[:100]}...")
                
        except Exception as e:
            pytest.fail(f"SerpApi integration test failed: {e}")
    
    def test_search_functionality_real_data(self):
        """Test search functionality with real SerpApi data."""
        try:
            from server import search_posts
            from config import SERPAPI_KEY
            
            if not SERPAPI_KEY or SERPAPI_KEY == 'your-serpapi-key':
                pytest.skip("No valid SerpApi key configured")
            
            print("\n🔍 Testing search with real SerpApi data")
            
            # Try a common search term
            result = search_posts('tutorial')  # Common word likely to appear in blog posts
            
            assert isinstance(result, str), "search_posts should return a string"
            assert len(result) > 0, "Search result should not be empty"
            
            print(f"✅ Search completed successfully")
            print(f"Result preview: {result[:200]}...")
            
        except Exception as e:
            pytest.fail(f"Search integration test failed: {e}")
    
    def test_get_post_content_real_data(self):
        """Test getting post content with real llms.txt and GitHub data."""
        try:
            from server import get_post_content
            from config import BLOG_BASE_URL
            
            print(f"\n� Testing get_post_content with real data from {BLOG_BASE_URL}")
            
            # Try to get content for a likely post title
            # This will test both llms.txt fetching and GitHub raw content fetching
            result = get_post_content('Python')  # Partial match that might exist
            
            assert isinstance(result, str), "get_post_content should return a string"
            assert len(result) > 0, "Post content result should not be empty"
            
            if result.startswith('Post with title'):
                print("⚠️  No post found with 'Python' in title")
            elif result.startswith('Error'):
                print(f"⚠️  Error retrieving content: {result[:100]}...")
            else:
                print(f"✅ Post content retrieved successfully")
                print(f"Content preview: {result[:200]}...")
            
        except Exception as e:
            pytest.fail(f"Get post content integration test failed: {e}")
    
    def test_llms_txt_availability(self):
        """Test that the llms.txt endpoint is available."""
        try:
            import requests
            from config import BLOG_BASE_URL
            
            print(f"\n📋 Testing llms.txt availability at {BLOG_BASE_URL}")
            
            llms_url = f"{BLOG_BASE_URL}/llms.txt"
            response = requests.get(llms_url, timeout=10)
            response.raise_for_status()
            
            content = response.text
            assert len(content) > 0, "llms.txt should not be empty"
            assert 'LLM Feed' in content or 'raw.githubusercontent.com' in content, "llms.txt should contain expected format"
            
            print(f"✅ llms.txt available and contains {len(content)} characters")
            
            # Count number of posts listed
            lines = content.split('\n')
            post_lines = [line for line in lines if 'raw.githubusercontent.com' in line]
            print(f"   Found {len(post_lines)} posts in llms.txt")
            
        except Exception as e:
            pytest.fail(f"llms.txt availability test failed: {e}")


def main():
    """Run integration tests manually (outside of pytest)."""
    print("Manual Integration Testing Blog Search MCP Server...")
    print("⚠️  This makes real API calls to SerpApi and GitHub")
    print("=" * 60)
    
    try:
        # Import from src directory
        from server import search_posts, get_post_content
        from config import BLOG_BASE_URL, SERPAPI_KEY
        
        print(f"Configuration loaded:")
        print(f"  Blog URL: {BLOG_BASE_URL}")
        print(f"  SerpApi Key: {'configured' if SERPAPI_KEY and SERPAPI_KEY != 'your-serpapi-key' else 'not configured'}")
        print()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you have:")
        print("1. Installed dependencies: uv sync")
        print("2. Configured .config file with your SerpApi key")
        return
    except Exception as e:
        print(f"Configuration error: {e}")
        print("Check your .config file settings")
        return
    
    if not SERPAPI_KEY or SERPAPI_KEY == 'your-serpapi-key':
        print("⚠️  No SerpApi key configured. Set SERPAPI_KEY in .config file.")
        print("Some tests will be skipped.")
        print()
    
    # Test 1: Search posts via SerpApi
    print("1. Searching for 'python' via SerpApi:")
    try:
        results = search_posts('python')
        print(results[:500] + "..." if len(results) > 500 else results)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Search posts with different term
    print("\n2. Searching for 'tutorial':")
    try:
        results = search_posts('tutorial')
        print(results[:500] + "..." if len(results) > 500 else results)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get specific post content
    print("\n3. Getting post content with 'Python' in title:")
    try:
        post = get_post_content('Python')
        print(post[:300] + "..." if len(post) > 300 else post)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Test llms.txt endpoint
    print("\n4. Testing llms.txt endpoint:")
    try:
        import requests
        llms_url = f"{BLOG_BASE_URL}/llms.txt"
        response = requests.get(llms_url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            lines = [line for line in content.split('\n') if 'raw.githubusercontent.com' in line]
            print(f"Found {len(lines)} posts in llms.txt")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()