import json
import logging
import re
import traceback
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from toposort import toposort

from tinybird.ch_utils.constants import CH_SETTINGS_JOIN_ALGORITHM_HASH
from tinybird.metrics.statsd_replaces_metrics import StatsdReplacesMetrics
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client

from .ch import (
    MAX_EXECUTION_TIME_CLUSTER_INSTANCES_SECONDS,
    VALID_WAIT_VALUES,
    WAIT_ALTER_REPLICATION_OWN,
    CHException,
    CHReplication,
    CHTable,
    CHTableLocation,
    HTTPClient,
    TablesToSwap,
    TablesToSwapWithWorkspace,
    ch_attach_partitions_sync,
    ch_create_materialized_view_sync,
    ch_create_null_table_with_mv_for_mv_populate,
    ch_create_table_as_table_sync,
    ch_drop_table_sync,
    ch_get_cluster_instances_sync,
    ch_get_columns_from_query_sync,
    ch_get_replicas_for_table_sync,
    ch_replace_partitions_sync,
    ch_source_table_for_view_sync,
    ch_swap_tables_sync,
    ch_table_dependent_views_sync,
    ch_table_details,
    ch_table_partitions_sync,
    ch_wait_for_mutations_sync,
    create_quarantine_table_from_landing_sync,
    url_from_host,
)
from .ch_utils.engine import TableDetails
from .datasource import Datasource
from .feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from .hook_resources import HookException
from .job import ImportJob, Job, sanitize_database_server
from .limits import Limit
from .matview_checks import origin_column_type_is_compatible_with_destination_type
from .pg import PGService
from .pipe import Pipe, PipeNode
from .resource import Resource
from .timing import Timer
from .tracker import HookLogEntry, OpsLogEntry
from .user import User, Users, public

DEFAULT_BATCH_EXECUTION_TIME = 60 * 3


def could_not_find_query_to_populate_depending_view_exception(dependent_view_name: str) -> RuntimeError:
    return RuntimeError(f"Could not find query to populate depending view: {dependent_view_name}")


def could_not_find_dependent_table_to_populate_exception(
    pipe_name: str, node_name: str, node_id: str, node_materialized: str
) -> RuntimeError:
    return RuntimeError(
        f"Could not find the dependent table to populate: [{pipe_name}]:{node_name}[{node_id}]"
        f" points to {node_materialized} but it does not exist"
    )


class HookStatsdLogs(Enum):
    FULL_CASCADE_REPLACES_ERROR = "tinybird-app.full-cascade-replaces-error"


