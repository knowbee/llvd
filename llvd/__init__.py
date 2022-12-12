# !/usr/bin/env  python3

import click
import sys
from llvd.app import App
from llvd import config
from llvd.process_io import parse_cookie_file
from llvd.utils import clean_dir


BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red
PATH = "path"
COURSE = "course"


@click.command()
@click.option(
    "--cookies",
    is_flag=True,
    help="Authenticate with cookies by following the guidelines provided in the documentation",
)
@click.option(
    "--resolution",
    "-r",
    default="720",
    help="Video resolution can either be 360, 540 or 720. 720 is the default",
)
@click.option("--caption", "-ca", is_flag=True, help="Download subtitles")
@click.option("--exercise", "-e", is_flag=True, help="Download Excercises")
@click.option("--course", "-c", help="Example: 'java-8-essential'")
@click.option(
    "--path",
    "-p",
    help="Specify learning path to download. Example: 'llvd -p become-a-php-developer -t 20'",
)
@click.option(
    "--throttle",
    "-t",
    help="A min,max wait in seconds before downloading next video. Example: -t 30,120",
)
def main(cookies, course, resolution, caption, exercise, path, throttle):
    """
    Linkedin learning video downloader cli tool
    example: llvd --course "java-8-essential"
    """
    if len(sys.argv) == 1:
        click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
        sys.exit(0)

    if path:
        course_slug = (clean_dir(path), PATH)
    else:
        course_slug = (clean_dir(course), COURSE)

    email = config.email
    password = config.password

    try:
        if throttle and "," in throttle:
            throttle = [int(i) for i in throttle.split(",")]
        elif throttle != None:
            throttle = [int(throttle)]
    except ValueError:
        click.echo(click.style("Throttle must be a number", fg="red"))
        sys.exit(0)

    # Check that both course and path are not both set. Can only be one or other.
    if course and path:
        click.echo(
            click.style(
                "Please specify either a course OR learning path, not both.", fg="red"
            )
        )
        sys.exit(0)

    if path and not throttle:
        click.echo(
            click.style(
                "Please use throttle option (-t) when downloading learning paths.",
                fg="red",
            )
        )
        sys.exit(0)

    if cookies:
        cookie_dict = parse_cookie_file()
        if "li_at" not in cookie_dict or "JSESSIONID" not in cookie_dict:
            click.echo(click.style(f"cookies.txt must not be empty", fg="red"))
            sys.exit(0)
        else:
            click.echo(click.style(f"Using cookie info from cookies.txt", fg="green"))

        llvd = App(
            email, password, course_slug, resolution, caption, exercise, throttle
        )
        llvd.run(cookie_dict)
    else:
        if email == "":
            email = click.prompt("Please enter your Linkedin email address")
        if password == "":
            password = click.prompt("Enter your Linkedin Password", hide_input=True)

        llvd = App(
            email, password, course_slug, resolution, caption, exercise, throttle
        )
        llvd.run()
