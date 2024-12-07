import json
from os import environ
from pathlib import Path
import re
import shlex
import subprocess
from typing import List, Optional, Tuple

import click

from hashboard.utils.cli import getenv_bool
from hashboard.utils.display import verbose_cli_print
from hashboard.utils.hbproject import (
    DBT_DEFER_OPTION,
    DBT_INCLUDE_DB_IN_SCHEMA_OPTION,
    DBT_OPTIONS_KEY,
    DBT_ROOT_KEY,
    get_hashboard_root_dir,
    read_hashboard_project_value,
)


def _get_selected_model_info(
    dbt_root, dbt_select_string: Optional[str], dbt_state: Optional[str]
) -> List[dict]:
    ls_options = " --resource-type model"
    if dbt_select_string:
        ls_options += f" --select '{dbt_select_string}'"
        if dbt_state:
            ls_options += f" --state {dbt_state}"
    else:
        # By default we ignore ephemeral models
        ls_options += " --select 'config.materialized:view config.materialized:table config.materialized:incremental'"

    verbose_cli_print("Running `dbt ls` to identify selected dbt models\n")

    ls_command = f"dbt ls{ls_options} --output json --output-keys 'unique_id name'"

    verbose_cli_print(ls_command)

    ls_out = _run_dbt_command(ls_command, dbt_root)

    inclusion_list = []
    for line in ls_out.split("\n"):
        try:
            # Remove anything before the start of a potential json object
            cleaned_output = re.sub(r"^.*?(?=\{)", "", line)
            model_info = json.loads(cleaned_output)
            inclusion_list.append(model_info)
        except:
            # Ignore non-json lines
            pass
    if not inclusion_list:
        click.echo("Warning: no dbt models selected\n")
    return inclusion_list


def _get_compiled_db_info(
    dbt_root,
    model_names_and_ids: List[dict],
    force_prod: bool,
    dbt_state: Optional[str],
    dbt_defer_db: bool = False,
) -> Optional[dict]:
    """
    dbt supports a pattern called 'defer' for Slim CI style workflows and dbt Cloud (https://docs.getdbt.com/reference/node-selection/defer)
    This means that dbt models can either point at a table in a prod target or a dev target however the manifest generated
    by dbt commands always outputs the the tables as if they were created in the dev target. In order to figure out the current
    state of the databases we compile an arbitrary dbt-SQL string that that returns a list of database_name.schema_name.table_name
    references which reflect the state of the actual warehouse which is ensures we're using the same dbs and schemas that dbt is
    """
    if not model_names_and_ids:
        return None

    compile_query = (
        "$$$"
        + "\n".join(
            [
                f'{m["unique_id"]}:{{{{ ref("{m["name"]}") }}}}'
                for m in model_names_and_ids
            ]
        )
        + "$$$"
    )

    compile_options = ""
    if force_prod:
        compile_options = f" --favor-state"
    if dbt_state:
        compile_options += f" --state {dbt_state} --defer"

    verbose_cli_print("Running `dbt compile` to identify selected schemas\n")

    compile_command = f"dbt compile --inline '{compile_query}'{compile_options}"

    verbose_cli_print(compile_command + "\n")

    stdout = _run_dbt_command(compile_command, dbt_root)

    verbose_cli_print("--- dbt output ---\n")
    verbose_cli_print(stdout + "\n")

    # Parses substring that matches this pattern: ###model_id:`db`.`schema`.`name`\nmodel_id2:`db`.`schema`.`name`###
    pattern = r"\${3}(.*?)\${3}"
    match = re.search(pattern, stdout, re.DOTALL)

    if match:
        extracted_text = match.group(1).strip()
        lines = extracted_text.split("\n")

        # Get a map of unique id to schema
        schema_map = {
            key: value.replace("`", "").replace('"', "").split(".")[-2]
            for line in lines
            for key, value in [line.split(":")]
            if ":" in line
        }

        # Get a map of unique id to db
        database_map = {
            key: value.replace("`", "").split(".")[0]
            for line in lines
            for key, value in [line.split(":")]
            if ":" in line
        }

        result = {}
        for m in model_names_and_ids:
            m_id = m["unique_id"]
            schema_els = []
            if database_map.get(m_id) and dbt_defer_db:
                schema_els.append(database_map.get(m_id))
            schema_els.append(schema_map.get(m_id))

            if schema_els:
                result[m_id] = ".".join(schema_els)

        verbose_cli_print(f"Schemas to be used when building dbt models: {result}\n")
        return result
    else:
        return None


