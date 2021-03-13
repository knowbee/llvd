# !/usr/bin/env  python3

import click
import sys
import re
from llvd.app import App
from llvd import config
from llvd.process_io import parse_cookie_file
BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red


@click.command()
@click.option('--cookies', is_flag=True,
              prompt='Do you want to login with cookies?')
@click.option("--resolution", "-r",
              default='720',
              help='Video resolution can either be 360, 540 or 720. 720 is the default')
@click.option("--caption", "-ca",
              is_flag=True,
              help="Download subtitles")
@click.option("--course", "-c", help="Example: 'Java 8 Essential'")
def main(cookies, course, resolution, caption):
    """
    Linkedin learning video downloader cli tool

    example: llvd --course "Java 8 Essential"
    """
    if len(sys.argv) == 1:
        click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
        sys.exit(0)

    course = re.sub("[)|(|,]|(-&)", "", course.lower())

    course_slug = course.replace(" ", "-").replace(":-", "-").replace(
        "-&", ""
    ).replace(".", "-")

    if cookies:
        cookie_dict = parse_cookie_file()
        email = ""
        password = ""
        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run(cookie_dict)
    else:
        email = click.prompt("Please enter your Linkedin email address")
        password = click.prompt(
            "Enter your Linkedin Password", hide_input=True)

        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run()
