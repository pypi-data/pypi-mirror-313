from typing import Any, Optional, OrderedDict

from dataclasses import dataclass
from hashboard.utils import grn
from hashboard.utils.grn import GRNComponents


# Represents any Hashboard resource which can be backed by a file.
# Right now, it is possible to represent invalid resources using this class since config types are only in TypeScript.
@dataclass
class Resource:
    # Hashboard config version string.
    hb_version: str

    # Underlying untyped dictionary.
    raw: OrderedDict[str, Any]

    # Type of resource.
    type: str = "model"

    # Extracted and parsed GRN, if one exists.
    grn: Optional[GRNComponents] = None

    @staticmethod
    # parse a resource from its (untyped) dictionary representation
    def from_dict(
        raw: OrderedDict[str, Any]
    ) -> Optional[Any]:  # use Self type in Python 3.11+
        if "hbVersion" in raw.keys():
            hb_version = raw["hbVersion"]
        elif "glean" in raw.keys():
            hb_version = raw["glean"]
        else:
            # file does not represent a hashboard/glean resource
            return None

        type = "model"  # for legacy reasons, by default assume model
        if "type" in raw.keys():
            type = raw["type"]

        parsed_grn = None
        if "grn" in raw.keys():
            parsed_grn = grn.parse_grn(raw["grn"])

        # TODO(meyer): ideally, we would validate the schema here...
        return Resource(hb_version, raw, type, parsed_grn)
