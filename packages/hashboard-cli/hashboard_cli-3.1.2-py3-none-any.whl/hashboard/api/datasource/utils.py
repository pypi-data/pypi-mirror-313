from copy import deepcopy
from enum import Enum
import pathlib
import click

from hashboard.api import (
    create_data_source,
    login,
    test_data_source,
    update_data_source,
)
from hashboard.credentials import get_credentials
from hashboard.session import get_current_session


# Make sure this stays consistent with glean/db/database_types.py
class DatabaseTypes(Enum):
    ATHENA = "athena"
    BIGQUERY = "big_query"
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SNOWFLAKE = "snowflake"
    DUCKDB = "duckdb"
    CLICKHOUSE = "clickhouse"
    MOTHERDUCK = "motherduck"
    DATABRICKS = "databricks"
    REDSHIFT = "redshift"


def mutate_datasource_from_subtype(
    ctx, subtype: DatabaseTypes, is_update: bool = False, **kwargs
):
    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])

    datasource_kwargs = deepcopy(kwargs)

    def replace_field(old_field_name, new_field_name):
        if old_field_name in datasource_kwargs:
            datasource_kwargs[new_field_name] = datasource_kwargs[old_field_name]
            del datasource_kwargs[old_field_name]

    # Converting user-friendly external argument names to our internal datasource fields
    kwarg_replacements = {
        "password": "secretCredential",
        "aws_region": "athenaRegionName",
        "s3_staging_dir": "athenaS3StagingDir",
        "aws_access_key_id": "athenaAWSAccessKeyID",
        "aws_secret_access_key": "secretCredential",
        "additional_query_params": "additionalQueryParams",
        "service_token": "secretCredential",
        "http_path": "httpPath",
        "access_token": "secretCredential",
        "catalog": "database",
    }

    if subtype == DatabaseTypes.BIGQUERY:
        json_key_filepath = kwargs["json_key"]
        if pathlib.Path(json_key_filepath).suffix != ".json":
            raise Exception("BigQuery JSON key must be a .json file.")
        with open(json_key_filepath, "r") as f:
            json_file = f.read()
            datasource_kwargs["secretCredential"] = json_file
        del datasource_kwargs["json_key"]
    else:
        for old_field_name, new_field_name in kwarg_replacements.items():
            replace_field(old_field_name, new_field_name)

    datasource = {
        "project": project_id,
        "type": "glean_database",
        "subType": subtype.value,
        **datasource_kwargs,
    }

    from hashboard.cli import _echo_datasource_creation_errors_and_exit

    try:
        if is_update:
            update_data_source(s, datasource)
            click.echo(f"📊 Successfully updated data source: {kwargs['name']}.")
        else:
            create_data_source(s, datasource)
            click.echo(f"📊 Successfully created data source: {kwargs['name']}.")
        _test(s, kwargs["name"], project_id)
    except Exception as e:
        _echo_datasource_creation_errors_and_exit([str(e)])


def _test(s, name, project_id):
    click.echo(f"🔍 Testing connection to {name}...")
    try:
        test_data_source(s, name, project_id)
        click.echo(f"🎉 Successfully connected to {name}.")
    except Exception as e:
        click.echo(f"❌ {e}")


# Common fields
data_source_name = click.option(
    "--name",
    type=str,
    required=True,
    help="""The user-facing name for the Hashboard data source you are creating.""",
    prompt=True,
)
data_source_user = click.option(
    "--user",
    type=str,
    required=True,
    help="""The user used to connect to the data source.""",
    prompt=True,
)
data_source_password = click.option(
    "--password",
    type=str,
    required=True,
    help="""The password used to connect to the data source.""",
    prompt=True,
    hide_input=True,
)


def data_source_db(required: bool):
    return click.option(
        "--database",
        type=str,
        required=required,
        help="""The name of the database to read from.""",
        prompt=True,
    )


data_source_schema = click.option(
    "--schema",
    type=str,
    required=False,
    help="""Specify a schema to limit which tables are available. 
    Otherwise, Hashboard will make all accessible schemas and tables available.""",
    prompt=True,
)
data_source_host = click.option(
    "--host",
    type=str,
    required=True,
    help="""The address of your database.""",
    prompt=True,
)


def data_source_port(default_port: str, required: bool):
    return click.option(
        "--port",
        type=str,
        required=required,
        help=f"""The port used to connect to your data source. Default port: {default_port}""",
        prompt=True,
    )


data_source_id = click.option(
    "--id",
    type=str,
    required=True,
    help="""The Hashboard ID of the data source you want to update. You can find this ID by running `hb datasource ls`.""",
    prompt=True,
)

