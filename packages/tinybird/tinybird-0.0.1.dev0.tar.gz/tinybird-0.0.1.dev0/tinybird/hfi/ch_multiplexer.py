import asyncio
import json
import logging
import time
import traceback
import uuid
from collections import defaultdict, namedtuple
from typing import Any, Dict, Optional

import aiohttp
import orjson

from tinybird import context
from tinybird.ch import (
    CHSummary,
    ch_check_all_mvs_are_empty,
    ch_table_exists_async,
    create_quarantine_table_from_landing,
    url_from_host,
)
from tinybird.ch_utils.exceptions import clickhouse_parse_code_error
from tinybird.default_timeouts import socket_connect_timeout, socket_read_timeout, socket_total_timeout
from tinybird.gatherer_common import compose_gatherer_table_create_request_params
from tinybird.gatherer_common.gatherer_config import send_gatherer_routing_metrics
from tinybird.hfi.circuit_breakers import get_circuit_breaker_id, global_hfi_circuit_breakers
from tinybird.hfi.errors import APIError
from tinybird.hfi.hfi_gatherer import HfiGatherer
from tinybird.hfi.hfi_settings import hfi_settings
from tinybird.hfi.utils import (
    get_mv_error_not_propagated,
    get_mv_error_not_propagated_null_engine,
    is_materialized_view_error,
)
from tinybird.user import User
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.api_errors.utils import replace_table_id_with_datasource_id
from tinybird_shared.clickhouse.errors import get_name_from_ch_code
from tinybird_shared.gatherer_settings import GathererFlushConfiguration
from tinybird_shared.metrics.statsd_client import statsd_client

# This files provides a way of multiplexing multiple incoming insertion requests to CH
# into a reduced number of requests to CH using HTTP 1.1 "Chunked transfer encoding"
#
# Incoming insertions using `insert_chunk()` are streamed to CH without ending the connection
# Calling `insert_chunk_flush()` will request to end the CH connection so the streamed data is flushed
# However, `insert_chunk_flush` may not immediately flush the connection, as the multiplexer
# limits the frequency of CH flushes to avoid the "too many partitions" error
# The rate limiting is based on GCRA (https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm)
# When a call to `insert_chunk_flush` is rate-limited, no further action is needed
# A background task will eventually perform the flush

# This controls the maximum number of enqueued chunks that hasn't been transmitted to CH yet
# When the limit is reached, big (more than one chunk sized) requests should wait
# before starting to process another chunk
# This is a backpressure mechanism
MAX_QUEUED_CHUNKS = 10
INTERNAL_TABLES_WAIT_TIME = 10
GET_SESSION_TIMEOUT = 3
internal_tables = {"data_guess"}


def get_ingestion_internal_tables_period():
    return hfi_settings.get("ch_ingestion_internal_tables_period", INTERNAL_TABLES_WAIT_TIME)


class AnalyzeError(Exception):
    pass


