import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Tuple

import click
from dateutil.parser import ParserError, parse

from tinybird.ch import (
    HTTPClient,
    TablesToSwap,
    _create_materialized_view_query,
    _generate_ch_swap_tables_sql,
    ch_create_materialized_view_sync,
    ch_drop_view,
    ch_guarded_query,
    ch_swap_tables_sync,
    ch_table_exists_sync,
)
from tinybird.datasource import Datasource
from tinybird.user import User as Workspace
from tinybird.user import UserDoesNotExist, Users

from ... import common
from ..cli_base import cli


def _query_count(
    workspace: Workspace,
    ds: Datasource,
    reference_time_column: str,
    reference_time_value: datetime,
    populate_value_old: datetime,
) -> Tuple[int, int]:
    sql_count = f"""
SELECT countIf({reference_time_column} < '{reference_time_value}') as c_pre,
    countIf({reference_time_column} >= '{reference_time_value}') as c_post
FROM {workspace.database}.{ds.id}
WHERE {reference_time_column} >= '{populate_value_old}'
FORMAT JSON
    """
    client = HTTPClient(workspace.database_server, database=workspace.database)
    _, body = client.query_sync(sql_count)
    result = json.loads(body)
    return int(result["data"][0]["c_pre"]), int(result["data"][0]["c_post"])


class PaginationAvailableValue(Enum):
    # to be improved once we have more use cases
    DAY = "day"


def _validate_pagination(
    populate_value_old: datetime, reference_time_value: datetime, populate_pagination: str
) -> PaginationAvailableValue:
    """
    >>> _validate_pagination('2022-01-01 18:01:02', '2022-02-01 17:01:02', 'day')
    <PaginationAvailableValue.DAY: 'day'>
    >>> _validate_pagination('2022-02-01 18:01:02', '2022-01-01 17:01:02', 'day')
    Traceback (most recent call last):
    ...
    click.exceptions.ClickException: Populate old value can't be more recent than the reference value
    >>> _validate_pagination('2022-01-01 18:01:02', '2022-02-01 17:01:02', 'not_recognized')
    Traceback (most recent call last):
    ...
    click.exceptions.ClickException: Pagination value not supported. Supported ones: ['day']
    """
    if populate_value_old >= reference_time_value:
        raise click.ClickException("Populate old value can't be more recent than the reference value")

    try:
        pagination_value_class = PaginationAvailableValue(populate_pagination)
    except ValueError:
        raise click.ClickException(
            f"Pagination value not supported. Supported ones: {[val.value for val in PaginationAvailableValue]}"
        )

    return pagination_value_class


def _move_to_start_of_day_period(the_date: datetime) -> datetime:
    """
    >>> _move_to_start_of_day_period(datetime(2023,1,1,15,30))
    datetime.datetime(2023, 1, 1, 0, 0)
    """
    return datetime(the_date.year, the_date.month, the_date.day)


def _prepare_timeframes(
    populate_value_old: datetime, reference_time_value: datetime, populate_pagination: PaginationAvailableValue
) -> List[Tuple[datetime, datetime]]:
    """
    >>> _prepare_timeframes(datetime(2023,1,1), datetime(2023,1,1), PaginationAvailableValue.DAY)
    []
    >>> _prepare_timeframes(datetime(2023,1,1), datetime(2023,1,3), PaginationAvailableValue.DAY)
    [(datetime.datetime(2023, 1, 1, 0, 0), datetime.datetime(2023, 1, 2, 0, 0)), (datetime.datetime(2023, 1, 2, 0, 0), datetime.datetime(2023, 1, 3, 0, 0))]
    >>> _prepare_timeframes(datetime(2023,1,1), datetime(2023,1,3,10,30), PaginationAvailableValue.DAY)
    [(datetime.datetime(2023, 1, 1, 0, 0), datetime.datetime(2023, 1, 2, 0, 0)), (datetime.datetime(2023, 1, 2, 0, 0), datetime.datetime(2023, 1, 3, 0, 0)), (datetime.datetime(2023, 1, 3, 0, 0), datetime.datetime(2023, 1, 3, 10, 30))]
    >>> _prepare_timeframes(datetime(2023,1,1,9,15), datetime(2023,1,3,10,30), PaginationAvailableValue.DAY)
    [(datetime.datetime(2023, 1, 1, 9, 15), datetime.datetime(2023, 1, 2, 0, 0)), (datetime.datetime(2023, 1, 2, 0, 0), datetime.datetime(2023, 1, 3, 0, 0)), (datetime.datetime(2023, 1, 3, 0, 0), datetime.datetime(2023, 1, 3, 10, 30))]
    """
    timeframes = []
    if populate_pagination == PaginationAvailableValue.DAY:
        time_delta = timedelta(days=1)
        move_to_start_of_period = _move_to_start_of_day_period
    else:
        raise Exception("Populate Pagination method used is incompatible")
    while populate_value_old < reference_time_value:
        new_date = populate_value_old + time_delta
        new_date = move_to_start_of_period(new_date)
        if new_date < reference_time_value:
            timeframes.append((populate_value_old, new_date))
            populate_value_old = new_date
        else:
            timeframes.append((populate_value_old, reference_time_value))
            break
    return timeframes