def _run_dbt_command(invocation_string: str, dbt_root: str):
    additional_flags = environ.get("HB_DBT_FLAGS", "")
    process = subprocess.Popen(
        shlex.split(invocation_string) + shlex.split(additional_flags),
        cwd=dbt_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = process.communicate()
    ret_code = process.wait()

    if ret_code != 0:
        click.echo(f"Error running dbt command: {invocation_string}\n")
        if stdout:
            click.echo(stdout)
        if stderr:
            click.echo(stderr, err=True)
        raise click.ClickException(f"dbt returned nonzero exit code ({ret_code})")

    return stdout


def _validate_manifest_path(target_dir: Path) -> Path:
    manifest_path = target_dir / "manifest.json"
    if not manifest_path.is_file():
        raise click.ClickException(
            f"⚠️ manifest file does not exist in target directory {target_dir}."
        )

    verbose_cli_print(f"Using dbt artifacts at {target_dir}\n")

    return manifest_path


def _get_dbt_root():
    hashboard_root = get_hashboard_root_dir()
    if not hashboard_root:
        return None
    relative_dbt_root = read_hashboard_project_value(DBT_ROOT_KEY)
    return (
        hashboard_root.absolute().joinpath(relative_dbt_root)
        if relative_dbt_root
        else None
    )


def _get_dbt_defer_options() -> Tuple[bool, bool]:
    use_defer = False
    include_db = False

    project_dbt_settings = read_hashboard_project_value(DBT_OPTIONS_KEY) or {}

    def get_setting(project_key: str, env_var: str):
        if environ.get(env_var) is not None:
            return getenv_bool(env_var)
        else:
            return project_dbt_settings.get(project_key, False)

    use_defer = get_setting(DBT_DEFER_OPTION, "HB_DBT_USE_DEFER")
    include_db = get_setting(
        DBT_INCLUDE_DB_IN_SCHEMA_OPTION, "HB_DBT_INCLUDE_DB_IN_SCHEMA"
    )

    if not use_defer and include_db:
        raise click.ClickException(
            "Enabling includeDbNameInSchema without enabling useDefer is not yet supported. Please set useDefer: true in .hbproject or update the HB_DBT_USE_DEFER env var to true and build again."
        )

    return use_defer, include_db


def handle_dbt_args(
    dbt_artifacts_path: Optional[str],
    dbt_select_options: List[str],
    dbt_state: Optional[str],
    dbt_force_prod: bool,
):
    """Convenience wrapper for running `dbt parse` before `hb preview` or `hb deploy`.
    Must be run from your Hashboard project directory.
    """

    # Find dbt root
    dbt_root = _get_dbt_root()
    # If explicit or implicit skip return early
    if not dbt_select_options or (dbt_root is None and dbt_artifacts_path is None):
        return None, None

    click.echo("Collecting dbt metadata...")

    # Get provided manifest path or run parse at dbt root
    if dbt_artifacts_path is not None:
        target_dir = Path(dbt_artifacts_path)

        if dbt_select_options and "all" not in dbt_select_options:
            click.echo(
                "Warning: Advanced dbt select options not supported when directly passing artifacts, all Hashboard models in provided manifest will be rebuilt."
            )
        return _validate_manifest_path(target_dir), None

    # Using dbt root allows more complex operations
    dbt_select_string = None
    if "all" not in dbt_select_options:
        dbt_select_string = " ".join(dbt_select_options)

    use_defer, defer_db = _get_dbt_defer_options()
    model_schema_info = None
    if dbt_select_string or use_defer:
        try:
            # Run dbt ls to get list of selected models
            model_names_and_ids = _get_selected_model_info(
                dbt_root, dbt_select_string, dbt_state
            )

            # This is a hacky way to support selection when deferral is not run since we
            # check the keys of this dict in the backend to filter dbt models
            model_schema_info = {m["unique_id"]: None for m in model_names_and_ids}
        except click.ClickException as e:
            raise e
        except Exception as e:
            verbose_cli_print(e)
            raise click.ClickException(
                "An unknown error occurred collecting database information for dbt models. Please try again or contact support for assistance."
            )

    if use_defer:
        try:
            # Compile a dbt-SQL string that references all the models above
            compiled_db_info = _get_compiled_db_info(
                dbt_root,
                model_names_and_ids,
                dbt_force_prod,
                dbt_state,
                defer_db,
            )
            if compiled_db_info:
                model_schema_info = compiled_db_info
        except click.ClickException as e:
            raise e
        except Exception as e:
            verbose_cli_print(e)

            raise click.ClickException(
                "An unknown error occurred collecting database information for dbt models. Please try again or contact support for assistance."
            )

    target_dir = Path(dbt_root) / "target"

    verbose_cli_print("Running `dbt parse` to generate a manifest file.\n")

    _run_dbt_command("dbt parse", dbt_root)

    manifest_path = _validate_manifest_path(target_dir)

    click.echo(f"dbt metadata collected successfully.\n")

    return manifest_path, (
        {
            "dbtCompiledSchemaDict": model_schema_info,
        }
        if model_schema_info
        else None
    )


def compile_manifest() -> str:
    dbt_root = _get_dbt_root()
    if not dbt_root:
        return None
    _run_dbt_command("dbt parse", dbt_root)
    target_dir = Path(dbt_root) / "target"
    return _validate_manifest_path(target_dir)


def get_properties_filepath(patch_path: str):
    relative_path = patch_path.split("://", 1)[-1]
    dbt_root = _get_dbt_root()
    return dbt_root / relative_path
