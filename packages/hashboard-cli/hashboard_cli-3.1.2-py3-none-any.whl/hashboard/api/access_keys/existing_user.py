from typing import Optional
import click
from dataclasses import fields
import os

from hashboard.api.access_keys.browser_auth import (
    QueryParamsHandler,
    auth_and_handle_query_params,
)
from hashboard.api.access_keys.utils import (
    AccessKeyInfo,
    confirm_credentials_filepath,
    direct_user_to_project_admin_settings,
    save_access_key,
)
from hashboard.constants import HASHBOARD_BASE_URI
from hashboard.utils.cli import parse_str_bool


def create_access_key(credentials_filepath: str, intended_project_id: Optional[str]):
    """Creates and saves a new access key for an existing user. Does not
    require the user to have an existing saved access key to do authentication,
    but rather opens a browser page that pushes them through our login flow.

    Args:
        credentials_filepath (str): Filepath to save access key to.
        intended_project_id (Optional[str]): Project ID to create a new access key for.
          Required if the user belongs to multiple projects. Defaults to None.
    """
    confirm_credentials_filepath(credentials_filepath)
    access_key_info = _get_existing_account_access_key_info(intended_project_id)
    if access_key_info:
        save_access_key(credentials_filepath, access_key_info)


def _get_existing_account_access_key_info(
    intended_project_id: Optional[str],
) -> Optional[AccessKeyInfo]:
    # If the logged-in user has multiple projects, this indicates that
    # we should request them to disambiguate the project ID they'd like
    # to create an access key for.
    has_multiple_projects = False

    # If project_id was passed but we find that the authenticated Hashboard user
    # is not a member of that project, this query param will be populated.
    invalid_project_id = False

    # Whether our request errored while finishing authentication.
    request_error = False

    # Access key info received from Hashboard's app server.
    access_key_info = None

    def qp_handler(query_params: dict) -> str:
        nonlocal has_multiple_projects
        nonlocal invalid_project_id
        nonlocal request_error
        nonlocal access_key_info

        if parse_str_bool(query_params.get("has_multiple_projects")):
            has_multiple_projects = True
            return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/error/multipleProjects"

        if parse_str_bool(query_params.get("invalid_project_id")):
            invalid_project_id = True
            return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/error/invalidProjectId?projectId={intended_project_id}"

        # If either of the above cases aren't true and we still don't have access key
        # info for the user, there's an issue.
        if any(
            map(
                lambda field: query_params.get(field.name) is None,
                fields(AccessKeyInfo),
            )
        ):
            request_error = True
            return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/error"

        access_key_info = AccessKeyInfo(**query_params)
        return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/success/existingUser?userEmail={access_key_info.user_email}"

    _login_and_handle_query_params(qp_handler, intended_project_id)

    # If encountered error while handling request, raise an exception.
    if request_error:
        raise click.ClickException(
            "Unknown error while finishing authentication. Please try again."
        )

    if has_multiple_projects:
        click.echo(
            f"You belong to multiple Hashboard projects. Please specify the ID of the project you'd like to create an access key for with the `--project-id` option."
        )
        direct_user_to_project_admin_settings()
        return

    if invalid_project_id:
        click.echo(
            f"Your Hashboard user does not belong to project {intended_project_id}. Please try again with the ID of a project you're a member of."
        )
        direct_user_to_project_admin_settings()
        return

    return access_key_info


def _login_and_handle_query_params(
    handle_get_query_params: QueryParamsHandler,
    intended_project_id: Optional[str] = None,
):
    base_url = f"{HASHBOARD_BASE_URI}/auth/login"
    query_params_dict = {}
    if intended_project_id:
        query_params_dict["cli-auth-project-id"] = intended_project_id
    auth_and_handle_query_params(handle_get_query_params, base_url, query_params_dict)