class CHMultiplexer:
    def __init__(self):
        self._channels = dict()

        # It's important to keep a reference to tasks
        # If not, the GC will destroy it eventually,
        # causing "Task was destroyed but it is pending!" errors
        # and global_shared_session.close() won't be called on shutdown
        # See https://bugs.python.org/issue21163
        self._pending_channels = set()

        self._tokens = defaultdict(CHIngestionTokens)

    async def insert_chunk(
        self,
        endpoint,
        database,
        workspace_id,
        table_id,
        columns_list,
        columns_types_list,
        format,
        chunk,
        user_agent="",
        extra_params=None,
    ):
        columns = ",".join(columns_list)
        insertion_id = self._insertion_uid(
            endpoint, database, table_id, columns, format, user_agent, context.wait_parameter.get(False)
        )
        channel = self._channels.get(insertion_id, None)
        new_channel = channel is None or channel.is_closed()
        if new_channel:
            hfi_gatherer = HfiGatherer(endpoint, database, table_id, columns_list, columns_types_list, user_agent)

            # This code needs to be sync, or there will be a race condition between channel creations
            ingestion_tokens = self._tokens[insertion_id]
            wait_time = (
                ingestion_tokens.time_to_wait_before_allowance(hfi_gatherer.in_use)
                if table_id not in internal_tables
                else get_ingestion_internal_tables_period()
            )
            channel = CHMultiplexerChannel(
                endpoint,
                database,
                workspace_id,
                table_id,
                columns_list,
                format,
                user_agent,
                wait_time,
                hfi_gatherer,
                extra_params,
                chunk,
            )
            ingestion_tokens.ingested(hfi_gatherer.in_use)
            self._channels[insertion_id] = channel
            self._pending_channels = {ch for ch in self._pending_channels if not ch.wait_for_flush_task.done()}
            self._pending_channels.add(channel)
        else:
            await channel.insert_chunk(chunk)
        return "new" if new_channel else "reused", channel

    def _insertion_uid(self, endpoint, database, table_id, columns, format, user_agent, wait_parameter):
        """
        WARNING!!!

        This method is used to generate a unique identifier that ensures
        that a new channel is created for each endpoint, database, table_id,
        columns, format and user_agent combination.

        Bear in mind that each channel will insert all of it's data into
        the endpoint, database and table_id defined by this insertion_id.

        >>> t = CHMultiplexer()

        >>> t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', True)
        'ch:ci_ch_d_123456_t_abcdef_timestamp,record_RowBinary_hfi_True'
        >>> 'ch:ci_ch' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 'd_123456' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 't_abcdef' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 'timestamp,record' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 'RowBinary' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 'hfi' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        >>> 'True' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', True)
        True
        >>> 'False' in t._insertion_uid('ch:ci_ch', 'd_123456', 't_abcdef', 'timestamp, record', 'RowBinary', 'hfi', False)
        True
        """
        return f"{endpoint}_{database}_{table_id}_{columns.replace(' ', '')}_{format}_{user_agent}_{wait_parameter}"


class CHIngestionTokens:
    def __init__(self):
        self.available_tokens = hfi_settings["ch_ingestion_burst_size"]
        self._last_update = time.time()

    def time_to_wait_before_allowance(self, use_gatherer: bool):
        self._update_with_time(use_gatherer)
        if self.available_tokens >= 1:
            return 0
        existing_tokens = self.available_tokens
        needed_tokens = 1 - existing_tokens
        wait_time = needed_tokens / self._get_tokens_per_second(use_gatherer)
        return wait_time

    def ingested(self, use_gatherer: bool):
        self.available_tokens -= 1
        self._update_with_time(use_gatherer)

    def _update_with_time(self, use_gatherer: bool):
        now = time.time()
        dt = now - self._last_update
        new_tokens = dt * self._get_tokens_per_second(use_gatherer)
        self.available_tokens = min(self.available_tokens + new_tokens, hfi_settings["ch_ingestion_burst_size"])
        self._last_update = now

    @staticmethod
    def _get_tokens_per_second(use_gatherer: bool):
        if use_gatherer:
            value = context.hfi_frequency_gatherer.get(hfi_settings["ch_ingestion_tokens_per_second_gatherer_default"])
        else:
            value = context.hfi_frequency.get(hfi_settings["ch_ingestion_tokens_per_second_default"])

        return value


