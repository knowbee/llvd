import re
from random import randint
from time import sleep

def subtitles_time_format(ms):
    """
    Formats subtitles time
    """
    seconds, milliseconds = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:02}'

def clean_name(name):
    digit_removed = re.sub(r'^\d+\.', "", name)
    chars_removed = re.sub(r'[\\:<>"/|?*’.\')(,]', "", digit_removed).replace("«", " ").replace("-»", " ").replace("»", " ").strip()
    extra_space_removed= re.sub(r'(\s+)', " ", chars_removed)
    return extra_space_removed.strip()

def clean_dir(course_name):
    course = course_name.lower().replace("c#", "c-sharp").replace(".net", "-dot-net")
    without_chars = re.sub(r'[\':)(,>.’/]', " ", course.strip()).replace("«", " ").replace("-»", " ").replace("»", " ").strip()
    return re.sub(r'(\s+)', "-", without_chars).replace("--", "-")


def throttle(wait_time=None):
    ESC = '\x1b['
    CLEAR_LINE = f'{ESC}2K'
    CURSOR_HOME = f'{ESC}0G'
    CURSOR_UP = f'{ESC}1A'
    if wait_time is None:
        print('utils.py#throttle - Error: missing throttle wait time.')
        return
    if(len(wait_time) > 1):
        min_delay = wait_time[0]
        max_delay = wait_time[1]
        delay = randint(min_delay, max_delay)
    else:
        delay = wait_time[0] # in case only one parameter passed
    print(f'Delaying for {delay} seconds.')
    sleep(delay)
    # clean up delay message
    print(f'{CURSOR_UP}{CLEAR_LINE}{CURSOR_UP}{CURSOR_HOME}')
