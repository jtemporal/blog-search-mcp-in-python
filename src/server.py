import logging
import requests
from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch
from config import SERVER_NAME, BLOG_BASE_URL, SERPAPI_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(name=SERVER_NAME)


@mcp.tool()
def get_post_content(title: str) -> str:
    """
    Get the full content of a blog post by title.

    Args:
        title: The title of the blog post (e.g., "Creating a Travel Diary With Django")

    Returns:
        The full markdown content of the blog post
    """
    try:
        # Fetch the llms.txt content from the blog
        llm_url = f"{BLOG_BASE_URL}/llms.txt"
        response = requests.get(llm_url, timeout=10)
        response.raise_for_status()

        # Parse the llm.txt content to find the post by title
        content = response.text
        lines = content.split('\n')

        # Find the line that contains the title and extract the raw GitHub URL
        raw_url = None
        for line in lines:
            if line.strip().startswith('#') or not line.strip():
                # Skip comments and empty lines for a more robust parser
                continue
            if title in line:
                # Extract URL from markdown link format: [title](url)
                raw_url = line.split('](')[1].strip(')')

        if not raw_url:
            return f"Post with title '{title}' not found in llm.txt"

        # Fetch the raw markdown content from GitHub
        content_response = requests.get(raw_url, timeout=10)
        content_response.raise_for_status()

        return content_response.text

    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"
    except Exception as e:
        return f"Error processing content: {str(e)}"


@mcp.tool()
def search_posts(query: str) -> str:
    """Search through blog posts for content matching the query."""
    search = GoogleSearch({
        "q": f"site:{BLOG_BASE_URL.strip('https://')} {query}", 
        "api_key": SERPAPI_KEY
    })
    search_result = search.get_dict()

    if search_result.get("search_metadata").get("status") == "Success":
        posts = search_result.get("organic_results", [])
        if posts:
            result = f"Found {len(posts)} post(s) matching '{query}':\n\n"
            for post in posts:
                title = post.get("title")
                url = post.get("link")
                snippet = post.get("snippet")
                result += f"**{title}**\n{url}\n{snippet}\n\n"
            return result

    return f"No posts found matching '{query}'."


if __name__ == "__main__":
    mcp.run(transport="stdio")