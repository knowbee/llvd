# !/usr/bin/env  python3

import click
import sys
import re
from llvd.app import App
from llvd import config

BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red


@click.command()
@click.option("--course", "-c", help="llvd --help")
def main(course):
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
    email = click.prompt("Please enter your Linkedin email address")
    password = click.prompt("Enter your Linkedin Password", hide_input=True)

    llvd = App(email, password, course_slug)
    llvd.run()
