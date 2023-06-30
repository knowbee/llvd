import os
import re
import sys
import requests
import click
import json
from bs4 import BeautifulSoup as bs
from requests import Session
from llvd import config
from llvd.exceptions import EmptyCourseList
from llvd.downloader import download_subtitles, download_video, download_exercises
from click_spinner import spinner
import re
from llvd.utils import clean_name
import click
import sys
from llvd import config
import subprocess
class App:
    def __init__(
        self, email, password, course_slug, resolution, caption, exercise, throttle
    ):
        self.email = email
        self.password = password
        self.course_slug = course_slug[0]
        self.course_type = course_slug[1]
        self.link = ""
        self.video_format = resolution
        self.caption = caption
        self.exercise = exercise
        self.cookies = {}
        self.headers = {}
        self.chapter_path = ""
        self.current_video_index = None
        self.current_chapter_index = None
        self.current_video_name = ""
        self.throttle = throttle

    def login(self, session, login_data):

        try:
            with spinner():

                session.post(config.signup_url, login_data)
                cookies = session.cookies.get_dict()
                self.cookies["JSESSIONID"] = cookies.get("JSESSIONID").replace('"', "")
                self.cookies["li_at"] = cookies.get("li_at")
                self.headers["Csrf-Token"] = cookies.get("JSESSIONID").replace('"', "")

                if cookies.get("li_at") == None:
                    return None
                return 200

        except ConnectionResetError:
            click.echo(
                click.style(
                    f"ConnectionResetError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )

        except requests.exceptions.ConnectionError:
            click.echo(
                click.style(
                    f"ConnectionError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )

    def run(self, cookies=None):
        """
        Main function, tries to login the user and when it succeeds, tries to download the course
        """
        try:

            if cookies is not None:
                self.cookies["JSESSIONID"] = cookies.get("JSESSIONID")
                self.cookies["li_at"] = cookies.get("li_at")
                self.headers["Csrf-Token"] = cookies.get("JSESSIONID")
                
                # remove empty files
                command = 'find . -depth -type f -size 0 -exec rm {} +'
                subprocess.run(command, shell=True)

                # proceed to download
                self.download()
            else:
                with Session() as session:
                    site = session.get(config.login_url)
                    bs_content = bs(site.content, "html.parser")

                    csrf = bs_content.find("input", {"name": "csrfToken"}).get("value")
                    loginCsrfParam = bs_content.find(
                        "input", {"name": "loginCsrfParam"}
                    ).get("value")
                    login_data = {
                        "session_key": self.email,
                        "session_password": self.password,
                        "csrfToken": csrf,
                        "loginCsrfParam": loginCsrfParam,
                    }

                    status = self.login(session, login_data)

                    if status is None:
                        click.echo(
                            click.style(f"Wrong credentials, try again", fg="red")
                        )
                        sys.exit(0)
                    else:
                        self.create_course_dirs(self.course_slug)
                        self.download()

        except ConnectionError:
            click.echo(click.style(f"ConnectionError: Failed to connect", fg="red"))

    @staticmethod
    def create_course_dirs(course_slug):
        """
        Create file system path for courses
        """
        if not os.path.exists(f"{course_slug}"):
            os.makedirs(f"{course_slug}")

    @staticmethod
    def remove_failed_downloads():
        """Remove failed downloads."""

    failed_files = [
        file for file in os.listdir() if ".mp4" in file and os.stat(file).st_size == 0
    ]
    if failed_files:
        for file in failed_files:
            os.remove(file)
        click.echo(click.style("Resuming download..", fg="red"))

    def download(self):
        """
        Determines whether to download from learning path
        or from a course directly.
        """
        PATH = "path"
        try:
            if self.course_type == PATH:
                self.download_courses_from_path()
            else:
                self.download_entire_course()
        except TypeError as e:
            print("retrying...")
            self.download_entire_course()
            # click.echo(
            #     click.style(
            #         f"TypeError: {e}\n",
            #         fg="red",
            #     )
            # )

        except ConnectionResetError:
            click.echo(
                click.style(
                    f"ConnectionResetError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )

        except requests.exceptions.ConnectionError:
            click.echo(
                click.style(
                    f"ConnectionError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )

    def download_courses_from_path(self):

        try:
            page_url = config.path_url.format(self.course_slug)
            page = requests.get(page_url)
            soup = bs(page.content, "html.parser")
            course_list = soup.select('script[type="application/ld+json"]')

            if not course_list:
                raise EmptyCourseList
            else:
                course_list = course_list[0]

            course_list = json.loads(course_list.string.replace("\n", ""))
            total_courses = len(course_list["itemListElement"])
            click.echo(
                f"Downloading {total_courses} courses from learning-path: {self.course_slug}\n"
            )

            for index, course in enumerate(course_list["itemListElement"]):
                course_token = course["item"]["url"].split("/")[-1]
                suppress = index + 1 != total_courses
                click.echo(
                    f"\nDownloading course {index+1}/{total_courses}: {course_token}"
                )
                self.course_slug = course_token
                self.create_course_dirs(course_token)
                self.download_entire_course(skip_done_alert=suppress)

        except EmptyCourseList as e:
            click.echo(click.style(f"EmptyCourseList: Error parsing learning path.\n{e}", fg="red"))

        except Exception as e:
            click.echo(
                click.style(
                    f"Error fetching courses from learning path!\n{e}", fg="red"
                )
            )

    def fetch_video(self, video):
        video_name = re.sub(r'[\\/*?:"<>|]', "", video["title"])
        self.current_video_name = video_name
        video_slug = video["slug"]
        video_url = config.video_url.format(
            self.course_slug, self.video_format, video_slug
        )
        page_data = requests.get(
            video_url,
            cookies=self.cookies,
            headers=self.headers,
            allow_redirects=False,
        )
        page_json = page_data.json()
        return page_json, video_name

    def fetch_chapter(self, chapter, chapters_pad_length, delay):

        chapter_name = chapter["title"]
        videos = chapter["videos"]
        chapters_index_padded = str(self.current_chapter_index).rjust(
            chapters_pad_length, "0"
        )
        chapter_path = (
            f"./{self.course_slug}/{chapters_index_padded}. {clean_name(chapter_name)}"
        )
        video_index = 1
        self.chapter_path = (
            f"./{self.course_slug}/{chapters_index_padded}. {clean_name(chapter_name)}"
        )
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)

        current_files = []
        for file in os.listdir(chapter_path):
            if file.endswith(".mp4") and ". " in file:
                ff = re.split("\d+\. ", file)[1].replace(".mp4", "")
                current_files.append(ff)

        # unique videos by checking if the video name is in the current files
        videos = [video for video in videos if clean_name(video["title"]) not in current_files]

        for video in videos:
            self.current_video_index = video_index + len(current_files)
            page_json, video_name = self.fetch_video(video)

            try:
                download_url = page_json["elements"][0]["selectedVideo"]["url"][
                    "progressiveUrl"
                ]
                try:
                    subtitles = page_json["elements"][0]["selectedVideo"]["transcript"]
                except:
                    click.echo(click.style(f"Subtitles not found", fg="red"))
                    subtitles = None
                duration_in_ms = (
                    int(page_json["elements"][0]["selectedVideo"]["durationInSeconds"])
                    * 1000
                )

                click.echo(
                    click.style(
                        f"\nCurrent: {chapters_index_padded}. {clean_name(chapter_name)}/"
                        f"{video_index + len(current_files):0=2d}. {video_name}.mp4 @{self.video_format}p"
                    )
                )
            except Exception as e:
                if "url" in str(e):
                    click.echo(
                        click.style(
                            f"This video is locked, you probably "
                            f"need a premium account",
                            fg="red",
                        )
                    )
                else:
                    click.echo(
                        click.style(f"Failed to download {video_name}", fg="red")
                    )
            finally:
                download_video(
                    download_url,
                    self.current_video_index,
                    video_name,
                    chapter_path,
                    delay,
                )
                if subtitles is not None and self.caption:
                    subtitle_lines = subtitles["lines"]
                    download_subtitles(
                        self.current_video_index,
                        subtitle_lines,
                        video_name,
                        chapter_path,
                        duration_in_ms,
                    )
            video_index += 1

    def download_entire_course(self, *args, **kwargs):

        self.remove_failed_downloads()
        try:
            r = requests.get(
                config.course_url.format(self.course_slug),
                cookies=self.cookies,
                headers=self.headers,
                allow_redirects=False,
            )
            course_name = r.json()["elements"][0]["title"]
            course_name = re.sub(r'[\\/*?:"<>|]', "", course_name)
            course_path = f"./{self.course_slug}"
            chapters = r.json()["elements"][0]["chapters"]
            exercise_files = r.json()["elements"][0]["exerciseFileUrls"]
            chapters_index = 1
            if len(chapters) > 0 and chapters[0]["title"] in [
                "Introduction",
                "Welcome",
            ]:
                chapters_index = 0
            chapters_pad_length = 1
            if chapters_index == 0:
                if len(chapters) - 1 > 9:
                    chapters_pad_length = 2
            else:
                if len(chapters) > 9:
                    chapters_pad_length = 2
            delay = self.throttle

            for chapter in chapters:

                self.current_chapter_index = chapters_index
                self.fetch_chapter(chapter, chapters_pad_length, delay)
                chapters_index += 1

            if self.exercise and len(exercise_files) > 0:
                download_exercises(exercise_files, course_path)

            if kwargs.get("skip_done_alert"):
                return
            click.echo(
                "\nYour download is complete. Begin your learning journey now.! :)"
            )

        except requests.exceptions.TooManyRedirects:
            click.echo(click.style(f"TooManyRedirects: Your cookie is expired", fg="red"))
        except KeyError as e:
            click.echo(click.style(f"KeyError: That course is not found {e}", fg="red"))

        except ConnectionResetError:
            click.echo(
                click.style(
                    f"ConnectionResetError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )

        except requests.exceptions.ConnectionError:
            click.echo(
                click.style(
                    f"ConnectionError: There is a connection error. Please check your connectivity.\n",
                    fg="red",
                )
            )
        except Exception as e:
            if os.path.exists(
                f"{self.chapter_path}/{self.current_video_index:0=2d}. {clean_name(self.current_video_name)}.mp4"
            ):
                os.remove(
                    f"{self.chapter_path}/{self.current_video_index:0=2d}. {clean_name(self.current_video_name)}.mp4"
                )
            self.download_entire_course()
