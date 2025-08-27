import logging
import requests
from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch
from config import SERVER_NAME, BLOG_BASE_URL, SERPAPI_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server: Code will be added later
