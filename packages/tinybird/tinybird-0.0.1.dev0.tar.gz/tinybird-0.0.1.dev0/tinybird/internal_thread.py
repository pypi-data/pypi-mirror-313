import json
import logging
import queue
import threading
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, cast

import requests.exceptions

from tinybird.ch import CHException, HTTPClient, ch_get_clusters_hosts, ch_insert_rows_sync, host_port_from_url
from tinybird.constants import BillingPlans
from tinybird.model import RedisModel
from tinybird.plans import PlansService
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, UserAccountDoesNotExist, public
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.retry.retry import retry_sync


class InternalThread(threading.Thread):
    """Base class for all our internal threads.
    Please, implement `action()` in your derived class.
    """

    def __init__(self, name: str, exit_queue_timeout: float = 600, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.name: str = name
        self.exit_queue: queue.Queue = queue.Queue()
        self.exit_queue_timeout: float = exit_queue_timeout
        self._root_statsd_key = f"tinybird-internal-thread.{statsd_client.region_app_machine}.{self.name}"
        self._exit_requested: bool = False

    def terminate(self) -> None:
        if self._exit_requested:
            return
        self.exit_queue.put(True)

    def is_exit_requested(self, wait: bool = False) -> bool:
        if self._exit_requested:
            return True

        try:
            exit_event: Optional[bool]

            if wait:
                exit_event = self.exit_queue.get(timeout=self.exit_queue_timeout)
            else:
                exit_event = self.exit_queue.get_nowait()

            if exit_event:
                self._exit_requested = True
        except queue.Empty:
            pass
        except Exception as e:
            logging.exception(f"Error fetching from exit_queue on internal thread '{self.name}': {e}")
            pass
        return self._exit_requested

    @staticmethod
    def get_public_user() -> Optional[Workspace]:
        try:
            return public.get_public_user()
        except UserAccountDoesNotExist:
            return None

    def incr_counter(self, counter_name: str) -> None:
        statsd_client.incr(f"{self._root_statsd_key}.{counter_name}")

    def time_event(self, event_name: str, duration: float) -> None:
        statsd_client.timing(f"{self._root_statsd_key}.{event_name}", duration)

    def run(self) -> None:
        """### We'll fire you if you override this method.

        While searching for ways to mark a method as `final` in Python (like you can do in
        other languages) I found the best solution here https://stackoverflow.com/a/2425818
        """

        self.incr_counter("start")

        while True:
            try:
                ok: bool
                msg: Optional[str]

                action_start_time: float = datetime.now(timezone.utc).timestamp()
                ok, msg = self.action()
                action_duration: float = datetime.now(timezone.utc).timestamp() - action_start_time
                if ok:
                    self.time_event("run_ok", action_duration)
                else:
                    self.time_event("run_ko", action_duration)
                    logging.exception(f"Internal thread '{self.name}' status: {msg}")
            except Exception as e:
                self.incr_counter("exception")
                logging.exception(f"Failed to run action() on internal thread '{self.name}': {e}")

            if self.is_exit_requested(wait=True):
                self.incr_counter("end")
                return

    def action(self) -> Tuple[bool, Optional[str]]:
        """Performs the actual operation of this thread."""
        raise NotImplementedError("Implement action() in a subclass")


class WorkspaceDatabaseUsageTracker(InternalThread):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__("ws_db_usage_tracker", *args, **kwargs)

    def track_model(
        self,
        models: Iterable[RedisModel],
        name: str,
        default_table_columns: Iterable[str],
        use_named_columns: bool = False,
    ) -> None:
        try:
            pu = public.get_public_user()
            datasource = pu.get_datasource(name)
            if not datasource:
                return
        except UserAccountDoesNotExist:
            return

        rows: List[List[str]] = []

        for model in models:
            try:
                row: List[str] = []
                for column in default_table_columns:
                    # FIXME RedisModel is not indexable
                    transform = None
                    if isinstance(column, tuple):
                        transform = column[1]
                        column = column[0]
                    value: Any = cast(Dict[str, Any], model)[column]
                    if transform is not None:
                        value = transform(value)
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(value, bool):
                        value = 1 if value else 0
                    elif isinstance(value, dict):
                        value = json.dumps(value)
                    row.append(str(value))
                rows.append(row)
            except Exception as e:
                logging.warning(f"Failed to append {model.id} workspace, reason={e}")

        try:
            named_columns = (
                f"({', '.join([c[0] if isinstance(c, tuple) else c for c in default_table_columns])})"
                if use_named_columns
                else ""
            )
            ch_insert_rows_sync(pu.database_server, pu.database, datasource.id, rows, named_columns=named_columns)
        except Exception as e:
            logging.exception(f"Track model: data could not be inserted into {datasource.id}, {e}")

    def track_database_usage(self, workspaces: Iterable[Workspace]) -> None:
        try:
            pu = public.get_public_user()
            db_usage_ds = pu.get_datasource("db_usage")
            if not db_usage_ds:
                return
        except UserAccountDoesNotExist:
            return

        workspaces_clusters = set([ws.cluster for ws in workspaces])
        clusters_hosts = ch_get_clusters_hosts(pu.database_server)
        default_database_host, _ = host_port_from_url(Workspace.default_database_server)

        database_servers: List[Tuple[str, str]] = [
            (h["host_address"], h["port"])
            for h in clusters_hosts
            if h["host_address"] == default_database_host
            or h["host_name"] == default_database_host
            or h["is_local"] == 1
            or h["cluster"] in workspaces_clusters
        ]

        client = HTTPClient(pu.database_server, database=pu.database)

        for database_server, port in database_servers:
            # Ideally, we could do remote(','.join(database_servers)),
            # but we go safe by doing it server by servers so the query does not fail for all of them.
            try:
                client.query_sync(
                    f"""INSERT INTO {pu.database}.{db_usage_ds.id}
                    SELECT
                        toStartOfHour(now()) AS timestamp,
                        database,
                        sum(coalesce(total_rows, 0)) as rows,
                        sum(coalesce(total_bytes, 0)) as bytes_on_disk
                    FROM remote('{database_server}:{port}', system.tables)
                    WHERE
                        database NOT IN ('public', 'system')
                        AND isNotNull(total_rows)
                        AND isNotNull(total_bytes)
                    GROUP BY timestamp, database
                """,
                    read_only=False,
                    connect_timeout_with_failover_ms=3000,
                )
                time.sleep(
                    0.1
                )  # Small slowdown to avoid the burst of inserts related to https://gitlab.com/tinybird/analytics/-/issues/5221
            except CHException as chex:
                logging.warning(
                    f"Failed to gather DB usage from system.tables for database_server={database_server}, reason={chex}"
                )

    def action(self) -> Tuple[bool, Optional[str]]:
        @dataclass
        class DataTrackerExecution:
            function: Callable
            arguments: List[Any]

        all_workspaces = Workspace.get_all(include_branches=True, include_releases=True)
        all_user_accounts = UserAccount.get_all()
        all_user_workspace_relationships = UserWorkspaceRelationship.get_all()

        data_trackers = [
            DataTrackerExecution(
                self.track_model,
                [
                    all_workspaces,
                    "workspaces_all",
                    [
                        "id",
                        "name",
                        "database",
                        "database_server",
                        "plan",
                        "deleted",
                        "created_at",
                        ("origin", lambda x: x or ""),
                    ],
                    True,
                ],
            ),
            DataTrackerExecution(
                self.track_model,
                [all_user_accounts, "user_accounts_all", ["id", "email", "feature_flags", "deleted", "created_at"]],
            ),
            DataTrackerExecution(
                self.track_model,
                [
                    all_user_workspace_relationships,
                    "user_workspaces_all",
                    ["id", "user_id", "workspace_id", "relationship", "created_at"],
                ],
            ),
            DataTrackerExecution(self.track_database_usage, [all_workspaces]),
        ]

        for execution in data_trackers:
            try:
                execution.function(*execution.arguments)
            except Exception as e:
                logging.exception(f"Failed to track data: {e}")

        return (True, None)


class UsageMetricsTracker(InternalThread):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__("usage_metrics_tracker", *args, **kwargs)

    def _retrieve_storage_used_per_database_and_table(
        self, public_user: Workspace
    ) -> Dict[str, Dict[str, Dict[str, Dict[str, int]]]]:
        client = HTTPClient(public_user.database_server, database=public_user.database)
        clusters = list(set([host["cluster"] for host in ch_get_clusters_hosts(public_user.database_server)]))

        storage_data: Dict[str, Dict[str, Dict[str, Dict[str, int]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: {"rows": 0, "bytes_on_disk": 0}))
        )

        def get_metrics_query(cluster=None):
            source_table = f"cluster('{cluster}', system.tables)" if cluster else "system.tables"

            return f"""
                SELECT
                    database,
                    name,
                    sum(coalesce(total_rows, 0)) as rows,
                    sum(coalesce(total_bytes, 0)) as bytes_on_disk
                FROM {source_table}
                WHERE
                    database != 'system'
                    AND isNotNull(total_rows)
                    AND isNotNull(total_bytes)
                    AND (((startsWith(name, 't_') OR startsWith(name, 'j_')) AND length(extractAll(name, '_')) < 2)
                    OR (endsWith(name, '_quarantine')))
                GROUP BY database, name
                FORMAT JSON
            """

        if not clusters:
            clusters = [""]

        for cluster in clusters:
            if "gatherer" in cluster:
                continue
            try:
                sql = get_metrics_query(cluster=cluster) if cluster else get_metrics_query()
                _, content = client.query_sync(sql, connect_timeout_with_failover_ms=3000)

                data = json.loads(content).get("data", [])

                for row in data:
                    name = row["name"]
                    table_dict = storage_data[cluster][row["database"]][name]
                    table_dict["rows"] += row["rows"]
                    table_dict["bytes_on_disk"] += row["bytes_on_disk"]

            except CHException as chex:
                if not cluster:
                    logging.exception(f"Failed to gather usage_metrics_storage from system.tables, reason={chex}")
                else:
                    logging.exception(
                        f"Failed to gather usage_metrics_storage from system.tables for {cluster}, reason={chex}"
                    )

        return storage_data

    def track_usage_metrics_storage(self, public_user: Workspace, workspaces: List[Workspace]) -> None:
        usage_metrics_storage_v2 = public_user.get_datasource("usage_metrics_storage__v2")

        if not usage_metrics_storage_v2:
            logging.warning("Could not find table `usage_metrics_storage_v2` to execute `track_usage_metrics_storage`")
            return None

        storage_data = self._retrieve_storage_used_per_database_and_table(public_user)

        now = datetime.now().strftime("%Y-%m-%d %H:00:00")
        usage_metrics_storage_rows__v2 = []

        # track only data sources present in the workspace, this filters deleted data sources that
        # are still on CH since they're bigger than 50GB
        for ws in workspaces:
            total_bytes_on_disk = 0
            total_rows = 0

            for ds in ws.datasources:
                # ignore shared datasources
                if "shared_from" in ds:
                    continue
                try:
                    # defensive code for workspaces without cluster assigned
                    cluster = ws.cluster
                    if not cluster:
                        for c in storage_data:
                            if ws["database"] in storage_data[c]:
                                cluster = c
                                break
                    if not cluster:
                        logging.warning(
                            f"Could add storage for workspace {ws.id} {ws.name}: " f"{ws['database']} not found"
                        )
                        continue

                    tbl_stats = storage_data[cluster][ws["database"]][f"{ds['id']}"]
                    quarantine_stats = storage_data[cluster][ws["database"]][f"{ds['id']}_quarantine"]

                    total_bytes_on_disk += tbl_stats["bytes_on_disk"]
                    total_bytes_on_disk += quarantine_stats["bytes_on_disk"]
                    total_rows += tbl_stats["rows"]
                    total_rows += quarantine_stats["rows"]

                    usage_metrics_storage_rows__v2.append(
                        [
                            now,
                            ws.id,
                            ds["id"],
                            ds["name"],
                            tbl_stats["rows"],
                            tbl_stats["bytes_on_disk"],
                            quarantine_stats["rows"],
                            quarantine_stats["bytes_on_disk"],
                        ]
                    )
                except Exception as e:
                    logging.warning(f"Could not add storage for data source {ds['id']}: {e}")
                    pass

        @retry_sync((CHException, requests.exceptions.ConnectionError), tries=4, delay=1)
        def insert_rows(database_server, database, table, rows):
            ch_insert_rows_sync(database_server, database, table, rows, log_as_error=False)

        try:
            insert_rows(
                public_user.database_server,
                public_user.database,
                usage_metrics_storage_v2.id,
                usage_metrics_storage_rows__v2,
            )
        except Exception as exc:
            logging.exception(f"Error inserting storage v2 for {ws.id}: {exc}")

    def action(self) -> Tuple[bool, Optional[str]]:
        public_user = self.get_public_user()
        if public_user:
            workspaces = Workspace.get_all(
                include_branches=True, include_releases=True
            )  # TODO: filter deleted workspaces
            self.track_usage_metrics_storage(public_user, workspaces)
            self.exit_queue_timeout = 600
        else:
            logging.warning("Could not find public_user to execute `track_usage_metrics_storage`")
            self.exit_queue_timeout = 300

        return (True, None)


class UsageRecordsTracker(InternalThread):
    def __init__(self, api_host: str, metrics_cluster: Optional[str] = None, *args: Any, **kwargs: Any) -> None:
        super().__init__("usage_records_tracker", 3600, *args, **kwargs)
        self.api_host = api_host
        self.metrics_cluster = metrics_cluster

    def track_usage_records(self) -> None:
        logging.info(f"Stripe: '{self.name}' start tracking usage records (metrics cluster '{self.metrics_cluster}')")

        for subscription in PlansService.list_active_subscriptions():
            if self._exit_requested:
                return

            if not PlansService.is_subscription_usage_trackable(subscription):
                continue

            workspace = None
            usage_records = None

            try:
                workspace_id = subscription.get("metadata", {}).get("workspace_id", None)
                if workspace_id:
                    workspace = Workspace.get_by_id(workspace_id)

                    if workspace:
                        PlansService.track_usage_records(
                            workspace,
                            subscription,
                            metrics_cluster=self.metrics_cluster,
                            api_host=self.api_host,
                        )

            except Exception as e:
                if workspace:
                    logging.exception(
                        f"Stripe: failed to track usage record for workspace {workspace.name} ({workspace.id}): {e}"
                    )
                else:
                    logging.exception(f"Stripe: Failed to track usage record for workspace {subscription['id']}: {e}")
            else:
                if workspace:
                    logging.info(
                        f"Stripe: usage record tracked for workspace {workspace.name} ({workspace.id}). Usage records: {usage_records}"
                    )

    def action(self) -> Tuple[bool, Optional[str]]:
        self.track_usage_records()
        return (True, None)


class PlanLimitsTracker(InternalThread):
    def __init__(self, api_host: str, metrics_cluster: Optional[str] = None, *args: Any, **kwargs: Any) -> None:
        super().__init__("plan_limits_tracker", *args, **kwargs)
        self.api_host = api_host
        self.metrics_cluster = metrics_cluster
        self.exit_queue_timeout = 3600

    def track_plan_limits(self) -> None:
        PlansService.track_build_plan_limits(self.api_host, self.metrics_cluster)

    def action(self) -> Tuple[bool, Optional[str]]:
        if Workspace.default_plan == BillingPlans.DEV:
            self.track_plan_limits()
        return (True, None)
