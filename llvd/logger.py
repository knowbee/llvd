import logging
import os
import sys
from datetime import datetime

def setup_logger(name="llvd", log_level=logging.INFO):
    """
    Set up and configure logger
    
    Args:
        name: Logger name
        log_level: Logging level
        
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.expanduser("~/.llvd/logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create file handler for logging to a file
    log_file = os.path.join(log_dir, f"llvd_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger

# Create a default logger instance
logger = setup_logger()
