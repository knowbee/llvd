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
@ click.option('--course', '-c', help='llvd --help')
def main(course):
    """
    Linkedin learning video downloader cli tool\n
    example: llvd --course "Java 8 Essential"\n
    Remember to set login credentials in the config file
    """
    if(len(sys.argv) == 1):
        print("missing required arguments: run llvd --help")
        sys.exit(0)

    course = re.sub('[)|(|,]|(-&)', '', course.lower())

    link = config.main_url + str(course).replace(" ", "-").replace(":-",
                                                                   "-").replace("-&", "").replace(".", "-")
    if(config.email == "" or config.password == ""):
        print("missing credentials llvd --help")
        sys.exit(0)
    try:
        browser = create_browser()
    except WebDriverException:
        print("chromedriver is missing")
        sys.exit(0)
    llvd = App(browser, config.email, config.password, link)
    llvd.run()


if __name__ == '__main__':
    main()
