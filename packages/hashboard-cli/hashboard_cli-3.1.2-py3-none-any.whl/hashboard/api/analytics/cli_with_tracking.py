from time import perf_counter
from typing import Optional
import click

from hashboard.api.analytics import track
from hashboard.api.analytics.events import COMMAND

raw_command = None


def set_raw_command(new_raw_command: str):
    """Setter for the global raw_command variable."""
    global raw_command
    raw_command = new_raw_command


class GroupWithTracking(click.Group):
    def invoke(self, ctx):
        return _invoke(self, ctx, click.Group.invoke)


class CommandWithTracking(click.Command):
    def invoke(self, ctx):
        return _invoke(self, ctx, click.Command.invoke)


def _invoke(self, ctx, invoke):
    is_root = ctx.find_root().info_name == ctx.info_name
    if is_root:
        # If this is the root context, initialize the `full_command`
        # variable that will be recursively appended to by subcommands.
        # Then, upon finishing invocation (in which case all applicable
        # subcommands have also finished invocation), track an event with
        # this value.
        param_names_to_display_names = _parse_param_names_to_display_names(
            ctx.to_info_dict()
        )
        ctx.ensure_object(dict)
        ctx.obj["param_names_to_display_names"] = param_names_to_display_names
        ctx.obj["commands"] = [_parse_command(ctx)]
        start_time = perf_counter()
        caught_exception = None

        try:
            result = invoke(self, ctx)
        except Exception as e:
            caught_exception = e

        duration = _calculate_command_duration(start_time)
        track(
            COMMAND,
            {
                "raw": raw_command,
                "commands": ctx.obj["commands"],
                "error": str(caught_exception)
                if caught_exception is not None
                else caught_exception,
            },
            duration,
        )
        if caught_exception:
            raise caught_exception
        return result
    else:
        # Otherwise, store this subcommand.
        ctx.obj["commands"].append(_parse_command(ctx))
        return invoke(self, ctx)


def _parse_command(ctx: click.Context) -> dict:
    """Converts a command context into the following shape:
    {
      "command": <command_name>,
      "parameters: {
        <param_1_name>: <param_1_value>,
        ...
      }
    }
    """

    parsed_params = {
        ctx.obj["param_names_to_display_names"][param_name]: value
        for param_name, value in ctx.params.items()
        if ctx.get_parameter_source(param_name) != click.core.ParameterSource.DEFAULT
    }
    return {"command": ctx.info_name, "parameters": parsed_params}


def _calculate_command_duration(start_time: int) -> int:
    end_time = perf_counter()
    return round(end_time - start_time, 2)


def _parse_param_names_to_display_names(info_dict: Optional[dict]) -> dict:
    """Click gives you param names as they're parsed into click variables.
    e.g. For the `--credentials-filepath` option, they give you `credentials_filepath`
    as the param name.
    This is annoying for analytics where we want to see the option as they typed it.
    So, we DFS the root context's `to_info_dict()` structure which _does_ have this
    information to create a mapping from param name to displayed option name.

    Args:
        info_dict (Optional[dict]): Current info dict to parse. Initial consumer should
          pass the root context.

    Returns:
        dict: Dictionary mapping param name to displayed option name.
    """
    if not info_dict:
        return {}

    param_names_to_display_names = {}
    for key, value in info_dict.items():
        if key == "params":
            for param_dict in value:
                param_names_to_display_names[param_dict["name"]] = param_dict["opts"][0]
        else:
            if isinstance(value, dict):
                recursive_result = _parse_param_names_to_display_names(value)
                param_names_to_display_names.update(recursive_result)
    return param_names_to_display_names
