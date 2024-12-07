import click
import rich
from rich.console import Console


rich_console = Console(highlight=False)


def is_verbose():
    ctx = click.get_current_context(silent=True)
    return ctx and ctx.obj.get("verbose")


def verbose_cli_print(s: str):
    if is_verbose():
        rich_console.print(s, style="dim")
