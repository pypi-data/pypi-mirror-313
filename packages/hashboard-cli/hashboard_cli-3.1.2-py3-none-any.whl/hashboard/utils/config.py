from click import ClickException
import json
import re
from string import Template
from typing import List
import yaml

parse_failure_message = (
    lambda filename, e: f"\n Could not parse file {filename}. \n Errors found in this file: \n ---- \n {e}"
)


def _is_valid_yaml_config_file(contents: str, filename: str) -> bool:
    try:
        data = yaml.safe_load(contents)
        return isinstance(data, dict) and (
            data.get("glean") is not None or data.get("hbVersion") is not None
        )
    except yaml.YAMLError as e:
        raise ClickException(parse_failure_message(filename, e))


def _is_valid_json_config_file(contents: str, filename: str) -> bool:
    try:
        data = json.loads(contents)
        return isinstance(data, dict) and (
            data.get("glean") is not None or data.get("hbVersion") is not None
        )
    except json.decoder.JSONDecodeError as e:
        raise ClickException(parse_failure_message(filename, e))


def is_valid_glean_config_file(filename: str, contents: str) -> bool:
    hashboard_keys = "(hbVersion|glean)"
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        if re.search(f"^{hashboard_keys}:", contents, re.MULTILINE):
            return _is_valid_yaml_config_file(contents, filename)

    if filename.endswith(".json"):
        if re.search(hashboard_keys, contents):
            return _is_valid_json_config_file(contents, filename)

    return False


def extract_variable_names(file_contents: str) -> List[str]:
    # Adapted from Template.get_identifiers(), which was added in Python 3.11
    # https://github.com/python/cpython/commit/dce642f24418c58e67fa31a686575c980c31dd37
    names = set()
    template = Template(file_contents)
    for mo in template.pattern.finditer(template.template):
        named = mo.group("named") or mo.group("braced")
        if named is not None:
            # add a named group only the first time it appears
            names.add(named)
        elif (
            named is None
            and mo.group("invalid") is None
            and mo.group("escaped") is None
        ):
            raise ValueError("Unexpected error parsing environment variables.")
    return names
