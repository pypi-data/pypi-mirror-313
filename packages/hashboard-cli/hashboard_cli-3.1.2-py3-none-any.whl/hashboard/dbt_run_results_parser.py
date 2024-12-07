import json
from typing import List

from dbt_artifacts_parser import parser


def parse_dbt_run_results(
    raw: str,
) -> List[str]:
    """Parses a serialized JSON representation of dbt run results into a list of dbt models to rebuild"""

    try:
        json_raw = json.loads(raw)
        manifest = parser.parse_run_results(json_raw)
    except json.JSONDecodeError as e:
        raise RuntimeError("dbt run results file is not valid JSON.", e)

    return [r.unique_id for r in manifest.results if r.status.value == "success"]
