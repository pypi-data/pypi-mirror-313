import re
import click
from pathlib import PurePath
import time
from typing import List, Optional
from rich.live import Live
from rich.control import Control
from rich.prompt import Confirm

from hashboard.api import (
    apply_preview_build,
    create_build_from_local_files,
    fetch_build,
    login,
)
from hashboard.api.analytics.cli_with_tracking import (
    CommandWithTracking,
    GroupWithTracking,
)
from hashboard.api.build.build_status_display import BuildStatusDisplay
from hashboard.api.build.dbt import handle_dbt_args
from hashboard.api.build.utils import (
    poll_for_build_results,
)
from hashboard.credentials import get_credentials
from hashboard.session import get_current_session
from hashboard.utils.display import rich_console, verbose_cli_print
from hashboard.utils.hbproject import (
    DEFAULT_BUILD_ID_KEY,
    MAX_DEFAULT_BUILD_SECS,
    get_hashboard_root_dir,
)
from hashboard.utils.session_state import (
    delete_session_state_value,
    read_session_state_value,
    write_session_state_value,
)


class GroupWithDefaultCommand(GroupWithTracking):
    def __init__(self, *args, **kwargs):
        self.default_command = kwargs.pop("default_command", None)
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        # If no arguments are given, invoke the default subcommand
        if not args and self.default_command:
            args.insert(0, self.default_command)
        # If the first argument is not a known subcommand, prepend the default subcommand
        elif args and args[0] not in self.commands and self.default_command:
            args.insert(0, self.default_command)
        super().parse_args(ctx, args)


