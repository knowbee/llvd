import os
import re
import sys
import requests
import click
from bs4 import BeautifulSoup as bs
from requests import Session
from llvd import config
from llvd.downloader import download_video, download_exercises
from click_spinner import spinner
import re
from llvd.utils import write_subtitles, clean_name


class App:
    def __init__(self, email, password, course_slug, resolution, caption):

        self.email = email
        self.password = password
        self.course_slug = course_slug
        self.link = ""
        self.video_format = resolution
        self.caption = caption
        self.headers = {}
        self.cookies = {}

    def login(self, s, login_data):
        """
            Login the user
        """
        with spinner():

            s.post(
                config.signup_url, login_data)
            cookies = s.cookies.get_dict()
            self.cookies["JSESSIONID"] = cookies.get("JSESSIONID").replace(
                '\"', "")
            self.cookies["li_at"] = cookies.get("li_at")
            self.headers["Csrf-Token"] = cookies.get("JSESSIONID").replace(
                '\"', "")

            if cookies.get("li_at") == None:
                return None
            return 200

    def run(self, cookies=None):
        """
        Main function, tries to login the user and when it succeeds, tries to download the course
        """
        try:

            if cookies is not None:
                self.cookies["JSESSIONID"] = cookies.get("JSESSIONID")
                self.cookies["li_at"] = cookies.get("li_at")
                self.headers["Csrf-Token"] = cookies.get("JSESSIONID")
                self.download_entire_course()
            else:
                with Session() as s:
                    if not os.path.exists(f'{self.course_slug}'):
                        os.makedirs(f'{self.course_slug}')
                    site = s.get(config.login_url)
                    bs_content = bs(site.content, "html.parser")

                    csrf = bs_content.find(
                        'input', {'name': 'csrfToken'}).get("value")
                    loginCsrfParam = bs_content.find(
                        "input", {"name": "loginCsrfParam"}).get("value")
                    login_data = {"session_key": self.email, "session_password": self.password,
                                  "csrfToken": csrf, "loginCsrfParam": loginCsrfParam}

                    status = self.login(s, login_data)

                    if status is None:
                        print("\n")
                        click.echo(
                            click.style(f"Wrong credentials, try again", fg="red"))
                        sys.exit(0)
                    else:
                        self.download_entire_course()

        except requests.exceptions.ConnectionError:
            print("\n")
            click.echo(click.style(
                f"Failed to connect", fg="red"))

    @staticmethod
    def resume_failed_ownloads():
        """
            Resume failed downloads
        """
        current_files = [file for file in os.listdir() if ".mp4" in file]
        if len(current_files) > 0:
            for file in current_files:
                if os.stat(file).st_size == 0:
                    os.remove(file)
            print("\n")
            click.echo(click.style(f"Resuming download..", fg="red"))

    def download_entire_course(self):
        """
            Download a course
        """
        self.resume_failed_ownloads()
        print("\n")
        try:
            r = requests.get(config.course_url.format(
                self.course_slug), cookies=self.cookies, headers=self.headers)
            course_name = r.json()['elements'][0]['title']
            course_name = re.sub(r'[\\/*?:"<>|]', "", course_name)
            chapters = r.json()['elements'][0]['chapters']
            exercise_files = r.json()["elements"][0]["exerciseFileUrls"]
            count = 1

            for chapter in chapters:
                chapter_name = chapter["title"]
                videos = chapter["videos"]
                if not os.path.exists(f'{self.course_slug}/{clean_name(chapter_name)}'):
                    os.makedirs(
                        f'{self.course_slug}/{clean_name(chapter_name)}')
                for video in videos:

                    video_name = re.sub(r'[\\/*?:"<>|]', "",
                                        video['title'])
                    video_slug = video['slug']
                    video_url = config.video_url.format(
                        self.course_slug, self.video_format, video_slug)
                    page_data = requests.get(
                        video_url, cookies=self.cookies, headers=self.headers)
                    page_json = page_data.json()
                    try:
                        download_url = page_json['elements'][0]['selectedVideo']['url']['progressiveUrl']
                        try:
                            subtitles = page_json['elements'][0]['selectedVideo']['transcript']
                        except:
                            click.echo(click.style(
                                f"Subtitles not found", fg="red"))
                            subtitles = None
                        duration_in_ms = int(page_json['elements'][0]
                                             ['selectedVideo']['durationInSeconds']) * 1000

                        click.echo(
                            click.style(f"current: {count}", fg="red"))
                        click.echo(
                            click.style(f"format: {self.video_format}p", fg="red"))
                        current_files = []
                        for file in os.listdir(f"./{self.course_slug}/{clean_name(chapter_name)}"):
                            if file.endswith(".mp4") and "-" in file:
                                ff = re.split(
                                    "\d+-", file)[1].replace(".mp4", "")
                                current_files.append(ff)
                    except Exception as e:
                        if 'url' in str(e):
                            click.echo(
                                click.style(f"This video is locked, you probably need a premium account", fg="red"))
                        else:
                            click.echo(
                                click.style(f"Failed to download this video", fg="red"))
                    else:
                        if clean_name(video_name) not in current_files:
                            if subtitles is not None and self.caption:
                                click.echo(click.style(
                                    f"Fetching subtitles..", fg="green"))
                                subtitle_lines = subtitles['lines']
                                write_subtitles(
                                    count, subtitle_lines, video_name, self.course_slug, chapter_name, duration_in_ms)
                            download_video(download_url, count,
                                           video_name, chapter_name, self.course_slug)
                        else:
                            click.echo(
                                click.style(f"skipping: " +
                                            video_name + "\n", fg="green"))
                        count += 1
            if len(exercise_files) > 0:
                download_exercises(exercise_files, self.course_slug)
            print("\n" + "Finished, start learning! :)")

        except Exception as e:
            print(e)
            click.echo(
                click.style("Failed to connect, try again later", fg="red"))
