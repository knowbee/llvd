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


class App:
    def __init__(self, email, password, course_slug, resolution):

        self.email = email
        self.password = password
        self.course_slug = course_slug
        self.link = ""
        self.video_format = resolution
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

    def run(self):
        """
        Main function, tries to login the user and when it succeeds, tries to download the course
        """
        try:
            with Session() as s:
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
                f"You don't have internet connection", fg="red"))

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
            c = 1

            for chapter in chapters:
                chapter_name = chapter["title"]
                videos = chapter["videos"]
                for video in videos:

                    video_name = re.sub(r'[\\/*?:"<>|]', "",
                                        video['title'])
                    video_slug = video['slug']
                    video_url = config.video_url.format(
                        self.course_slug, self.video_format, video_slug)
                    req = requests.get(
                        video_url, cookies=self.cookies, headers=self.headers)
                    try:
                        download_url = re.search(
                            '"progressiveUrl":"(.+)"', req.text).group(1).split('","expiresAt')[0]
                        click.echo(
                            click.style(f"current: {c}", fg="red"))
                        click.echo(
                            click.style(f"format: {self.video_format}p", fg="red"))
                        current_files = [re.split("\d+-", file)[1].replace(".mp4", "")
                                         for file in os.listdir() if "-" in file]
                    except Exception:
                        click.echo(
                            click.style(f"You probably need a premium account, or your internet is too slow to download this video", fg="red"))
                    else:
                        if video_name not in current_files:
                            download_video(download_url, c, video_name)
                        else:
                            click.echo(
                                click.style(f"skipping: " +
                                            video_name + "\n", fg="green"))
                        c += 1
            if len(exercise_files) > 0:
                download_exercises(exercise_files)
            print("\n" + "Finished, start learning! :)")

        except Exception:
            click.echo(
                click.style("You must have a premium account to download this course", fg="red"))