class Hook:
    HOOK_METHODS = {
        "before_create",
        "after_create",
        "before_append",
        "after_append",
        "before_delete",
        "after_delete",
        "before_truncate",
        "after_truncate",
        "before_delete_with_condition",
        "after_delete_with_condition",
        "before_alter_datasource",
        "after_alter_datasource",
    }

    def __init__(self, user: User):
        self.user_id = user.id
        self.user = user
        self.hook_id = str(uuid.uuid4())
        self.start = datetime.now(timezone.utc)
        self.log: List[HookLogEntry] = []
        self.ops_log: List[OpsLogEntry] = []
        self.on_error_invoked = False
        self.tear_down_invoked = False
        self.table_locations_to_drop: List[CHTableLocation] = []
        self.ops_log_options: Dict[Any, Any] = {}

    def __getstate__(self):
        state = self.__dict__.copy()
        if "user" in state:
            del state["user"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if "user" in state:
            self.user_id = state["user"].id
        self.user = User.get_by_id(self.user_id)

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if name == "on_error" and callable(attr):

            def newfunc(datasource, error):
                if self.on_error_invoked:
                    logging.warning("Method on_error already called")
                    return
                self.on_error_invoked = True
                result = None
                try:
                    result = attr(datasource, error)
                except Exception as e:
                    logging.exception(f"Failed to call on_error method: {e}")
                finally:
                    self.tear_down(datasource)
                return result

            return newfunc
        elif name == "tear_down" and callable(attr):

            def newfunc(datasource):  # type: ignore
                if self.tear_down_invoked:
                    logging.warning("Method tear_down already called")
                    return
                self.tear_down_invoked = True
                result = None
                try:
                    result = attr(datasource)
                except Exception as e:
                    logging.exception(f"Failed to call tear_down method: {e}")
                return result

            return newfunc
        elif name in Hook.HOOK_METHODS and callable(attr):

            def newfunc(datasource: Any, **kwargs: Any) -> Any:  # type: ignore
                with Timer(f"<{self.hook_id}> {self.__class__.__name__}.{attr.__name__}") as timing:
                    error = None
                    try:
                        result = attr(datasource, **kwargs)
                    except Exception as e:
                        error = e
                self.log_event(datasource, attr.__name__, timing, error)
                if error:
                    self.on_error(datasource, error)
                else:
                    try:
                        attribute_name = f"{name}_ops_log"
                        if hasattr(self, attribute_name):
                            log_method = object.__getattribute__(self, attribute_name)
                            if callable(log_method):
                                log_method(datasource, **kwargs)
                    except AttributeError as e:
                        logging.debug(f"Failed to call log method: {e}")
                    except Exception as e:
                        logging.exception(f"Failed to call log method: {e}")
                if error:
                    raise error
                return result

            return newfunc
        else:
            return attr

    def log_event(
        self, datasource: Datasource, operation: str, timing: Timer, error: Optional[Exception] = None
    ) -> None:
        # We try to get the real data source because sometimes you are using a
        # temporal or auxiliar data source, e.g. when replacing data, that uses
        # a different/temporal internal identifier.
        # This is a best-effort approach.
        actual_datasource = self.user.get_datasource(datasource.name) or datasource
        self.log.append(
            HookLogEntry(
                hook_id=self.hook_id,
                name=self.__class__.__name__,
                operation=operation,
                datasource_id=actual_datasource.id,
                datasource_name=actual_datasource.name,
                workspace_id=self.user.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                workspace_email=self.user["email"] if "email" in self.user else self.user.name,  # noqa: SIM401
                timestamp=timing.start,
                elapsed=timing.interval,
                status="error" if error else "done",
                error=str(error) if error else None,
            )
        )

    def log_operation(
        self,
        event_type,
        datasource: Datasource,
        rows=None,
        rows_quarantine=None,
        error=None,
        options=None,
        elapsed_time=None,
        workspace=None,
        use_tracker=False,
        update_with_blocks=False,
        pipe_id=None,
        pipe_name=None,
    ) -> None:
        options = self.ops_log_options if not options else {**self.ops_log_options, **options}
        result = "error" if error else "ok"

        if event_type in ["append", "replace"]:
            start_time = self.start + timedelta(seconds=1)
        else:
            start_time = self.start

        workspace = workspace or self.user

        self.ops_log.append(
            OpsLogEntry(
                start_time=start_time,
                event_type=event_type,
                datasource_id=datasource.id,
                datasource_name=datasource.name,
                workspace_id=workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                workspace_email=self.user["email"] if "email" in self.user else self.user.name,  # noqa: SIM401\
                result=result,
                elapsed_time=(datetime.now(timezone.utc) - self.start).total_seconds()
                if not elapsed_time
                else elapsed_time,
                error=str(error) if error else None,
                rows=rows,
                rows_quarantine=rows_quarantine,
                options=options,
                use_tracker=use_tracker,
                update_with_blocks=update_with_blocks,
                pipe_id=pipe_id,
                pipe_name=pipe_name,
            )
        )

    def get_rows(self, datasource: Datasource) -> Tuple[int, int]:
        info = self._get_rows_in_tables([datasource.id, datasource.id + "_quarantine"])
        rows = info.get(datasource.id, 0)
        rows_quarantine = info.get(datasource.id + "_quarantine", 0)
        return rows, rows_quarantine

    def _get_rows_in_tables(self, table_names: List[str]) -> Dict[str, int]:
        query = f"""
            SELECT name, total_rows
            FROM system.tables
            WHERE
                database = '{self.user.database}'
                AND name IN {table_names}
            FORMAT JSON
        """

        result, _ = self.run_query(query)
        info: Dict[str, int] = {name: 0 for name in table_names}

        try:
            tables = json.loads(result)["data"]
            for table in tables:
                name = table.get("name", "")
                info[name] = table.get("total_rows", 0)

        except Exception as e:
            logging.warning(f"Failed to compute info for tables={table_names}: {e}")
        return info

    def before_create(self, datasource):
        pass

    def after_create(self, datasource):
        pass

    def before_append(self, datasource):
        pass

    def after_append(self, datasource):
        pass

    def before_delete(self, datasource):
        pass

    def after_delete(self, datasource):
        pass

    def before_delete_with_condition(self, datasource):
        pass

    def after_delete_with_condition(self, datasource: Datasource):
        database_server = self.user.database_server
        database = self.user.database
        datasource_id = datasource.id
        cluster = self.user.cluster
        max_mutations_seconds_to_wait = self.user.get_limits(prefix="ch").get(
            "max_mutations_seconds_to_wait", Limit.ch_max_mutations_seconds_to_wait
        )

        mutations_success = ch_wait_for_mutations_sync(
            database_server,
            database,
            datasource_id,
            max_mutations_seconds_to_wait=max_mutations_seconds_to_wait,
            cluster=cluster,
            skip_unavailable_replicas=True,
        )

        if not mutations_success:
            error_message = "Failed to wait for mutations of delete data"
            logging.error(error_message)
            user_error = "Could not determine the status of the job. The job will keep running in the background until it finishes, check the data is deleted in the Data Source or contact us at support@tinybird.co to know the status of the job."
            raise RuntimeError(user_error)

    def before_truncate(self, datasource):
        pass

    def after_truncate(self, datasource):
        pass

    def before_alter_datasource(self, datasource):
        pass

    def after_alter_datasource(self, datasource):
        pass

    def on_error(self, datasource, error):
        pass

    def tear_down(self, datasource: Datasource):
        with Timer("TEAR DOWN") as timing:
            database_server = self.user.database_server
            cluster = self.user.cluster

            for table_location in self.table_locations_to_drop:
                try:
                    hook_name = type(self).__name__
                    logging.info(
                        f"before dropping table: {table_location.database}.{table_location.table} in {hook_name}"
                    )
                    ch_drop_table_sync(
                        database_server,
                        table_location.database,
                        table_location.table,
                        cluster,
                        exists_clause=True,
                        avoid_max_table_size=True,
                        **self.get_extra_params(),
                    )
                    logging.info(f"dropped table: {table_location.database}.{table_location.table}")
                except Exception as e:
                    logging.exception(f"Exception on hook tear down: {e}")

        self.log_event(datasource, "tear_down", timing)

    def get_extra_params(self, ddl_parameters: bool = True) -> Dict[str, Any]:
        return {**self.user.ddl_parameters(skip_replica_down=True)} if ddl_parameters else {}

    def run_query(
        self,
        sql: str,
        host=None,
        read_only=False,
        max_execution_time=60,
        insert_deduplicate=1,
        max_insert_threads=Limit.ch_max_insert_threads,
        join_algorithm=CH_SETTINGS_JOIN_ALGORITHM_HASH,
        user_agent=None,
        **extra_params: Any,
    ):
        if user_agent:
            extra_params["user_agent"] = user_agent

        def _run_query(
            u,
            sql,
            read_only,
            max_execution_time,
            host,
            insert_deduplicate,
            max_insert_threads,
            join_algorithm,
            extra_params,
        ):
            host = host or u["database_server"]
            database = u["database"]
            client = HTTPClient(host, database)
            try:
                with Timer(f"<{self.hook_id}> DatasourceHook query {host}/{database}: {sql}"):
                    _, body = client.query_sync(
                        sql,
                        read_only=read_only,
                        max_execution_time=max_execution_time,
                        insert_deduplicate=insert_deduplicate,
                        max_insert_threads=max_insert_threads,
                        join_algorithm=join_algorithm,
                        **extra_params,
                    )
                    logging.debug(
                        f"<{self.hook_id}> DatasourceHook query {host}/{database}: {sql} result: {body.decode('utf-8')}"
                    )
                return body or True, None
            except Exception as e:
                hook_message = f"DatasourceHook query {host}/{database}: {sql}"
                exception_message = f"Exception: {e}"
                traceback_message = f"Traceback: {traceback.format_exc()}"
                logging.exception(f"<{self.hook_id}> {hook_message}\n{exception_message}\n{traceback_message}")
                return False, e

        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="hooks_run_query") as executor:
            future = executor.submit(
                _run_query,
                self.user,
                sql,
                read_only,
                max_execution_time,
                host,
                insert_deduplicate,
                max_insert_threads,
                join_algorithm,
                extra_params,
            )
            return future.result()

    def create_staging_table(
        self,
        workspace: User,
        table_details: TableDetails,
        cluster: Optional[str] = None,
        mirror_table_sufix: Optional[str] = None,
        **extra_params: Any,
    ) -> str:
        table_name = table_details.name
        staging_table_name = mirror_table_sufix if mirror_table_sufix is not None else Resource.guid()

        new_table_name = f"{table_name}_{staging_table_name}"
        create_staging_table_query = CHTable(
            [], cluster=cluster, engine=table_details.engine_full, as_table=f"{workspace['database']}.{table_name}"
        ).as_sql(workspace["database"], new_table_name)

        self.table_locations_to_drop.append(CHTableLocation(workspace.database, new_table_name))
        ok, e = self.run_query(create_staging_table_query, read_only=False, **extra_params)
        if not ok:
            logging.error(
                f"error when creating staging table {new_table_name} for table {table_name} with sql"
                f" {create_staging_table_query}"
            )
            raise e

        return new_table_name

    def run_query_with_replica_support(
        self,
        sql: str,
        table_details: TableDetails,
        source_table: str,
        cluster: Optional[str] = None,
        source_database=None,
        max_insert_threads=Limit.ch_max_insert_threads,
        join_algorithm: str = CH_SETTINGS_JOIN_ALGORITHM_HASH,
        user_agent: Optional[str] = None,
        **extra_params: Any,
    ) -> None:
        extra_params = extra_params or {}
        if user_agent:
            extra_params["user_agent"] = user_agent

        # if target table is replicated it's fine to run on just one machine
        if table_details.is_replicated():
            ok, e = self.run_query(
                sql,
                max_execution_time=3600,
                insert_deduplicate=0,
                max_insert_threads=max_insert_threads,
                join_algorithm=join_algorithm,
                **extra_params,
            )
            if not ok:
                logging.warning(f"1. failed to run query {sql}")
                raise e
        else:
            # manually run insert query on every replica
            # the original table is replicated
            source_database = self.user["database"] if source_database is None else source_database
            if cluster:
                replicas = ch_get_replicas_for_table_sync(
                    self.user["database_server"], source_database, source_table, cluster
                )
            if not replicas:
                if cluster:
                    replicas = [
                        x[0]
                        for x in ch_get_cluster_instances_sync(
                            self.user["database_server"],
                            source_database,
                            cluster,
                            max_execution_time=MAX_EXECUTION_TIME_CLUSTER_INSTANCES_SECONDS,
                        )
                    ]
                else:
                    # original table is not replicated so run just in current database
                    url = url_from_host(self.user["database_server"])
                    replicas = [url]

            with ThreadPoolExecutor(
                max_workers=len(replicas), thread_name_prefix="hooks_table_replication"
            ) as executor:

                def _run_query_on_replica(http_server):
                    return self.run_query(
                        sql,
                        host=http_server,
                        max_execution_time=3600,
                        read_only=False,
                        join_algorithm=join_algorithm,
                        **extra_params,
                    )

                try:
                    for ok, e in executor.map(_run_query_on_replica, replicas):
                        if not ok:
                            logging.warning(f"2. failed to run query {sql} on replicas {replicas}")
                            raise e

                except Exception as e:
                    logging.warning(f"3. failed to run query {sql}")
                    raise e

    def copy_mergetree_table(self, workspace: User, target_table, source_table, partitions):
        database_server = workspace["database_server"]
        database = workspace["database"]
        ch_attach_partitions_sync(
            database_server,
            database,
            destination_table=target_table,
            origin_table=source_table,
            partitions=partitions,
            wait_setting=WAIT_ALTER_REPLICATION_OWN,
            query_settings=self.get_extra_params(),
        )

    def copy_join_table(
        self, workspace: User, target_table: str, source_table: str, join_algorithm=CH_SETTINGS_JOIN_ALGORITHM_HASH
    ):
        max_insert_threads = workspace.get_limits(prefix="ch").get("max_insert_threads", Limit.ch_max_insert_threads)
        database_server = workspace["database_server"]
        database = workspace["database"]
        cluster = workspace["cluster"]

        select_sql = f"SELECT * FROM {database}.{source_table}"

        columns = ch_get_columns_from_query_sync(database_server, database, select_sql)
        table_details = ch_table_details(target_table, database_server, database)

        sql = f"""INSERT INTO {database}.{target_table}
            (
                {','.join([f"`{c['name']}`" for c in columns])}
            )
            {select_sql}"""
        try:
            self.run_query_with_replica_support(
                sql,
                table_details,
                source_table=source_table,
                cluster=cluster,
                max_insert_threads=max_insert_threads,
                join_algorithm=join_algorithm,
            )
        except Exception as e:
            logging.exception(e)
            raise e

    def copy_data_with_replica_support(
        self,
        workspace: User,
        target_table,
        source_table,
        replacing_datasource: Datasource,
        origin_datasource_id: str,
        origin_workspace_id: str,
        join_algorithm=CH_SETTINGS_JOIN_ALGORITHM_HASH,
    ):
        database_server = workspace["database_server"]
        database = workspace["database"]
        partitions = ch_table_partitions_sync(
            database_server=database_server, database_name=database, table_names=[source_table]
        )

        try:
            if partitions:
                self.copy_mergetree_table(workspace, target_table, source_table, partitions)
            else:
                self.copy_join_table(workspace, target_table, source_table, join_algorithm=join_algorithm)
        except Exception as e:
            logging.exception(e)
            ops_log_options = {
                "replace_origin_datasource": origin_datasource_id,
                "replace_origin_workspace": origin_workspace_id,
            }
            self.log_operation(
                "replace",
                datasource=replacing_datasource,
                error=str(e),
                options={**self.ops_log_options, **ops_log_options},
                workspace=workspace,
            )

            statsd_prefix = StatsdReplacesMetrics.replaces_dependent_error(
                replace_type=self.replace_type,
                database_server=sanitize_database_server(self.user.database_server),
                destination_workspace_id=workspace.id,
                destination_datasource_id=replacing_datasource.id,
            )

            statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - self.start).seconds)
            raise e

    def populate_dependent_views(
        self,
        datasource_to_replace_id: str,
        new_datasource_id: str,
        database_server: str,
        database: str,
        cluster: Optional[str] = None,
    ):
        dependent_views = ch_table_dependent_views_sync(database_server, database, datasource_to_replace_id)

        self.populate_dependent_views_with_swap(
            datasource_to_replace_id,
            new_datasource_id,
            dependent_views,
            self.user,
            cluster=cluster,
            origin_datasource_id=datasource_to_replace_id,
            origin_workspace_id=self.user.id,
        )

        for tables_to_swap in self.group_tables_to_swap:
            if len(tables_to_swap):
                ch_swap_tables_sync(
                    database_server,
                    tables_to_swap,
                    cluster,
                    **self.get_extra_params(),
                )
                logging.info(f"Swapped tables: {tables_to_swap}")

        self.swapped_tables.update(self.unique_tables_to_swap)

        return

    def populate_dependent_views_with_swap(
        self,
        table_name: str,
        view_source_table_name: str,
        dependent_views: List[CHTableLocation],
        workspace: User,
        origin_workspace_id: str,
        origin_datasource_id: str,
        is_cascade: bool = False,
        cluster: Optional[str] = None,
        origin_start_time: Optional[datetime] = None,
    ) -> None:
        """
        This truncates the depending `table_name` views and uses the view query to update the view
        with the new data present in the `table_name` table.

        Use the `view_source_table_name` parameter to select from another existing table.
        I.e., it will use `table_name` to find the dependent views/tables,
        but it will populate the depending views from `view_source_table_name` instead of using `table_name`.

        This makes sense for the following scenarios:
         - When you want to populate dependent tables based on staging tables,
           doing it on cascade, allowing to swap all the tables at the same time.
         - When replacing a data source, you can make a shadow data source you use for the ingestion process,
           regenerating all the depending views/tables, and finally replacing/swapping the data source with
           the shadowed one.
        """
        tables_to_swap: List[TablesToSwapWithWorkspace] = []
        unique_tables_to_swap: Set[TablesToSwapWithWorkspace] = set()
        origin_start_time = origin_start_time or datetime.now(timezone.utc)
        join_algorithm = workspace.get_join_algorithm()

        if cluster:
            # TODO statsd wait for replication sync start
            max_wait_for_replication_seconds = workspace.get_limits(prefix="ch").get(
                "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
            )
            replication_success = CHReplication.ch_wait_for_replication_sync(
                workspace.database_server,
                workspace.cluster,
                workspace.database,
                view_source_table_name,
                wait=max_wait_for_replication_seconds,
                **self.get_extra_params(ddl_parameters=False),
            )
            # TODO statsd wait for replication sync end
            if not replication_success:
                error_message = f"Failed to wait for replication in table {workspace.database}.{view_source_table_name} when populating dependent views"
                logging.error(error_message)
                raise RuntimeError(error_message)

        map_database_to_workspace = _map_database_to_workspace(workspace, table_name)

        def _repopulate_dependent_view(dependent_view: CHTableLocation):
            if dependent_view.database not in map_database_to_workspace:
                logging.warning(
                    f"Dependent view is in a deleted workspace: {dependent_view.database}.{dependent_view.table}"
                )
                return None, None, None, None

            start_time = datetime.now(timezone.utc)

            workspace_with_dependent_view = map_database_to_workspace[dependent_view.database]
            max_insert_threads = workspace_with_dependent_view.get_limits(prefix="ch").get(
                "max_insert_threads", Limit.ch_max_insert_threads
            )
            node = Users.get_node(workspace_with_dependent_view, dependent_view.table)
            if not node:
                raise could_not_find_query_to_populate_depending_view_exception(
                    f"{dependent_view.database}.{dependent_view.table}"
                )

            assert isinstance(node, PipeNode)

            dependent_ds = Users.get_datasource(workspace_with_dependent_view, node.materialized)

            if not dependent_ds:
                # looks like there is a pipe with a materialzed node that points to a table
                # that was removed
                pipe = Users.get_pipe_by_node(workspace_with_dependent_view, dependent_view.table)
                assert isinstance(pipe, Pipe)
                raise could_not_find_dependent_table_to_populate_exception(
                    pipe.name, node.name, node.id, f"{workspace_with_dependent_view.database}{node.materialized}"
                )

            assert isinstance(dependent_ds, Datasource)
            table_to_repopulate = dependent_ds.id
            table_to_repopulate_details = ch_table_details(
                table_name=table_to_repopulate,
                database_server=workspace_with_dependent_view.database_server,
                database=workspace_with_dependent_view.database,
            )
            table_to_repopulate_staging_table = self.create_staging_table(
                workspace_with_dependent_view,
                table_to_repopulate_details,
                cluster=workspace_with_dependent_view.cluster,
                **self.get_extra_params(),
            )

            error = None
            max_wait_for_replication_seconds = workspace_with_dependent_view.get_limits(prefix="ch").get(
                "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
            )

            for p in workspace_with_dependent_view.get_pipes():
                for node in p.pipeline.nodes:
                    assert isinstance(node, PipeNode)
                    if node.materialized == dependent_ds.id:
                        extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]] = {}
                        if view_source_table_name:
                            extra_replacements = {
                                (workspace.database, table_name): (workspace.database, view_source_table_name)
                            }
                        select_sql = Users.replace_tables(
                            workspace_with_dependent_view,
                            node.sql,
                            pipe=p,
                            use_pipe_nodes=True,
                            extra_replacements=extra_replacements,
                        )

                        columns = ch_get_columns_from_query_sync(
                            workspace_with_dependent_view.database_server,
                            workspace_with_dependent_view.database,
                            select_sql,
                        )
                        sql = f"""INSERT INTO {workspace_with_dependent_view.database}.{table_to_repopulate_staging_table}
                        (
                            {','.join([f"`{c['name']}`" for c in columns])}
                        )
                        {select_sql}"""

                        try:
                            unique_tables_to_swap.add(
                                TablesToSwapWithWorkspace(
                                    workspace_with_dependent_view.database,
                                    dependent_ds.id,
                                    None,
                                    workspace_with_dependent_view.id,
                                    p.id,
                                    p.name,
                                )
                            )
                            self.run_query_with_replica_support(
                                sql,
                                table_to_repopulate_details,
                                source_table=view_source_table_name,
                                cluster=cluster,
                                max_insert_threads=max_insert_threads,
                                join_algorithm=join_algorithm,
                                **self.get_extra_params(ddl_parameters=False),
                            )
                        except Exception as e:
                            error = str(e)
                            logging.exception(error)
                            # We raise an error only if it's in the first cascade level
                            # We want to avoid raising an error on child replaces for now,
                            # in order to understand these errors before changing this behavior
                            if not is_cascade:
                                self.log_operation(
                                    "replace",
                                    datasource=dependent_ds,
                                    error=error,
                                    options=self.ops_log_options,
                                    workspace=workspace_with_dependent_view,
                                )

                                statsd_prefix = StatsdReplacesMetrics.replaces_origin_error(
                                    replace_type=self.replace_type,
                                    database_server=sanitize_database_server(self.user.database_server),
                                    origin_workspace_id=origin_workspace_id,
                                    origin_datasource_id=origin_datasource_id,
                                )

                                assert isinstance(origin_start_time, datetime)
                                statsd_client.timing(
                                    statsd_prefix, (datetime.now(timezone.utc) - origin_start_time).seconds
                                )

                                raise HookException(f'Error replacing data source "{dependent_ds.name}": {e}')
                            else:
                                ops_log_options = {
                                    "replace_origin_datasource": origin_datasource_id,
                                    "replace_origin_workspace": origin_workspace_id,
                                }
                                self.log_operation(
                                    "replace",
                                    datasource=dependent_ds,
                                    error=error,
                                    options={**self.ops_log_options, **ops_log_options},
                                    workspace=workspace_with_dependent_view,
                                )

                                statsd_prefix = StatsdReplacesMetrics.replaces_dependent_error(
                                    replace_type=self.replace_type,
                                    database_server=sanitize_database_server(self.user.database_server),
                                    destination_workspace_id=workspace.id,
                                    destination_datasource_id=dependent_ds.id,
                                )

                                statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - start_time).seconds)
                        if cluster:
                            # TODO statsd wait for replication replace start
                            replication_success = CHReplication.ch_wait_for_replication_sync(
                                workspace_with_dependent_view.database_server,
                                workspace_with_dependent_view.cluster,
                                workspace_with_dependent_view.database,
                                table_to_repopulate_staging_table,
                                wait=max_wait_for_replication_seconds,
                                **self.get_extra_params(ddl_parameters=False),
                            )
                            # TODO statsd wait for replication replace end
                            if not replication_success:
                                error_message = f"Failed to wait for replication in table {workspace.database}.{table_to_repopulate_staging_table} when populating dependent views of {view_source_table_name}"
                                logging.exception(error_message)
                                raise RuntimeError(error_message)

            if error is None:
                tables_to_swap.append(
                    TablesToSwapWithWorkspace(
                        workspace_with_dependent_view.database,
                        dependent_ds.id,
                        table_to_repopulate_staging_table,
                        workspace_with_dependent_view.id,
                        p.id,
                        p.name,
                    )
                )
                return dependent_view, dependent_ds, table_to_repopulate_staging_table, workspace_with_dependent_view
            else:
                return None, None, None, None

        max_workers = max(1, min(4, len(dependent_views)))
        dependent_datasources = []

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="hooks_dependent_views") as executor:
            for dependent_view, dependent_ds, table_to_repopulate, workspace_with_dependent_view in executor.map(
                _repopulate_dependent_view, dependent_views
            ):
                if dependent_view:
                    dependent_datasources.append((dependent_ds, table_to_repopulate, workspace_with_dependent_view))
                    logging.info(f"Populated dependent view {dependent_view}")

        # Note: from here it starts the replaces cascade
        if dependent_datasources:
            dependent_datasources_sorted = sorted(dependent_datasources, key=lambda ds: ds[0].name)
            for dependent_ds, table_to_repopulate, dependent_ws in dependent_datasources_sorted:
                dependent_views = ch_table_dependent_views_sync(
                    dependent_ws.database_server, dependent_ws.database, dependent_ds.id
                )
                if not dependent_views:
                    continue
                new_datasource = Datasource.duplicate_datasource(dependent_ds)
                table_locations_to_drop = _prepare_replace(
                    dependent_ws,
                    new_datasource,
                    dependent_ds,
                    **self.get_extra_params(),
                )

                self.copy_data_with_replica_support(
                    dependent_ws,
                    new_datasource.id,
                    table_to_repopulate,
                    dependent_ds,
                    origin_datasource_id,
                    origin_workspace_id,
                    join_algorithm=join_algorithm,
                )

                self.table_locations_to_drop.extend(table_locations_to_drop)
                self.populate_dependent_views_with_swap(
                    dependent_ds.id,
                    new_datasource.id,
                    dependent_views,
                    dependent_ws,
                    origin_datasource_id=origin_datasource_id,
                    origin_workspace_id=origin_workspace_id,
                    is_cascade=True,
                    cluster=dependent_ws.cluster,
                    origin_start_time=origin_start_time,
                )

        if len(unique_tables_to_swap):
            self.unique_tables_to_swap.update(unique_tables_to_swap)

        if len(tables_to_swap):
            self.group_tables_to_swap.append(tables_to_swap)
        self.group_tables_to_swap.append(
            [
                TablesToSwapWithWorkspace(
                    workspace.database, view_source_table_name, table_name, workspace.id, None, None
                )
            ]
        )
        return


