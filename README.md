# MCP Blog Search Server

A Model Context Protocol (MCP) server that allows AI assistants like Claude to search through your blog posts using SerpApi and retrieve content via llms.txt indexing. Built with Python and designed for seamless integration with Claude Desktop.

## Features

- 🔍 **Smart blog search** using SerpApi for reliable, Google-powered search results
- 📖 **Full content retrieval** via llms.txt indexing and GitHub raw content
- ⚡ **Fast and lightweight** with minimal dependencies
- 🔧 **Simple configuration** with just a few required settings
- 🧪 **Comprehensive testing** with unit, integration, and fixture-based tests
- 🤖 **Claude Desktop ready** with easy MCP configuration

## Architecture

Our server uses a modern, reliable architecture:
- **SerpApi** for site-specific blog post search (no complex GitHub API setup)
- **llms.txt** standard for AI-optimized content indexing
- **GitHub raw content** for fast markdown retrieval
- **FastMCP** framework for clean tool definitions

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone https://github.com/jtemporal/blog-search-mcp-in-python.git
   cd blog-search-mcp-in-python
   uv sync
   ```

2. **Configure your blog**:
   ```bash
   cp .config.example .config
   # Edit .config with your blog URL and SerpApi key
   ```

3. **Test the setup**:
   ```bash
   uv run pytest tests/test_config.py -v
   ```

4. **Inspect the server** with MCP Inspector:
    ```bash
    npx @modelcontextprotocol/inspector uv run src/server.py
    ```

## Configuration

Copy `.config.example` to `.config` and update with your blog details:

```ini
[MCP_SERVER]
blog_base_url = https://yourblog.com
serpapi_key = your-serpapi-key-here
server_name = Blog Search Server
log_level = INFO
```

### Getting a SerpApi Key

1. Sign up for free at [SerpApi](https://serpapi.com)
2. Get your API key from the dashboard
3. Add it to your `.config` file

**Note**: SerpApi provides 100 free searches per month, which is usually sufficient for personal blog searching.

## Testing

### Unit Tests (Fast, Mock Data)

```bash
# Run all unit tests (default)
uv run pytest

# Verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py -v
```

### Integration Tests (Real API Calls)

```bash
# Run integration tests (requires SerpApi key)
uv run pytest tests/test_integration.py -v -m integration

