##!/usr/bin/env  python3

import click
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import threading
import time
import config
import re
from core.app import App
from click_spinner import spinner

BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red

"""
create browser instance
"""


def create_browser():
    threadLocal = threading.local()
    browser = getattr(threadLocal, "browser", None)
    if browser is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        browser = webdriver.Chrome(options=options, service_log_path=None)
        browser.delete_all_cookies()
        setattr(threadLocal, "browser", browser)
        return browser


@click.command()
@click.option("--course", "-c", help="llvd --help")
def main(course):
    """
    Linkedin learning video downloader cli tool
    example: llvd --course "Java 8 Essential"
    Remember to set login credentials in the config file
    """
    if len(sys.argv) == 1:
        click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
        sys.exit(0)

    course = re.sub("[)|(|,]|(-&)", "", course.lower())

    link = config.main_url + str(course).replace(" ", "-").replace(":-", "-").replace(
        "-&", ""
    ).replace(".", "-")
    email = click.prompt("Please enter your linkedin email address")
    password = click.prompt("Enter your Linkedin Password: ", hide_input=True)
    try:
        browser = create_browser()
    except WebDriverException:
        click.echo(f"{RED_COLOR}{BOLD}Please install chromedriver")
        sys.exit(0)
    with spinner():
        llvd = App(browser, email, password, link)
        llvd.run()