@click.group(cls=GroupWithDefaultCommand, default_command="create")
@click.pass_context
def build(ctx):
    """Commands for managing Hashboard builds\u2024 By default, creates a new build."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(build_create)


dbt_artifacts_option = click.option(
    "--dbt-artifacts",
    "dbt_artifacts_path",
    required=False,
    help="Path to folder containing dbt manifest and dbt run results JSON files, used to build Hashboard models defined in in dbt. All other dbt related arguments will be ignored if this option is specified.",
    type=click.Path(exists=True, readable=True, file_okay=False, dir_okay=True),
)
dbt_state_option = click.option(
    "--dbt-state",
    "dbt_state",
    required=False,
    help="Path to folder containing previous dbt state if using the --dbt-select or --dbt-prod flags with dbt-core. If your build is not configured to read from your dbt project, this flag will be ignored.",
    type=click.Path(exists=True, readable=True, file_okay=False, dir_okay=True),
)
dbt_force_prod = click.option(
    "--dbt-force-prod",
    "dbt_force_prod",
    required=False,
    help="A flag to determine whether to use production tables of all dbt models. If your build is not configured to read from your dbt project, this flag will be ignored.",
    is_flag=True,
    default=False,
)
full_rebuild_option = click.option(
    "--full-rebuild",
    "full_rebuild",
    is_flag=True,
    default=False,
    help="Rebuilds all code-controlled resources, deleting any code-controlled resources that are no longer included in your build.",
)
local_path_argument = click.argument("filepaths", type=click.STRING, nargs=-1)


@build.command(
    "create",
    cls=CommandWithTracking
)
@dbt_artifacts_option
@local_path_argument
@dbt_state_option
@dbt_force_prod
@full_rebuild_option
@click.pass_context
def build_create(
    ctx,
    dbt_artifacts_path,
    filepaths,
    dbt_state,
    dbt_force_prod,
    full_rebuild,
):
    """
    Creates and validates a new build.
    If a dbt root was defined when initializing your Hashboard project will run
    `dbt parse` to build Hashboard models defined in in dbt.
    This is the default command if you just run `hb build`.
    """

    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    is_partial = not full_rebuild

    # Since click doesn't support defaults for unlimited args we manually set the default
    # filepath argument
    hashboard_root = get_hashboard_root_dir()
    default_build_path = str(hashboard_root) if hashboard_root else "."
    args = list(filepaths) if filepaths else [default_build_path, "dbt:all"]

    dbt_pattern = r"^dbt:(.+)$"

    dbt_selectors = [x[4:] for x in args if re.search(dbt_pattern, x)]
    paths_as_list = [x for x in args if x not in dbt_selectors]

    dbt_manifest_path, dbt_metadata = handle_dbt_args(
        dbt_artifacts_path, dbt_selectors, dbt_state, dbt_force_prod
    )

    build_status_display = BuildStatusDisplay()
    with Live(build_status_display, console=rich_console):
        build_id = _start_async_build_using_options(
            project_id,
            paths_as_list,
            deploy=False,
            dbt_manifest_path=dbt_manifest_path,
            dbt_metadata=dbt_metadata,
            partial=is_partial,
        )
        build_status_display.build_id = build_id
        build_results = poll_for_build_results(build_id)
        build_status_display.build_results = build_results

    if _build_has_errors(build_results):
        exit(1)
    write_session_state_value(DEFAULT_BUILD_ID_KEY, f"{build_id},{int(time.time())}")
    click.echo("Check and apply these changes at the link or use `hb build apply`.")


@build.command(
    "apply",
    cls=CommandWithTracking
)
@click.argument("build_id", type=click.STRING, required=False)
@click.option(
    "--no-confirm",
    "skip_verification",
    is_flag=True,
    default=False,
    help="Applies changes with no additional confirmation step",
)
@click.pass_context
def build_apply(ctx: click.Context, build_id: Optional[str], skip_verification: bool):
    """Applies the changes from a build to your project. If no build_id is provided, this command will apply the most recently created build in your session, if one exists."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    login(s, ctx.obj["credentials"])

    build_id = build_id or _get_default_build_id()

    build_status_display = BuildStatusDisplay(build_id)
    with Live(build_status_display, console=rich_console) as live:
        # Verify before applying:
        if not skip_verification:
            fetched_build_results = _fetch_build(build_id)
            build_status_display.build_results = fetched_build_results
            live.stop()
            if not Confirm.ask("Confirm and apply these changes to your project?"):
                ctx.exit(1)
            # reset cursor and continue
            live.start()
            live.update("", refresh=True)
            rich_console.control(Control.move_to_column(0, -2))
            live.update(build_status_display, refresh=True)

        live.update(build_status_display)
        apply_results = _apply_build(build_id)
        build_status_display.build_results = apply_results
        build_status_display.applied = True

    delete_session_state_value(DEFAULT_BUILD_ID_KEY)


def _get_default_build_id():
    default_build_id = None
    try:
        default_build_id, timestamp = read_session_state_value(
            DEFAULT_BUILD_ID_KEY
        ).split(",")
        if time.time() - int(timestamp) > MAX_DEFAULT_BUILD_SECS:
            default_build_id = None
    except:
        pass

    if default_build_id is None:
        raise click.ClickException(
            "Could not find most recent build to apply, please explicitly specify a build id to apply to the project."
        )
    verbose_cli_print(
        f"No build id specified. Using most recent build ({default_build_id})."
    )
    return default_build_id


def _start_async_build_using_options(
    project_id: str,
    filepaths: List[str],
    dbt_manifest_path: Optional[PurePath] = None,
    dbt_metadata: Optional[dict] = None,
    deploy: bool = False,
    partial: bool = False,
) -> str:
    s = get_current_session()
    async_build = create_build_from_local_files(
        s,
        project_id,
        filepaths,
        deploy,
        dbt_manifest_path=dbt_manifest_path,
        dbt_metadata=dbt_metadata,
        partial=partial,
    )
    return async_build["data"]["createAsyncBuild"]


def _apply_build(preview_build_id: str):
    s = get_current_session()
    return apply_preview_build(s, preview_build_id)


def _fetch_build(preview_build_id: str):
    s = get_current_session()
    return fetch_build(s, preview_build_id)

def _build_has_errors(build_results: dict):
    return "errors" in build_results.get("data", {}).get("fetchBuild") and build_results["data"]["fetchBuild"]["errors"]
