import base64
from contextlib import suppress
from itertools import count
import gzip
import logging
import os
import sys
from pathlib import Path, PurePosixPath
import traceback

from hashboard.api.build.dbt import compile_manifest, get_properties_filepath
from hashboard.api.datasource.datasource_cli import datasource
from hashboard.api.build.build_cli import build
import string
from typing import Dict, Optional, List, Union
from uuid import UUID, uuid3
from rich.table import Table

import click
from hashboard.session import get_current_session
from ruamel.yaml import YAML

from hashboard.api.analytics.cli_with_tracking import (
    CommandWithTracking,
    GroupWithTracking,
    set_raw_command,
)
from hashboard.utils.dbt_properties import apply_hashboard_meta
from hashboard.utils.env import env_with_fallback

from hashboard import VERSION
from hashboard.api import (
    clear_model_cache,
    login,
    get_datasources,
    get_tables,
    pull_resource,
    remove_from_data_ops_mutation,
)
from hashboard.api.access_keys.existing_user import create_access_key
from hashboard.constants import (
    DEFAULT_CREDENTIALS_FILEPATH,
    HASHBOARD_DEBUG,
)
from hashboard.credentials import get_credentials
from hashboard.filesystem import compress_manifest, local_resources
from hashboard.utils.cli import cli_error_boundary, echo_list, getenv_bool
from hashboard.utils.grn import (
    GRN_TYPE_KEY_HOMEPAGE_LAUNCHPAD,
    GRN_TYPE_KEY_MODEL,
    GRNComponents,
    parse_grn,
)
from hashboard.utils.hbproject import (
    DBT_ROOT_KEY,
    create_hashboard_root,
    get_hashboard_root_dir,
    read_hashboard_project_value,
    write_hashboard_project_value,
)
from hashboard.utils.pull import (
    RESOURCE_TYPE_FROM_ABBREV,
    get_local_file_mappings,
    optionally_update_dbt_properties_file,
)
from hashboard.utils.resource import Resource
from hashboard.utils.display import rich_console


# Turning this on will result in secrets getting logged to stdout.
HASHBOARD_VERBOSE_DEBUG_UNSAFE = getenv_bool("HASHBOARD_VERBOSE_DEBUG_UNSAFE")


MAX_COLUMN_REGEX_LENGTH = 30
MAX_COLUMN_FILTER_CHARS = 1000


def main():
    root_command_with_path, *rest = sys.argv
    root_command = root_command_with_path.split("/")[-1]
    raw_command = " ".join([root_command, *rest])
    set_raw_command(raw_command)
    with cli_error_boundary(debug=HASHBOARD_DEBUG):
        if not _check_version():
            logging.warning(
                "There is a newer version of the Hashboard CLI available on PyPI. Upgrade your hashboard-cli package for the latest features.\n"
            )

        cli()


@click.group(cls=GroupWithTracking, context_settings=dict(max_content_width=130))
@click.version_option(version=VERSION, prog_name="Hashboard CLI")
@click.option(
    "--credentials-filepath",
    type=str,
    help="Path to your Hashboard access key credentials. You can also control this by setting a HASHBOARD_CREDENTIALS_FILEPATH environment variable.",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose output. Provides additional details for debugging.",
)
@click.pass_context
def cli(ctx: click.Context, credentials_filepath: Optional[str], verbose: bool):
    """A command-line interface for interacting with Hashboard."""
    if HASHBOARD_DEBUG or HASHBOARD_VERBOSE_DEBUG_UNSAFE:
        _enable_http_logging()
    ctx.ensure_object(dict)
    if credentials_filepath is None:
        credentials_filepath = env_with_fallback(
            "HASHBOARD_CREDENTIALS_FILEPATH",
            "GLEAN_CREDENTIALS_FILEPATH",
            DEFAULT_CREDENTIALS_FILEPATH,
        )
    ctx.obj["credentials_filepath"] = os.path.expanduser(credentials_filepath)
    ctx.obj["verbose"] = verbose