def _map_database_to_workspace(workspace: User, table_to_replace: str) -> Dict[str, User]:
    map_database_to_workspace = {workspace.database: workspace}
    source_datasource = Users.get_datasource(workspace, table_to_replace)

    if source_datasource:
        for shared_with_workspace in source_datasource.shared_with:
            external_workspace = User.get_by_id(shared_with_workspace)
            map_database_to_workspace[external_workspace.database] = external_workspace

    return map_database_to_workspace


class PGSyncDatasourceHook(Hook):
    def __init__(self, user: User):
        super().__init__(user)
        self.done = False

    def after_create(self, datasource: Datasource):
        self.done = PGService(self.user).sync_foreign_tables(datasources=[datasource])

    def after_alter_datasource(self, datasource: Datasource):
        self.done = PGService(self.user).sync_foreign_tables(datasources=[datasource])

    def after_delete(self, datasource: Datasource):
        self.done = PGService(self.user).drop_foreign_table(datasource.id)

    def after_create_ops_log(self, datasource: Datasource):
        if self.done:
            self.log_operation("create foreign table", datasource)

    def after_delete_ops_log(self, datasource: Datasource):
        if self.done:
            self.log_operation("drop foreign table", datasource)

    def after_alter_datasource_ops_log(self, datasource: Datasource):
        if self.done:
            self.log_operation("alter applied to foreign table", datasource)


class CreateDatasourceHook(Hook):
    def before_create(self, datasource: Datasource):
        Users.update_datasource_sync(self.user, datasource)

    def after_create(self, datasource: Datasource):
        engine = ch_table_details(datasource.id, self.user["database_server"], database=self.user["database"])
        datasource.engine = engine.to_json(exclude=["engine_full"])
        Users.update_datasource_sync(self.user, datasource)

    def after_create_ops_log(self, datasource: Datasource):
        self.log_operation("create", datasource)

    def after_append_ops_log(self, datasource: Datasource):
        rows, rows_quarantine = self.get_rows(datasource)
        self.log_operation("append", datasource, rows=rows, rows_quarantine=rows_quarantine)

    def on_error(self, datasource: Datasource, error):
        event_type = "append" if len(self.ops_log) > 0 else "create"
        self.log_operation(event_type, datasource, error=error)


class DeleteCompleteDatasourceHook(Hook):
    def before_delete_ops_log(self, datasource: Datasource):
        self.deleted_rows, self.deleted_rows_quarantine = self.get_rows(datasource)

    def after_delete_ops_log(self, datasource: Datasource):
        self.log_operation("delete", datasource, rows=self.deleted_rows, rows_quarantine=self.deleted_rows_quarantine)


class DeletePartialDatasourceHook(Hook):
    def __init__(self, user: User, datasource_to_delete: Datasource, delete_condition: str):
        super().__init__(user)
        self.datasource_to_delete = datasource_to_delete
        self.delete_condition = delete_condition
        self.ops_log_options = {}
        if self.delete_condition:
            self.ops_log_options["delete_condition"] = self.delete_condition

    def on_error(self, datasource, error):
        self.log_operation("delete_data", datasource, options=self.ops_log_options, error=error)

    def before_delete_with_condition_ops_log(self, datasource):
        self.total_rows, _ = self.get_rows(datasource)

    def after_delete_with_condition_ops_log(self, datasource):
        if self.user.cluster:
            max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
            )
            replication_success = CHReplication.ch_wait_for_replication_sync(
                self.user["database_server"],
                self.user.cluster,
                self.user["database"],
                datasource.id,
                wait=max_wait_for_replication_seconds,
            )
            if not replication_success:
                error_message = f"Failed to wait for replication in table {self.user['database']}.{datasource.id}"
                logging.error(error_message)
                raise RuntimeError(error_message)

        self.deleted_rows, _ = self.get_rows(datasource)
        self.log_operation(
            "delete_data", datasource, rows=self.total_rows - self.deleted_rows, options=self.ops_log_options
        )


class TruncateDatasourceHook(Hook):
    def before_truncate_ops_log(self, datasource: Datasource):
        self.truncated_rows, _ = self.get_rows(datasource)

    def after_truncate_ops_log(self, datasource: Datasource):
        self.log_operation("truncate", datasource, rows=self.truncated_rows)


class AlterDatasourceHook(Hook):
    def __init__(self, workspace: User, operations: List[str], dependencies: List[str]):
        super().__init__(workspace)
        self.ops_log_options = {"operations": str(operations)}
        if dependencies:
            self.ops_log_options.update({"dependencies": str(dependencies)})

    def before_alter_datasource(self, datasource: Datasource):
        # In the branches, we are creating the quarantine tables on demand https://gitlab.com/tinybird/analytics/-/issues/9012
        # In internal we might have no quarantine tables created
        def should_create_quarantine(user: User) -> bool:
            return user.is_branch or user.is_release_in_branch or user.id == public.get_public_user().id

        if should_create_quarantine(self.user):
            create_quarantine_table_from_landing_sync(
                landing_datasource_name=datasource.id,
                database_server=self.user.database_server,
                database=self.user.database,
                cluster=self.user.cluster,
            )

    def after_alter_datasource_ops_log(self, datasource):
        self.log_operation("alter", datasource, options=self.ops_log_options)

    def on_error(self, datasource, error):
        self.log_operation("alter", datasource, options=self.ops_log_options, error=error)


