from itertools import starmap
import re


def subtitles_time_format(ms):
    """
    Formats subtitles time
    """
    seconds, milliseconds = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:02}'


def write_subtitles(count, subs, video_name, course_slug, chapter_name, video_duration):
    """
    Writes to a file(subtitle file) caption matching the right time
    """
    def subs_to_lines(idx, sub):
        starts_at = sub['transcriptStartAt']
        ends_at = subs[idx]['transcriptStartAt'] if idx < len(
            subs) else video_duration
        caption = sub['caption']
        return f"{idx}\n" \
            f"{subtitles_time_format(starts_at)} --> {subtitles_time_format(ends_at)}\n" \
            f"{caption}\n\n"

    with open(f"{course_slug}/{clean_name(chapter_name)}/{count}-{clean_name(video_name).strip()}.srt", 'wb') as f:
        for line in starmap(subs_to_lines, enumerate(subs, start=1)):
            f.write(line.encode('utf8'))

def clean_name(name):
    digit_removed = re.sub(r'^\d+\.', "", name)
    chars_removed = re.sub(r'[\\:<>"/|?*’.\')(,]', "", digit_removed).replace("«", " ").replace("-»", " ").replace("»", " ").strip()
    extra_space_removed= re.sub(r'(\s+)', " ", chars_removed)
    return extra_space_removed.strip()