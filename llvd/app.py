import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import requests
import click

from llvd import config
from llvd.downloader import download
from click_spinner import spinner


class App:
    def __init__(self, browser, email, password, course_slug):

        self.browser = browser
        self.email = email
        self.password = password
        self.course_slug = course_slug
        self.link = ""
        self.video_format = "360p"
        self.headers = {}
        self.cookies = {}

    def run(self):
        try:
            self.browser.get(config.login_url)
            WebDriverWait(self.browser, 4).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "text-input__input"))
            )
            email_field = self.browser.find_element_by_class_name(
                "text-input__input")
            email_field.send_keys(self.email)
            self.browser.find_element_by_class_name(
                "signin__button-v3").click()

            WebDriverWait(self.browser, 4).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "mercado-text_input--round")
                )
            )

            time.sleep(2)

            password_field = self.browser.find_element_by_class_name(
                "mercado-text_input--round"
            )
            password_field.send_keys(self.password)
            with spinner():
                self.browser.find_element_by_class_name(
                    "btn__primary--large").click()
                WebDriverWait(self.browser, 6).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "ember-application"))
                )
                print("\nPutting things together...")
            cookies_list = self.browser.get_cookies()

            for cookie in cookies_list:
                if(cookie["name"] == "li_at"):
                    self.cookies["li_at"] = cookie["value"]
                if(cookie["name"] == "JSESSIONID"):
                    self.cookies["JSESSIONID"] = cookie["value"].replace(
                        '\"', "")
                    self.headers["Csrf-Token"] = cookie["value"].replace(
                        '\"', "")
            self.browser.quit()
            self.crawl()
        except Exception:
            print("\nPlease try again and make sure your credentials are right")
            print("\n")
            print("llvd --help")
            self.browser.quit()

    @staticmethod
    def resumeFailedDownloads():
        current_files = [file for file in os.listdir() if ".mp4" in file]
        if len(current_files) > 0:
            for file in current_files:
                if os.stat(file).st_size == 0:
                    os.remove(file)
            print("resuming download.." + "\n")

    def crawl(self):
        self.resumeFailedDownloads()
        print("Sit back and drink your coffee :)")
        try:
            r = requests.get(config.course_url.format(
                self.course_slug), cookies=self.cookies, headers=self.headers)
            course_name = r.json()['elements'][0]['title']
            course_name = re.sub(r'[\\/*?:"<>|]', "", course_name)
            chapters = r.json()['elements'][0]['chapters']

            c = 1
            for chapter in chapters:
                chapter_name = chapter["title"]
                videos = chapter["videos"]
                for video in videos:

                    video_name = re.sub(r'[\\/*?:"<>|]', "",
                                        video['title'])
                    video_slug = video['slug']
                    video_url = config.video_url.format(
                        self.course_slug, video_slug)
                    req = requests.get(
                        video_url, cookies=self.cookies, headers=self.headers)
                    try:
                        download_url = re.search(
                            '"progressiveUrl":"(.+)"', req.text).group(1).split('","expiresAt')[0]
                        click.echo(
                            click.style(f"current: {c}", fg="red"))
                        click.echo(
                            click.style(f"format: {self.video_format}", fg="red"))
                        current_files = [file.split("-")[1].replace(".mp4", "")
                                         for file in os.listdir() if "-" in file]
                        if video_name not in current_files:
                            download(download_url, c, video_name)
                        else:
                            click.echo(
                                click.style(f"skipping: " +
                                            video_name + "\n", fg="green"))
                        c += 1
                    except Exception:
                        print("network error...try again")
            print("\n" + "Finished, start learning! :)")

        except Exception:
            print("network error...try again")