class CHMultiplexerChannel:
    def __init__(
        self,
        endpoint,
        database,
        workspace_id,
        table_id,
        columns_list,
        format,
        user_agent,
        duration,
        hfi_gatherer,
        extra_params,
        first_chunk,
    ):
        self._error = None
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._queue.put_nowait(first_chunk)
        self._queue_semaphore = asyncio.Semaphore(value=MAX_QUEUED_CHUNKS)
        self._data_sent = False
        self._request_ready_time = None
        self._closed = False
        self._ch_summary = CHSummary(query_id=str(uuid.uuid4()), summary={})

        self._wait_parameter: bool = context.wait_parameter.get(False)
        self._user_agent = user_agent
        self.use_gatherer: bool = hfi_gatherer.in_use
        self._allow_gatherer_fallback: bool = hfi_gatherer.allow_gatherer_fallback
        self._total_flushed_bytes = 0

        if self.use_gatherer and (hfi_gatherer is None or not hfi_gatherer.gatherer_available):
            if self._allow_gatherer_fallback:
                statsd_client.incr(
                    f"tinybird-hfi.gatherer_not_available_fallback.{statsd_client.region}.{workspace_id}"
                )
                self.use_gatherer = False
            else:
                statsd_client.incr(f"tinybird-hfi.gatherer_not_available_failed.{statsd_client.region}.{workspace_id}")
                logging.exception("Using the Gatherer is enabled but there are none available. Raising 503 error")
                raise APIError(503, "Service temporarily unavailable, no data ingested, please retry again\n")

        self.insertion_time: float = 0
        t_get_session_0 = time.monotonic()
        session = get_shared_session()
        elapsed_get_session = time.monotonic() - t_get_session_0
        if elapsed_get_session > GET_SESSION_TIMEOUT:
            statsd_client.timing(
                f"tinybird-hfi.get_session_time.{statsd_client.region_machine}.{workspace_id}", elapsed_get_session
            )

        columns = ",".join(columns_list)
        params = {
            "database": database,
            "query": f"INSERT INTO {database}.{table_id}({columns}) FORMAT {format}",
            "query_id": self._ch_summary.query_id,
        }
        if extra_params:
            params.update(extra_params)

        url = url_from_host(endpoint)
        gatherer_config = hfi_gatherer.gatherer_config

        statsd_client.incr(f"tinybird-hfi.insertions.{statsd_client.region}.{workspace_id}")

        if self.use_gatherer:
            params["query"] = (
                f"INSERT INTO `{gatherer_config.database}`.`{hfi_gatherer.gatherer_table_name}` ({columns}) FORMAT {format}"
            )
            params["database"] = gatherer_config.database

            url = url_from_host(gatherer_config.url)

        async def make_request():
            circuit_breaker_id = get_circuit_breaker_id(workspace_id, table_id)
            result_status = -1
            try:
                start_time = time.time()
                headers = {
                    "User-Agent": self._user_agent,
                }
                timeout = aiohttp.ClientTimeout(
                    total=socket_total_timeout() + duration,
                    connect=socket_connect_timeout(),
                    sock_read=socket_read_timeout() + duration,
                )

                destination_ch_url = url_from_host(endpoint)

                if table_id.endswith("_quarantine"):
                    await self._create_quarantine_table_if_needed(table_id, destination_ch_url, database)

                if self.use_gatherer:
                    gatherer_ch_url = url_from_host(gatherer_config.url)

                    if not await ch_table_exists_async(
                        hfi_gatherer.gatherer_table_name, gatherer_ch_url, gatherer_config.database
                    ):
                        await self._create_gatherer_table(
                            session=session,
                            destination_url=destination_ch_url,
                            destination_database=database,
                            destination_table_name=table_id,
                            gatherer_url=url_from_host(gatherer_config.url),
                            gatherer_database=gatherer_config.database,
                            gatherer_table_name=hfi_gatherer.gatherer_table_name,
                            gatherer_ch_config=hfi_gatherer.gatherer_ch_config,
                            extra_comment={
                                "backup_on_user_errors": hfi_gatherer.gatherer_allow_s3_backup_on_user_errors,
                                "multiwriter_enabled": hfi_gatherer.workspace_multiwriter_enabled,
                                "multiwriter_type": hfi_gatherer.workspace_multiwriter_type,
                                "multiwriter_tables": hfi_gatherer.workspace_multiwriter_tables,
                                "multiwriter_tables_excluded": hfi_gatherer.workspace_multiwriter_tables_excluded,
                                "multiwriter_hint_backend_ws": hfi_gatherer.workspace_multiwriter_hint_backend_ws,
                                "multiwriter_hint_backend_tables": hfi_gatherer.workspace_multiwriter_hint_backend_tables,
                            },
                        )

                async with session.request(
                    "POST",
                    url=url,
                    params=params,
                    headers=headers,
                    data=self._generator(),
                    compress=False,
                    timeout=timeout,
                ) as resp:
                    result = (await resp.content.read()).decode("utf-8", "replace")
                    result_status = resp.status
                    self._ch_summary.summary = orjson.loads(resp.headers.get("X-Clickhouse-Summary", "{}"))
                    if result_status >= 400:
                        # log here the error, when working with varnish the response could be totally different to what
                        # CH reports and therefore the CHException parsing will not work
                        is_mv_error = is_materialized_view_error(result)
                        data_not_ingested = False

                        # Only send a query against CH to check whether all MVs lost data in case wait=true.
                        # Otherwise, we've already returned a 202 and there's no point in checking that now.
                        if is_mv_error and self._wait_parameter:
                            engine = context.engine.get(None)
                            # TODO: Remove the type ignore once context.workspace return correct type
                            workspace: Optional[User] = context.workspace.get(None)
                            cluster = workspace.cluster if workspace else None
                            data_not_ingested = (
                                engine is not None
                                and engine.lower() == "null"
                                and cluster is not None
                                and await ch_check_all_mvs_are_empty(url, cluster, self.query_id, 60)
                            )
                        self._error = CHError(result, result_status, url, params, is_mv_error, data_not_ingested)
            except Exception as e:
                logging.exception(
                    f"ClickHouse connection error, exception_type={type(e).__name__} exception={e} url={url} params={params} data_sent={self._data_sent}"
                    f"\nTraceback: {traceback.format_exc()}"
                )
                self._error = CHError(str(e), -1, url, params)
            finally:
                # Defensive programming, it would be problematic to leave an async put waiting
                while True:
                    try:
                        self._queue.get_nowait()
                        logging.warning("CHMultiplexerChannel queue was not empty, data loss may have occurred")
                        self._queue_semaphore.release()
                    except Exception:
                        break
                self._closed = True

                target = "gatherer" if self.use_gatherer else "ch"

                statsd_client.incr(
                    f"tinybird-hfi.{target}.insertion-status.{statsd_client.region_machine}.{workspace_id}.{table_id}.{result_status}.{context.origin.get('unknown')}"
                )
                self.insertion_time = time.time() - start_time
                statsd_client.timing(
                    f"tinybird-hfi.{target}.insertion-time.{statsd_client.region_machine}.{workspace_id}.{table_id}.{context.origin.get('unknown')}",
                    self.insertion_time,
                )
                if self._request_ready_time:
                    statsd_client.timing(
                        f"tinybird-hfi.{target}.flush-time.{statsd_client.region_machine}.{workspace_id}.{table_id}.{context.origin.get('unknown')}",
                        time.time() - self._request_ready_time,
                    )

                if self._error is not None:
                    logging.warning(self._error.get_json_error())
                if self._error is not None and self._error.is_circuit_breaker_error:
                    global_hfi_circuit_breakers.failed(circuit_breaker_id, str(self._error))
                else:
                    global_hfi_circuit_breakers.succeeded(circuit_breaker_id)

        self._request_task = asyncio.create_task(make_request())

        self.force_flush_event = asyncio.Event()

        async def eventually_flush():
            force_flush_event_wait_task = asyncio.create_task(self.force_flush_event.wait())
            sleep_task = asyncio.create_task(asyncio.sleep(duration))
            await asyncio.wait([sleep_task, force_flush_event_wait_task], return_when=asyncio.FIRST_COMPLETED)
            # Python has a task waiting for this behind the scenes.
            # If we don't set it, it will be here forever, and a "Task was destroyed but it is pending!"
            # error will be logged
            self.force_flush_event.set()

            if not self._closed:
                self._closed = True
                await self._queue.put(None)
            await self._request_task
            if self._error:
                # Workaround for Python's bug https://bugs.python.org/issue45924
                # See related duplicated issue https://bugs.python.org/issue46954
                return self._error

            send_gatherer_routing_metrics(
                gatherer_config=gatherer_config,
                workspace_id=workspace_id,
                table_id=table_id,
                flushed_bytes=self._total_flushed_bytes,
            )

        self.wait_for_flush_task = asyncio.create_task(eventually_flush())

    @staticmethod
    async def _create_quarantine_table_if_needed(quarantine_datasource_id, database_server, database):
        try:
            exists_table = await ch_table_exists_async(f"{quarantine_datasource_id}", database_server, database)
        except Exception:
            exists_table = False

        if not exists_table:
            # TODO: Remove the type ignore once context.workspace return correct type
            workspace: Optional[User] = context.workspace.get(None)
            cluster = workspace.cluster if workspace else None
            original_datasource_id = quarantine_datasource_id.replace("_quarantine", "")
            logging.info(f"Creating quarantine table for table '{database_server}.{quarantine_datasource_id}'")
            try:
                await create_quarantine_table_from_landing(
                    original_datasource_id,
                    database_server,
                    database,
                    cluster,
                )
                return True
            except Exception as e:
                logging.error(f"Unable to create quarantine table: {str(e)}")
                return False
        return True

    @staticmethod
    async def _create_gatherer_table(
        session,
        destination_table_name,
        destination_url,
        destination_database,
        gatherer_url,
        gatherer_database,
        gatherer_table_name,
        gatherer_ch_config: Optional[GathererFlushConfiguration] = None,
        extra_comment: Optional[Dict[str, str]] = None,
    ):
        logging.info(f"Creating gatherer table '{gatherer_table_name}'")
        try:
            request_params = compose_gatherer_table_create_request_params(
                gatherer_database,
                gatherer_table_name,
                destination_url,
                destination_database,
                destination_table_name,
                gatherer_ch_config,
                extra_comment,
            )

            async with session.request("POST", url=gatherer_url, params=request_params) as resp:
                _ = await resp.read()
                if resp.status != 200:
                    resp_content = (await resp.content.read()).decode("utf-8", "replace")
                    logging.exception(
                        f"Error creating gatherer table {gatherer_database}.`{gatherer_table_name}`. "
                        f"Status {resp.status} / {resp_content} / Query: {request_params['query']}"
                    )
        except Exception as e:
            logging.exception(f"Error creating gatherer table {gatherer_database}.`{gatherer_table_name}`: {e}")

    async def _generator(self):
        try:
            while True:
                self._queue_semaphore.release()
                chunk = await self._queue.get()
                if chunk is None:
                    break
                if len(chunk) == 0:
                    continue
                self._data_sent = True
                self._total_flushed_bytes += len(chunk)
                yield chunk
            self._request_ready_time = time.time()
        except asyncio.CancelledError:
            # This can happen upon HTTP errors
            # The error is handled in other coroutine, so ignore the issue here
            return
        finally:
            self._closed = True

    async def insert_chunk(self, chunk: bytes):
        if self._error:
            # Workaround for Python's bug https://bugs.python.org/issue45924
            # See related duplicated issue https://bugs.python.org/issue46954
            raise Exception(str(self._error))
        # Avoid putting async put() here, since it will create a race condition
        # with the retrieval of chunks and the channel closing
        self._queue.put_nowait(chunk)
        await self._queue_semaphore.acquire()

    def is_closed(self):
        return self._closed

    @property
    def query_id(self):
        return self._ch_summary.query_id

    @property
    def stats_summary(self):
        return self._ch_summary.summary