class AppendDatasourceHook(Hook):
    def before_append_ops_log(self, datasource: Datasource):
        if not datasource.json_deserialization:
            self.rows_before_append, self.rows_quarantine_before_append = self.get_rows(datasource)

    def after_append(self, datasource, appended_rows=None, appended_rows_quarantine=None, elapsed_time=None):
        pass

    def after_append_ops_log(
        self,
        datasource: Datasource,
        appended_rows: Optional[int] = None,
        appended_rows_quarantine: Optional[int] = None,
        elapsed_time: Optional[float] = None,
    ):
        if not datasource.json_deserialization:
            rows, rows_quarantine = self.get_rows(datasource)
            appended_rows = rows - self.rows_before_append
            appended_rows_quarantine = rows_quarantine - self.rows_quarantine_before_append
        self.log_operation(
            "append",
            datasource,
            rows=appended_rows,
            rows_quarantine=appended_rows_quarantine,
            elapsed_time=elapsed_time,
        )

    def on_error(self, datasource, error):
        self.log_operation("append", datasource, error=error)


class ReplaceDatasourceBaseHook(Hook):
    replace_truncate_when_empty_flag = "replace_truncate_when_empty"

    def __init__(
        self,
        user: User,
        datasource_to_replace: Datasource,
        replace_condition: Optional[str] = None,
        job_id: Optional[str] = None,
    ) -> None:
        super().__init__(user)
        self.datasource_to_replace = datasource_to_replace
        self.replace_condition = replace_condition
        self.ops_log_options: Dict[str, str] = {}
        self.swapped_tables: Set[TablesToSwapWithWorkspace] = set()
        if self.replace_condition:
            self.ops_log_options["replace_condition"] = self.replace_condition
        self.replace_type = "partial" if self.replace_condition else "complete"
        self._job_id = job_id

    def _log_comment(self, extra_fields: Dict[str, Any] | None = None) -> Dict:
        from tinybird.job import JobKind

        return {"job_id": self._job_id, "job_kind": JobKind.IMPORT, **(extra_fields or {})}

    def _generate_log_comment(self, extra_fields: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Generate a log that will be used for debugging or validator to have better tracking of the queries
        """
        if self._job_id:
            return {"log_comment": json.dumps(self._log_comment(extra_fields))}
        return {}

    def get_extra_params(self, ddl_parameters: bool = True) -> Dict[str, Any]:
        return (
            {**self.user.ddl_parameters(skip_replica_down=True), **self._generate_log_comment()}
            if ddl_parameters
            else {**self._generate_log_comment()}
        )

    def before_append_ops_log(self, datasource):
        self.rows_before_replace, self.rows_quarantine_before_replace = self.get_rows(self.datasource_to_replace)
        self.ops_log_options["rows_before_replace"] = str(self.rows_before_replace)

    def after_append_ops_log(self, datasource, ops_log_options=None):
        ops_log_options = self.ops_log_options if ops_log_options is None else ops_log_options
        rows, rows_quarantine = self.get_rows(self.datasource_to_replace)
        replaced_rows_quarantine = rows_quarantine - self.rows_quarantine_before_replace

        # Log options
        if len(self.swapped_tables):
            for swaps in self.swapped_tables:
                try:
                    workspace = Users.get_by_id(swaps.workspace) if self.user.id != swaps.workspace else self.user
                    swap_datasource = Users.get_datasource(workspace, swaps.old_table)

                    if swap_datasource:
                        # Add 'replace_origin_datasource' option if it's not the target data source
                        options = {**self.ops_log_options, **ops_log_options}
                        if self.datasource_to_replace.id != swap_datasource.id:
                            options.update(
                                {
                                    "replace_origin_datasource": self.datasource_to_replace.id,
                                    "replace_origin_workspace": self.user.id,
                                }
                            )

                        rows, _ = self.get_rows(swap_datasource)

                        self.log_operation(
                            "replace",
                            swap_datasource,
                            rows=rows,
                            options=options,
                            workspace=workspace,
                            use_tracker=False,
                            pipe_id=swaps.pipe_id,
                            pipe_name=swaps.pipe_name,
                        )

                        statsd_prefix = StatsdReplacesMetrics.replaces_dependent_success(
                            replace_type=self.replace_type,
                            database_server=sanitize_database_server(self.user.database_server),
                            destination_workspace_id=workspace.id,
                            destination_datasource_id=swap_datasource.id,
                        )

                        statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - self.start).seconds)
                except Exception as e:
                    logging.error(f"Error logging operation: {e}\nTraceback: {traceback.format_exc()}")

        self.log_operation(
            "replace",
            self.datasource_to_replace,
            rows=rows,
            rows_quarantine=replaced_rows_quarantine,
            options={**self.ops_log_options, **ops_log_options},
            use_tracker=False,
            update_with_blocks=True,
        )

        statsd_prefix = StatsdReplacesMetrics.replaces_origin_success(
            replace_type=self.replace_type,
            database_server=sanitize_database_server(self.user.database_server),
            origin_workspace_id=self.user.id,
            origin_datasource_id=self.datasource_to_replace.id,
        )

        statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - self.start).seconds)

    def on_error(self, datasource, error, ops_log_options=None):
        ops_log_options = self.ops_log_options if ops_log_options is None else ops_log_options
        self.log_operation(
            "replace", self.datasource_to_replace, options={**self.ops_log_options, **ops_log_options}, error=error
        )

        statsd_prefix = StatsdReplacesMetrics.replaces_origin_error(
            replace_type=self.replace_type,
            database_server=sanitize_database_server(self.user.database_server),
            origin_workspace_id=self.user.id,
            origin_datasource_id=self.datasource_to_replace.id,
        )

        statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - self.start).seconds)


def ReplaceDatasourceHook(
    workspace: User,
    datasource_to_replace: Datasource,
    replace_options: Dict[str, bool],
    replace_condition: Optional[str] = None,
    job_id: Optional[str] = None,
) -> ReplaceDatasourceBaseHook:
    """Check https://gitlab.com/tinybird/analytics/-/merge_requests/324 for more details about this"""
    if replace_condition:
        return ReplacePartialDatasourceHook(
            workspace, datasource_to_replace, replace_condition, replace_options, job_id
        )

    replace_truncate_when_empty = replace_options.pop(ReplaceDatasourceBaseHook.replace_truncate_when_empty_flag, False)

    if replace_options:
        non_supported_options = ", ".join(sorted(list(replace_options.keys())))
        raise ValueError(f"Replace of complete Data Sources doesn't support replace options: {non_supported_options}.")
    return ReplaceCompleteDatasourceHook(workspace, datasource_to_replace, replace_truncate_when_empty, job_id)


def DeleteDatasourceHook(user, datasource_to_delete, delete_condition=None):
    if delete_condition:
        return DeletePartialDatasourceHook(user, datasource_to_delete, delete_condition)
    return DeleteCompleteDatasourceHook(user)


class ReplaceCompleteDatasourceHook(ReplaceDatasourceBaseHook):
    def __init__(self, user, datasource_to_replace, replace_truncate_when_empty, job_id=None):
        super().__init__(user, datasource_to_replace, job_id=job_id)
        self.did_create_table = False
        self.group_tables_to_swap = []
        self.unique_tables_to_swap = set()
        self.replace_truncate_when_empty = replace_truncate_when_empty

    def before_create(self, datasource):
        table_locations_to_drop = _prepare_replace(
            self.user, datasource, self.datasource_to_replace, **self.get_extra_params()
        )
        self.table_locations_to_drop.extend(table_locations_to_drop)
        return True

    def after_create(self, datasource):
        self.did_create_table = True

    def after_append(self, new_datasource: Datasource) -> None:
        """
        Replacing a data source requires recalculating all its depending materialized views.
        We do this atomically, performing all the operations in staging tables and swapping
        all the tables after the views re-population has finished.

        TODO the new datasource should exist in the same cluster
        """

        if not self.did_create_table:
            return

        rows, rows_quarantine = self.get_rows(new_datasource)

        if not rows and not self.replace_truncate_when_empty:
            self.tear_down(new_datasource)
            return

        datasource_to_replace = Users.get_datasource(self.user, self.datasource_to_replace.id)  # reload from database
        assert isinstance(datasource_to_replace, Datasource)
        self.populate_dependent_views(
            datasource_to_replace.id,
            new_datasource.id,
            self.user.database_server,
            self.user.database,
            self.user.cluster,
        )

        self.tear_down(new_datasource)


@dataclass
class MVToRecalculate:
    pipe: Pipe
    node: PipeNode  # having pipe + node here is just to support multiple MV nodes.
    source_has_been_replaced: bool


@dataclass
class PartialReplaceSteps:
    ds_to_replace: Datasource
    ds_workspace: User
    mvs_to_recalculate: List[MVToRecalculate]


class ReplaceStatus:
    SKIPPED = "skipped"
    WAITING = "waiting"
    WORKING = "working"
    ERROR = "error"
    CANCELLED = "cancelled"

    # For Data Sources:
    READY = "ready"
    REPLACED = "replaced"

    # For Materialized views:
    DONE = "done"


def partition_value_can_be_replaced_in_the_destination_ds(
    common_database_server: str, source_table_details: TableDetails, destination_table_details: TableDetails
) -> bool:
    if need_swap(destination_table_details):
        return True

    if not source_table_details.partition_key or source_table_details.partition_key in ["tuple()", ""]:
        return False

    if not destination_table_details.partition_key or destination_table_details.partition_key in ["tuple()", ""]:
        return False

    source_partition_key_type = _get_partition_key_type(common_database_server, source_table_details)
    destination_partition_key_type = _get_partition_key_type(common_database_server, destination_table_details)

    compatible, _ = origin_column_type_is_compatible_with_destination_type(
        source_partition_key_type, destination_partition_key_type
    )
    return compatible


def _get_partition_key_type(database_server: str, table_details: TableDetails) -> str:
    describe = ch_get_columns_from_query_sync(
        database_server,
        table_details.database,
        f"""
        SELECT {table_details.partition_key} from {table_details.name}
    """,
    )
    return describe[0]["type"]


def need_swap(table_details: TableDetails) -> bool:
    return table_details.engine.lower() == "join"


class ReplacePartialDataSourceReporter:
    def __init__(self, job_id: Optional[str]):
        if job_id is None or Job.get_by_id(job_id) is None:
            self._job_present = False
            return

        self._job_id = job_id
        self._job_present = True

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                job.other_datasources_to_replace = {
                    "progress_percentage": 0,
                    "replaces_to_execute": [],
                    "skipped_replaces": [],
                }
        self._total_mvs_to_recalculate = 0

    def add_steps(self, steps_to_execute: List[PartialReplaceSteps]) -> None:
        if not self._job_present:
            return

        replaces_to_execute = [self._map_replace_step_to_json(step, ReplaceStatus.WAITING) for step in steps_to_execute]
        self._total_mvs_to_recalculate = sum([len(replace["pipes"]) for replace in replaces_to_execute])

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                job.other_datasources_to_replace["replaces_to_execute"] = replaces_to_execute

    @staticmethod
    def _map_replace_step_to_json(step_to_map: PartialReplaceSteps, status: Optional[str] = None) -> Dict[str, Any]:
        pipes = []

        for mv in step_to_map.mvs_to_recalculate:
            pipe = {
                "id": mv.pipe.id,
                "name": mv.pipe.name,
                "node": {"id": mv.node.id, "name": mv.node.name},
            }
            if status:
                pipe["status"] = status
            pipes.append(pipe)

        return {
            "workspace": {"id": step_to_map.ds_workspace.id, "name": step_to_map.ds_workspace.name},
            "status": status,
            "pipes": pipes,
            "datasource": {"id": step_to_map.ds_to_replace.id, "name": step_to_map.ds_to_replace.name},
        }

    def add_skipped_steps(self, skipped_steps: List[PartialReplaceSteps]):
        if not self._job_present:
            return

        skipped_replaces = self._map_skipped_steps_to_json(skipped_steps)

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                job.other_datasources_to_replace["skipped_replaces"] = skipped_replaces

    @staticmethod
    def _map_skipped_steps_to_json(skipped_steps: List[PartialReplaceSteps]):
        return [
            {
                "workspace": {"id": step_to_map.ds_workspace.id, "name": step_to_map.ds_workspace.name},
                "datasource": {"id": step_to_map.ds_to_replace.id, "name": step_to_map.ds_to_replace.name},
            }
            for step_to_map in skipped_steps
        ]

    def change_step_status(self, step_index: int, step_new_status: str):
        if not self._job_present:
            return

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                job.other_datasources_to_replace["replaces_to_execute"][step_index]["status"] = step_new_status

    def _update_process_percentage(
        self, job_info: Dict[str, Any], new_step_status: str, step_index: int, mv_index: int
    ) -> float:
        if new_step_status != ReplaceStatus.DONE:
            return job_info["progress_percentage"]

        current_position = 0
        for step_position in range(0, step_index):
            if step_position == step_index:
                current_position += mv_index
            else:
                current_position += len(job_info["replaces_to_execute"][step_position]["pipes"])

        if self._total_mvs_to_recalculate == 0:
            return 0
        else:
            return (current_position + 1) / self._total_mvs_to_recalculate * 100

    def change_mv_status(self, step_index: int, mv_index: int, step_new_status: str):
        if not self._job_present:
            return

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                job.other_datasources_to_replace["replaces_to_execute"][step_index]["pipes"][mv_index]["status"] = (
                    step_new_status
                )
                job.other_datasources_to_replace["progress_percentage"] = self._update_process_percentage(
                    job.other_datasources_to_replace, step_new_status, step_index, mv_index
                )

    def mark_dss_as_replaced(self) -> None:
        if not self._job_present:
            return

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                for ds in job.other_datasources_to_replace["replaces_to_execute"]:
                    ds["status"] = ReplaceStatus.REPLACED

    def mark_ongoing_work_as_error(self) -> None:
        if not self._job_present:
            return

        with ImportJob.transaction(self._job_id) as job:
            if hasattr(job, "other_datasources_to_replace"):
                for ds in job.other_datasources_to_replace["replaces_to_execute"]:
                    ds["status"] = (
                        ReplaceStatus.ERROR if ds["status"] == ReplaceStatus.WORKING else ReplaceStatus.CANCELLED
                    )
                    for mv in ds["pipes"]:
                        mv["status"] = (
                            ReplaceStatus.ERROR if mv["status"] == ReplaceStatus.WORKING else ReplaceStatus.CANCELLED
                        )


class ReplacePartialDatasourceHook(ReplaceDatasourceBaseHook):
    def __init__(
        self,
        user: User,
        datasource_to_replace: Datasource,
        replace_condition: str,
        replace_options: Dict[str, bool],
        job_id: Optional[str],
    ) -> None:
        super().__init__(user, datasource_to_replace, replace_condition, job_id)

        # For replace process:
        self._replace_partitions_tables: List[Tuple[str, str, str, str]] = []
        self._tables_to_swap: List[TablesToSwap] = []
        self._mirror_table_sufix = job_id.replace("-", "") if job_id is not None else Resource.guid()
        # Options:
        self._skip_incompatible_partition_key = replace_options.get("skip_incompatible_partition_key", False)

    def before_create(self, datasource: Datasource):
        database_server = self.user["database_server"]
        database = self.user["database"]
        cluster = self.datasource_to_replace.cluster
        table_landing_mirror = datasource.id
        table_landing_mirror_quarantine = f"{table_landing_mirror}_quarantine"
        table_to_replace = self.datasource_to_replace.id
        table_to_replace_quarantine = f"{table_to_replace}_quarantine"
        view_name = f"{table_landing_mirror_quarantine}_generator_{self._mirror_table_sufix}"

        # Check the replace condition to verify it's valid and replace any tables used in the condition
        try:
            select_query = f"SELECT * FROM {self.datasource_to_replace.id} WHERE ({self.replace_condition})"
            replaced_select = Users.replace_tables(self.user, select_query)
            self.replace_condition = replaced_select[replaced_select.find("WHERE") + len("WHERE") :]
        except Exception as e:
            error_message = f"Failed to apply replace_condition='{self.replace_condition}': {str(e)}"
            logging.warning(f"{error_message}")
            raise ValueError(error_message) from e

        self.table_locations_to_drop.append(CHTableLocation(database, view_name))
        self.table_locations_to_drop.append(CHTableLocation(database, table_landing_mirror))
        self.table_locations_to_drop.append(CHTableLocation(database, table_landing_mirror_quarantine))

        # Create a landing table
        # - Matching the schema,
        # - using a Null() engine,
        # - forwarding the data to another table but filtered.
        ch_create_table_as_table_sync(
            database_server,
            database,
            table_landing_mirror,
            table_to_replace,
            engine="Null()",
            cluster=cluster,
            not_exists=True,
            **self.get_extra_params(),
        )
        # Push quarantine data into the original quarantine table
        try:
            ch_create_table_as_table_sync(
                database_server,
                database,
                table_landing_mirror_quarantine,
                table_to_replace_quarantine,
                engine="Null()",
                cluster=cluster,
                not_exists=True,
                **self.get_extra_params(),
            )
        except CHException as e:
            if e.code == CHErrors.UNKNOWN_TABLE:
                create_quarantine_table_from_landing_sync(
                    landing_datasource_name=table_to_replace,
                    database_server=database_server,
                    database=database,
                    cluster=cluster,
                )

                ch_create_table_as_table_sync(
                    database_server,
                    database,
                    table_landing_mirror_quarantine,
                    table_to_replace_quarantine,
                    engine="Null()",
                    cluster=cluster,
                    not_exists=True,
                    **self.get_extra_params(),
                )
            else:
                raise e

        view_sql = f"SELECT * FROM {database}.{table_landing_mirror_quarantine}"
        ch_create_materialized_view_sync(
            database_server,
            database,
            view_name,
            view_sql,
            table_to_replace_quarantine,
            cluster=cluster,
            if_not_exists=True,
            **self.get_extra_params(),
        )
        return True

    def after_create(self, datasource: Datasource):
        database_server = self.user["database_server"]
        database = self.user["database"]
        cluster = self.datasource_to_replace.cluster
        table_landing_mirror = datasource.id
        table_to_replace = self.datasource_to_replace.id
        # Create another table
        # - Matching the schema and the engine,
        # - will receive the data from the landing table but filtered.
        table_landing_mirror_filtered = f"{table_landing_mirror}_filtered_{self._mirror_table_sufix}"
        # Create a materialized view that pushes from the landing to the filtered table
        table_landing_to_filtered = f"{table_landing_mirror}_landing_to_filtered_{self._mirror_table_sufix}"

        self.table_locations_to_drop = [
            CHTableLocation(database, table_landing_to_filtered),
            CHTableLocation(database, table_landing_mirror_filtered),
            *self.table_locations_to_drop,
        ]

        table_details = ch_table_details(table_to_replace, database_server, database)
        ch_create_table_as_table_sync(
            database_server,
            database,
            table_landing_mirror_filtered,
            table_to_replace,
            engine=table_details.engine_full,
            cluster=cluster,
            not_exists=True,
            **self.get_extra_params(),
        )

        view_sql = f"""
        SELECT *
        FROM {database}.{table_landing_mirror}
        WHERE {self.replace_condition}
        """
        ch_create_materialized_view_sync(
            database_server,
            database,
            table_landing_to_filtered,
            view_sql,
            table_landing_mirror_filtered,
            cluster=cluster,
            if_not_exists=True,
            **self.get_extra_params(),
        )

    def after_append(self, datasource: Datasource) -> None:
        reporter = ReplacePartialDataSourceReporter(self._job_id)
        try:
            self._after_append(datasource, reporter)
            reporter.mark_dss_as_replaced()
        except Exception as e:
            reporter.mark_ongoing_work_as_error()
            logging.exception(e)
            raise e

    def _after_append(self, datasource: Datasource, reporter: ReplacePartialDataSourceReporter) -> None:
        database_server = self.user.database_server
        database = self.user.database
        cluster = self.user.cluster
        join_algorithm = self.user.get_join_algorithm()
        table_landing_mirror = datasource.id
        table_to_replace = self.datasource_to_replace.id
        table_landing_mirror_filtered = f"{table_landing_mirror}_filtered_{self._mirror_table_sufix}"

        if cluster:
            max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
            )
            replication_success = CHReplication.ch_wait_for_replication_sync(
                database_server,
                cluster,
                database,
                table_landing_mirror_filtered,
                wait=max_wait_for_replication_seconds,
                **self.get_extra_params(ddl_parameters=False),
            )
            if not replication_success:
                error_message = f"Failed to wait for replication of replacement data in table {database}.{table_landing_mirror_filtered}"
                logging.error(error_message)
                raise RuntimeError(error_message)

        # Create another table
        # - Matching the schema and the engine,
        # - will merge existing data and replacing (remove + insert) the new data based on the condition.
        table_landing_replaced = f"{table_landing_mirror}_replaced_{self._mirror_table_sufix}"
        self.table_locations_to_drop.append(CHTableLocation(database, table_landing_replaced))
        table_details = ch_table_details(table_to_replace, database_server, database)
        ch_create_table_as_table_sync(
            database_server,
            database,
            table_landing_replaced,
            table_to_replace,
            engine=table_details.engine_full,
            cluster=cluster,
            not_exists=True,
            **self.get_extra_params(),
        )

        # Find the partitions present in the filtered table
        partitions = ch_table_partitions_sync(
            database_server=database_server,
            database_name=database,
            table_names=[table_landing_mirror_filtered],
            query_settings=self.get_extra_params(ddl_parameters=False),
        )

        if partitions:
            # Add all partitions we discovered through the mirror table
            try:
                lock_acquire_timeout = self.user.get_limits(prefix="ch").get(
                    "lock_acquire_timeout", Limit.ch_lock_acquire_timeout
                )
                max_execution_time_replace_partitions = self.user.get_limits(prefix="ch").get(
                    "max_execution_time_replace_partitions", Limit.ch_max_execution_time_replace_partitions
                )
                ch_replace_partitions_sync(
                    database_server,
                    database,
                    table_landing_replaced,
                    table_to_replace,
                    partitions,
                    wait_setting=WAIT_ALTER_REPLICATION_OWN,
                    lock_acquire_timeout=lock_acquire_timeout,
                    max_execution_time=max_execution_time_replace_partitions,
                    **self.get_extra_params(ddl_parameters=False),
                )

                if cluster:
                    max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                        "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
                    )

                    replication_success = CHReplication.ch_wait_for_replication_sync(
                        database_server,
                        cluster,
                        database,
                        table_landing_replaced,
                        wait=max_wait_for_replication_seconds,
                        **self.get_extra_params(ddl_parameters=False),
                    )
                    if not replication_success:
                        error_message = (
                            f"Failed to wait for replication of replacement data in {database}.{table_landing_replaced}"
                        )
                        logging.error(error_message)
                        raise RuntimeError(error_message)

            except CHException as che:
                if che.code == CHErrors.INVALID_PARTITION_VALUE:
                    raise HookException(
                        f"Invalid partition when replacing data at Data Source '{datasource.name}'. Reason: {che}"
                    ) from che
                raise

            # Delete any data that matches the replace condition
            on_cluster = f"ON CLUSTER {cluster}" if cluster else ""
            sql = f"""
            ALTER TABLE {database}.{table_landing_replaced}
            {on_cluster}
            DELETE WHERE {self.replace_condition}
            """

            ok, e = self.run_query(
                sql,
                read_only=False,
                join_algorithm=join_algorithm,
                alter_sync=VALID_WAIT_VALUES.index(WAIT_ALTER_REPLICATION_OWN),
                **self.get_extra_params(),
            )
            if not ok:
                raise e

            # Check mutations status
            # Avoid moving the partitions without the mutations applied.
            max_mutations_seconds_to_wait = self.user.get_limits(prefix="ch").get(
                "max_mutations_seconds_to_wait", Limit.ch_max_mutations_seconds_to_wait
            )
            mutations_success = ch_wait_for_mutations_sync(
                database_server,
                database,
                table_landing_replaced,
                max_mutations_seconds_to_wait=max_mutations_seconds_to_wait,
                cluster=cluster,
                skip_unavailable_replicas=True,
                **self.get_extra_params(ddl_parameters=False),
            )
            if not mutations_success:
                error_message = "Failed to wait for mutations of replacement data"
                logging.error(error_message)
                raise RuntimeError(error_message)

            # Fill data from the filtered table
            sql = f"""
            INSERT INTO {database}.{table_landing_replaced}
            SELECT * FROM {database}.{table_landing_mirror_filtered}
            """

            max_insert_threads = self.user.get_limits(prefix="ch").get(
                "max_insert_threads", Limit.ch_max_insert_threads
            )
            ok, e = self.run_query(
                sql,
                read_only=False,
                max_execution_time=3600,
                max_insert_threads=max_insert_threads,
                join_algorithm=join_algorithm,
                **self.get_extra_params(ddl_parameters=False),
            )
            if not ok:
                raise e

            if cluster:
                max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                    "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
                )
                replication_success = CHReplication.ch_wait_for_replication_sync(
                    database_server,
                    cluster,
                    database,
                    table_landing_replaced,
                    wait=max_wait_for_replication_seconds,
                    **self.get_extra_params(ddl_parameters=False),
                )
                if not replication_success:
                    error_message = (
                        f"Failed to wait for replication of replacement data in {database}.{table_landing_replaced}"
                    )
                    logging.error(error_message)
                    raise RuntimeError(error_message)

            # change all partitions later
            self._replace_partitions_tables.append(
                (database_server, database, table_to_replace, table_landing_replaced)
            )

            extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]] = {
                (self.user.database, self.datasource_to_replace.id): (self.user.database, table_landing_replaced)
                # TODO question May also be useful to filter here by the partitions? WHERE {source_table_meta['partition_key']} IN ({','.join(partitions)})
            }

            partial_replace_steps, skipped_steps = _calculate_execution_steps(
                table_details,
                self.user,
                self.datasource_to_replace,
                skip_incompatible_partition_key=self._skip_incompatible_partition_key,
            )

            reporter.add_steps(partial_replace_steps)
            reporter.add_skipped_steps(skipped_steps)

            for step_index, step in enumerate(partial_replace_steps):
                reporter.change_step_status(step_index, ReplaceStatus.WORKING)

                self._execute_partial_replace_step(
                    step,
                    extra_replacements,
                    partitions,
                    reporter,
                    step_index,
                    origin_datasource=self.datasource_to_replace,
                    origin_workspace=self.user,
                )

                reporter.change_step_status(step_index, ReplaceStatus.READY)

            for database_server, database, destination_table, origin_table in self._replace_partitions_tables:
                try:
                    lock_acquire_timeout = self.user.get_limits(prefix="ch").get(
                        "lock_acquire_timeout", Limit.ch_lock_acquire_timeout
                    )
                    max_execution_time_replace_partitions = self.user.get_limits(prefix="ch").get(
                        "max_execution_time_replace_partitions", Limit.ch_max_execution_time_replace_partitions
                    )
                    ch_replace_partitions_sync(
                        database_server,
                        database,
                        destination_table,
                        origin_table,
                        partitions,
                        wait_setting=WAIT_ALTER_REPLICATION_OWN,
                        lock_acquire_timeout=lock_acquire_timeout,
                        max_execution_time=max_execution_time_replace_partitions,
                        **self.get_extra_params(ddl_parameters=False),
                    )

                    if cluster:
                        max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                            "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
                        )

                        replication_success = CHReplication.ch_wait_for_replication_sync(
                            database_server,
                            cluster,
                            database,
                            destination_table,
                            wait=max_wait_for_replication_seconds,
                            **self.get_extra_params(ddl_parameters=False),
                        )
                        if not replication_success:
                            error_message = (
                                f"Failed to wait for replication of replacement data in {database}.{destination_table}"
                            )
                            logging.error(error_message)
                            raise RuntimeError(error_message)

                except CHException as che:
                    if che.code == CHErrors.INVALID_PARTITION_VALUE:
                        raise HookException(
                            f"Error replacing data at '{datasource.name}', the depedent Data Source '{destination_table}' does not have a compatible partition. Check the PARTITION KEY is present and it's the same in both Data Sources. e.g. both Data Sources are partitions using toYYYYMM or toDate, as opposed to one having toYYMMMM and the other tuple(). Reason details: {che}"
                        ) from che
                    raise

            if len(self._tables_to_swap):
                ch_swap_tables_sync(
                    self.user.database_server,
                    self._tables_to_swap,
                    cluster,
                    **self.get_extra_params(),
                )

        self.tear_down(datasource)

    def _execute_partial_replace_step(
        self,
        step: PartialReplaceSteps,
        extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]],
        partitions: List[str],
        reporter: ReplacePartialDataSourceReporter,
        step_index: int,
        origin_datasource: Datasource,
        origin_workspace: User,
    ):
        table_details = ch_table_details(
            table_name=step.ds_to_replace.id,
            database_server=step.ds_workspace.database_server,
            database=step.ds_workspace.database,
        )
        if not table_details:
            raise HookException(
                f"The partial replace can't be executed as the Data Source '{step.ds_to_replace.name}' "
                f"was deleted before the replace finished."
            )
        if need_swap(table_details):
            mirror_table = self.create_staging_table(
                step.ds_workspace,
                table_details,
                cluster=step.ds_workspace.cluster,
                mirror_table_sufix=self._mirror_table_sufix,
                **self.get_extra_params(),
            )

            self._tables_to_swap.append(TablesToSwap(step.ds_workspace.database, step.ds_to_replace.id, mirror_table))

        else:
            # TODO get rid of this abstraction for "create_mirror_table_once". We can extract it to a function.
            def create_mirror_table_once():
                def wrapper():
                    if wrapper.mirror_table_name is None:  # type: ignore[attr-defined]
                        #  Create a mirror table where the view will redirect the data to.
                        wrapper.mirror_table_name = f"{step.ds_to_replace.id}_mirror_{self._mirror_table_sufix}"  # type: ignore[attr-defined]
                        self.table_locations_to_drop.insert(
                            0,
                            CHTableLocation(step.ds_workspace.database, wrapper.mirror_table_name),  # type: ignore[attr-defined]
                        )
                        ch_create_table_as_table_sync(
                            step.ds_workspace.database_server,
                            step.ds_workspace.database,
                            wrapper.mirror_table_name,  # type: ignore[attr-defined]
                            step.ds_to_replace.id,
                            engine=table_details.engine_full,
                            cluster=step.ds_workspace.cluster,
                            not_exists=True,
                            **self.get_extra_params(),
                        )
                        self._replace_partitions_tables.append(
                            (
                                step.ds_workspace.database_server,
                                step.ds_workspace.database,
                                step.ds_to_replace.id,
                                wrapper.mirror_table_name,  # type: ignore[attr-defined]
                            )
                        )
                    return wrapper.mirror_table_name  # type: ignore[attr-defined]

                wrapper.mirror_table_name = None  # type: ignore[attr-defined]
                return wrapper

            get_or_create_mirror_table = create_mirror_table_once()
            mirror_table = get_or_create_mirror_table()

        ops_log_options = {
            "replace_origin_datasource": origin_datasource.id,
            "replace_origin_workspace": origin_workspace.id,
        }

        join_algorithm = origin_workspace.get_join_algorithm()
        null_feature_activated = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PARTIAL_REPLACES_WITH_NULL_TABLES, "", self.user.feature_flags
        )
        max_insert_threads = self.user.get_limits(prefix="ch").get("max_insert_threads", Limit.ch_max_insert_threads)

        for mv_index, mv_to_recalculate in enumerate(step.mvs_to_recalculate):
            start_time = datetime.now(timezone.utc)
            reporter.change_mv_status(step_index, mv_index, ReplaceStatus.WORKING)

            source_table = ch_source_table_for_view_sync(
                step.ds_workspace.database_server,
                step.ds_workspace.database,
                mv_to_recalculate.node.id,
                **self.get_extra_params(ddl_parameters=False),
            )
            if not source_table:
                raise Exception(
                    f"Source table not found for materialized view {step.ds_to_replace.name} in workspace {step.ds_workspace.name} (node {mv_to_recalculate.node.name})"
                )

            if null_feature_activated:
                generate_insert_sql_function = self._prepare_insert_query_with_null_table_to_repopulate_with_new_data
            else:
                generate_insert_sql_function = self._prepare_insert_query_to_repopulate_with_new_data

            insert_sql = generate_insert_sql_function(
                destination_ds_workspace=step.ds_workspace,
                destination_ds_table_details=table_details,
                destination_ds_mirror=mirror_table,
                mv_to_recalculate=mv_to_recalculate,
                mv_source_table=source_table,
                extra_replacements=extra_replacements,
                partitions_involved=partitions,
            )

            try:
                self.run_query_with_replica_support(
                    insert_sql,
                    table_details,
                    source_database=source_table.database,
                    source_table=source_table.table,
                    cluster=step.ds_workspace.cluster,
                    max_insert_threads=max_insert_threads,
                    join_algorithm=join_algorithm,
                    user_agent="no-tb-internal-replace",
                    **self.get_extra_params(ddl_parameters=False),
                )
            except Exception as e:
                logging.exception(e)

                self.log_operation(
                    "replace",
                    datasource=step.ds_to_replace,
                    error=str(e),
                    options={**self.ops_log_options, **ops_log_options},
                    workspace=step.ds_workspace,
                )

                statsd_prefix = StatsdReplacesMetrics.replaces_dependent_error(
                    replace_type=self.replace_type,
                    database_server=sanitize_database_server(self.user.database_server),
                    destination_workspace_id=step.ds_workspace.id,
                    destination_datasource_id=step.ds_to_replace.id,
                )

                statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - start_time).seconds)

                raise e

            rows, _ = self.get_rows(step.ds_to_replace)
            self.log_operation(
                "replace",
                datasource=step.ds_to_replace,
                rows=rows,
                options={**self.ops_log_options, **ops_log_options},
                workspace=step.ds_workspace,
            )

            reporter.change_mv_status(step_index, mv_index, ReplaceStatus.DONE)

            statsd_prefix = StatsdReplacesMetrics.replaces_dependent_success(
                replace_type=self.replace_type,
                database_server=sanitize_database_server(self.user.database_server),
                destination_workspace_id=step.ds_workspace.id,
                destination_datasource_id=step.ds_to_replace.id,
            )

            statsd_client.timing(statsd_prefix, (datetime.now(timezone.utc) - start_time).seconds)

        # Make the replacement DS available for future execution steps:
        extra_replacements[(step.ds_workspace.database, step.ds_to_replace.id)] = (
            step.ds_workspace.database,
            mirror_table,
        )

    @staticmethod
    def _prepare_insert_query_to_repopulate_with_new_data(
        destination_ds_workspace: User,
        destination_ds_table_details: TableDetails,
        destination_ds_mirror: str,
        mv_to_recalculate: MVToRecalculate,
        mv_source_table: CHTableLocation,
        extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]],
        partitions_involved: List[str],
    ) -> str:
        extra_replacements_for_query = extra_replacements.copy()

        source_table_details = ch_table_details(
            mv_source_table.table, destination_ds_workspace.database_server, mv_source_table.database
        )

        # handle tuple() partitions
        if not source_table_details.partition_key:
            where_clause = ""
            not_where_clause = ""
        else:
            where_clause = f"WHERE {source_table_details.partition_key} IN ({','.join(partitions_involved)})"
            not_where_clause = f"WHERE {source_table_details.partition_key} NOT IN ({','.join(partitions_involved)})"

        if not mv_to_recalculate.source_has_been_replaced and not need_swap(source_table_details):
            extra_replacements_for_query[(source_table_details.database, source_table_details.name)] = f"""(
                    SELECT *
                    FROM {source_table_details.database}.{source_table_details.name}
                    {where_clause}
                )"""
        elif (
            mv_to_recalculate.source_has_been_replaced
            and need_swap(destination_ds_table_details)
            and not need_swap(source_table_details)
        ):
            # If current DS needs swap and source has been replaced, calculate MV with:
            # - New partitions from replaced table
            # - old partitions from original table
            source_replaced = extra_replacements[(source_table_details.database, source_table_details.name)]
            extra_replacements_for_query[(source_table_details.database, source_table_details.name)] = f"""(
                SELECT *
                FROM {source_replaced[0]}.{source_replaced[1]}
                {where_clause}
                UNION ALL
                SELECT *
                FROM {source_table_details.database}.{source_table_details.name}
                {not_where_clause}
            )"""

            # we do this to let know `sql_toolset.replace_tables` the tables inside the previous query are legit
            extra_replacements_for_query[(source_replaced[0], source_replaced[1])] = (
                source_replaced[0],
                source_replaced[1],
            )

        select_sql = Users.replace_tables(
            destination_ds_workspace,
            mv_to_recalculate.node.sql,
            pipe=mv_to_recalculate.pipe,
            use_pipe_nodes=True,
            extra_replacements=extra_replacements_for_query,
        )
        columns = ch_get_columns_from_query_sync(
            destination_ds_workspace.database_server, destination_ds_workspace.database, select_sql
        )
        insert_sql = f"""
        INSERT INTO {destination_ds_workspace.database}.{destination_ds_mirror}
        (
            {','.join([f"`{c['name']}`" for c in columns])}
        )
        {select_sql}
        """

        return insert_sql

    def _prepare_insert_query_with_null_table_to_repopulate_with_new_data(
        self,
        destination_ds_workspace: User,
        destination_ds_table_details: TableDetails,
        destination_ds_mirror: str,
        mv_to_recalculate: MVToRecalculate,
        mv_source_table: CHTableLocation,
        extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]],
        partitions_involved: List[str],
    ) -> str:
        extra_replacements_for_query = extra_replacements.copy()

        source_table_details = ch_table_details(
            table_name=mv_source_table.table,
            database_server=destination_ds_workspace.database_server,
            database=mv_source_table.database,
        )

        # handle tuple() partitions
        if not source_table_details.partition_key:
            where_clause = ""
            not_where_clause = ""
        else:
            where_clause = f"WHERE {source_table_details.partition_key} IN ({','.join(partitions_involved)})"
            not_where_clause = f"WHERE {source_table_details.partition_key} NOT IN ({','.join(partitions_involved)})"

        if not mv_to_recalculate.source_has_been_replaced and not need_swap(source_table_details):
            extra_replacements_for_query[(source_table_details.database, source_table_details.name)] = f"""(
                    SELECT *
                    FROM {source_table_details.database}.{source_table_details.name}
                    {where_clause}
                )"""
        elif (
            mv_to_recalculate.source_has_been_replaced
            and need_swap(destination_ds_table_details)
            and not need_swap(source_table_details)
        ):
            # If current DS needs swap and source has been replaced, calculate MV with:
            # - New partitions from replaced table
            # - old partitions from original table
            source_replaced = extra_replacements[(source_table_details.database, source_table_details.name)]
            extra_replacements_for_query[(source_table_details.database, source_table_details.name)] = f"""(
                SELECT *
                FROM {source_replaced[0]}.{source_replaced[1]}
                {where_clause}
                UNION ALL
                SELECT *
                FROM {source_table_details.database}.{source_table_details.name}
                {not_where_clause}
            )"""

            # we do this to let know `sql_toolset.replace_tables` the tables inside the previous query are legit
            extra_replacements_for_query[(source_replaced[0], source_replaced[1])] = (
                source_replaced[0],
                source_replaced[1],
            )

        if need_swap(destination_ds_table_details):
            # Extracted from the Populate's code:
            # join tables need to be populated without chunks because if the mat view contains a group by and they join
            # key is in the grouping keys when they are inserted in many batches, later batches could override the first
            # ones.
            select_sql = Users.replace_tables(
                destination_ds_workspace,
                mv_to_recalculate.node.sql,
                pipe=mv_to_recalculate.pipe,
                use_pipe_nodes=True,
                extra_replacements=extra_replacements_for_query,
            )
            table_to_write_in = destination_ds_mirror

        else:
            view_sql = Users.replace_tables(
                destination_ds_workspace,
                mv_to_recalculate.node.sql,
                pipe=mv_to_recalculate.pipe,
                use_pipe_nodes=True,
                extra_replacements=extra_replacements,
            )

            mv_has_a_new_mv_source_table = extra_replacements.get(
                (mv_source_table.database, mv_source_table.table), None
            )
            if mv_has_a_new_mv_source_table:
                mv_source_table = CHTableLocation(mv_has_a_new_mv_source_table[0], mv_has_a_new_mv_source_table[1])

            # Create new Null table + MV.

            # The NULL table will be recreated for each MV. If two different MVs part from DS1 to DS2 the Table is the same.
            sufix_for_new_resources = str(uuid.uuid4())[:8]
            temporal_null_table, temporal_view_from_null_table = ch_create_null_table_with_mv_for_mv_populate(
                workspace=destination_ds_workspace,
                source_table=mv_source_table,
                target_table=destination_ds_mirror,
                target_table_details=destination_ds_table_details,
                temporal_table_sufix=f"tmp_replace_{self._mirror_table_sufix}_{sufix_for_new_resources}",
                view_sql=view_sql,
                temporal_view_sufix=f"tmp_replace_view_{self._mirror_table_sufix}_{sufix_for_new_resources}",
                **self.get_extra_params(),
            )

            self.table_locations_to_drop = [
                CHTableLocation(destination_ds_workspace.database, temporal_view_from_null_table),
                CHTableLocation(destination_ds_workspace.database, temporal_null_table),
                *self.table_locations_to_drop,
            ]

            select_sql = f"SELECT * FROM {source_table_details.database}.{source_table_details.name}"

            select_sql = Users.replace_tables(
                destination_ds_workspace, select_sql, extra_replacements=extra_replacements_for_query
            )
            table_to_write_in = temporal_null_table

        columns = ch_get_columns_from_query_sync(
            destination_ds_workspace.database_server, destination_ds_workspace.database, select_sql
        )

        insert_sql = f"""
        INSERT INTO {destination_ds_workspace.database}.{table_to_write_in}
        (
            {','.join([f"`{c['name']}`" for c in columns])}
        )
        {select_sql}
        """

        return insert_sql


