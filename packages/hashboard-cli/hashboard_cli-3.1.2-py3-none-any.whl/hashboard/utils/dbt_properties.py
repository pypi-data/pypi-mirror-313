import copy
import re

from io import StringIO
from typing import Optional
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from hashboard.utils.grn import parse_grn

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


def apply_hashboard_meta(
    dbt_properties_raw_str: str, dbt_model_name: str, model_spec: dict
):
    is_done = False
    is_updated = False
    updated_yml = dbt_properties_raw_str
    covered_col_ids = set()
    i = 0
    while (
        not is_done and i < 5000
    ):  # arbitrary max iterations to avoid an infinite loop
        updated_yml, is_done, is_updated = _apply_part(
            updated_yml, dbt_model_name, model_spec, covered_col_ids
        )
        i += 1
    return updated_yml, is_updated


def _apply_part(
    dbt_properties_raw_str: str,
    dbt_model_name: str,
    model_spec: dict,
    covered_col_ids: set,
):
    parsed_dbt_yml = yaml.load(dbt_properties_raw_str)
    if not isinstance(parsed_dbt_yml, CommentedMap):
        raise RuntimeError(f"Could not parse yml: {dbt_properties_raw_str}")

    # Find correct model
    dbt_models = parsed_dbt_yml.get("models", [])
    target_model = None
    for dbt_model in dbt_models:
        pinned_grn = dbt_model.get("meta", {}).get("hashboard", {}).get("grn", None)
        if dbt_model.get("name") == dbt_model_name or (
            pinned_grn is not None
            and parse_grn(pinned_grn) == parse_grn(model_spec.get("grn"))
        ):
            target_model = dbt_model
            break
    if not target_model:
        raise RuntimeError(f"Could not find model with name {dbt_model_name}")

    col_id_to_spec = {col["id"]: col for col in model_spec.get("cols", [])}

    # Update first column we find that needs updating
    for dbt_col in target_model.get("columns", []):
        hb_col_id = (
            dbt_col.get("meta", {}).get("hashboard", {}).get("id", None)
            or dbt_col["name"]
        )
        if hb_col_id in col_id_to_spec and hb_col_id not in covered_col_ids:
            covered_col_ids.add(hb_col_id)

            dbt_col_hb_meta = dbt_col.get("meta", {}).get("hashboard", {})
            hb_spec = dict(col_id_to_spec[hb_col_id])

            updated_meta = _filter_column_meta(dbt_col, hb_spec)

            if updated_meta != dbt_col_hb_meta:
                return (
                    _insert_hashboard_meta(
                        dbt_properties_raw_str, dbt_col, updated_meta
                    ),
                    False,
                    True,
                )

    remaining_model_spec = _filter_model_meta(target_model, model_spec, covered_col_ids)

    if remaining_model_spec != target_model.get("meta", {}).get("hashboard", {}):
        return (
            _insert_hashboard_meta(
                dbt_properties_raw_str, target_model, remaining_model_spec
            ),
            True,
            True,
        )
    else:
        return dbt_properties_raw_str, True, False


def _escape_custom_sql(sql: str):
    replacements = {"{{": '{{ "{{', "}}": '}}" }}'}
    return re.sub(r"\{\{|\}\}", lambda m: replacements[m.group(0)], sql)


def _filter_column_meta(dbt_col, hb_col_spec):
    new_spec = copy.deepcopy(hb_col_spec)
    fields_to_ignore_if_not_specified = [
        "id",
        "description",
        "type",
        "physicalName",
    ]

    fields_to_ignore_if_defaults_match = ["name", "description"]

    if new_spec.get("sql"):
        new_spec["sql"] = _escape_custom_sql(new_spec["sql"])

    return _filter_fields(
        fields_to_ignore_if_defaults_match,
        fields_to_ignore_if_not_specified,
        hb_col_spec,
        dbt_col,
        new_spec,
    )


