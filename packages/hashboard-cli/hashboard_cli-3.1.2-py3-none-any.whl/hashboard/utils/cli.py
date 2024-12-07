from os import environ
from contextlib import contextmanager
from typing import List, Optional

import click


def parse_str_bool(str_bool: Optional[str]) -> bool:
    if str_bool is None:
        return False
    return str_bool.lower() in ["true", "t", "1", "*"]


def getenv_bool(key: str) -> bool:
    return parse_str_bool(environ.get(key))


def echo_list(items: List[str], color="white"):
    for item in items:
        lines = item.split("\n")
        click.echo(click.style("*", fg=color) + "  " + lines[0])
        for line in lines[1:]:
            click.echo("   " + line)


@contextmanager
def cli_error_boundary(debug=False):
    try:
        yield
    except Exception as err:
        if debug:
            # will raise the whole stack trace
            raise
        else:
            # just print the error description
            print(f"Unexpected Error: {type(err).__name__}: {err}")
            exit(1)
