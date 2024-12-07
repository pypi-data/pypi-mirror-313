import click
from typing import Optional


def prompt_and_validate_value_length(
    prompt: str,
    value_name: str,
    min_value_length_limit: Optional[int] = 1,
    max_value_length_limit: Optional[int] = 100,
):
    value = ""
    while True:
        value = click.prompt(prompt, type=str).strip()
        value_length = len(value)
        if value_length < min_value_length_limit:
            write_error_message(
                f"{value_name} must be {min_value_length_limit} character{'' if min_value_length_limit == 1 else 's'} or more."
            )
            continue

        if value_length > max_value_length_limit:
            write_error_message(
                f"{value_name} must be {max_value_length_limit} character{'' if max_value_length_limit == 1 else 's'} or fewer."
            )
            continue

        return value


def write_error_message(message: str):
    click.secho(message, fg="red", bold=True)
