import os
from dotenv import load_dotenv
from typing import Any, Dict

# Load environment variables from .env file
load_dotenv()

def get_config(key: str, default: Any = None) -> Any:
    """
    Get a configuration value from environment variables.
    
    Args:
        key: The configuration key to retrieve
        default: Default value to return if key is not found
        
    Returns:
        The configuration value
    """
    return os.environ.get(key, default)

def get_all_config() -> Dict[str, str]:
    """
    Get all configuration values.
    
    Returns:
        Dictionary of all configuration values
    """
    return dict(os.environ)