def _calculate_execution_steps(
    original_table_details: TableDetails,
    workspace: User,
    datasource_to_replace: Datasource,
    skip_incompatible_partition_key: bool,
) -> Tuple[List[PartialReplaceSteps], List[PartialReplaceSteps]]:
    datasource_deps = defaultdict(set)
    mvs_that_write_to_ds = defaultdict(list)

    map_ds_to_id: Dict[str, Datasource] = {datasource_to_replace.id: datasource_to_replace}
    map_ds_to_workspace: Dict[str, User] = {datasource_to_replace.id: workspace}

    skipped_replaces: List[PartialReplaceSteps] = []

    datasources_to_analyze = [(workspace, datasource_to_replace)]
    datasources_visited = set()

    while len(datasources_to_analyze) > 0:
        datasource_to_analyze = datasources_to_analyze.pop()
        if datasource_to_analyze[1].id in datasources_visited:
            continue
        datasources_visited.add(datasource_to_analyze[1].id)

        dependent_views = ch_table_dependent_views_sync(
            datasource_to_analyze[0].database_server, datasource_to_analyze[0].database, datasource_to_analyze[1].id
        )
        map_database_to_workspace = _map_database_to_workspace(datasource_to_analyze[0], datasource_to_analyze[1].id)

        for dependent_view in dependent_views:
            if dependent_view.database not in map_database_to_workspace:
                logging.warning(
                    f"Dependent view is in a deleted workspace: {dependent_view.database}.{dependent_view.table}"
                )
                continue

            workspace_with_dependent_view = map_database_to_workspace[dependent_view.database]
            node = Users.get_node(workspace_with_dependent_view, dependent_view.table)
            if not node:
                raise could_not_find_query_to_populate_depending_view_exception(
                    f"{dependent_view.database}.{dependent_view.table}"
                )
            assert isinstance(node, PipeNode)

            pipe = Users.get_pipe_by_node(workspace_with_dependent_view, node.id)
            assert isinstance(pipe, Pipe)

            dependent_ds = Users.get_datasource(workspace_with_dependent_view, node.materialized)
            if not dependent_ds:
                # looks like there is a pipe with a materialzed node that points to a table
                # that was removed
                pipe = Users.get_pipe_by_node(workspace_with_dependent_view, dependent_view.table)
                assert isinstance(pipe, Pipe)

                raise could_not_find_dependent_table_to_populate_exception(
                    pipe.name, node.name, node.id, f"{workspace_with_dependent_view.database}{node.materialized}"
                )
            dependent_ds_details = ch_table_details(
                table_name=dependent_ds.id,
                database_server=workspace_with_dependent_view.database_server,
                database=workspace_with_dependent_view.database,
            )
            if not partition_value_can_be_replaced_in_the_destination_ds(
                workspace_with_dependent_view.database_server, original_table_details, dependent_ds_details
            ):
                if skip_incompatible_partition_key:
                    skipped_replaces.append(
                        PartialReplaceSteps(
                            ds_to_replace=dependent_ds,
                            ds_workspace=workspace_with_dependent_view,
                            mvs_to_recalculate=[],
                        )
                    )
                    continue
                else:
                    raise HookException(
                        f"Partial replace can't be executed as at least one of the Data Sources involved ({dependent_ds.name}) has incompatible partitions. Check the PARTITION KEY is present and it's the same in both Data Sources. e.g. both Data Sources are partitions using toYYYYMM or toDate, as opposed to one having toYYMMMM and the other tuple(). If you want to ignore all the Data Sources with incompatible partitions in the replace operation, please use the option 'skip_incompatible_partition_key' to skip them."
                    )

            datasource_deps[(workspace_with_dependent_view.id, dependent_ds.id)].add(
                (datasource_to_analyze[0].id, datasource_to_analyze[1].id)
            )
            mvs_that_write_to_ds[dependent_ds.id].append(MVToRecalculate(pipe, node, True))
            map_ds_to_id[dependent_ds.id] = dependent_ds
            map_ds_to_workspace[dependent_ds.id] = workspace_with_dependent_view

            datasources_to_analyze.append((workspace_with_dependent_view, dependent_ds))

    def mv_writes_to_this_ds_and_is_not_already_added(pipe: Pipe, node: PipeNode, dependent_ds_id: str) -> bool:
        if node.materialized == dependent_ds_id:
            list_of_mvs = [
                (mv_location.pipe, mv_location.node) for mv_location in mvs_that_write_to_ds[dependent_ds_id]
            ]
            if (pipe, node) not in list_of_mvs:
                return True
        return False

    # Search for MVs that write to the DSs that depends on the original DS being replaced.
    for ds_location in datasource_deps:
        workspace_where_ds_exists = User.get_by_id(ds_location[0])
        for p in workspace_where_ds_exists.get_pipes():
            for n in p.pipeline.nodes:
                if mv_writes_to_this_ds_and_is_not_already_added(p, n, ds_location[1]):
                    mvs_that_write_to_ds[ds_location[1]].append(MVToRecalculate(p, n, False))

    partial_replace_steps = []

    ds_dep_graph_topological_sort = toposort(datasource_deps)
    for datasources_in_step in ds_dep_graph_topological_sort:
        for datasource_location in datasources_in_step:
            mvs_to_recalculate = mvs_that_write_to_ds[datasource_location[1]]
            if len(mvs_to_recalculate):
                partial_replace_steps.append(
                    PartialReplaceSteps(
                        ds_to_replace=map_ds_to_id[datasource_location[1]],
                        ds_workspace=map_ds_to_workspace[datasource_location[1]],
                        mvs_to_recalculate=mvs_to_recalculate,
                    )
                )
    return partial_replace_steps, skipped_replaces


