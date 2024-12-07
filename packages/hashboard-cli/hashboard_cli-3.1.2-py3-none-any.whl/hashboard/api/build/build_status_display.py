from typing import List
from rich.console import Console, ConsoleOptions, RenderResult, Group
from rich.panel import Panel

from hashboard.api import build_details_uri
from hashboard.api.build.utils import convert_to_resource_update_list


class BuildStatusDisplay:
    """
    Helper to display a build's current information to the console.
    """

    def __init__(self, build_id: str = None) -> None:
        self.build_id = build_id
        self.build_results = None
        self.build_results_pending_reason = "Loading" if build_id else "Building"
        self.applied = False
        self.fps = 4
        self._frame_counter = 0
        # set the minimum width to match the expected size of the link
        # which is generally the longest line of text in the panel
        self.min_width = len(build_details_uri("X" * 16))

    def __rich_console__(
        self,
        console: Console,
        console_options: ConsoleOptions,
    ) -> RenderResult:
        self._frame_counter += 1
        yield from self._display()

    def _display(self):
        title = f"📦 Build" + (f" [b]{self.build_id}[/b]" if self.build_id else "")
        applied_status = "[b green]✅ Applied [/b green]" if self.applied else None

        yield Panel.fit(
            Group(
                " " * self.min_width,
                *self._display_panel_body(),
                "",
            ),
            title=title,
            title_align="left",
            subtitle=applied_status,
            subtitle_align="right",
            padding=[0, 2],
        )
        yield ""

    def _display_panel_body(self):
        if not self.build_id:
            yield f"Creating{self._waiting_dots}"
            return
        if not self.build_results:
            yield f"{self.build_results_pending_reason} changes{self._waiting_dots}"
            return
        if "errors" in self.build_results and self.build_results["errors"]:
            yield from self._display_errors(
                [
                    e["extensions"]["userMessage"]
                    for e in self.build_results["errors"]
                    if "extensions" in e and "userMessage" in e["extensions"]
                ]
            )
        else:
            yield from self._display_results()
        yield ""
        link_url = build_details_uri(self.build_id)
        yield "[dim u]View build[/dim u]"
        yield f"[u]{link_url}[/u]"

    def _display_results(self):
        results = next(
            self.build_results["data"][query_key]
            for query_key in ["fetchBuild", "applyBuild"]
            if query_key in self.build_results["data"]
        )
        yield from self._display_errors(results["errors"])

        changes = (results.get("changeSet") or {}).get("resourceChanges")
        changes = convert_to_resource_update_list(changes) if changes else None

        if changes:
            yield from self._display_resources(changes)
        yield from self._display_warnings(results["warnings"])

    def _display_resources(self, changes: dict):
        rows = []
        for action, type_map in changes.items():
            for type_key, items in type_map.items():
                get_name = lambda r: r["name"]
                if type_key == "modelBundles":
                    get_name = lambda r: r["model"]["name"]
                elif type_key == "homepageLaunchpads":
                    get_name = lambda r: "Project launchpad"
                for item in items:
                    rows.append([action, type_key, get_name(item)])

        prev_action = ""
        for row_idx, row in enumerate(rows):
            action, type_key, name = row
            first_of_action = action != prev_action
            if first_of_action:
                if row_idx != 0:
                    yield ""
                yield f"[b]{self._get_action_text(action)}[/b]"

            yield f"{self._get_action_bullet(action)} {name} [dim]{self._get_type_text(type_key)}[/dim]"
            prev_action = action

    def _get_action_text(self, action: str):
        text = {
            "added": "Create",
            "changed": "Update",
            "deleted": "Delete",
            "unchanged": "Unchanged",
        }[action]
        return self._style_action_text(action, text)

    def _get_action_bullet(self, action: str):
        symbol = {
            "added": "+",
            "changed": "~",
            "deleted": "-",
            "unchanged": "=",
        }[action]
        return self._style_action_text(action, symbol)

    def _style_action_text(self, action: str, text: str):
        style = {
            "added": "green",
            "changed": "cyan",
            "deleted": "red",
            "unchanged": "dim",
        }[action]
        return f"[{style}]{text}[/{style}]"

    def _get_type_text(self, type_key: str):
        return {
            "modelBundles": "Model",
            "metrics": "Metric",
            "savedViews": "View",
            "reportSchedules": "Report",
            "dashboards": "Dashboard",
            "colorPalettes": "Palette",
            "homepageLaunchpads": "Launchpad",
        }[type_key]

    def _display_errors(self, errors: List[str]):
        if not errors:
            return
        yield ""
        yield f"[bold red]{len(errors)} build error{'s' if len(errors) > 1 else ''}[/bold red]"
        for error in errors:
            yield f" [red]*[/red] {error}"

    def _display_warnings(self, warnings: List[str]):
        if not warnings:
            return
        yield ""
        yield f"[bold yellow]⚠️ {len(warnings)} build warning{'s' if len(warnings) > 1 else ''}[/bold yellow]"
        for warning in warnings:
            yield f" [yellow]*[/yellow] {warning}"

    @property
    def _waiting_dots(self):
        DOTS_PER_SEC = 2
        MAX_DOTS = 3
        dots = (self._frame_counter // int(self.fps / DOTS_PER_SEC)) % MAX_DOTS + 1
        spaces = MAX_DOTS - dots
        return "." * dots + " " * spaces
