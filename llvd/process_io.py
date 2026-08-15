import sys
import click


def parse_cookie_file():
    try:
        with open("cookies.txt", "r") as file:
            cookies = {}
            for line in file:
                line = line.strip()
                if line.startswith("li_at"):
                    cookies["li_at"] = line.split("li_at=")[1]
                if line.startswith("JSESSIONID"):
                    cookies["JSESSIONID"] = line.split("JSESSIONID=")[1].replace(
                        '\"', "")
            return cookies
    except FileNotFoundError:
        click.echo(
            click.style(f"cookies.txt not found or is empty", fg="red"))
        sys.exit(0)

def parse_header_file(path="headers.txt"):
    headers = {}
    try:
        with open(path, "r", encoding="utf8") as file:
            for line in file:
                line = line.strip()
                # Skip empty lines and lines without '='
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                headers[key] = value.replace('"', "").strip()
        return headers
    except FileNotFoundError:
        click.echo(
            click.style(f"{path} not found or is empty", fg="red"))
        sys.exit(0)