def get_partial_replace_dependencies(workspace: User, datasource: Datasource) -> Dict[str, Any]:
    table_details = ch_table_details(
        table_name=datasource.id, database_server=workspace.database_server, database=workspace.database
    )

    partial_replace_steps, skipped_steps = _calculate_execution_steps(
        table_details, workspace, datasource, skip_incompatible_partition_key=True
    )

    return {
        "compatible_datasources": [
            ReplacePartialDataSourceReporter._map_replace_step_to_json(step) for step in partial_replace_steps
        ],
        "incompatible_datasources": ReplacePartialDataSourceReporter._map_skipped_steps_to_json(skipped_steps),
    }


class LastDateDatasourceHook(Hook):
    """
    creates a table datasource_last_date with the last date of the column "date"
    """

    DATE_COLUMN = "toDate(local_timeplaced)"

    def is_active(self, datasource: Datasource):
        return datasource.tags.get("last_date", False)

    def source_table_name(self, name: str):
        """
        >>> from tinybird.user import User, UserAccount
        >>> u = UserAccount.register('source_table_name@example.com', 'pass')
        >>> w = User.register('source_table_name', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> h = LastDateDatasourceHook(w)
        >>> h.source_table_name('sales_historic_landing__dev')
        'sales_historic__dev'
        >>> h.source_table_name('sales_historic_landing__v0')
        'sales_historic__v0'
        >>> h.source_table_name('sales_historic_landing')
        'sales_historic'
        >>> h.source_table_name('sales_historic__dev')
        'sales_historic__dev'
        >>> h.source_table_name('sales_historic__v0')
        'sales_historic__v0'
        >>> h.source_table_name('sales_historic')
        'sales_historic'
        """
        m = re.search(r"(.+)_landing__(dev|v[0-9]+)$", name)
        if m:
            return m.group(1) + "__" + m.group(2)
        LANDING_TAG = "_landing"
        if name.endswith(LANDING_TAG):
            return name[: -len(LANDING_TAG)]
        return name

    def get_last_date_datasources(self, read_ds: Datasource):
        """
        >>> from tinybird.user import User, UserAccount
        >>> u = UserAccount.register('last_date@example.com', 'pass')
        >>> w = User.register('last_date', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> read_ds = Users.add_datasource_sync(w, 'test')
        >>> write_ds = Users.add_datasource_sync(w, 'test_last_date')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date']

        >>> write_ds = Users.add_datasource_sync(w, 'test_last_date__dev')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date', 'test_last_date__dev']

        >>> read_ds = Users.add_datasource_sync(w, 'test__dev')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date', 'test_last_date__dev']

        >>> read_ds = Users.add_datasource_sync(w, 'test__v1')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date', 'test_last_date__dev']

        >>> write_ds = Users.add_datasource_sync(w, 'test_last_date__v0')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date', 'test_last_date__dev', 'test_last_date__v0']

        >>> read_ds = Users.add_datasource_sync(w, 'test_landing__v1')
        >>> h = LastDateDatasourceHook(w)
        >>> [ds.name for ds in h.get_last_date_datasources(read_ds)]
        ['test_last_date', 'test_last_date__dev', 'test_last_date__v0']
        """
        last_data_datasources = []

        suffix = "_last_date"

        def get_name_prefix(name: str):
            m = re.search(r"(.+)__(dev|v[0-9]+)$", name)
            if m:
                prefix_name = m.group(1)
                LANDING_TAG = "_landing"
                if prefix_name.endswith(LANDING_TAG):
                    prefix_name = prefix_name[: -len(LANDING_TAG)]
                return prefix_name + suffix
            return name + suffix

        datasources = Users.get_datasources(self.user)
        read_ds_name_prefix = get_name_prefix(read_ds.name)
        for ds in datasources:
            if ds.name.startswith(read_ds_name_prefix):
                last_data_datasources.append(ds)

        return last_data_datasources

    def after_append(self, datasource: Datasource):
        if not self.is_active(datasource):
            return
        read_ds = Users.get_datasource(self.user, self.source_table_name(datasource.name))
        if not read_ds:
            read_ds = Users.get_datasource(self.user, datasource.name)
        assert isinstance(read_ds, Datasource)
        write_datasources = self.get_last_date_datasources(read_ds)
        if write_datasources:
            for write_ds in write_datasources:
                # We check both max_date and max_time since CH does not necessarily updates both. For example:
                #   min_date:                              1970-01-01
                #   max_date:                              1970-01-01
                #   min_time:                              2022-02-01 00:00:00
                #   max_time:                              2022-02-01 23:59:59
                # OR
                #   min_date:                              2022-01-21
                #   max_date:                              2022-01-21
                #   min_time:                              1970-01-01 00:00:00
                #   max_time:                              1970-01-01 00:00:00
                ok, e = self.run_query(
                    f"""INSERT INTO {write_ds.id}
                        SELECT  greatest(max(max_date), toDate(max(max_time))),
                                now()
                        FROM system.parts
                        WHERE database='{self.user.database}' AND table='{read_ds.id}' AND active""",
                    read_only=False,
                )
                if not ok:
                    raise e
        else:
            logging.warning(f"Could not find 'last date' datasources for {datasource.name}")

    def after_truncate(self, datasource: Datasource):
        self.after_append(datasource)

    def after_delete_with_condition(self, datasource: Datasource):
        self.after_append(datasource)


