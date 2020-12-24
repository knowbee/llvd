
from tqdm import tqdm
import requests
import time


def download(url, index, filename):
    print("\n" + filename + "\n")
    with open(f"{index}-{filename}.mp4", 'wb') as f:
        try:
            response = requests.get(
                url, stream=True)
            time.sleep(1)
            if(response and response.headers):
                download_size = response.headers.get('content-length')
                if download_size is None:
                    download_size = len(response.raw.read())
                    if download_size is None:
                        print("video not found")
                    return
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
                            pbar.set_description("downloading")
                            pbar.update(1024)
                    pbar.close()
            else:
                print("network is too slow")

        except Exception as e:
            print(e)
            print("network error...try again")
