import os
import json
from pathlib import Path
from llvd.logger import logger
from llvd.exceptions import ConfigurationError

# API endpoints
login_url = "https://www.linkedin.com/checkpoint/lg/login"
signup_url = "https://www.linkedin.com/checkpoint/lg/login-submit"
course_url = "https://www.linkedin.com/learning-api/detailedCourses??fields=videos&addParagraphsToTranscript=true&courseSlug={0}&q=slugs"
video_url = "https://www.linkedin.com/learning-api/detailedCourses?addParagraphsToTranscript=false&courseSlug={0}&q=slugs&resolution=_{1}&videoSlug={2}"
path_url = "https://www.linkedin.com/learning/paths/{0}"

# Default credentials
email = ""
password = ""

# Config directory
CONFIG_DIR = os.path.expanduser("~/.llvd")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def load_config():
    """
    Load configuration from config file if it exists
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config
        else:
            logger.info("No configuration file found, using defaults")
            return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise ConfigurationError(f"Invalid configuration file format: {e}") from e
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise ConfigurationError(f"Failed to load configuration: {e}") from e

def save_config(config_dict):
    """
    Save configuration to config file
    
    Args:
        config_dict (dict): Configuration to save
    """
    try:
        # Create config directory if it doesn't exist
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_dict, f, indent=2)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        raise ConfigurationError(f"Failed to save configuration: {e}") from e

# Try to load config at module import time
try:
    config = load_config()
    # Update email and password if they exist in config
    if 'email' in config:
        email = config['email']
    if 'password' in config:
        password = config['password']
    logger.debug("Configuration initialized")
except Exception as e:
    logger.warning(f"Failed to load configuration: {e}")
    # Continue with default values
