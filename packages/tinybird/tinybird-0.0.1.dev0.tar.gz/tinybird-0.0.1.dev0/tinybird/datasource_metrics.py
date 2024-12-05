import json
import logging
from typing import Any, Callable, Dict, List, Optional

from tinybird.ch import HTTPClient
from tinybird.ch_utils.exceptions import CHException
from tinybird.datasource import Datasource
from tinybird.user import User, public

_SECONDS_IN_MINUTE: int = 60
_SECONDS_IN_HALF_HOUR: int = 30 * _SECONDS_IN_MINUTE
_SECONDS_IN_HOUR: int = 60 * _SECONDS_IN_MINUTE
_SECONDS_IN_SIX_HOURS: int = 6 * _SECONDS_IN_HOUR
_SECONDS_IN_HALF_DAY: int = 12 * _SECONDS_IN_HOUR
_SECONDS_IN_DAY: int = 24 * _SECONDS_IN_HOUR
_SECONDS_IN_WEEK: int = 7 * _SECONDS_IN_DAY
_SECONDS_IN_MONTH: int = 30 * _SECONDS_IN_DAY

TIME_GRANULARITIES: Dict[int, int] = {
    _SECONDS_IN_MINUTE: 5,
    _SECONDS_IN_HOUR: _SECONDS_IN_MINUTE,
    _SECONDS_IN_HALF_HOUR: _SECONDS_IN_MINUTE,
    _SECONDS_IN_SIX_HOURS: _SECONDS_IN_HOUR,
    _SECONDS_IN_HALF_DAY: _SECONDS_IN_HOUR,
    _SECONDS_IN_DAY: _SECONDS_IN_HOUR,
    _SECONDS_IN_WEEK: _SECONDS_IN_DAY,
    _SECONDS_IN_MONTH: _SECONDS_IN_DAY,
}


class DataSourceMetrics:
    def __init__(self, workspace: User, datasource: Datasource, metric: str, interval: int) -> None:
        self.datasource: Datasource = datasource
        self.workspace: User = workspace
        self.metric: str = metric
        self.interval: int = interval
        self.granularity: int = self._get_granurality()
        self.ticks: float = self._get_ticks()

    def _get_granurality(self) -> int:
        if self.interval not in TIME_GRANULARITIES.keys():
            return _SECONDS_IN_MINUTE
        return TIME_GRANULARITIES[self.interval]

    def _get_ticks(self) -> float:
        return self.interval / self.granularity + 1

    async def get_metric(self) -> Dict[str, Any]:
        get_query: Optional[Callable[[], Optional[str]]] = None
        error: Optional[str] = None
        data: Optional[List[Any]] = None

        match self.metric:
            case "storage":
                get_query = self._get_storage
            case "new_rows":
                get_query = self._get_new_rows
            case "total_rows":
                get_query = self._get_total_rows
            case "storage_quarantine":
                get_query = self._get_storage_quarantine
            case "new_rows_quarantine":
                get_query = self._get_new_rows_quarantine
            case "total_rows_quarantine":
                get_query = self._get_total_rows_quarantine
            case _:
                error = "Invalid metric"

        if get_query:
            sql = get_query()
            if not sql:
                error = "Can't get metric query"
            else:
                try:
                    pu = public.get_public_user()
                    client = HTTPClient(pu.database_server)

                    result: bytes
                    _, result = await client.query(sql)
                    data = json.loads(result).get("data", [])
                except CHException as e:
                    error = str(e)

        if error:
            logging.exception(
                f"Failed to get {self.metric} metric by datasource. "
                f"Workspace: {self.workspace.id}."
                f"Datasource: {self.datasource.id}. "
                f"Error: {error}"
            )

        return {"data": data or [], "ticks": self.ticks, "error": error}

    def _get_storage(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        return f"""
            SELECT time, sum(max_bytes) as storage FROM (
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                max(bytes) as max_bytes
                FROM {pu.database}.{usage_metrics_storage.id}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                GROUP BY time, datasource_id
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """

    def _get_new_rows(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        is_kafka = self.datasource.to_json()["type"] == "kafka"
        rows_field = "committed_messages" if is_kafka else "rows"
        ops_log = "kafka_ops_log" if is_kafka and self.metric == "new_rows" else "datasources_ops_log"
        table = next(x for x in pu.datasources if x["name"] == ops_log)
        filter_events_condition = "" if is_kafka else "AND NOT event_type in ('truncate', 'delete_data')"
        return f"""
            SELECT time, max({rows_field}) new_rows FROM (
                SELECT
                toDateTime(intDiv(toUInt32(now() - interval (number * {self.granularity}) second), {self.granularity}) * {self.granularity}) time,
                toUInt16(0) {rows_field}
                FROM numbers({self.ticks})
                UNION ALL
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                sum({rows_field})
                FROM {pu.database}.{table['id']}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                {filter_events_condition}
                GROUP BY time
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """

    def _get_total_rows(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        return f"""
            SELECT time, sum(rows) as total_rows FROM (
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                max(rows) as rows
                FROM {pu.database}.{usage_metrics_storage.id}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                GROUP BY time, datasource_id
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """

    def _get_storage_quarantine(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        return f"""
            SELECT time, sum(max_bytes_quarantine) as storage_quarantine FROM (
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                max(bytes_quarantine) as max_bytes_quarantine
                FROM {pu.database}.{usage_metrics_storage.id}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                GROUP BY time, datasource_id
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """

    def _get_new_rows_quarantine(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        table = next(x for x in pu.datasources if x["name"] == "datasources_ops_log")
        if not table:
            return None
        return f"""
            SELECT time, max(rows_quarantine) new_rows_quarantine FROM (
                SELECT
                toDateTime(intDiv(toUInt32(now() - interval (number * {self.granularity}) second), {self.granularity}) * {self.granularity}) time,
                toUInt16(0) rows_quarantine
                FROM numbers({self.ticks})
                UNION ALL
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                sum(rows_quarantine)
                FROM {pu.database}.{table['id']}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                GROUP BY time
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """

    def _get_total_rows_quarantine(self) -> Optional[str]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        if not usage_metrics_storage:
            return None
        return f"""
            SELECT time, sum(rows_quarantine) as total_rows_quarantine FROM (
                SELECT toDateTime(intDiv(toUInt32(timestamp), {self.granularity}) * {self.granularity}) time,
                        max(rows_quarantine) as rows_quarantine
                FROM {pu.database}.{usage_metrics_storage.id}
                WHERE timestamp > now() - interval {self.interval} second
                AND user_id = '{self.workspace.id}'
                AND datasource_id = '{self.datasource.id}'
                GROUP BY time, datasource_id
                ORDER BY time
            )
            GROUP BY time
            ORDER BY time ASC
            FORMAT JSON
            """
