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
| ✅     | cookie-based authentication             |
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
    $ llvd -c "course-slug" -r 720

```

## How to find the course slug ?

- Click on the course
- Copy the slug next to learning in the URL `https://www.linkedin.com/learning/l-essentiel-d-asp-dot-net-core-pour-dot-net-5`, in this example the course slug is `l-essentiel-d-asp-dot-net-core-pour-dot-net-5`

## Cookie-based authentication

- 1.  Click on the options in the google chrome (top right with 3 vertical dots).
- 2.  After this, click on more tools followed by Developer Tools (you can also reach here by using the keyboard combination — ctrl+shift+I).

- 3.  Now once you’ve gained access to the developer tools, navigate to the Application tab, and copy the value of two cookies from there named li_at and JSESSIONID respectively.

- 3.  create a cookies.txt file to a place you want to download your courses then paste in the values of li_at and JSESSIONID as shown below.

#### Example (`cookies.txt`)

```sh
li_at=xxxxx
JSESSIONID="ajax:xxxxxx"
```

```cli

    $ llvd --help
    $ llvd -c "course-slug" -r 720 --cookies

```

### Download the course with subtitles

Use the `--caption` flag to download videos with subtitles

```cli

    $ llvd -c "course-slug" -r 720 --caption
```

or

```cli

    $ llvd -c "course-slug" -r 720 -ca
```

## Author

Igwaneza Bruce
