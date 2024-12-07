import click
from click import ClickException
import json
import os
from pathlib import PurePath
from requests import Session
from typing import List, Optional, Dict

from hashboard.constants import FILE_SIZE_LIMIT_MB, HASHBOARD_BASE_URI
from hashboard.credentials import CliCredentials
from hashboard.filesystem import build_spec_from_local
from hashboard import VERSION
from hashboard.utils.resource import Resource
from hashboard.utils.display import rich_console, verbose_cli_print


def login(session: Session, credentials: CliCredentials):
    """Authenticates the session with the provided credentials.

    :return The user's project ID, if successfully logged in.
    :raises ClickException if the login is not successful.
    """
    r = session.post(
        HASHBOARD_BASE_URI + "/auth/login-cli",
        data={
            "accessKeyId": credentials.access_key_id,
            "accessKeyToken": credentials.access_key_token,
        },
        headers={"Glean-CLI-Version": VERSION},
    )
    # TODO(dse): Show custom error message from server, if present.
    if r.status_code >= 500:
        raise ClickException("Unexpected error initiating your Hashboard session.")
    elif r.status_code >= 400:
        raise ClickException("Your access key is invalid.")
    if not r.ok:
        raise ClickException("Unexpected error initiating your Hashboard session.")

    rich_console.print(f"🔑 Logged in to [b]{r.text}[/b]")
    verbose_cli_print(f"Project ID: {credentials.project_id}")
    verbose_cli_print(f"Access Key ID: {credentials.access_key_id}")
    rich_console.print()

    return credentials.project_id


def create_build_from_local_files(
    session: Session,
    project_id: str,
    paths: List[str],
    deploy: bool,
    dbt_manifest_path: Optional[PurePath] = None,
    dbt_metadata: Optional[dict] = None,
    partial: bool = False,
):
    """Creates a build using local files and returns the result."""
    build_spec = build_spec_from_local(
        paths, project_id, dbt_manifest_path, dbt_metadata
    )

    return _create_async_build(session, project_id, build_spec, deploy, partial)


def get_datasources(s: Session, project_id: str) -> list:
    """Queries and formats datasources"""
    query = _get_data_connections(s, project_id)
    data_sources = [
        [d["name"], d["subType"], d["id"]] for d in query["data"]["dataConnections"]
    ]
    return data_sources


def clear_model_cache(s: Session, model_id: str) -> str:
    """Clears the cache for the specified model"""
    return _graphql_query(
        s,
        """
        mutation UpdateModelFreshnessKey($id: String!) {
            updateModelFreshnessKey(id: $id)
        }
        """,
        {"id": model_id},
    )


class PullResourceResponse(dict):
    configs: List[Resource]
    errors: List[str]


def pull_resource(
    s: Session,
    project_id: str,
    resource_type: Optional[str],
    dbt_manifest_compressed: Optional[str],
    resource_id: Optional[str],
    resource_alias: Optional[str],
    dataops_only: Optional[bool],
) -> PullResourceResponse:
    """Pulls the config for the given resource, or all resources in the project if none is specified."""
    res = _graphql_query(
        s,
        """
        query PullResource($projectId: String!, $resourceType: String, $dbtManifestCompressed: String, $resourceId: String, $resourceAlias: String, $dataOpsOnly: Boolean) {
            pullResource(
                projectId: $projectId,
                resourceType: $resourceType,
                dbtManifestCompressed: $dbtManifestCompressed,
                resourceId: $resourceId,
                resourceAlias: $resourceAlias,
                dataOpsOnly: $dataOpsOnly
            ) { configs, errors, dbtModelFilepaths { grn, dbtModelId, schemaFilepath }, aliasMappings}
        }
        """,
        {
            "projectId": project_id,
            "resourceType": resource_type,
            "resourceId": resource_id,
            "dbtManifestCompressed": dbt_manifest_compressed,
            "resourceAlias": resource_alias,
            "dataOpsOnly": dataops_only,
        },
    )["data"]["pullResource"]
    res["configs"] = [
        Resource.from_dict(json.loads(string)) for string in res["configs"]
    ]
    return res


