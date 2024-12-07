import os
from hashboard.api import get_datasources, login, upload_files_to_hashboard
from hashboard.api.analytics.cli_with_tracking import CommandWithTracking, GroupWithTracking
from hashboard.api.datasource.utils import DatabaseTypes, _test, athena_arguments, bigquery_arguments, clickhouse_arguments, mutate_datasource_from_subtype, databricks_arguments, motherduck_arguments, mysql_arguments, postgres_arguments, snowflake_arguments, data_source_id
from hashboard.credentials import get_credentials
from hashboard.session import get_current_session
import click

@click.group(cls=GroupWithTracking)
@click.pass_context
def datasource(ctx):
    """Commands for managing Hashboard data sources."""
    pass

@datasource.command("ls", cls=CommandWithTracking)
@click.pass_context
def list_datasources(ctx):
    """See your available database connections.

    A database connection can be added in the Settings tab on hashboard.com."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    datasources = get_datasources(s, project_id)

    from hashboard.cli import _echo_datasources
    _echo_datasources(datasources)

# Commands for create are defined in datasource_management.py
@datasource.group(
    "create", 
    cls=GroupWithTracking,
    context_settings=dict(),
)
@click.pass_context
def create(ctx):
    """Commands for creating Hashboard data sources."""
    pass

@datasource.group(
    "update",
    cls=GroupWithTracking,
    context_settings=dict(),
)
@click.pass_context
def update(ctx):
    """Commands for updating existing Hashboard data sources."""
    pass

@create.command("bigquery")
@bigquery_arguments
@click.pass_context
def create_bigquery(ctx, **kwargs):
    """Create a BigQuery data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/bigquery
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.BIGQUERY, **kwargs)


@update.command("bigquery")
@data_source_id
@bigquery_arguments
@click.pass_context
def update_bigquery(ctx, **kwargs):
    """Update a BigQuery data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/bigquery
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.BIGQUERY, is_update=True, **kwargs)

@create.command("snowflake")
@snowflake_arguments
@click.pass_context
def create_snowflake(ctx, **kwargs):
    """Create a Snowflake data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/snowflake
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.SNOWFLAKE, **kwargs)

@update.command("snowflake")
@data_source_id
@snowflake_arguments
@click.pass_context
def update_snowflake(ctx, **kwargs):
    """Update a Snowflake data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/snowflake
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.SNOWFLAKE, is_update=True, **kwargs)

@create.command("postgres")
@postgres_arguments
@click.pass_context
def create_postgres(ctx, **kwargs):
    """Create a Postgres data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.POSTGRES, **kwargs)

@update.command("postgres")
@data_source_id
@postgres_arguments
@click.pass_context
def update_postgres(ctx, **kwargs):
    """Update a Postgres data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.POSTGRES, is_update=True, **kwargs)

@create.command("redshift")
@postgres_arguments
@click.pass_context
def create_redshift(ctx, **kwargs):
    """Create a Redshift data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.REDSHIFT, **kwargs)

@update.command("redshift")
@data_source_id
@postgres_arguments
@click.pass_context
def update_redshift(ctx, **kwargs):
    """Update a Redshift data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/postgresql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.REDSHIFT, is_update=True, **kwargs)

@create.command("athena")
@athena_arguments
@click.pass_context
def create_athena(ctx, **kwargs):
    """Create an Athena data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/athena
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.ATHENA, **kwargs)

@update.command("athena")
@data_source_id
@athena_arguments
@click.pass_context
def update_athena(ctx, **kwargs):
    """Update an Athena data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/athena
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.ATHENA, is_update=True, **kwargs)

@create.command("clickhouse")
@clickhouse_arguments
@click.pass_context
def create_clickhouse(ctx, **kwargs):
    """Create a Clickhouse data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/clickhouse
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.CLICKHOUSE, **kwargs)

@update.command("clickhouse")
@data_source_id
@clickhouse_arguments
@click.pass_context
def update_clickhouse(ctx, **kwargs):
    """Update a Clickhouse data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/clickhouse
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.CLICKHOUSE, is_update=True, **kwargs)

@create.command("mysql")
@mysql_arguments
@click.pass_context
def create_mysql(ctx, **kwargs):
    """Create a MySql data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/mysql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.MYSQL, **kwargs)

@update.command("mysql")
@data_source_id
@mysql_arguments
@click.pass_context
def update_mysql(ctx, **kwargs):
    """Update a MySQL data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/mysql
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.MYSQL, is_update=True, **kwargs)

@create.command("motherduck")
@motherduck_arguments
@click.pass_context
def create_motherduck(ctx, **kwargs):
    """Create a MotherDuck data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/motherduck
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.MOTHERDUCK, **kwargs)

@update.command("motherduck")
@data_source_id
@motherduck_arguments
@click.pass_context
def update_motherduck(ctx, **kwargs):
    """Update a MotherDuck data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/motherduck
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.MOTHERDUCK, is_update=True, **kwargs)

@create.command("databricks")
@databricks_arguments
@click.pass_context
def create_databricks(ctx, **kwargs):
    """Create a Databricks data connection in your project. 
    More info: https://docs.hashboard.com/docs/database-connections/databricks
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.DATABRICKS, **kwargs)

@update.command("databricks")
@data_source_id
@databricks_arguments
@click.pass_context
def update_databricks(ctx, **kwargs):
    """Update a Databricks data connection in your project. 
    The ID of the connection you provide must match the ID of an existing connection.
    More info: https://docs.hashboard.com/docs/database-connections/databricks
    """
    mutate_datasource_from_subtype(ctx, DatabaseTypes.DATABRICKS, is_update=True, **kwargs)

@datasource.command(
    "upload",
    cls=CommandWithTracking,
    context_settings=dict(),
)
@click.argument(
    "filepaths",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
)
@click.pass_context
def upload(ctx, filepaths):
    """
    Upload file(s) to Hashboard that can be queried using duckdb and
    used as the basis for a data model.
    """

    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])

    files_noun = f"{len(filepaths)} file{'' if len(filepaths) == 1 else 's'}"
    click.echo(f"📄 Uploading {files_noun} to Hashboard...")
    for filepath in filepaths:
        fp = os.path.expanduser(filepath)
        uploaded_name = upload_files_to_hashboard(s, project_id, fp)
        click.echo(f'   Uploaded "{uploaded_name}"')
    click.echo(f"✅ Successfully uploaded {files_noun}.")

@datasource.command(
    "test",
    cls=CommandWithTracking,
    context_settings=dict(),
)
@click.argument(
    "name",
    required=True,
    type=str,
)
@click.pass_context
def test(ctx, name):
    """Test a data connection by its name."""
    s = get_current_session()
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    project_id = login(s, ctx.obj["credentials"])
    _test(s, name, project_id)
