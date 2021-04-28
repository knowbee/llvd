import re


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
