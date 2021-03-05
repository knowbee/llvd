# LLVD (Linkedin Learning Video Downloader)

[![Downloads](https://pepy.tech/badge/llvd)](https://pepy.tech/project/llvd)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

<p>
    <img src="https://raw.githubusercontent.com/knowbee/hosting/master/assets/progress_llvd.png" width="auto" height="auto"/>
</p>

## Features

| Status | Feature                                 |
| :----- | :-------------------------------------- |
| ✅     | download a course and all its exercises |
| ✅     | group videos by chapters                |
| ✅     | subtitles                               |
| ✅     | nice progress bar                       |
| ✅     | resume failed downloads                 |
| ✅     | skip already downloaded videos          |
| ✅     | set video format (360p, 540p, 720p)     |
| ✅     | all platforms                           |

## Prerequisites

- [Python 3](https://www.python.org/downloads/)

## Installation

    $ pip --no-cache-dir install llvd

If you have multiple versions of python installed in your system, use **pip3** instead.

## Example

```cli

    $ llvd --help
    $ llvd -c "Course Title" -r 720

```

### Download the course with subtitles

Use the `--caption` flag to download videos with subtitles

```cli

    $ llvd -c "Course Title" -r 720 --caption
```

or

```cli

    $ llvd -c "Course Title" -r 720 -ca
```

## Author

Igwaneza Bruce
