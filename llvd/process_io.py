import sys
import os
import click
from llvd.logger import logger
from llvd.exceptions import FileAccessError, ParsingError

def parse_cookie_file(file_path="cookies.txt"):
    """
    Parse the cookie file and return a dictionary of cookies.
    
    Args:
        file_path: Path to the cookie file
        
    Returns:
        Dictionary containing cookie values
        
    Raises:
        FileAccessError: If the file cannot be accessed or read
        ParsingError: If the file format is invalid
    """
    if not os.path.exists(file_path):
        logger.error(f"Cookie file not found: {file_path}")
        click.echo(click.style(f"Cookie file not found: {file_path}", fg="red"))
        raise FileAccessError(f"Cookie file not found: {file_path}")
        
    try:
        with open(file_path, "r") as file:
            cookies = {}
            for line in file:
                line = line.strip()
                if line.startswith("li_at"):
                    cookies["li_at"] = line.split("li_at=")[1]
                if line.startswith("JSESSIONID"):
                    cookies["JSESSIONID"] = line.split("JSESSIONID=")[1].replace('"', "")
                    
            # Validate required cookies are present
            if "li_at" not in cookies or "JSESSIONID" not in cookies:
                logger.error("Missing required cookies: li_at and JSESSIONID must be present")
                raise ParsingError("Missing required cookies: li_at and JSESSIONID must be present")
                
            logger.info(f"Successfully parsed cookie file: {file_path}")
            return cookies
    except FileNotFoundError:
        logger.error(f"Cookie file not found: {file_path}")
        click.echo(click.style(f"Cookie file not found: {file_path}", fg="red"))
        raise FileAccessError(f"Cookie file not found: {file_path}")
    except IOError as e:
        logger.error(f"Error reading cookie file: {e}")
        click.echo(click.style(f"Error reading cookie file: {e}", fg="red"))
        raise FileAccessError(f"Error reading cookie file: {e}")

def parse_header_file(file_path="headers.txt"):
    """
    Parse the header file and return a dictionary of headers.
    
    Args:
        file_path: Path to the header file
        
    Returns:
        Dictionary containing header values
        
    Raises:
        FileAccessError: If the file cannot be accessed or read
        ParsingError: If the file format is invalid
    """
    if not os.path.exists(file_path):
        logger.error(f"Header file not found: {file_path}")
        click.echo(click.style(f"Header file not found: {file_path}", fg="red"))
        raise FileAccessError(f"Header file not found: {file_path}")
        
    headers = {}
    try:
        with open(file_path, "r", encoding="utf8") as file:
            lines = file.readlines()
            if not lines:
                logger.warning(f"Header file is empty: {file_path}")
                
            for line_num, line in enumerate(lines, 1):
                try:
                    parts = line.split("=", 1)
                    if len(parts) < 2:
                        logger.warning(f"Invalid header format at line {line_num}: {line.strip()}")
                        continue
                        
                    key, value = parts
                    if not key.strip():
                        logger.warning(f"Empty header key at line {line_num}")
                        continue
                        
                    headers[key.strip()] = value.replace('"', "").strip()
                except Exception as e:
                    logger.error(f"Error parsing header at line {line_num}: {e}")
                    
        logger.info(f"Successfully parsed header file: {file_path} with {len(headers)} headers")
        return headers
    except FileNotFoundError:
        logger.error(f"Header file not found: {file_path}")
        click.echo(click.style(f"Header file not found: {file_path}", fg="red"))
        raise FileAccessError(f"Header file not found: {file_path}")
    except IOError as e:
        logger.error(f"Error reading header file: {e}")
        click.echo(click.style(f"Error reading header file: {e}", fg="red"))
        raise FileAccessError(f"Error reading header file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error parsing header file: {e}")
        click.echo(click.style(f"Unexpected error parsing header file: {e}", fg="red"))
        raise ParsingError(f"Unexpected error parsing header file: {e}")
