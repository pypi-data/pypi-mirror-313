import sys
import time
import click
from hashboard.api import (
    fetch_build,
    fetch_build_status,
)
from hashboard.session import get_current_session


def poll_for_build_results(build_id):
    s = get_current_session()

    is_running = False
    for i in range(3000):  # arbitrary upper limit
        if not i % 10:
            sys.stdout.flush()
            partial_build = fetch_build_status(s, build_id)
            if ("errors" in partial_build and partial_build["errors"]) or partial_build[
                "data"
            ]["fetchBuild"]["status"] in ["completed", "applied"]:
                build = fetch_build(s, build_id)
                return build
            elif (
                partial_build["data"]["fetchBuild"]["status"] == "building"
                and not is_running
            ):
                is_running = True
        time.sleep(0.5)

    click.echo("Could not load build.", fg="red")
    click.get_current_context().exit(1)


def convert_to_resource_update_list(resource_changes: dict):
    result = {
        "added": _get_empty_status_groups(),
        "changed": _get_empty_status_groups(),
        "deleted": _get_empty_status_groups(),
        "unchanged": _get_empty_status_groups(),
    }
    action_to_status = {
        "create": "added",
        "update": "changed",
        "delete": "deleted",
        "unchanged": "unchanged",
    }
    type_to_status_group = {
        "modelBundle": "modelBundles",
        "savedView": "savedViews",
        "dashboard-v2": "dashboards",
        "projectMetric": "metrics",
        "colorPalette": "colorPalettes",
        "homepageLaunchpad": "homepageLaunchpads",
        "reportSchedule": "reportSchedules",
    }
    for rc in resource_changes.values():
        rcType = rc["newContent"]["value"]["type"]
        content = rc["newContent"]["value"]
        if rcType == "reportSchedule":
            report_id = content.get("id")
            content["name"] = content.get("subject", f"Report schedule {report_id}")
        result[action_to_status[rc["action"]]][
            type_to_status_group[rc["newContent"]["value"]["type"]]
        ].append(rc["newContent"]["value"])

    return result


def _get_empty_status_groups():
    return {
        "modelBundles": [],
        "metrics": [],
        "savedViews": [],
        "dashboards": [],
        "colorPalettes": [],
        "homepageLaunchpads": [],
        "reportSchedules": [],
    }
