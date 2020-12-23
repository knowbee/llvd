
#!/usr/bin/env python3
"""
Author:Igwaneza Bruce
Email:knowbeeinc@gmail.com
"""


import requests
import click
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
import time
threadLocal = threading.local()


def download(url, filename):
    print("downloading " + filename + "\n")
    with open(f"{filename}.mp4", 'wb') as f:
        try:
            response = requests.get(
                url, stream=True)
            total = response.headers.get('content-length')
            if total is None:
                print("video not found")
                return
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(
                        chunk_size=max((int(total) / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('o' * done,
                                                       '.' * (50 - done)))
                    sys.stdout.flush()
        except Exception:
            print("network error...try again")


@click.command()
@click.option('--link', '-l', help='llvd --help')
@click.option('--email', '-e', help='llvd --help')
@click.option('--password', '-p', help='llvd --help')
def llvd(link, email, password):
    """
    Linkedin learning video downloader cli tool\n
    example: llvd --email test@gmail.com --password Test@123 --link https://www.linkedin.com/learning/java-8-essential
    """
    if(len(sys.argv) == 1):
        print("missing required arguments: run llvd --help")
        sys.exit(0)
    login(link, email, password)


"""
Initialize browser
"""


def create_browser():
    browser = getattr(threadLocal, 'browser', None)
    if browser is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        browser = webdriver.Chrome(options=options, service_log_path=None)
        browser.delete_all_cookies()
        setattr(threadLocal, 'browser', browser)
    return browser


browser = create_browser()

"""
Authenticate
"""


def login(link, email, password):
    try:
        url = "https://www.linkedin.com/learning-login/?upsellOrderOrigin=default_guest_learning&fromSignIn=true&trk=homepage-learning_nav-header-signin"
        browser.get(url)
        WebDriverWait(browser, 4).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-input__input")))
        email_field = browser.find_element_by_class_name("text-input__input")
        email_field.send_keys(email)
        browser.find_element_by_class_name("signin__button-v3").click()

        WebDriverWait(browser, 4).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mercado-text_input--round")))

        time.sleep(2)

        password_field = browser.find_element_by_class_name(
            "mercado-text_input--round")
        password_field.send_keys(password)
        browser.find_element_by_class_name("btn__primary--large").click()

        WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ember-application")))

        print("You are successfully authenticated")
        print("\n")
        print("Now sit back and drink your coffee :)")
        main(link)
    except Exception:
        print("Please try again and make sure your credentials are right")
        print("\n")
        print("llvd --help")
        browser.quit()


"""
Main application
"""


def main(link):
    browser.get(
        link)
    time.sleep(2)
    course_links = browser.find_elements_by_class_name(
        "classroom-toc-item__link")
    # current_lesson = course_links[0]
    all_courses = []
    for lesson in course_links:
        course_link = lesson.get_attribute("href")
        all_courses.append(course_link)
    for course in all_courses:
        browser.get(course)
        try:
            WebDriverWait(browser, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech")))
            playing_video = browser.find_element_by_class_name("vjs-tech")
            video_link = playing_video.get_attribute("src")
            video_title = browser.find_element_by_class_name(
                "classroom-nav__details").text
            # download(video_link.replace("#mp4", ""), video_title)
            print(video_link, video_title)
        except Exception:
            pass


if __name__ == '__main__':
    llvd()
