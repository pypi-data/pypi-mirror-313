import click
from dataclasses import dataclass
import json
import os
import stat

from hashboard.constants import HASHBOARD_BASE_URI


@dataclass
class AccessKeyInfo:
    project_name: str
    access_key_id: str
    access_key_token: str
    project_id: str
    user_email: str
    user_full_name: str


def confirm_credentials_filepath(credentials_filepath: str):
    if os.path.exists(credentials_filepath):
        click.echo(
            "If you continue, the file at the following location will be overwritten with your new access key:"
        )
        click.echo()
        click.echo(credentials_filepath)
        click.echo()
        click.echo(
            "💡 To save your new access key to a different file path, re-run this command with that path passed via the `--credentials-filepath` option."
        )
        click.echo()
        if not click.confirm("Continue and overwrite existing file?"):
            raise click.Abort()
        click.echo()


def direct_user_to_project_admin_settings():
    click.echo(
        f"You can find the ID of any given Hashboard project in the {click.style('Project Administration', bold=True)} settings section:"
    )
    click.echo()
    click.echo(f"{HASHBOARD_BASE_URI}/app/p/settings#project_administration")
    click.echo()


def save_access_key(credentials_filepath: str, access_key_info: AccessKeyInfo):
    credentials_file_already_exists = os.path.exists(credentials_filepath)
    f = open(credentials_filepath, "w")
    f.write(
        json.dumps(
            {
                "access_key_id": access_key_info.access_key_id,
                "access_key_token": access_key_info.access_key_token,
                "project_id": access_key_info.project_id,
            }
        )
    )
    if not credentials_file_already_exists:
        os.chmod(credentials_filepath, stat.S_IRUSR | stat.S_IWUSR)

    click.echo(
        f"✅ Saved new access key for {click.style(access_key_info.project_name, bold=True)} to {credentials_filepath}"
    )
    click.echo()


def echo_horizontal_rule():
    terminal_size = os.get_terminal_size()
    click.echo("─" * terminal_size.columns)
