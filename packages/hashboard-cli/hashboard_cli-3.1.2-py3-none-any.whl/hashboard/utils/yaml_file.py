from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


yaml = YAML()


def read_yaml_file(filepath: Path) -> CommentedMap:
    if filepath.exists():
        with open(filepath, "r") as f:
            content = yaml.load(f)
            if isinstance(content, CommentedMap):
                return content
            elif content is not None:
                return CommentedMap(content)
    return CommentedMap()


def write_yaml_file(filepath: Path, data: CommentedMap):
    with open(filepath, "w") as f:
        yaml.dump(data, f)


def write_yaml_key(filepath: Path, key: str, value: Any):
    values = read_yaml_file(filepath)
    values[key] = value
    write_yaml_file(filepath, values)


def delete_yaml_key(filepath: Path, key: str):
    values = read_yaml_file(filepath)
    if key in values:
        del values[key]
    write_yaml_file(filepath, values)