# Or run manually for detailed output
uv run python tests/test_integration.py
```

### Test Structure
- **Unit tests**: Fast tests with mocked SerpApi responses and fixtures
- **Integration tests**: Real API calls to SerpApi and GitHub (requires valid API key)
- **Fixtures**: Test data stored in `tests/fixtures/` for better maintainability

### Test Markers
- `pytest` - Runs unit tests only (default, integration tests excluded)
- `pytest -m integration` - Runs integration tests only
- `pytest -m ""` - Runs all tests (unit + integration)

## Development

### Project Structure
```
mcp-with-python-blog/
├── src/
│   ├── server.py            # Main MCP server with tools
│   └── config.py            # Configuration management
├── tests/
│   ├── fixtures/            # Test data in JSON files
│   ├── conftest.py          # Pytest fixtures (loads from fixtures/)
│   ├── test_server.py       # Unit tests with mocked responses
│   ├── test_config.py       # Configuration loading tests
│   └── test_integration.py  # Integration tests (real API calls)
├── blog-post/               # Blog post about this project
├── .config                  # Your blog configuration
├── .config.example          # Configuration template
├── pyproject.toml           # Project configuration and dependencies
└── uv.lock                  # Dependency lock file
```

### Running the MCP Server

```bash
# Run locally for testing
uv run mcp src/server.py
```

### Available Tools

The MCP server provides two main tools:

1. **`search_posts(query: str)`** - Search through blog posts using SerpApi
   - Performs site-specific Google search
   - Returns titles, URLs, and excerpts
   - Example: "Search for posts about Python"

2. **`get_post_content(title: str)`** - Get full content of a specific post
   - Uses llms.txt index to find posts
   - Fetches raw markdown from GitHub
   - Supports partial title matching
   - Example: "Get content for 'Python Tips'"

## Claude Desktop Setup

To use this MCP server with Claude Desktop:

1. **Run the install command**:
   ```bash
   uv run mcp install "src/server.py" --with google-search-results
   ```
   This will create the server configuration within Claude automatically.

2. **Restart Claude Desktop** completely

3. **Test the integration**:
   - Start a new conversation
   - Ask: "Search my blog for posts about Python"
   - Claude should offer to use the `search_posts` tool

## Cursor Desktop Setup

To use this MCP server with Cursor Desktop:

1. **Locate your Cursor MCP config file**:
   - **macOS**: `~/.cursor/mcp.json`
   - **Windows**: `%APPDATA%\Cursor\mcp.json`
   - **Linux**: `~/.config/Cursor/mcp.json`

2. **Add the MCP server configuration**:
   ```json
   {
     "mcpServers": {
       "blog-search": {
         "command": "/path/to/uv",
         "args": [
           "run",
           "--python", "3.12.11",
           "--with", "mcp[cli]",
           "--with", "google-search-results",
           "--with", "python-dotenv",
           "mcp",
           "run",
           "/absolute/path/to/your/project/src/server.py"
         ],
         "cwd": "/absolute/path/to/your/project"
       }
     }
   }
   ```

3. **Update the paths**:
   - Replace `/path/to/uv` with your uv executable path (find with `which uv`)
   - Replace `/absolute/path/to/your/project` with your project directory

4. **Restart Cursor** completely and test the integration

## Usage Examples

Once configured with Claude Desktop, you can:

### Search for Posts
- *"Search my blog for posts about Python"*
- *"Find articles related to web development"*
- *"Look for tutorials on data science"*

### Get Full Content
- *"Get the content of the Python tips post"*
- *"Show me the full article about Django"*
- *"Retrieve the content for 'Introduction to Data Science'"*

### Workflow Integration
- *"Search for my post about JWT handling, then summarize the key points"*
- *"Find my Django tutorial and explain the main concepts"*
- *"Look up my Python posts and create a learning roadmap"*

## Requirements

### For Your Blog

Your blog needs to provide an `llms.txt` file at `https://yourblog.com/llms.txt` that follows this format:

```
# LLM Feed for yourblog.com

This file contains links to blog posts in markdown format for easy LLM consumption.

- [Post Title 1](https://raw.githubusercontent.com/username/repo/main/_posts/post1.md)
- [Post Title 2](https://raw.githubusercontent.com/username/repo/main/_posts/post2.md)
...
```

This file serves as an index that links to the raw markdown content of your posts on GitHub.

If you don't have a blog or `llms.txt` file feel free to use mine: `https://jtemporal.com`.

## Dependencies

- Python 3.12+
- `SerpApi` account (free tier available, [sign up here](https://serpapi.com))
- Blog with llms.txt index (or you can use mine if you prefer: `https://jtemporal.com`)
- `uv` package manager

## Contributing

1. **Setup development environment**:
   ```bash
   git clone https://github.com/jtemporal/mcp-with-python-blog.git
   cd mcp-with-python-blog
   uv sync
   ```

2. **Run tests**: 
   ```bash
   uv run pytest -v
   ```

3. **Add tests for new features** in appropriate test files

4. **Update fixtures** in `tests/fixtures/` when adding new test data

5. **Follow the existing code style** and add proper docstrings

### Adding New Fixtures

Test data is stored in `tests/fixtures/` as JSON files:
- `blog_posts.json` - Sample blog post data
- `config.json` - Test configuration
- `serpapi_*.json` - Mock SerpApi responses

To add new test data, create a JSON file and load it in `conftest.py` using the `load_fixture()` function.

## Troubleshooting

### Common Issues

- **SerpApi key not working**: Verify your key at [SerpApi dashboard](https://serpapi.com/dashboard)
- **No search results**: Check that your blog URL is correct and publicly accessible
- **llms.txt not found**: Ensure your blog serves the llms.txt file at the root
- **Claude Desktop not recognizing server**: Check file paths and restart Claude completely

### Debug Mode

Run the server manually to see detailed logs:
```bash
uv run python src/server.py
```

Run integration tests to verify API connectivity:
```bash
uv run python tests/test_integration.py
```

## License

MIT License - see LICENSE file for details.