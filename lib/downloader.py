
from tqdm import tqdm
import requests


def download(url, filename):
    print("\n" + filename + "\n")
    with open(f"{filename}.mp4", 'wb') as f:
        try:
            response = requests.get(
                url, stream=True)
            download_size = int(response.headers.get('content-length'))
            if download_size is None:
                print("video not found")
                return
            else:
                pbar = tqdm(
                    total=download_size,
                    initial=0,
                    unit='B',
                    unit_scale=True,
                    position=0,
                    leave=True)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.set_description("downloading")
                        pbar.update(1024)
                pbar.close()
        except Exception as e:
            print(e)
            print("network error...try again")