class LandingDatasourceHook(Hook):
    def __init__(self, user):
        super().__init__(user)
        self.swapped_tables: Set[TablesToSwapWithWorkspace] = set()
        self.group_tables_to_swap = []
        self.unique_tables_to_swap = set()
        self.replace_type = "landing"

    def after_append(self, datasource: Datasource):
        database_server = self.user["database_server"]
        database = self.user["database"]

        # TODO use the returned database
        dependent_views = ch_table_dependent_views_sync(database_server, database, datasource.id)
        dependent_views_tables = [dependent.table for dependent in dependent_views]
        for dependent_view in dependent_views_tables:
            node = Users.get_node(self.user, dependent_view)
            if not node:
                logging.warning(f"Could not find the dependent node for the datasource='{datasource}'")
                continue
            staging = node.tags.get("staging", False)
            if not staging:
                continue

            dependent_ds = Users.get_datasource(self.user, node.materialized)
            if not dependent_ds:
                raise RuntimeError(f"Could not find the dependent table {node.materialized} to optimize")

            staging_staging_id = f"{dependent_ds.id}_staging"

            if self.user.cluster:
                max_wait_for_replication_seconds = self.user.get_limits(prefix="ch").get(
                    "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
                )
                replication_success = CHReplication.ch_wait_for_replication_sync(
                    database_server,
                    self.user.cluster,
                    database,
                    staging_staging_id,
                    wait=max_wait_for_replication_seconds,
                    wait_for_merges=True,
                )
                if not replication_success:
                    error_message = f"Failed to wait for replication in table {database}.{staging_staging_id} when optimizing datasource '{dependent_ds.name}'"
                    logging.error(error_message)
                    raise RuntimeError(error_message)

            with Timer("OPTIMIZE TABLE") as timing:
                sql = f"OPTIMIZE TABLE {database}.{staging_staging_id} FINAL"
                for _ in range(3):
                    ok, e = self.run_query(sql, read_only=False, max_execution_time=DEFAULT_BATCH_EXECUTION_TIME)
                    if ok:
                        break
                if not ok:
                    raise e
            self.log_event(datasource, "optimize_query", timing)

            with Timer("POPULATE VIEWS") as timing:
                # Look for depending views and optimize/switch them as well
                self.populate_dependent_views(
                    dependent_ds.id,
                    staging_staging_id,
                    self.user.database_server,
                    self.user.database,
                    self.user.cluster,
                )
                logging.info(f"Tables to swap: {self.group_tables_to_swap}")
                self.group_tables_to_swap = []

            self.log_event(datasource, "populate_views", timing)

            with Timer("RESET STAGING TABLE") as timing:
                partitions = ch_table_partitions_sync(
                    database_server=database_server,
                    database_name=database,
                    table_names=[staging_staging_id, dependent_ds.id],
                )
                if partitions:
                    lock_acquire_timeout = self.user.get_limits(prefix="ch").get(
                        "lock_acquire_timeout", Limit.ch_lock_acquire_timeout
                    )
                    max_execution_time_replace_partitions = self.user.get_limits(prefix="ch").get(
                        "max_execution_time_replace_partitions", Limit.ch_max_execution_time_replace_partitions
                    )
                    ch_replace_partitions_sync(
                        database_server,
                        database,
                        staging_staging_id,
                        dependent_ds.id,
                        partitions,
                        max_execution_time=max_execution_time_replace_partitions,
                        wait_setting=WAIT_ALTER_REPLICATION_OWN,
                        lock_acquire_timeout=lock_acquire_timeout,
                    )
            self.log_event(datasource, "reset_staging_table", timing)

        self.tear_down(datasource)

    def after_truncate(self, datasource):
        self.after_append(datasource)

    def after_delete_with_condition(self, datasource):
        self.after_append(datasource)


