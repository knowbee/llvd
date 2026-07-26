import sys
import click
from llvd import config
from llvd.app import App
from llvd.process_io import parse_cookie_file, parse_header_file
from llvd.utils import clean_dir
from llvd.logger import logger
from llvd.exceptions import FileAccessError, ParsingError, ConfigurationError


BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red
PATH = "path"
COURSE = "course"


@click.command()
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Display the current version of the application",
)
@click.option(
    "--cookies",
    is_flag=True,
    help="Authenticate with cookies by following the guidelines provided in the documentation",
)
@click.option(
    "--headers",
    is_flag=True,
    help="Change request headers",
)
@click.option(
    "--resolution",
    "-r",
    default="720",
    help="Video resolution can either be 360, 540 or 720. 720 is the default",
)
@click.option("--caption", "-ca", is_flag=True, help="Download subtitles")
@click.option("--exercise", "-e", is_flag=True, help="Download Exercises")
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
def main(version, cookies, headers, course, resolution, caption, exercise, path, throttle):
    """
    Linkedin learning video downloader cli tool
    example: llvd --course "java-8-essential"
    """
    try:
        logger.info("Starting LLVD")
        
        if not len(sys.argv) != 1:
            logger.warning("Missing required arguments")
            click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
            return
        
        if version:
            from llvd import __version__
            logger.info(f"Displaying version: {__version__}")
            click.echo(f"{BOLD}Version: {__version__}")
            return
            
        # Validate course or path is provided
        if not course and not path:
            logger.error("No course or path specified")
            click.echo(click.style("Please specify either a course or a learning path", fg="red"))
            return
            
        if path:
            logger.info(f"Using learning path: {path}")
            course_slug = (clean_dir(path), PATH)
        else:
            logger.info(f"Using course: {course}")
            course_slug = (clean_dir(course), COURSE)

        email = config.email
        password = config.password

        # Parse throttle parameter
        try:
            if throttle and "," in throttle:
                throttle = [int(i) for i in throttle.split(",")]
                logger.info(f"Using throttle range: {throttle}")
            elif throttle:
                throttle = [int(throttle)]
                logger.info(f"Using throttle value: {throttle[0]}")
        except ValueError as e:
            logger.error(f"Invalid throttle value: {throttle}")
            click.echo(click.style("Throttle must be a number", fg="red"))
            raise ConfigurationError("Throttle must be a number") from e

        # Validate configuration
        if course and path:
            logger.error("Both course and path specified")
            click.echo(
                click.style(
                    "Please specify either a course OR learning path, not both.", fg="red"
                )
            )
            raise ConfigurationError("Please specify either a course OR learning path, not both.")

        if path and not throttle:
            logger.error("Learning path specified without throttle")
            click.echo(
                click.style(
                    "Please use throttle option (-t) when downloading learning paths.",
                    fg="red",
                )
            )
            raise ConfigurationError("Please use throttle option (-t) when downloading learning paths.")

        # Handle authentication
        try:
            if cookies:
                logger.info("Using cookie authentication")
                cookie_dict = parse_cookie_file()
                click.echo(click.style(f"Using cookie info from cookies.txt", fg="green"))

                app = App(email, password, course_slug, resolution, caption, exercise, throttle)
                if headers:
                    logger.info("Using custom headers")
                    header_dict = parse_header_file()
                    app.run(cookie_dict, header_dict)
                else:
                    app.run(cookie_dict)

            else:
                logger.info("Using email/password authentication")
                if email == "":
                    email = click.prompt("Please enter your Linkedin email address")
                    logger.info("Email address provided via prompt")
                if password == "":
                    password = click.prompt("Enter your Linkedin Password", hide_input=True)
                    logger.info("Password provided via prompt")

                app = App(email, password, course_slug, resolution, caption, exercise, throttle)
                app.run()
                
        except (FileAccessError, ParsingError) as e:
            logger.error(f"Authentication error: {str(e)}")
            click.echo(click.style(f"Authentication error: {str(e)}", fg="red"))
            return
            
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        return
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        click.echo(click.style(f"An unexpected error occurred: {str(e)}", fg="red"))
        click.echo("Check the log file for more details.")
        return