@cli.command(cls=CommandWithTracking)
@click.option(
    "--dbt-root",
    "dbt_root",
    type=click.Path(exists=True, readable=True, file_okay=False, dir_okay=True),
    required=False,
    help="Specifies the root of the dbt directory containing any Hashboard models to build when using the dbt integration. Will be used when running hb build create to run dbt parse in the correct location and build Hashboard models defined in dbt.",
)
@click.pass_context
def init(ctx: click.Context, dbt_root: Optional[Path]):
    """Initializes the root of your Hashboard project."""
    existing_root_dir = get_hashboard_root_dir()
    if existing_root_dir:
        click.echo(f"Found existing .hbproject file at {existing_root_dir}.")
        res = click.prompt(
            f"Overwrite? (y/n)",
            type=bool,
        )
        if not res:
            click.echo()
            click.echo("Exiting.")
            ctx.exit(0)

    create_hashboard_root(root_dir=existing_root_dir)

    click.echo()
    click.echo(click.style("✅ Initialized Hashboard project root.", fg="white"))

    if dbt_root:

        click.echo()
        click.echo("Validating dbt configuration...")
        dbt_root = Path(dbt_root).absolute()
        if not Path(dbt_root / "target").is_dir():
            raise click.ClickException(
                "Could not find a target/ directory inside dbt project, failed to configure dbt integration. Please rerun hb init with a valid dbt project for the --dbt-root argument.",
            )

        write_hashboard_project_value(
            DBT_ROOT_KEY,
            str(
                os.path.relpath(
                    dbt_root.resolve(),
                    get_hashboard_root_dir().resolve(),
                )
            ),
        )
        click.echo()
        click.echo("✅ Successfully configured dbt integration.\n")
        click.echo(
            "When running hb build create Hashboard will now build models specified in the provided dbt root directory by default. Use hb build create --no-dbt to ignore dbt models when building local files."
        )


@cli.command(cls=CommandWithTracking)
@click.option(
    "--project-id",
    type=str,
    required=False,
    help="If specified, creates an access key for this project ID. Required if your Hashboard user is a member of multiple projects.",
)
@click.pass_context
def token(ctx: click.Context, project_id: Optional[str]):
    """Log into a Hashboard account and create a new access key.

    If `--credentials-filepath` is passed, will save the access key in that location.
    """
    create_access_key(ctx.obj["credentials_filepath"], project_id)


@cli.command(cls=CommandWithTracking)
@click.argument("database")
@click.pass_context
def tables(ctx, database):
    """Lists the tables inside of a Hashboard data source."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    datasource_list = get_datasources(s, project_id)
    name_lookup = {d[0]: d[2] for d in datasource_list}

    if database in name_lookup.keys():
        datasource_id = name_lookup[database]
    elif database in name_lookup.values():
        datasource_id = database
    else:
        _echo_datasource_not_found(database, datasource_list)
        ctx.exit(1)

    tables = get_tables(s, datasource_id)
    table_names = list(tables.keys())
    _echo_tables(table_names, database)


@cli.group(cls=GroupWithTracking)
@click.pass_context
def cache(ctx):
    """Commands for managing Hashboard's data cache."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    pass


