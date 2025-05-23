import os
import json
from typing import Any, Dict, List

# Directory for storing data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def save_data(filename: str, data: Any) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        filename: Name of the file to save to
        data: Data to save
        
    Returns:
        True if save was successful, False otherwise
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data to {filepath}: {str(e)}")
        return False

def load_data(filename: str, default: Any = None) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        filename: Name of the file to load from
        default: Default value to return if file doesn't exist or loading fails
        
    Returns:
        Loaded data or default value
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return default
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data from {filepath}: {str(e)}")
        return default