def _filter_model_meta(dbt_model, hb_spec, covered_col_ids: set):
    new_spec = copy.deepcopy(hb_spec)
    fields_to_ignore_if_not_specified = [
        "hbVersion",
        "type",
        "source",
    ]

    fields_to_ignore_if_defaults_match = ["name", "description"]

    new_spec = _filter_fields(
        fields_to_ignore_if_defaults_match,
        fields_to_ignore_if_not_specified,
        hb_spec,
        dbt_model,
        new_spec,
    )

    # Filter out cols already in dbt spec
    additional_cols = [c for c in hb_spec["cols"] if c["id"] not in covered_col_ids]

    # Special quoting is necessary for {{ }} refs in custom sql cols
    for c in additional_cols:
        if c.get("sql"):
            c["sql"] = _escape_custom_sql(c["sql"])

    if additional_cols:
        new_spec["cols"] = additional_cols
    else:
        del new_spec["cols"]

    return new_spec


def _filter_fields(
    fields_to_ignore_if_defaults_match,
    fields_to_ignore_if_not_specified,
    hb_spec,
    dbt_spec,
    new_spec,
):
    "in place mutation of spec"
    for f in fields_to_ignore_if_defaults_match:
        if hb_spec.get(f) == dbt_spec.get(f):
            new_spec.pop(f, None)

    existing_meta = dbt_spec.get("meta", {}).get("hashboard", {})
    for f in fields_to_ignore_if_not_specified:
        if f not in existing_meta:
            new_spec.pop(f, None)

    return new_spec


def _insert_hashboard_meta(dbt_properties_raw_str, target_block, updated_meta):
    """
    dbt_properties_raw_str
    target_block: either model or column block
    updated_meta: new hashboard meta to insert

    """
    s = StringIO(newline="")

    meta_key = target_block.get("meta", None)
    hashboard_key = (meta_key or {}).get("hashboard", None)

    # If meta exists and hashboard meta exists
    if hashboard_key is not None:
        yaml.dump({"hashboard": updated_meta}, s)
        return _insert_yaml_block(
            dbt_properties_raw_str,
            hashboard_key.lc.line,
            s.getvalue(),
            replace_existing=True,
        )
    # If meta exists but no hashboard key exists
    elif meta_key is not None:
        yaml.dump({"hashboard": updated_meta}, s)
        return _insert_yaml_block(
            dbt_properties_raw_str,
            meta_key.lc.line,
            s.getvalue(),
            replace_existing=False,
            insert_nested=True,
        )

    # If neither meta key nor hashboard key exists
    # insert after description or name
    else:
        yaml.dump({"meta": {"hashboard": updated_meta}}, s)
        return _insert_yaml_block(
            dbt_properties_raw_str,
            target_block.lc.data.get("description", target_block.lc.data["name"])[0]
            + 1,
            s.getvalue(),
            replace_existing=False,
            insert_nested=False,
        )


def _insert_yaml_block(
    yaml_content: str,
    start_line: int,
    new_block: str,
    replace_existing=False,
    insert_nested=False,
):
    """
    Replace a YAML block in a string and return the modified string.

    Args:
        yaml_content: The original YAML content as a string
        nested_key_path: The nested path to the key to replace (dot-separated)
        new_block: The new YAML block to insert
        replace_existing: If False, new_block will be inserted. If True, new_block will replace the existing block at this line.

    Returns:
        A tuple containing:
        - The modified YAML content as a string
        - A boolean indicating whether the replacement was successful

    Raises:
        ValueError: If the nested key is not found in the YAML content
    """
    # Get the indentation level of the key
    target_indentation = _get_block_indentation(yaml_content, start_line, insert_nested)
    # Prepare the new block with proper indentation
    indented_block = "\n".join(
        " " * target_indentation + line for line in new_block.strip().split("\n")
    )

    # Process the content line by line
    lines = yaml_content.split("\n")
    new_lines = []
    in_block = False

    for i, line in enumerate(lines, 1):
        if i == start_line:
            # Add the new block
            if replace_existing:
                in_block = True
            else:
                new_lines.append(line)
            new_lines.append(indented_block)

        elif in_block:
            # Check if we're still in the block to be replaced
            line_indentation = len(line) - len(line.lstrip())
            if not line.strip() or line_indentation > target_indentation:
                continue  # Skip lines in the original block
            else:
                in_block = False
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def _get_block_indentation(content: str, line_number: int, insert_nested: bool) -> int:
    lines = content.split("\n")
    if 0 <= line_number - 1 < len(lines):
        line_content = lines[line_number - 1]
        indent = len(line_content) - len(line_content.lstrip())
        if line_content.lstrip().startswith("-"):
            indent += 2
        if insert_nested:
            indent += 2
        return indent
    return 0
