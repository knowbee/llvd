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
from lib.app import App

"""
create browser instance
"""


def create_browser():
    threadLocal = threading.local()
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


@ click.command()
@ click.option('--link', '-l', help='llvd --help')
@ click.option('--email', '-e', help='llvd --help')
@ click.option('--password', '-p', help='llvd --help')
def main(link, email, password):
    """
    Linkedin learning video downloader cli tool\n
    example: llvd --email test@gmail.com --password Test@123 --link https://www.linkedin.com/learning/java-8-essential
    """
    if(len(sys.argv) == 1):
        print("missing required arguments: run llvd --help")
        sys.exit(0)
    try:
        browser = create_browser()
    except WebDriverException:
        print("chromedriver is missing")
        sys.exit(0)
    llvd = App(browser, email, password, link)
    llvd.run()


if __name__ == '__main__':
    main()
