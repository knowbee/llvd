from tqdm import tqdm
import requests
import click
import re
from llvd.utils import clean_name, subtitles_time_format, throttle


def download_video(url, index, filename, path, delay=None):
    """
    Downloads a video and saves it by its name plus index for easy sorting
    """
    if delay:
        throttle(delay)
    maximum_retries = 5
    with open(f"{path}/{index:0=2d}. {clean_name(filename)}.mp4", "wb") as f:
        download_size = 0
        while maximum_retries > 0:
            requests.adapters.HTTPAdapter(max_retries=maximum_retries)
            response = requests.get(
                url,
                stream=True,
                headers={"Accept-Encoding": None, "Content-Encoding": "gzip"},
            )
            download_size = response.headers.get("content-length")
            if download_size is None and maximum_retries > 0:
                maximum_retries -= 1
            else:
                break
        pbar = tqdm(
            total=int(download_size),
            initial=0,
            unit="B",
            unit_scale=True,
            position=0,
            leave=True,
        )
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.set_description("Downloading video... ")
                pbar.update(len(chunk))
        pbar.close()


def download_subtitles(index, subs, video_name, path, video_duration):
    """Write to a file (subtitle file) caption matching the right time."""
    with open(f"{path}/{index:0=2d}. {clean_name(video_name).strip()}.srt", "wb") as f:
        click.echo("Downloading subtitles..")
        for i, sub in enumerate(subs, start=1):
            starts_at = sub["transcriptStartAt"]
            ends_at = subs[i]["transcriptStartAt"] if i < len(subs) else video_duration
            caption = sub["caption"]
            line = f"{i}\n{subtitles_time_format(starts_at)} --> {subtitles_time_format(ends_at)}\n{caption}\n\n"
            f.write(line.encode("utf8"))


def download_exercises(links, path):
    """Download exercises."""
    for link in links:
        filename = re.split("exercises/(.+).zip", link)[1]
        filepath = f"{path}/{clean_name(filename)}.zip"
        with open(filepath, "wb") as f:
            # Set up the request
            request = requests.get(
                link,
                stream=True,
                headers={"Accept-Encoding": None, "Content-Encoding": "gzip"},
            )
            download_size = request.headers.get("content-length")

            # Show a progress bar while downloading the file
            if download_size:
                pbar = tqdm(
                    total=int(download_size),
                    initial=0,
                    unit="B",
                    unit_scale=True,
                    position=0,
                    leave=True,
                    desc="Downloading exercise files...",
                )
            else:
                pbar = None

            # Write the file in chunks to the disk
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    if pbar:
                        pbar.update(len(chunk))

            # Close the progress bar
            if pbar:
                pbar.close()
            print("\n")