def build_fetch_timeout_error(build_id):
    def error_func(status_code):
        if status_code == 401:
            raise ClickException(
                f"The Hashboard CLI client has timed out but your request is still running on our server. Please check the build page to view build progress: {build_details_uri(build_id)}"
            )
        elif status_code != 200:
            raise ClickException("Unexpected error received from the Hashboard server.")

    return error_func


def fetch_build_status(s: Session, build_id):
    return _graphql_query(
        s,
        """
        query fetchBuild($buildId: String!){
            fetchBuild (buildId: $buildId){
                id,
                status,
            }
        }
        """,
        {"buildId": build_id},
        custom_status_response_func=build_fetch_timeout_error(build_id),
    )


def fetch_build(s: Session, build_id):
    return _graphql_query(
        s,
        """
        query fetchBuild($buildId: String!){
            fetchBuild (buildId: $buildId){
                id,
                status,
                changeSet {
                    id
                    resourceChanges
                    errors
                    warnings
                },
                warnings,
                errors
            }
        }
        """,
        {"buildId": build_id},
        custom_status_response_func=build_fetch_timeout_error(build_id),
    )


def apply_preview_build(s: Session, preview_build_id):
    return _graphql_query(
        s,
        """
        mutation applyBuild($buildId: String!){
            applyBuild (buildId: $buildId){
                id,
                status,
                changeSet {
                    id
                    resourceChanges
                    errors
                    warnings
                },
                warnings,
                errors
            }
        }
        """,
        {"buildId": preview_build_id},
    )


def _parse_table_data(table_data: dict) -> Dict[str, Dict[str, str]]:
    """Formats table names for output, and returns tables names and schemas"""
    tables = table_data["data"]["getAvailableGleanDbTables"]
    tables_by_name = {}
    for table in tables:
        name = (
            table["schema"] + "." + table["name"] if table["schema"] else table["name"]
        )
        tables_by_name[name] = {"schema": table["schema"], "name": table["name"]}
    return tables_by_name


def _create_async_build(
    session,
    project_id,
    build_spec,
    deploy,
    partial=True,
):
    return _graphql_query(
        session,
        """
        mutation CreateAsyncBuild($projectId: String!, $buildSpec: BuildSpecInput!, $deploy: Boolean!, $partial: Boolean) {
            createAsyncBuild( projectId: $projectId, buildSpec: $buildSpec, deploy: $deploy, partial: $partial)
        }
        """,
        {
            "projectId": project_id,
            "buildSpec": build_spec,
            "deploy": deploy,
            "partial": partial,
        },
    )


def _get_data_connections(session: Session, project_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query dataConnections($projectId: String!){
            dataConnections(projectId: $projectId){
                id,
                name,
                subType
            }
        }
        """,
        {"projectId": project_id},
    )
    return query


def _get_table_data(session: Session, datasource_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query getAvailableGleanDbTables($datasourceId: String!){
            getAvailableGleanDbTables (datasourceId: $datasourceId){
                name,
                schema
            }
        }
        """,
        {"datasourceId": datasource_id},
    )
    return query


def create_data_source(session: Session, datasource: dict) -> dict:
    # Assumes that error handling occurs a level up
    return _graphql_query(
        session,
        """
        mutation AddDatasource($datasource: DatasourceInput!) {
          addDatasource(datasource: $datasource) {
            id
          }
        }
        """,
        {"datasource": datasource},
    )["data"]["addDatasource"]["id"]


def update_data_source(session: Session, datasource: dict) -> dict:
    # Assumes that error handling occurs a level up
    return _graphql_query(
        session,
        """
        mutation UpdateDatasource($datasource: DatasourceInput!) {
          updateDatasource(datasource: $datasource) {
            id
          }
        }
        """,
        {"datasource": datasource},
    )["data"]["updateDatasource"]["id"]


def test_data_source(session: Session, datasource_name: str, project_id: str) -> bool:
    return _graphql_query(
        session,
        """
        query TestDatasourceByName($name: String!, $projectId: String!) {
            testDatasourceByName(name: $name, projectId: $projectId)
        }
        """,
        {"name": datasource_name, "projectId": project_id},
    )["data"]["testDatasourceByName"]


