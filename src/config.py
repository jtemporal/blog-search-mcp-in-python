import logging
import os
from configparser import ConfigParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(env: str = "dev"):
    """Load configuration for the MCP server"""
    
    env = os.getenv("ENV", env)
    logger.info(f"Loading configuration for environment: {env}")
    
    if env == "dev":
        # Try to load from .config file first
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(script_dir, ".config")
        config = ConfigParser()
        
        if os.path.exists(config_path):
            try:
                config.read(config_path)
                if "MCP_SERVER" in config:
                    logger.info("Loaded configuration from .config file")
                return config["MCP_SERVER"]
            except Exception as e:
                logger.warning(f"Could not load .config file: {e}")
        
        # Fallback to .config.example if .config doesn't exist or failed to load
        config_example_path = os.path.join(script_dir, ".config.example")
        if os.path.exists(config_example_path):
            try:
                config.read(config_example_path)
                if "MCP_SERVER" in config:
                    logger.info("Loaded configuration from .config.example file (fallback)")
                return config["MCP_SERVER"]
            except Exception as e:
                logger.warning(f"Could not load .config.example file: {e}")
        
        logger.warning("No config file found, using defaults")
    
    # Production or fallback configuration using environment variables
    config = {
        "blog_base_url": os.getenv("BLOG_BASE_URL", "https://yourblog.com"),
        "server_name": os.getenv("SERVER_NAME", "Blog Search Server"),
        "log_level": os.getenv("LOG_LEVEL", "WARNING" if env == "production" else "INFO"),
        "serpapi_key": os.getenv("SERPAPI_KEY", "your-serpapi-key")
    }
    
    return config

# Load configuration on import
CONFIG = load_config()

# Export configuration values for easy import
BLOG_BASE_URL = CONFIG.get("blog_base_url", "https://yourblog.com")
SERVER_NAME = CONFIG.get("server_name", "Blog Search Server")
LOG_LEVEL = CONFIG.get("log_level", "INFO")
SERPAPI_KEY = CONFIG.get("serpapi_key")

# Log token status
if SERPAPI_KEY:
    logger.info("SerpAPI key loaded for authenticated requests")
