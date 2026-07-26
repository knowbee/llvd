import sys
import click
from llvd.logger import logger
from llvd.exceptions import LLVDBaseException

def handle_error(error, exit_on_error=False, show_traceback=False):
    """
    Centralized error handler for LLVD
    
    Args:
        error: The exception to handle
        exit_on_error: Whether to exit the program after handling the error
        show_traceback: Whether to show the full traceback in logs
    """
    if isinstance(error, LLVDBaseException):
        # Handle custom exceptions
        logger.error(str(error))
        click.echo(click.style(f"Error: {str(error)}", fg="red"))
    else:
        # Handle unexpected exceptions
        if show_traceback:
            logger.exception(f"Unexpected error: {str(error)}")
        else:
            logger.error(f"Unexpected error: {str(error)}")
        
        click.echo(click.style(f"An unexpected error occurred: {str(error)}", fg="red"))
        click.echo("Check the log file for more details.")
    
    if exit_on_error:
        sys.exit(1)

def format_error_message(error_type, message):
    """
    Format an error message with consistent styling
    
    Args:
        error_type: Type of error (e.g., "Authentication", "Network")
        message: Error message
        
    Returns:
        Formatted error message
    """
    return f"{error_type} Error: {message}"