Clickhouse_error = namedtuple("Clickhouse_error", ["id", "code"])

circuit_breakers_errors_for_landing = {
    "TABLE_IS_READ_ONLY",
    "NO_ZOOKEEPER",
    "TOO_MANY_PARTS",
    "MEMORY_LIMIT_EXCEEDED",
    "NOT_ENOUGH_SPACE",
    "UNKNOWN_TABLE",
    "UNEXPECTED_ZOOKEEPER_ERROR",
    "UNKNOWN_STATUS_OF_INSERT",
    "TOO_MANY_SIMULTANEOUS_QUERIES",
    "UNKNOWN_DATABASE",
    "KEEPER_EXCEPTION",
    "VIOLATED_CONSTRAINT",
    "DISCONNECTED",
    "VARNISH_503",
}

circuit_breakers_errors_for_mv = {
    "TABLE_IS_READ_ONLY",
    "NO_ZOOKEEPER",
    "MEMORY_LIMIT_EXCEEDED",
    "NOT_ENOUGH_SPACE",
    "UNEXPECTED_ZOOKEEPER_ERROR",
    "TOO_MANY_SIMULTANEOUS_QUERIES",
    "KEEPER_EXCEPTION",
    "DISCONNECTED",
    "VARNISH_503",
}


class CHError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int,
        url: str,
        params: dict[str, Any],
        is_mv_error: bool = False,
        data_not_ingested: bool = False,
    ):
        error_code = clickhouse_parse_code_error(message, headers=None)
        if error_code is not None:
            clickhouse_error = get_name_from_ch_code(error_code)
        elif status_code == 503:
            clickhouse_error = "VARNISH_503"
            error_code = -2
        elif status_code >= 0:
            clickhouse_error = "UNKNOWN"
            error_code = -1
        else:
            clickhouse_error = "DISCONNECTED"
            error_code = -2
        self.code = error_code
        self.str_code = clickhouse_error
        self.is_materialized_view = is_mv_error
        self.is_circuit_breaker_error = self._is_circuit_breaker_error()
        self.query_id = params.get("query_id", None)
        self.data_not_ingested = data_not_ingested
        if message:
            workspace = context.workspace.get(None)
            if workspace:
                message = replace_table_id_with_datasource_id(workspace, message)
        if self.is_materialized_view:
            if data_not_ingested:
                message = get_mv_error_not_propagated_null_engine(message, url)
            else:
                message = get_mv_error_not_propagated(message, url)
        else:
            message = f"ClickHouse error, {message}"
        message = hide_some_errors(message)
        self.message = message
        self.internal_message = f"ClickHouse error, status={status_code} message={message} url={url} params={params}"
        super().__init__(self.message)

    def get_json_error(self) -> str:
        return json.dumps(
            {
                "code": self.code,
                "str_code": self.str_code,
                "is_materialized_view": self.is_materialized_view,
                "is_circuit_breaker_error": self.is_circuit_breaker_error,
                "internal_message": self.internal_message,
                "message": self.message,
            }
        )

    def _is_circuit_breaker_error(self) -> bool:
        if self.is_materialized_view:
            return self.str_code in circuit_breakers_errors_for_mv
        else:
            return self.str_code in circuit_breakers_errors_for_landing


