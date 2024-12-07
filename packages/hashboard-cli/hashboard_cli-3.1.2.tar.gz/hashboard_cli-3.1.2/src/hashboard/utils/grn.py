import os
from pathlib import Path, PurePath, PurePosixPath
from typing import Optional
from dataclasses import dataclass
from uuid import UUID, uuid3

from click import ClickException

from hashboard.utils.hbproject import get_hashboard_root_dir


GRN_TYPE_KEY_MODEL = "m"
GRN_TYPE_KEY_SAVED_VIEW = "sv"
GRN_TYPE_KEY_DASHBOARD = "dsb"
GRN_TYPE_KEY_COLOR_PALETTE = "palette"
GRN_TYPE_KEY_HOMEPAGE_LAUNCHPAD = "launchpad"
GRN_TYPE_KEY_METRIC = "mtr"


@dataclass
class GRNComponents:
    resource_type: str
    gluid: Optional[str] = None
    alias: Optional[str] = None

    @staticmethod
    def generate(resource_type: str, project_id: str, local_path: PurePath):
        # mirrors server logic
        default_namespace = UUID("{00000000-0000-0000-0000-000000000000}")

        # local path must be relative to .hbproject file if it exists
        path: PurePosixPath = (
            PurePosixPath("/tmp/repos") / project_id / PurePosixPath(local_path)
        )
        return GRNComponents(
            resource_type, str(uuid3(default_namespace, f"{project_id}|{str(path)}"))
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GRNComponents):
            return False
        if self.resource_type != other.resource_type:
            return False

        if self.alias and other.alias:
            return self.alias == other.alias

        return self.gluid == other.gluid

    def __str__(self) -> str:
        if self.alias is not None:
            return f"{self.resource_type}:{self.gluid}:{self.alias}"
        else:
            return f"{self.resource_type}:{self.gluid}"


def parse_grn(grn: str) -> GRNComponents:
    components = grn.split(":")

    resource_type = components[0]
    if resource_type not in [
        GRN_TYPE_KEY_MODEL,
        GRN_TYPE_KEY_SAVED_VIEW,
        GRN_TYPE_KEY_DASHBOARD,
        GRN_TYPE_KEY_COLOR_PALETTE,
        GRN_TYPE_KEY_HOMEPAGE_LAUNCHPAD,
        GRN_TYPE_KEY_METRIC,
    ]:
        raise ClickException(
            f"""Invalid GRN. {resource_type} is not a valid resource type.
        The valid resource types are:
        - "{GRN_TYPE_KEY_MODEL}" for models
        - "{GRN_TYPE_KEY_METRIC}" for metrics
        - "{GRN_TYPE_KEY_SAVED_VIEW}" for saved views
        - "{GRN_TYPE_KEY_DASHBOARD}" for dashboards
        - "{GRN_TYPE_KEY_COLOR_PALETTE}" for color palettes
        - "{GRN_TYPE_KEY_HOMEPAGE_LAUNCHPAD}" for homepage launchpads"""
        )

    if len(components) == 2:
        return GRNComponents(
            resource_type=components[0],
            gluid=components[1],
            alias=None,
        )
    elif len(components) == 3:
        has_gluid = components[1] != ""
        return GRNComponents(
            resource_type=components[0],
            gluid=components[1] if has_gluid else None,
            alias=components[2],
        )

    raise ClickException(
        """Invalid GRN. The GRN should be in one of these formats:
    \n <resource_type>:<gluid>
    \n <resource_type>:<gluid>:<alias>
    \n <resource_type>::<alias>
    """
    )