@cache.command("clear", cls=CommandWithTracking)
@click.argument("resource_grn")
@click.pass_context
def cache_clear(ctx, resource_grn):
    """Clears the cache associated with a Hashboard resource."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    login(s, ctx.obj["credentials"])

    grn = parse_grn(resource_grn)
    if not grn.gluid:
        click.echo("GRN must specify an id when clearing cache.")
        ctx.exit(1)
    if grn.resource_type != GRN_TYPE_KEY_MODEL:
        click.echo("Cache can only be cleared for models.")
        ctx.exit(1)

    clear_model_cache(s, grn.gluid)
    click.echo(f"Successfully cleared cache for {resource_grn}.")


@cli.command(cls=CommandWithTracking)
@click.argument("grn", required=False, type=str)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Pulls all project resources, including those not managed by code.",
)
@click.option(
    "--include-dbt",
    "include_dbt",
    is_flag=True,
    default=False,
    help="Inserts updated Hashboard configuration for dbt models directly into your dbt properties.yml files.",
)
@click.pass_context
def pull(ctx: click.Context, grn: str, all: bool = False, include_dbt: bool = False):
    """Pulls the latest resource configuration from Hashboard into the working directory.

    GRN is the Hashboard resource name of the target resource. If the resource has dependencies, they will also be
    pulled. If no GRN is specified, all code-controlled resources in the project will be pulled.
    """
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])

    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    resource_type = None
    resource_id = None
    resource_alias = None

    if grn:
        grn_components = parse_grn(grn)
        try:
            resource_type = RESOURCE_TYPE_FROM_ABBREV[grn_components.resource_type]
        except:
            raise click.ClickException(
                "Hashboard pull currently only supports models, saved views, dashboards, and color palettes"
            )
        resource_id = grn_components.gluid
        resource_alias = grn_components.alias

        # pulling a grn means we ignore the normal dataops-only filter
        all = True

    # get dbt model info
    dbt_manifest = None
    if include_dbt:
        dbt_manifest_path = compile_manifest()
        if dbt_manifest_path:
            dbt_manifest = compress_manifest(dbt_manifest_path)
        else:
            click.echo(
                "\nCould not compile dbt manifest, will skip pulling models defined in dbt.\n"
            )
    else:
        # check if this is a dbt project
        if read_hashboard_project_value(DBT_ROOT_KEY):
            click.secho(
                "\nThis project is configured to include models defined in dbt. Models defined in dbt will not be pulled down by default, to pull these model definitions please rerun using the `--include-dbt` flag.\n",
                fg="yellow",
            )

    result = pull_resource(
        s,
        project_id,
        resource_type,
        dbt_manifest,
        resource_id,
        resource_alias,
        dataops_only=(not all),
    )

    remote: list[Resource] = result["configs"]
    errors = result.get("errors", [])
    if len(remote) == 0 and not all and not errors:
        click.echo(
            "No code-controlled resources were found. To pull all resources in the project, use `hb pull --all`."
        )
        return

    touched_files = set()  # either created or modified
    num_updated = 0

    local_by_grn = get_local_file_mappings(project_id, result["aliasMappings"])

    grn_to_dbt_filepath = {
        d["grn"]: (d["dbtModelId"], d["schemaFilepath"])
        for d in (result.get("dbtModelFilepaths") or [])
    }
    missing_local_dbt_models = []

    for resource in remote:
        assert resource.grn is not None
        yaml = YAML(pure=True)
        local_match = next((x for x in local_by_grn if resource.grn == x[0]), None)
        if local_match:
            # we've matched the resource to a local file
            (_, path, local_resource) = local_match
            if local_resource.raw == resource.raw:
                continue
            # the resource has changed!
            num_updated += 1

            # update the path
            hashboard_root = get_hashboard_root_dir()
            path_to_update = (
                # get relative path from cwd based on fully qualified path using hashboard root if it exists
                os.path.relpath(
                    (hashboard_root / Path(path)).resolve(),
                    os.getcwd(),
                )
                if hashboard_root
                # else use default path relative to cwd
                else Path(path)
            )

            touched_files.add(path_to_update)
            with open(Path(path_to_update), "w") as f:
                yaml.dump(resource.raw, f)
            continue

        dbt_schema_patch_path = grn_to_dbt_filepath.get(str(resource.grn))
        if dbt_schema_patch_path:
            # we've matched the resource to a dbt model
            dbt_model_id = dbt_schema_patch_path[0]
            dbt_model_fp = dbt_schema_patch_path[1]

            if not dbt_model_id or not dbt_model_fp:
                missing_local_dbt_models.append(resource)
                continue
            else:
                try:
                    updated_fp = optionally_update_dbt_properties_file(
                        dbt_model_fp, dbt_model_id, resource
                    )
                    if updated_fp:
                        touched_files.add(updated_fp)
                except click.ClickException as e:
                    errors.append(str(e))
                continue

        # resource is not present locally, so we need to make a new file
        name = "".join(
            filter(
                lambda x: x in string.ascii_letters or x in string.digits,
                resource.raw.get("name", "untitled").lower().replace(" ", "_"),
            )
        )
        name = (
            resource.grn.resource_type
            if resource.grn.resource_type == GRN_TYPE_KEY_HOMEPAGE_LAUNCHPAD
            else resource.grn.resource_type + "_" + name
        )
        for i in count(0):
            if i > 0:
                path = Path(f"{name}_{i}.yml")
            else:
                path = Path(f"{name}.yml")
            if path.exists():
                continue

            touched_files.add(path)
            with open(path, "w") as f:
                yaml.dump(resource.raw, f)

            break

    click.echo()

    if missing_local_dbt_models:
        missing_dbt_schema_msg = "The following existing Hashboard models are linked to a dbt model, but the configuration of that dbt model is missing in your local project:\n"
        resource_identifiers = [
            resource.raw.get(
                "name",
                (
                    f"{resource.grn.resource_type}::{resource.grn.alias}"
                    if resource.grn.alias
                    else resource.grn
                ),
            )
            for resource in missing_local_dbt_models
        ]
        missing_dbt_schema_msg += "\n".join([f"- {id}" for id in resource_identifiers])
        click.secho(missing_dbt_schema_msg, fg="yellow")
        click.echo()

    if touched_files:
        click.echo(f"{len(touched_files)} files were created or modified:")
        echo_list(list(sorted([str(p) for p in touched_files])))
        click.echo()
        local_resource_count = len(local_by_grn)
        if num_updated < local_resource_count:
            click.echo(f"{local_resource_count - num_updated} files were not modified.")
    else:
        click.echo("No files were updated.")

    if errors:
        _echo_pull_errors_and_exit(errors)

    click.echo("✅ Project pulled successfully")


@cli.command("remove-from-code-control", cls=CommandWithTracking, hidden=True)
@click.argument("resource_grns", nargs=-1)
@click.pass_context
def remove_from_code_control(ctx, resource_grns):
    """Removes a Hashboard resource from code control."""

    if len(resource_grns) == 0:
        raise click.UsageError("At least one GRN is required.")

    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    click.echo(f"Removing resources from code control...")
    result = remove_from_data_ops_mutation(s, project_id, resource_grns)
    if result:
        click.echo(f"Resources removed from code control successfully.")
    else:
        click.echo(
            f"An unknown error occurred, please try again or contact support for assistance."
        )


cli.add_command(datasource)

cli.add_command(build)

#############################
# Legacy (v2) command stubs #
#############################


@cli.command("preview", cls=CommandWithTracking, hidden=True)
def preview():
    click.echo()
    click.echo("`hb preview` is no longer supported. Please use `hb build` instead.")


@cli.command("deploy", cls=CommandWithTracking, hidden=True)
def deploy():
    click.echo()
    click.echo(
        "`hb deploy` is no longer supported. Please use `hb build && hb build apply` instead."
    )


def _echo_tables(table_names: list, datasource: str) -> None:
    click.secho(f"📂 Available Tables From {datasource}", fg="bright_green")
    echo_list(table_names)


def _echo_table_not_found(table: str, tables: dict, datasource: str) -> None:
    """If table is not found in the available tables, output warning and display available tables."""
    click.echo("")
    click.secho(f"❗{table} was not found in {datasource}'s tables.", fg="red")
    click.echo("")
    _echo_tables(list(tables.keys()), datasource)
    click.echo("")


def _echo_datasources(datasources: list) -> None:
    table = Table(title="Available data connections")
    table.add_column("Name", justify="left")
    table.add_column("Type", justify="left")
    table.add_column("ID", justify="left")
    for ds in datasources:
        table.add_row(*ds)
    rich_console.print(table)


def _echo_datasource_not_found(datasource: str, datasources: list) -> None:
    """If datasource not found, output warning and available datasources."""
    click.echo("")
    click.secho(f"❗{datasource} was not found in your database connections.", fg="red")
    click.echo("")
    _echo_datasources(datasources)
    click.echo("")
    click.echo(
        "You can add another database connection in your Settings tab on hashboard.com."
    )
    click.echo("")


def _echo_pull_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when pulling resources")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.secho(
        "Resources that failed to export were not written to local files.",
        fg="red",
    )
    click.echo("")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    echo_list(errors, color="red")
    click.echo("")
    click.get_current_context().exit(1)


def _echo_datasource_creation_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――–––", fg="red")
    click.echo("❗ Errors encountered when creating your datasource")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――–––", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    echo_list(errors, color="red")
    click.echo("")
    click.secho("Datasource creation failed.", fg="red")
    click.get_current_context().exit(1)


def _enable_http_logging():
    # From: https://docs.python-requests.org/en/master/api/#api-changes
    from http.client import HTTPConnection

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    if HASHBOARD_VERBOSE_DEBUG_UNSAFE:
        HTTPConnection.debuglevel = 1


def _check_version():
    from pathlib import Path
    import time, requests
    import semver

    ttl = 24 * 60 * 60
    hb_path = Path.home() / ".hashboard"
    version_path = hb_path / ".cache" / "version"

    try:
        semver.Version.parse(VERSION)
    except ValueError:
        # if the current version string isn't valid, then assume we're on
        # an explicitly selected pre-release version
        return True

    try:
        old_umask = os.umask(0)
        os.makedirs(hb_path, exist_ok=True, mode=0o700)
        os.umask(old_umask)

        os.makedirs(version_path.parent, exist_ok=True)
    except:
        # Could be a permissions issue, or hard drive full, or weird cosmic bit flip...
        # Just assume we're up-to-date.
        return True

    try:
        prev_mtime = os.path.getmtime(version_path)
    except Exception:
        prev_mtime = None

    if prev_mtime is None or time.time() - prev_mtime > ttl:
        # delete stale cache
        try:
            version_path.unlink()  # missing_ok not available in Python 3.7
        except:
            pass

    try:
        with open(version_path, "r") as f:
            return semver.compare(VERSION, f.readline().strip()) >= 0
    except:
        pass

    # cache was stale or did not exist; fetch from pypi
    try:
        with open(version_path, "w+") as f:
            PACKAGE_JSON_URL = "https://pypi.org/pypi/hashboard-cli/json"
            resp = requests.get(PACKAGE_JSON_URL, timeout=1)
            data = resp.json()
            latest_version = _get_latest_public_version(data["releases"])
            f.write(latest_version)
            return semver.compare(VERSION, latest_version) >= 0
    except Exception as e:
        logging.warning("Unable to check the latest version of the CLI.", e)
        # Unable to pull version information currently, just return true
        return True


def _get_latest_public_version(releases: Dict[str, Dict]) -> str:
    from semver import Version

    max_version = Version.parse("0.0.1")
    for release_version_str, release in releases.items():
        try:
            release_version = Version.parse(release_version_str)
        except ValueError:
            # if a version string isn't valid, then skip it
            continue
        if [item for item in release if item.get("yanked", False)]:
            # if any distributions in this release are yanked, skip it
            continue

        if release_version.compare(max_version) >= 0:
            max_version = release_version

    return str(max_version)