# hide_some_errors removes some known internal errors that are not actionable by the user
# replacing them by a generic error
def hide_some_errors(msg: str) -> str:
    """
    >>> hide_some_errors("hola")
    'hola'
    >>> hide_some_errors("hola TABLE_IS_READ_ONLY wadus")
    'Internal Tinybird error'
    """
    internal_errors = [
        "TABLE_IS_READ_ONLY",
        "NO_ZOOKEEPER",
        "UNEXPECTED_ZOOKEEPER_ERROR",
        "KEEPER_EXCEPTION",
        "VARNISH_503",
    ]
    if any(err in msg for err in internal_errors):
        return "Internal Tinybird error"
    return msg


global_ch_multiplexer: Optional[CHMultiplexer] = None


async def insert_chunk(
    endpoint,
    database,
    workspace_id,
    table_id,
    columns_list,
    columns_types_list,
    format,
    chunk,
    user_agent="tb-ch-multiplexer",
    extra_params=None,
) -> CHMultiplexerChannel:
    global global_ch_multiplexer
    if global_ch_multiplexer is None:
        global_ch_multiplexer = CHMultiplexer()
    return await global_ch_multiplexer.insert_chunk(
        endpoint,
        database,
        workspace_id,
        table_id,
        columns_list,
        columns_types_list,
        format,
        chunk,
        user_agent,
        extra_params,
    )


async def force_flush_ch_multiplexer():
    global global_ch_multiplexer
    if global_ch_multiplexer:
        logging.warning("HFI: force_flush_ch_multiplexer()")
        global_ch_multiplexer._pending_channels = {
            ch for ch in global_ch_multiplexer._pending_channels if not ch.wait_for_flush_task.done()
        }
        if global_ch_multiplexer._pending_channels:
            logging.warning(f"HFI: flushing {len(global_ch_multiplexer._pending_channels)} channels")
            for ch in global_ch_multiplexer._pending_channels:
                ch.force_flush_event.set()
            await asyncio.wait([ch.wait_for_flush_task for ch in global_ch_multiplexer._pending_channels])
