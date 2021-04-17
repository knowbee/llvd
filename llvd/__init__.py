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
              prompt='Do you want to login with cookies?',
              help="Authenticate with cookies by following the guidelines provided in the documentation")
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

    course = course.lower().replace("c#", "c-sharp").replace(".net", "dot-net")
    without_chars = re.sub(r'[\':)(,>.’/]', " ", course.strip()).replace("«", " ").replace("-»", " ").replace("»", " ").strip()
    course_slug= re.sub(r'(\s+)', "-", without_chars.lower())
    email = ""
    password = ""
    if cookies:
        cookie_dict = parse_cookie_file()
        if "li_at" not in cookie_dict or "JSESSIONID" not in cookie_dict:
            click.echo(
                click.style(f"cookies.txt must not be empty", fg="red"))
            sys.exit(0)

        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run(cookie_dict)
    else:
        email = click.prompt("Please enter your Linkedin email address")
        password = click.prompt(
            "Enter your Linkedin Password", hide_input=True)

        llvd = App(email, password, course_slug, resolution, caption)
        llvd.run()
