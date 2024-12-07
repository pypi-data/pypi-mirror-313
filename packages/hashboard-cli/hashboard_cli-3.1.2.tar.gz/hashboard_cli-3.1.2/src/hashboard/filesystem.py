import base64
from contextlib import suppress
import glob
import gzip
import json
import os
import pathlib
from pathlib import Path, PurePath
from typing import Any, Callable, List, Optional, Dict, Tuple, Union, Set

import click
import yaml
from click import ClickException

from hashboard.utils.hbproject import (
    HASHBOARD_PROJECT_FILE_NAME,
    get_hashboard_root_dir,
)
from hashboard.utils.resource import Resource
from hashboard.utils.config import extract_variable_names, is_valid_glean_config_file


VALID_FILE_EXTENSIONS = set([".json", ".yml", ".yaml"])


def validate_file(path: Path):
    if path.suffix in VALID_FILE_EXTENSIONS:
        with open(path, "r") as f:
            raw_contents = f.read()

        # Check that the file is a valid config file. Otherwise, ignore it.
        if is_valid_glean_config_file(path.name, raw_contents):
            return raw_contents

    return None


def process_filepaths(
    filepaths_or_patterns: List[str],
    project_id: str,
    project_root_dir: Optional[Path] = None,
) -> Tuple[List[Dict], Set]:
    inline_files = []
    env_var_names: Set[str] = set()

    for fp_pattern in filepaths_or_patterns:
        input_as_path = Path(fp_pattern)
        if input_as_path.is_file():
            validated_contents = validate_file(input_as_path)
            if validated_contents:
                env_var_names |= extract_variable_names(validated_contents)
                # We pull out the parent directory directly from the path
                # and adjust if its relative to match how we represent
                # default deploys
                path = (
                    input_as_path.parent
                    if input_as_path.is_absolute()
                    else f"./{input_as_path.parent}"
                )

                # If a project root is provided we reference relative to that path
                if project_root_dir:
                    path = os.path.relpath(
                        input_as_path.parent.resolve(),
                        Path(project_root_dir).resolve(),
                    )

                parent_directory = f"/tmp/repos/{project_id}/{path}"
                # Maps parent_directory -> filename -> file contents
                inline_files.append(
                    {
                        "parentDirectory": parent_directory,
                        "filename": input_as_path.name,
                        "fileContents": validated_contents,
                    }
                )
        elif input_as_path.is_dir():
            for root, subdirs, filenames in os.walk(input_as_path):
                current_dir = os.path.basename(root)
                if current_dir.startswith(".") and current_dir != ".":
                    continue
                root = Path(root)
                if (
                    project_root_dir != root.absolute()
                    and (root / HASHBOARD_PROJECT_FILE_NAME).is_file()
                ):
                    raise click.ClickException(
                        f"Builds cannot be created when above the root of an initialized project directory. Please rerun command from the root of your Hashboard project: `{root}`."
                    )
                expanded_files = [str(root / filename) for filename in filenames]
                files, env_vars = process_filepaths(
                    expanded_files, project_id, project_root_dir
                )
                env_var_names |= env_vars
                inline_files.extend(files)
        else:
            expanded_paths: List[str] = glob.glob(fp_pattern, recursive=True)
            expanded_files = [p for p in expanded_paths if Path(p).is_file()]
            files, env_vars = process_filepaths(
                expanded_files, project_id, project_root_dir
            )
            env_var_names |= env_vars
            inline_files.extend(files)
    return inline_files, env_var_names


def compress_manifest(dbt_manifest_path: str):
    try:
        with open(Path(dbt_manifest_path), "r") as f:
            dbt_manifest_raw = f.read()
            compressed_data = gzip.compress(dbt_manifest_raw.encode("utf-8"))
            return base64.b64encode(compressed_data).decode("utf-8")
    except Exception as e:
        raise ClickException(f"Could not read dbt manifest file: {e}")


def build_spec_from_local(
    paths: List[str],
    project_id: str,
    dbt_manifest_path: Optional[PurePath] = None,
    dbt_metadata: Optional[dict] = None,
) -> dict:
    dbt_manifest = None

    if dbt_manifest_path:
        dbt_manifest = compress_manifest(dbt_manifest_path)

    root = get_hashboard_root_dir()

    inline_files, env_var_names = process_filepaths(paths, project_id, root)

    if root is None:
        click.echo()
        click.secho(
            "Could not find Hashboard project root, defaulting to current directory. Please run hb init in the root of your Hashboard project to ensure consistent build behavior.",
            fg="yellow",
        )

    env_vars = [
        {"name": name, "value": os.environ[name]}
        for name in env_var_names
        if name in os.environ
    ]
    return {
        "inlineConfigFiles": inline_files,
        "dbtManifestCompressed": dbt_manifest,
        "dbtMetadata": dbt_metadata,
        "clientEnvVars": env_vars,
    }


def local_resources(root: Union[str, os.PathLike]) -> Dict[PurePath, Resource]:
    """
    Recursively searches root for files that represent Hashboard resources.
    """
    root = Path(root)

    def parse_yaml(raw: str) -> Optional[Dict[str, Any]]:
        with suppress(yaml.YAMLError):
            return yaml.safe_load(raw)

    def parse_json(raw: str) -> Optional[Dict[str, Any]]:
        with suppress(json.JSONDecodeError):
            return json.loads(raw)

    PARSERS: Dict[str, Callable[[str], Optional[Dict[str, Any]]]] = {
        ".yml": parse_yaml,
        ".yaml": parse_yaml,
        ".json": parse_json,
    }

    resources: Dict[PurePath, Resource] = {}

    for path in root.rglob("*"):
        if (not path.is_file()) or (path.suffix not in VALID_FILE_EXTENSIONS):
            continue

        with open(path, "r") as f:
            raw_contents = f.read()

            # parse the file as a dictionary
            parser = PARSERS[path.suffix]
            raw = parser(raw_contents)
            if raw is None or not isinstance(raw, dict):
                continue

            # parse the dictionary as a Hashboard Resource
            resource: Optional[Resource] = Resource.from_dict(raw)
            if resource is not None:
                resources[PurePath(path.relative_to(root))] = resource

    return resources
