import os
from pathlib import Path, PurePath, PurePosixPath
from typing import List, Tuple, Union
from uuid import UUID, uuid3

import click
from hashboard.api.build.dbt import get_properties_filepath
from hashboard.filesystem import local_resources
from hashboard.utils.dbt_properties import apply_hashboard_meta
from hashboard.utils.grn import GRNComponents, parse_grn
from hashboard.utils.hbproject import get_hashboard_root_dir
from hashboard.utils.resource import Resource

# map the GRN resource type abbreviation to the full name
RESOURCE_TYPE_FROM_ABBREV = {
    "dsb": "dashboard",
    "sv": "savedExploration",
    "m": "model",
    "palette": "colorPalette",
    "launchpad": "homepageLaunchpad",
    "mtr": "metric",
}


def get_local_file_mappings(
    project_id, alias_to_id: dict
) -> List[Tuple[GRNComponents, PurePath, Resource]]:
    """
    Given a project id and a mapping of current aliases -> grns returns a list of tuples with
    the generated grn, file path, and resource config for local Hashboard files
    """
    SUPPORTED_TYPES = [
        "dashboard",
        "saved_view",
        "saved_exploration",
        "model",
        "color_palette",
        "homepage_launchpad",
        "metric",
    ]
    local_by_path = {
        k: v
        for k, v in local_resources(get_hashboard_root_dir() or Path(".")).items()
        if v.type in SUPPORTED_TYPES
    }
    click.echo(
        f"🔎 Found {len(local_by_path)} Hashboard resources in working directory."
    )

    def get_grn(path: PurePosixPath, resource: Resource) -> GRNComponents:
        RESOURCE_TYPE_TO_ABBREV = {
            "model": "m",
            "saved_view": "sv",
            "saved_exploration": "sv",
            "dashboard": "dsb",
            "color_palette": "palette",
            "homepage_launchpad": "launchpad",
            "metric": "mtr",
        }
        if resource.grn is not None:
            return resource.grn

        elif resource.type in ["saved_view", "saved_exploration", "metric"]:
            # terrible special case logic for saved views to maintain backwards compatibility,
            # since saved view and metric IDs include a hash of the model ID
            def get_model_id():
                if resource.type != "metric":
                    model = resource.raw["model"]
                    if type(model) is str:
                        return model
                    else:
                        # For models with adhocs this is an object not a string
                        return model.get("modelId")
                else:
                    return resource.raw.get("config", {}).get("dataModel")

            model_ref: str = get_model_id()
            model_id = ""

            # Attempt to resolve by GRN if reference contains grn abbreviation
            if model_ref.startswith("m:"):
                model_grn = parse_grn(model_ref)
                model_id = model_grn.gluid
                if not model_id:
                    # map by alias instead
                    model_id = alias_to_id.get(model_grn.alias, "")
            # Otherwise resolve by file path
            else:
                try:
                    # resolve model references by file paths to their project-local path
                    model_path = (
                        Path(path.parent / model_ref).resolve().relative_to(Path.cwd())
                    )
                    if model_path.exists():
                        model = local_by_path[PurePosixPath(model_path)]
                        assert model is not None
                        model_grn = get_grn(PurePosixPath(model_path), model)
                        model_id = model_grn.gluid
                except:
                    print(
                        f"Warning: found malformed model reference in local file at ${path}, this may cause inconsistent results when pulling resources."
                    )

            default_namespace = UUID("{00000000-0000-0000-0000-000000000000}")
            initial_id = GRNComponents.generate(
                RESOURCE_TYPE_TO_ABBREV[resource.type], project_id, path
            ).gluid
            assert initial_id is not None
            sv_or_mtr_id = str(uuid3(default_namespace, model_id + initial_id))

            return GRNComponents(RESOURCE_TYPE_TO_ABBREV[resource.type], sv_or_mtr_id)

        else:
            return GRNComponents.generate(
                RESOURCE_TYPE_TO_ABBREV[resource.type], project_id, path
            )

    # Can't use a map here because we actually _do_ want to compare GRNs that hash to different values!
    # In particular, if they have the same type/alias but different guid (because local hasn't received a guid),
    # they should be considered equal.
    local_by_grn = list(
        (get_grn(path, resource), path, resource)
        for (path, resource) in local_by_path.items()
    )

    return local_by_grn


def optionally_update_dbt_properties_file(
    dbt_model_fp, dbt_model_id, resource: Resource
) -> Union[str, None]:
    """Returns touched file path if resource was updated, else None"""
    properties_filepath = get_properties_filepath(dbt_model_fp)
    with open(properties_filepath, "r") as schema_file:
        schema_str = schema_file.read()
    try:
        modified_schema_str, is_updated = apply_hashboard_meta(
            schema_str,
            dbt_model_id.split(".")[-1],
            resource.raw,
        )
    except RuntimeError as e:
        raise click.ClickException(
            f"Error updating Hashboard metadata for `{dbt_model_id}` model at {dbt_model_fp}: {e}"
        )
    except Exception as e:
        raise click.ClickException(
            f"Unknown error updating Hashboard metadata for `{dbt_model_id}` model at {dbt_model_fp}."
        )
    if is_updated:
        with open(properties_filepath, "w") as schema_file:
            schema_file.write(modified_schema_str)

        pretty_path = os.path.relpath(
            Path(properties_filepath).resolve(),
            os.getcwd(),
        )
        return pretty_path
    return None