# Bigquery-specific fields
bigquery_json_key = click.option(
    "--json_key",
    required=True,
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
    help="""A path to a JSON file containing the BigQuery service account JSON key.""",
)

# Snowflake-specific fields
snowflake_account = click.option(
    "--account",
    required=True,
    type=str,
    help="""
    Your snowflake account identifier (opens in a new tab) is provided by Snowflake and
    included in the start of the URL you use to login to Snowflake: <account_identifier>.snowflakecomputing.com.
    """,
    prompt=True,
)

snowflake_warehouse = click.option(
    "--warehouse",
    required=True,
    type=str,
    help="""The warehouse to use in Snowflake. Warehouses correspond with compute resources.""",
    prompt=True,
)
snowflake_role = click.option(
    "--role",
    required=True,
    type=str,
    prompt=True,
)

# Athena-specific fields
athena_aws_region = click.option(
    "--aws_region",
    type=str,
    required=True,
    help="""The AWS region to use to query data.""",
    prompt=True,
)
athena_port = click.option(
    "--port",
    type=str,
    required=False,
    help="""The port to connect to.""",
    prompt=True,
)
athena_staging_directory = click.option(
    "--s3_staging_dir",
    type=str,
    required=True,
    help="""The S3 path where Athena will store query results.""",
    prompt=True,
)
athena_aws_access_key_id = click.option(
    "--aws_access_key_id",
    type=str,
    required=True,
    help="""The IAM user's access key.""",
    prompt=True,
)
athena_aws_secret_access_key = click.option(
    "--aws_secret_access_key",
    type=str,
    required=True,
    help="""The IAM user's scret access key.""",
    prompt=True,
    hide_input=True,
)
athena_query_parameters = click.option(
    "--additional_query_params",
    type=str,
    help="""Additional database connection parameters in the format workGroup=value&param=value.""",
    required=False,
    prompt=True,
)

# Motherduck-specific fields
motherduck_service_token = click.option(
    "--service_token",
    type=str,
    required=True,
    help="""Your MotherDuck service token.""",
    hide_input=True,
    prompt=True,
)

# Databricks-specific fields
databricks_http_path = click.option(
    "--http_path",
    type=str,
    required=True,
    help="""The HTTP path of the SQL warehouse. Can be found in the Connection Details tab of your SQL warehouse.""",
    prompt=True,
)
databricks_access_token = click.option(
    "--access_token",
    type=str,
    required=True,
    help="""A personal access token generated in Databricks for a user with access to the data you want to query.""",
    hide_input=True,
    prompt=True,
)
databricks_catalog = click.option(
    "--catalog",
    type=str,
    required=True,
    help="""The Databricks catalog within the warehouse to connect to.""",
    prompt=True,
)

# Clickhouse-specific fields
clickhouse_protocol = click.option(
    "--protocol",
    type=str,
    required=True,
    help="""The protocol used to connect to your data source. Should be one of "https", "https-no-verify", or "native".""",
    prompt=True,
)


def bigquery_arguments(func):
    @data_source_name
    @bigquery_json_key
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def snowflake_arguments(func):
    @data_source_name
    @snowflake_account
    @data_source_user
    @data_source_password
    @data_source_db(required=True)
    @data_source_schema
    @snowflake_warehouse
    @snowflake_role
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def postgres_arguments(func):
    @data_source_name
    @data_source_host
    @data_source_port(default_port="5432", required=True)
    @data_source_user
    @data_source_password
    @data_source_db(required=True)
    @data_source_schema
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def athena_arguments(func):
    @data_source_name
    @athena_aws_region
    @athena_port
    @data_source_schema
    @athena_staging_directory
    @athena_aws_access_key_id
    @athena_aws_secret_access_key
    @athena_query_parameters
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def clickhouse_arguments(func):
    @data_source_name
    @data_source_port(default_port="9440", required=True)
    @data_source_host
    @data_source_user
    @data_source_password
    @clickhouse_protocol
    @data_source_db(required=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mysql_arguments(func):
    @data_source_name
    @data_source_host
    @data_source_port(default_port="3306", required=True)
    @data_source_user
    @data_source_password
    @data_source_db(required=False)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def motherduck_arguments(func):
    @data_source_name
    @motherduck_service_token
    @data_source_db(required=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def databricks_arguments(func):
    @data_source_name
    @data_source_host
    @data_source_port(default_port="443", required=False)
    @databricks_http_path
    @databricks_access_token
    @databricks_catalog
    @data_source_schema
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
