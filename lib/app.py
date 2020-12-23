import requests
import click
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time
from .downloader import download


class App():

    def __init__(self, browser, email, password, link):

        self.browser = browser
        self.email = email
        self.password = password
        self.link = link

    def run(self):
        try:
            url = "https://www.linkedin.com/learning-login/?upsellOrderOrigin=default_guest_learning&fromSignIn=true&trk=homepage-learning_nav-header-signin"
            self.browser.get(url)
            print("Connecting...")
            WebDriverWait(self.browser, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-input__input")))
            email_field = self.browser.find_element_by_class_name(
                "text-input__input")
            email_field.send_keys(self.email)
            self.browser.find_element_by_class_name(
                "signin__button-v3").click()

            WebDriverWait(self.browser, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mercado-text_input--round")))

            time.sleep(2)

            password_field = self.browser.find_element_by_class_name(
                "mercado-text_input--round")
            password_field.send_keys(self.password)
            self.browser.find_element_by_class_name(
                "btn__primary--large").click()

            WebDriverWait(self.browser, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ember-application")))
            print("Putting things together...")
            self.crawl(self.link)
        except Exception:
            print("Please try again and make sure your credentials are right")
            print("\n")
            print("llvd --help")
            self.browser.quit()

    def crawl(self, link):
        self.browser.get(
            link)
        print("Sit back and drink your coffee :)")
        course_links = self.browser.find_elements_by_class_name(
            "classroom-toc-item__link")
        all_courses = [lesson.get_attribute("href") for lesson in course_links]
        for course in all_courses:
            self.browser.get(course)
            try:
                WebDriverWait(self.browser, 4).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech")))
                playing_video = self.browser.find_element_by_class_name(
                    "vjs-tech")
                video_link = playing_video.get_attribute("src")
                video_title = self.browser.find_element_by_class_name(
                    "classroom-nav__details").text
                download(video_link.replace("#mp4", ""), video_title)

            except Exception:
                pass
        print("\n" + "Finished, start learning! :)")