@cli.command(
    help=(
        "Populate and exchange two datasource in same workspace and with scheme compatible. Useful when changing"
        " sorting key or partitionin"
    )
)
@click.argument("workspace_id")
@click.option(
    "--datasource-name", required=True, type=str, help="Datasource name where exchange is doing to take place"
)
@click.option(
    "--datasource-tmp-name",
    required=True,
    type=str,
    help="Temporary datasource name where table is goind to be populate to be echanged",
)
@click.option("--reference-time-column", required=True, type=str, help="Column to control populate")
@click.option(
    "--reference-time-value",
    required=True,
    type=str,
    help=(
        "Time reference to control populate. Will be used in the Materialized view as starting point in the future to"
        " fill the new table"
    ),
)
@click.option(
    "--populate-value-old",
    required=True,
    type=str,
    help="Will be used in the populates to limit the amount of old data that will be copied from the old table",
)
@click.option("--populate-pagination", required=True, type=str, help="Size of the pages used for each populate query")
@click.option("--populate-timeout", required=True, type=int, help="Timeout for populating")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--yes", is_flag=True)
@click.option("--dry-run", is_flag=True)
def populate_and_exchange_datasource(
    workspace_id: str,
    datasource_name: str,
    datasource_tmp_name: str,
    reference_time_column: str,
    reference_time_value: str,
    populate_value_old: str,
    populate_pagination: str,
    populate_timeout: int,
    config: click.Path,
    yes: bool,
    dry_run: bool,
):
    # TODO when creating dates, the timezone selected is the one from the laptop but CH may store the values already in UTC

    common.setup_redis_client(config)
    try:
        workspace = Users.get_by_id(workspace_id)

    except UserDoesNotExist:
        click.secho(f"Workspace {workspace_id} doesn't exists", fg="red")
        return

    datasource = workspace.get_datasource(datasource_name)
    datasource_tmp = workspace.get_datasource(datasource_tmp_name)
    if datasource is None or datasource_tmp is None:
        click.secho(f"Datasource not found in {workspace.name}")
        return

    try:
        populate_value_old_datetime = parse(populate_value_old)
    except ParserError:
        click.secho(f"Parameter populate-value-old doesn't have a supported datetime format: {populate_value_old}")
        return

    try:
        reference_time_value_datetime = parse(reference_time_value)
    except ParserError:
        click.secho(f"Parameter reference-time-value doesn't have a supported datetime format: {reference_time_value}")
        return

    populate_pagination_value = _validate_pagination(
        populate_value_old_datetime, reference_time_value_datetime, populate_pagination
    )

    # Create the MV to start filling the new table with the data that is coming to the old one.
    temporal_view_name = f"for_exchange_{datasource.name}_to_{datasource_tmp.name}"

    if yes or click.confirm(
        f"- Creating view '{workspace.database}.{temporal_view_name}' to populate {datasource_tmp.name} from"
        f" {datasource.name} using {reference_time_column} >= '{reference_time_value}'. Are you sure?"
    ):
        sql = f"""SELECT *
                FROM {workspace.database}.{datasource.id}
                WHERE {reference_time_column} >= '{reference_time_value}'
                """

        view_exists = ch_table_exists_sync(temporal_view_name, workspace.database_server, workspace.database)
        if view_exists:
            recreate = click.confirm("- View already exists. Do you want to recreate it?")

            if recreate:
                if not dry_run:
                    asyncio.run(
                        ch_drop_view(
                            workspace.database_server, workspace.database, temporal_view_name, workspace.cluster
                        )
                    )
                click.secho(
                    f"{'[DRY RUN] ' if dry_run else ''}Old view '{workspace.database}.{temporal_view_name}' dropped",
                    fg="green",
                )
                view_exists = False

        if not view_exists:
            if dry_run:
                create_view_query = _create_materialized_view_query(
                    workspace.database,
                    temporal_view_name,
                    sql,
                    target_table=datasource_tmp.id,
                    cluster=workspace.cluster,
                    if_not_exists=True,
                )
                click.secho(f"[DRY RUN] running: {create_view_query}", fg="cyan")
            else:
                ch_create_materialized_view_sync(
                    database_server=workspace.database_server,
                    database=workspace.database,
                    view_name=temporal_view_name,
                    sql=sql,
                    target_table=datasource_tmp.id,
                    cluster=workspace.cluster,
                    if_not_exists=True,
                    **workspace.ddl_parameters(skip_replica_down=True),
                )
                click.secho(f"View '{workspace.database}.{temporal_view_name}' created", fg="green")
    else:
        return

    # Wait until the MV is loading the data.
    click.secho("Checking if the MV is loading the data...")

    def check_mv_status_is_inserting() -> bool:
        assert isinstance(datasource, Datasource)
        assert isinstance(datasource_tmp, Datasource)
        _, ds_tmp_post = _query_count(
            workspace, datasource_tmp, reference_time_column, reference_time_value_datetime, populate_value_old_datetime
        )
        if ds_tmp_post == 0:
            click.secho(
                (
                    f"Still not inserting in {datasource_tmp.name}. Wait to : {reference_time_column} >="
                    f" '{reference_time_value}"
                ),
                fg="yellow",
            )
            return False
        else:
            click.secho(f"Already inserting into {datasource_tmp.name}: {ds_tmp_post} ", fg="green")
            return True

    check_mv_status_is_inserting()
    if not yes:
        while click.confirm("- Check again if view is already materializing?", default=True):
            is_inserting = check_mv_status_is_inserting()
            if is_inserting and click.confirm(
                f"- Do you want to continue doing backfill from '{reference_time_column}' >="
                f" {populate_value_old_datetime} and '{reference_time_column}' < {reference_time_value_datetime} to"
                f" {datasource_tmp.name}. If you say no, the command will continue checking if the MV is"
                " materializing."
            ):
                break

    # Prepare partitions
    timeframes = _prepare_timeframes(
        populate_value_old_datetime, reference_time_value_datetime, populate_pagination_value
    )

    filter_per_frame = [
        f"'{frame[0]}' <= {reference_time_column} and {reference_time_column} < '{frame[1]}'" for frame in timeframes
    ]

    click.secho(
        f"- Preparing insert for old data from {datasource.name} to populate {datasource_tmp.name} using the following"
        " timeframes:"
    )
    for filter in filter_per_frame:
        click.secho(f"    - {filter}.")

    # Start the populate with the new data
    if yes or click.confirm("- Are you sure?"):
        for frame in filter_per_frame:
            insert_sql = f"""INSERT INTO {workspace.database}.{datasource_tmp.id}
                                SELECT *
                                FROM {workspace.database}.{datasource.id}
                                WHERE {frame}
                        """

            click.secho(f"{'[DRY RUN] ' if dry_run else ' '}Running: {insert_sql}", fg="cyan")
            if not dry_run:
                assert isinstance(workspace.cluster, str)
                _, query_finish = ch_guarded_query(
                    workspace.database_server,
                    workspace.database,
                    insert_sql,
                    workspace.cluster,
                    populate_timeout,
                    retries=False,
                )
                if query_finish:
                    click.secho("Query finished", fg="green")
        click.secho("Populate finished", fg="green")
    else:
        return

    # Check if populate finished correctly.
    click.secho("Checking count of rows between the two tables...")

    def check_count() -> None:
        assert isinstance(datasource, Datasource)
        assert isinstance(datasource_tmp, Datasource)
        ds_pre, ds_post = _query_count(
            workspace, datasource, reference_time_column, reference_time_value_datetime, populate_value_old_datetime
        )
        ds_tmp_pre, ds_tmp_post = _query_count(
            workspace, datasource_tmp, reference_time_column, reference_time_value_datetime, populate_value_old_datetime
        )
        if (ds_pre + ds_post) == (ds_tmp_pre + ds_tmp_post):
            click.secho(
                (
                    f"Same count {datasource.name}:{ds_pre} + {ds_post} == {datasource_tmp.name}:{ds_tmp_pre} +"
                    f" {ds_tmp_post}"
                ),
                fg="green",
            )
        else:
            click.secho(
                (
                    f"Not same count {datasource.name}:{ds_pre} + {ds_post} != {datasource_tmp.name}:{ds_tmp_pre} +"
                    f" {ds_tmp_post}"
                ),
                fg="red",
            )

    check_count()
    if not yes:
        while click.confirm("Do you want to check again the count?", default=True):
            check_count()

    # Swap the tables
    tables_to_swap = [
        TablesToSwap(common_database=workspace.database, old_table=datasource.id, new_table=datasource_tmp.id)
    ]

    if yes or click.confirm(f"- Exchange tables between {datasource.name} and {datasource_tmp.name}"):
        if dry_run:
            query_exchange = _generate_ch_swap_tables_sql(tables_to_swap, workspace.cluster)
            click.secho(f"[DRY RUN] exchange: {query_exchange}", fg="cyan")
        else:
            ch_swap_tables_sync(
                workspace.database_server,
                tables_to_swap,
                workspace.cluster,
                **workspace.ddl_parameters(skip_replica_down=True),
            )
            click.secho(f"Swapped datasources tables {datasource.name} and {datasource_tmp.name}", fg="green")

    if yes or click.confirm(f"- Removing view {temporal_view_name}'. Are you sure?"):
        if dry_run:
            click.secho(f"[DRY RUN] running: droping '{workspace.database}.{temporal_view_name}'", fg="cyan")
        else:
            asyncio.run(
                ch_drop_view(
                    database_server=workspace.database_server,
                    database=workspace.database,
                    view_name=temporal_view_name,
                    cluster=workspace.cluster,
                )
            )
            click.secho(f"{workspace.database}.{temporal_view_name} dropped", fg="green")
