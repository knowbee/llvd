
from tqdm import tqdm
import requests
import time
import click
import re
import os
from llvd.utils import clean_name


def download_video(url, index, filename, chapter_name, course_slug):
    """
        Downloads a video and saves it by its name plus index for easy sorting
    """
    print("\n" + clean_name(filename) + "\n")
    maximum_retries = 5
    with open(f'{course_slug}/{clean_name(chapter_name)}/{index}-{clean_name(filename)}.mp4', 'wb') as f:
        download_size = 0
        while maximum_retries > 0:
            requests.adapters.HTTPAdapter(max_retries=maximum_retries)
            response = requests.get(
                url, stream=True, headers={'Accept-Encoding': None, 'Content-Encoding': 'gzip'})
            download_size = response.headers.get('content-length')
            if download_size is None and maximum_retries > 0:
                maximum_retries -= 1
            else:
                break
        pbar = tqdm(
            total=int(download_size),
            initial=0,
            unit='B',
            unit_scale=True,
            position=0,
            leave=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.set_description("progress")
                pbar.update(len(chunk))
        pbar.close()
        print("\n")


def download_exercises(links, course_slug):
    """
        Downloads exercises
    """
    maximum_retries = 5
    click.echo(
        click.style(f"Downloading exercise files..." + "\n", fg="green"))

    for link in links:

        filename = re.split("exercises/(.+).zip", link)[1]

        with open(f"{course_slug}/{clean_name(filename)}.zip", 'wb') as f:
            download_size = 0
            while maximum_retries > 0:
                requests.adapters.HTTPAdapter(max_retries=maximum_retries)
                response = requests.get(
                    link, stream=True, headers={'Accept-Encoding': None, 'Content-Encoding': 'gzip'})
                download_size = response.headers.get('content-length')
                if download_size is None and maximum_retries > 0:
                    maximum_retries -= 1
                else:
                    break
            pbar = tqdm(
                total=int(download_size),
                initial=0,
                unit='B',
                unit_scale=True,
                position=0,
                leave=True)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.set_description("progress")
                    pbar.update(len(chunk))
            pbar.close()
            print("\n")
