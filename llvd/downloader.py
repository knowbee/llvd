
from tqdm import tqdm
import requests
import time

def download_video(url, index, filename):
    """
        Downloads a video and saves it by its name plus index for easy sorting
    """
    print("\n" + filename + "\n")
    with open(f"{index}-{filename}.mp4", 'wb') as f:
        try:
            response = requests.get(
                url, stream=True, timeout=None, headers={'Accept-Encoding': None, 'Content-Encoding':'gzip' })
            time.sleep(1)
            download_size = response.headers.get('content-length')
            if download_size is None:
                download_size = len(response.raw.read())
            else:
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
        except Exception:
            click.echo(
                            click.style(f"Your internet connection is slow", fg="red"))