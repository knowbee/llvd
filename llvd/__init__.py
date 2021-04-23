# !/usr/bin/env  python3

import click
import sys
import re
from llvd.app import App
from llvd import config
from llvd.process_io import parse_cookie_file
from llvd.utils import clean_dir


BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red


@click.command()
@click.option('--cookies', is_flag=True,
              help="Authenticate with cookies by following the guidelines provided in the documentation")
@click.option("--resolution", "-r",
              default='720',
              help='Video resolution can either be 360, 540 or 720. 720 is the default')
@click.option("--caption", "-ca",
              is_flag=True,
              help="Download subtitles")
@click.option("--course", "-c", help="Example: 'java-8-essential'")
def main(cookies, course, resolution, caption):
    """
    Linkedin learning video downloader cli tool

    example: llvd --course "java-8-essential"
    """
    if len(sys.argv) == 1:
        click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
        sys.exit(0)

    course_slug = clean_dir(course)

    email = config.email
    password = config.password

    if cookies:
        cookie_dict = parse_cookie_file()
        if "li_at" not in cookie_dict or "JSESSIONID" not in cookie_dict:
            click.echo(
                click.style(f"cookies.txt must not be empty", fg="red"))
            sys.exit(0)
        else:
            click.echo(
                click.style(f"Using cookie info from cookies.txt", fg="green"))

        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run(cookie_dict)
    else:
        if email == "":
            email = click.prompt("Please enter your Linkedin email address")
        if password == "":
            password = click.prompt(
                "Enter your Linkedin Password", hide_input=True)

        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run()