def get_tables(s: Session, datasource_id: str) -> Dict[str, Dict[str, str]]:
    """Queries and formats table from datasource"""
    query = _get_table_data(s, datasource_id)
    tables = _parse_table_data(query)
    return tables


build_details_uri = lambda id: f"{HASHBOARD_BASE_URI}/app/p/builds/{id}"


def _graphql_query(
    session: Session, query: str, variables: dict, custom_status_response_func=None
):
    r = session.post(
        HASHBOARD_BASE_URI + "/graphql/",
        json={"query": query, "variables": variables},
        headers={"Glean-CLI-Version": VERSION},
    )
    if custom_status_response_func:
        custom_status_response_func(r.status_code)
    else:
        # This 504 status should only be encountered by legacy build commands
        if r.status_code == 504:
            raise ClickException(
                f"The Hashboard CLI client has timed out but your request is still running on our server. Please check your project's build page in a few minutes to see build results: {HASHBOARD_BASE_URI}/app/p/data-ops"
            )
        elif r.status_code != 200:
            raise ClickException("Unexpected error received from the Hashboard server.")

    results = r.json()
    graphql_exceptions = results.get("errors")
    if (
        graphql_exceptions
        and isinstance(graphql_exceptions[0], dict)
        and graphql_exceptions[0].get("message")
    ):
        error = graphql_exceptions[0]["message"]

        # Must match error message in server code at glean/services/data_ops/build_management.py line #543 (as of 7/5/23).
        if (
            error
            == "No Glean config files were found, and empty builds were not enabled, so the build was aborted."
            or error
            == "No Hashboard config files were found, and empty builds were not enabled, so the build was aborted."
        ):
            error += "\n\tTo enable empty builds, use the --allow-dangerous-empty-build flag.\n\tWARNING: This will remove all data-ops managed resources, and any resources that depend on them, from your project."
            from hashboard.cli import _echo_build_errors_and_exit

            _echo_build_errors_and_exit([error])

        raise ClickException(f"Error received from the Hashboard server:\n  {error}")

    return results


def upload_files_to_hashboard(session: Session, project_id: str, path: str) -> str:
    return _post_file(session, project_id, path)


def _is_over_filesize_limit(file_path: str) -> bool:
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    return size_in_mb > FILE_SIZE_LIMIT_MB


def _post_file(session: Session, project_id: str, file_path: str) -> str:
    if _is_over_filesize_limit(file_path):
        raise ClickException(
            f"File exceeds upload limit of {FILE_SIZE_LIMIT_MB} megabytes"
        )

    r = session.post(
        HASHBOARD_BASE_URI + "/upload/data-file",
        data={"projectId": project_id},
        files={"file": open(file_path, "rb")},
        headers={"Glean-CLI-Version": VERSION},
    )

    results = r.json()
    file_errors = results.get("error")
    if file_errors:
        raise ClickException(f"Error uploading file\n  {file_errors}")

    uploaded_filename = results.get("filename")

    if uploaded_filename:
        return uploaded_filename
    else:
        raise ClickException(f"Error uploading file\n  Unexpected result from server")


def export_query(
    session: Session, endpoint: str, data: dict, additional_headers: dict = {}
):
    """POST request to export controllers"""
    r = session.post(
        HASHBOARD_BASE_URI + f"/export/{endpoint}",
        data=json.dumps(data),
        headers={"Glean-CLI-Version": VERSION, **additional_headers},
    )
    if r.status_code != 200:
        raise ClickException("Unexpected error received from the Hashboard server.")
    return r.text


def remove_from_data_ops_mutation(
    session: Session, project_id: str, grns: List[str]
) -> dict:
    # Assumes that error handling occurs a level up
    return _graphql_query(
        session,
        """
        mutation RemoveFromManagedByDataOps($projectId: String!, $grns: [String]!) {
          removeFromManagedByDataOps(projectId: $projectId, grns: $grns)
        }
        """,
        {"projectId": project_id, "grns": grns},
    )["data"]
