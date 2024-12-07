from pathlib import Path
from typing import Union
import os
from ruamel.yaml.comments import CommentedMap

from hashboard.utils.yaml_file import read_yaml_file, write_yaml_file, write_yaml_key

HASHBOARD_PROJECT_FILE_NAME = ".hbproject"
DBT_ROOT_KEY = "dbtRoot"
DBT_OPTIONS_KEY = "dbtOptions"
DBT_DEFER_OPTION = "useDefer"
DBT_INCLUDE_DB_IN_SCHEMA_OPTION = "includeDbNameInSchema"
DEFAULT_BUILD_ID_KEY = "most_recent_build_id"
MAX_DEFAULT_BUILD_SECS = 3600  # One hour


def create_hashboard_root(*, root_dir=None):
    empty = CommentedMap()
    empty[DBT_ROOT_KEY] = None

    empty.yaml_set_start_comment(
        "This file marks the root of your Hashboard project directory. It determines the identity of the resources in your local filesystem\nand encodes additional project configuration metadata. For additional information please visit docs.hashboard.com."
    )

    hbproject_filename = (
        os.path.join(root_dir, HASHBOARD_PROJECT_FILE_NAME)
        if root_dir
        else HASHBOARD_PROJECT_FILE_NAME
    )

    write_yaml_file(hbproject_filename, empty)


def read_hashboard_project_value(key: str):
    root = get_hashboard_root_dir()
    if root is None:
        return None
    filepath = root / HASHBOARD_PROJECT_FILE_NAME
    values = read_yaml_file(filepath)
    return values.get(key, None)


def write_hashboard_project_value(key: str, value):
    root = get_hashboard_root_dir()
    if root is None:
        return
    filepath = root / HASHBOARD_PROJECT_FILE_NAME
    write_yaml_key(filepath, key, value)


def get_hashboard_root_dir() -> Union[Path, None]:
    current_path = os.getcwd()

    # Arbitrary limit to prevent searching for too long
    for _ in range(100):
        try:
            # List all files in the current directory
            for filename in os.listdir(current_path):
                if filename == HASHBOARD_PROJECT_FILE_NAME:
                    return Path(current_path)

            # Move to the parent directory
            parent_path = os.path.dirname(current_path)

            # If we've reached the root directory, stop
            if parent_path == current_path:
                break
            current_path = parent_path
        except PermissionError:
            return None
    return None