class DBSizeTrackerDatasourceHook(Hook):
    pass


def _prepare_replace(
    workspace: User, datasource: Datasource, datasource_to_replace: Datasource, **extra_params: Any
) -> List[CHTableLocation]:
    database_server = workspace.database_server
    database = workspace.database
    cluster = workspace.cluster

    table_details = ch_table_details(datasource_to_replace.id, database_server, database)
    ch_create_table_as_table_sync(
        database_server,
        database,
        table_name=datasource.id,
        as_table_name=datasource_to_replace.id,
        engine=table_details.engine_full,
        cluster=cluster,
        not_exists=True,
        **extra_params,
    )

    # redirect quarantine table
    table_to_replace_quarantine = datasource_to_replace.id + "_quarantine"
    temporal_quarantine = datasource.id + "_quarantine"
    try:
        ch_create_table_as_table_sync(
            database_server,
            database,
            table_name=temporal_quarantine,
            as_table_name=table_to_replace_quarantine,
            engine="Null()",
            cluster=cluster,
            not_exists=True,
            **extra_params,
        )
    except CHException as e:
        # When running a replace in a branch, we might not have a quarantine table. https://gitlab.com/tinybird/analytics/-/issues/9012
        # So we need to create one manually instead of using CREATE TABLE __ AS
        if e.code == CHErrors.UNKNOWN_TABLE:
            create_quarantine_table_from_landing_sync(
                landing_datasource_name=datasource_to_replace.id,
                database_server=database_server,
                database=database,
                cluster=cluster,
            )

            ch_create_table_as_table_sync(
                database_server,
                database,
                table_name=temporal_quarantine,
                as_table_name=table_to_replace_quarantine,
                engine="Null()",
                cluster=cluster,
                not_exists=True,
                **extra_params,
            )
        else:
            raise e

    view_name = f"{datasource.id}_generator"
    view_sql = f"SELECT * FROM {database}.{temporal_quarantine}"
    ch_create_materialized_view_sync(
        database_server,
        database,
        view_name,
        view_sql,
        target_table=table_to_replace_quarantine,
        cluster=cluster,
        if_not_exists=True,
        **extra_params,
    )

    return [
        CHTableLocation(database, view_name),
        CHTableLocation(database, temporal_quarantine),
        CHTableLocation(database, datasource.id),
    ]
