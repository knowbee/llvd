##### Table of Contents
- [Linkedin Learning Video Downloader (LLVD) download links](#llvd)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Windows Users](#windows)
- [Common questions](#common)
    - [How do I find the course slug?](#course-slug)
    - [Cookie-based authentication](#setup-cookie-based)
    - [Header-based authentication](#setup-header-based)
- [Examples](#examples)
    - [Accessing llvd documentation](#llvd-doc)
    - [Using cookie-based authentication](#use-cookie-based)
    - [Using header-based authentication](#use-header-based)
    - [Download a course at a specific resolution](#specific-res)
    - [Download a course with subtitles](#with-sub)
    - [Download a course path with throttling between 30 to 120 seconds](#course-path)
- [Screenshots](#screenshot)
- [Author](#author)

<a name="llvd"/>

# Linkedin Learning Video Downloader (LLVD) download links

[![Downloads](https://pepy.tech/badge/llvd)](https://pepy.tech/project/llvd)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)


<a name="features"/>

# Features
| Status | Feature                                 |
| :----- | :-------------------------------------- |
| ✅     | cookie-based authentication             |
| ✅     | download by learning path               |
| ✅     | download a course and all its exercises |
| ✅     | group videos by chapters                |
| ✅     | subtitles                               |
| ✅     | nice progress bar                       |
| ✅     | resume failed downloads                 |
| ✅     | skip already downloaded videos          |
| ✅     | set video format (360p, 540p, 720p)     |
| ✅     | all platforms                           |

<a name="prerequisites"/>

# Prerequisites
- [Python 3](https://www.python.org/downloads/)

<a name="installation"/>

# Installation
```cli
$ pip --no-cache-dir install llvd
```
If you have multiple versions of python installed in your system, use **pip3** instead.
<!-- TODO: can someone confirm this is how the install would look with pip3? -->
```cli
$ pip3 --no-cache-dir install llvd
```

### Running from local installation
```
llvd --help
llvd -c "course-slug" -r 720
```
### Running from docker container
```
# You will need to either use `docker cp` to get the course or mount it when running.
docker run ghcr.io/knowbee/llvd:master -c "course-slug" -r 720
```

<a name="windows"/>

## Windows Users

When you get `'llvd' is not recognized as an internal or external command` after successfully installing `llvd`, run `python3 -m llvd <flags>`

<a name="common"/>

# Common Questions

<a name="course-slug"/>

## How do I find the course slug?

1. Click on the desired course
2. Your URl will look something like, `https://www.linkedin.com/learning/l-essentiel-d-asp-dot-net-core-pour-dot-net-5`
    - The course slug is: `l-essentiel-d-asp-dot-net-core-pour-dot-net-5`

<a name="setup-cookie-based"/>

## How do I setup cookie-based authentication?

<!-- NOTE: I tried to get this to work and was having problems. The directions may not be accurate. -->

1.  Click on the options in Google Chrome (top right with 3 vertical dots).
2.  Click on `More tools` -> `Developer tools`
    - You can also reach here by using the keyboard combination: `ctrl`+`shift`+`I`).
3. Now once you’ve gained access to the developer tools, navigate to the Application tab, and copy the value of two cookies named `li_at` and `JSESSIONID`
4. Create a file named `cookies.txt` and place it in the folder you want to download your courses to
5. Open the `cookies.txt` file and paste in the values of `li_at` and `JSESSIONID`

```sh
li_at=xxxxx
JSESSIONID="ajax:xxxxxx"
```

<a name="setup-header-based"/>

## How do I setup header-based corporate account access?

If you have a corporate connected account you can fix the download issue by using a `headers.txt` as per below.

1. Create a file named `headers.txt` and place it in the folder you want to download your courses to
2.  Right click on the page and select view source
    - You can also reach here by using the keyboard combination: `ctrl`+`U`.
3. Search for `enterpriseProfileHash` using `ctrl`+`F`
4. `enterpriseProfileHash&quot;:&quot;XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&quot;,&quot;` copy the code between the double `&quot;`
<img src="https://raw.githubusercontent.com/bigmadkev/knowbee-hosting/master/assets/llvd_FindCodeInSourceCode.png" width="auto" height="auto"/>
5. Open the `headers.txt` file and paste in the values of `x-li-identity` from the above.

```sh
x-li-identity=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 
```

<a name="examples"/>

# Examples

<a name="llvd-doc"/>

### Accessing llvd documentation
```cli
$ llvd --help
```

<a name="use-cookie-based"/>

## Using cookie-based authentication

```cli
$ llvd -c "course-slug" --cookies
```

<a name="use-headers-based"/>

## Using header-based authentication
Has to use cookies in conjection with headers

```cli
$ llvd -c "course-slug" --cookies --headers
```

<a name="specific-res"/>

## Download a course at a specific resolution
```cli
$ llvd -c "course-slug" -r 720
```
Note: The default is set to 720.

<a name="with-sub"/>

## Download a course with subtitles

```cli

    $ llvd -c "course-slug" --caption
```

or

```cli

    $ llvd -c "course-slug" -ca
```

<a name="course-path"/>

## Download a course path with throttling between 10 to 30 seconds
To avoid rate limits because of downloading a lot of videos, use the following:

```cli
$ llvd -p "path-slug" -t 10,30
```


<a name="screenshot"/>

# Screenshots

<p>
    <img src="https://raw.githubusercontent.com/knowbee/hosting/master/assets/progress_llvd.png" width="auto" height="auto"/>
</p>

<a name="author"/>

# Author
Igwaneza Bruce
