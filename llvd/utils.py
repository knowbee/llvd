import re
import sys
from random import randint
from time import sleep
from llvd.logger import logger
from llvd.exceptions import ParsingError


def subtitles_time_format(ms):
    """
    Formats subtitles time from milliseconds to SRT format
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Formatted time string in SRT format (HH:MM:SS,MS)
    """
    try:
        seconds, milliseconds = divmod(ms, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:02}'
    except Exception as e:
        logger.error(f"Error formatting subtitle time: {e}")
        return "00:00:00,000"


def clean_name(name):
    """
    Clean a name by removing special characters and formatting
    
    Args:
        name: String to clean
        
    Returns:
        Cleaned string
    """
    try:
        if not name:
            logger.warning("Attempted to clean an empty name")
            return ""
            
        digit_removed = re.sub(r'^\d+\.', "", name)
        chars_removed = re.sub(r'[\\:<>"/|?*’.\')(,]', "", digit_removed).replace("«", " ")\
        .replace("-»", " ").replace("»", " ").strip()
        extra_space_removed = re.sub(r'(\s+)', " ", chars_removed)
        result = extra_space_removed.strip()
        
        logger.debug(f"Cleaned name: '{name}' -> '{result}'")
        return result
    except Exception as e:
        logger.error(f"Error cleaning name '{name}': {e}")
        return name


def clean_dir(course_name):
    """
    Clean a directory name by removing special characters and formatting
    
    Args:
        course_name: Directory name to clean
        
    Returns:
        Cleaned directory name suitable for filesystem
    """
    try:
        if not course_name:
            logger.warning("Attempted to clean an empty directory name")
            return ""
            
        course = course_name.lower().replace("c#", "c-sharp").replace(".net", "-dot-net")
        without_chars = re.sub(r'[\':)(,>.\''/]', " ", course.strip()).replace("«", " ")\
            .replace("-»", " ").replace("»", " ").strip()
        result = re.sub(r'(\s+)', "-", without_chars).replace("--", "-")
        
        logger.debug(f"Cleaned directory name: '{course_name}' -> '{result}'")
        return result
    except Exception as e:
        logger.error(f"Error cleaning directory name '{course_name}': {e}")
        # Return a safe fallback that won't cause filesystem issues
        return re.sub(r'[^a-zA-Z0-9-]', "-", course_name.lower())


def throttle(wait_time=None):
    """
    Throttle execution by waiting for a specified amount of time
    
    Args:
        wait_time: List containing either [delay] or [min_delay, max_delay]
    """
    esc: str = '\x1b['
    clear_line = f'{esc}2K'
    cursor_home = f'{esc}0G'
    cursor_up = f'{esc}1A'
    
    if wait_time is None:
        logger.error("Missing throttle wait time")
        print('Error: missing throttle wait time.')
        return
        
    try:
        if len(wait_time) > 1:
            min_delay = max(0, wait_time[0])  # Ensure non-negative
            max_delay = max(min_delay, wait_time[1])  # Ensure max >= min
            delay = randint(min_delay, max_delay)
            logger.info(f"Throttling with random delay between {min_delay} and {max_delay} seconds: {delay}s")
        else:
            delay = max(0, wait_time[0])  # Ensure non-negative
            logger.info(f"Throttling with fixed delay: {delay}s")
            
        print(f'Delaying for {delay} seconds.')
        sleep(delay)
        # Clean up delay message
        print(f'{cursor_up}{clear_line}{cursor_up}{cursor_home}')
    except Exception as e:
        logger.error(f"Error during throttle: {e}")
        # Still sleep for a minimum time to avoid hammering the server
        sleep(5)
