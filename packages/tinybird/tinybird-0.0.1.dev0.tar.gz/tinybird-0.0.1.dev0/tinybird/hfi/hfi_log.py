import asyncio
import logging
import time
import traceback
import typing
from datetime import datetime, timezone
from io import BytesIO
from typing import NamedTuple, Optional

import orjson

from tinybird.hfi.ch_multiplexer import CHMultiplexerChannel, insert_chunk
from tinybird.hfi.utils import HFI_LOGGER_USER_AGENT
from tinybird.tracker import DatasourceOpsLogEntry, DatasourceOpsLogRecord, DatasourceOpsTrackerRegistry
from tinybird.user import User, public

HFI_LOG_TIME_INTERVAL = 2

hfi_logger_task: Optional[asyncio.Task] = None
hfi_logger_queue: Optional[asyncio.Queue] = None


class HFILogPoint(NamedTuple):
    workspace_id: str
    datasource_id: str
    datasource_name: str
    successful_rows: int
    quarantined_rows: int
    error: Optional[str]
    channel: CHMultiplexerChannel
    channel_state: str
    gatherer: bool = False


def hfi_log(log_point: HFILogPoint):
    global hfi_logger_task, hfi_logger_queue
    if not hfi_logger_task:
        hfi_logger_queue = asyncio.Queue()
        hfi_logger_task = asyncio.create_task(_hfi_logger())
    hfi_logger_queue.put_nowait(log_point)  # type: ignore


async def _hfi_logger():
    while True:
        try:
            await _hfi_logger_impl()
        except Exception as error:
            logging.warning(f"HFI logger. Unexpected exception {error}.\n{traceback.format_exc()}")


class HFILogAggregatedEntry(NamedTuple):
    workspace_id: str
    datasource_id: str
    datasource_name: str
    successful_rows: int
    quarantined_rows: int
    error: Optional[str]
    channel_ended: bool
    gatherer: bool


async def _hfi_logger_impl():
    global hfi_logger_queue
    pu = public.get_public_user()
    table = next(x for x in pu.datasources if x["name"] == "datasources_ops_log")
    endpoint = pu.database_server
    columns_list = [
        "timestamp",
        "event_type",
        "datasource_id",
        "datasource_name",
        "user_id",
        "user_mail",
        "result",
        "elapsed_time",
        "error",
        "request_id",
        "import_id",
        "job_id",
        "rows",
        "rows_quarantine",
        "blocks_ids",
        "Options.Names",
        "Options.Values",
    ]
    columns_types_list = [
        "DateTime",
        "String",
        "String",
        "String",
        "String",
        "String",
        "String",
        "Float32",
        "Nullable(String)",
        "String",
        "Nullable(String)",
        "Nullable(String)",
        "Nullable(UInt64)",
        "Nullable(UInt64)",
        "Array(String)",
        "Array(String)",
        "Array(String)",
    ]
    format = "JSONEachRow"

    pending_flushes: typing.Dict[CHMultiplexerChannel, HFILogAggregatedEntry] = {}
    completed_flushes: typing.Dict[CHMultiplexerChannel, HFILogAggregatedEntry] = {}
    time_last_flush = time.time()

    async def flush():
        for channel, agg_log in pending_flushes.copy().items():
            if agg_log.channel_ended:
                completed_flushes[channel] = pending_flushes[channel]
                del pending_flushes[channel]
        nonlocal time_last_flush
        if not completed_flushes:
            time_last_flush = time.time()
            return

        ndjson_buffer = BytesIO()
        datasources_ops_tracker = DatasourceOpsTrackerRegistry.get()
        # cache workspace inside a flush
        workspaces_in_flush: typing.Dict[str, User] = {}

        for ch, log_entry in completed_flushes.items():
            workspace: Optional[User] = None
            if datasources_ops_tracker and datasources_ops_tracker.is_alive:
                try:
                    workspace = workspaces_in_flush.get(log_entry.workspace_id)
                    if workspace is None:
                        workspace = User.get_by_id(log_entry.workspace_id)
                        if workspace:
                            workspaces_in_flush.update({workspace.id: workspace})
                        else:
                            # If the workspace is not found, does it make sense to log the entry?
                            continue

                except Exception as exc:
                    logging.exception(f"Error getting workspace {log_entry.workspace_id}: {exc}")

            if log_entry.gatherer and not log_entry.error:
                # Do not write gatherer inserts without error
                # They will be handled by tracker
                continue

            if workspace:
                resource_tags = [
                    tag.name
                    for tag in workspace.get_tags_by_resource(log_entry.datasource_id, log_entry.datasource_name)
                ]
                record = DatasourceOpsLogRecord(
                    timestamp=datetime.now(timezone.utc),
                    event_type="append-hfi",
                    datasource_id=log_entry.datasource_id,
                    datasource_name=log_entry.datasource_name,
                    user_id=log_entry.workspace_id,
                    user_mail="",
                    result="ok" if not log_entry.error else "error",
                    elapsed_time=ch.insertion_time,
                    error=log_entry.error,
                    request_id="",
                    import_id=None,
                    job_id=None,
                    rows=log_entry.successful_rows + log_entry.quarantined_rows,
                    rows_quarantine=log_entry.quarantined_rows,
                    blocks_ids=[],
                    Options__Names=[],
                    Options__Values=[],
                    operation_id=ch.query_id,
                    read_rows=0,
                    read_bytes=0,
                    written_rows=int(ch.stats_summary.get("written_rows", 0)),
                    written_bytes=int(ch.stats_summary.get("written_bytes", 0)),
                    written_rows_quarantine=0,
                    written_bytes_quarantine=0,
                    pipe_id="",
                    pipe_name="",
                    release="",
                    resource_tags=resource_tags,
                )
                datasources_ops_tracker.submit(
                    DatasourceOpsLogEntry(
                        record=record,
                        eta=record.timestamp,
                        workspace=workspace,
                        query_ids=[ch.query_id],
                        query_ids_quarantine=[],
                        landing_reached=False if log_entry.gatherer and log_entry.error else True,
                    )
                )
            else:
                raw_log_entry: typing.Dict[str, typing.Any] = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "event_type": "append-hfi",
                    "datasource_id": log_entry.datasource_id,
                    "datasource_name": log_entry.datasource_name,
                    "user_id": log_entry.workspace_id,
                    "user_mail": "",
                    "result": "ok" if not log_entry.error else "error",
                    "elapsed_time": ch.insertion_time,
                    "error": log_entry.error,
                    "request_id": "",
                    "import_id": None,
                    "job_id": None,
                    "rows": log_entry.successful_rows + log_entry.quarantined_rows,
                    "rows_quarantine": log_entry.quarantined_rows,
                    "blocks_ids": [],
                    "Options.Names": [],
                    "Options.Values": [],
                }
                ndjson_buffer.write(orjson.dumps(raw_log_entry))
                ndjson_buffer.write(b"\n")

        try:
            if ndjson_buffer.getbuffer().nbytes > 0:
                await insert_chunk(
                    endpoint,
                    pu.database,
                    pu.id,
                    table["id"],
                    columns_list,
                    columns_types_list,
                    format,
                    ndjson_buffer.getvalue(),
                    user_agent=HFI_LOGGER_USER_AGENT,
                )
        except Exception as e:
            logging.warning(f"Cannot insert in datasource_ops_log. Error:{e}")

        time_last_flush = time.time()
        completed_flushes.clear()

    while True:
        time_since_flush = time.time() - time_last_flush
        remaining_time = HFI_LOG_TIME_INTERVAL - time_since_flush
        if remaining_time <= 0:
            await flush()
            continue
        try:
            if hfi_logger_queue:
                request_log: HFILogPoint = await asyncio.wait_for(hfi_logger_queue.get(), timeout=remaining_time)
            else:
                await asyncio.sleep(remaining_time)
        except asyncio.TimeoutError:
            await flush()
            continue
        if request_log.channel in pending_flushes:
            pending_flushes[request_log.channel] = HFILogAggregatedEntry(
                workspace_id=request_log.workspace_id,
                datasource_id=request_log.datasource_id,
                datasource_name=request_log.datasource_name,
                successful_rows=request_log.successful_rows + pending_flushes[request_log.channel].successful_rows,
                quarantined_rows=request_log.quarantined_rows + pending_flushes[request_log.channel].quarantined_rows,
                error=pending_flushes[request_log.channel].error or request_log.error,
                channel_ended=pending_flushes[request_log.channel].channel_ended
                or request_log.channel_state == "ended",
                gatherer=request_log.gatherer,
            )
        else:
            pending_flushes[request_log.channel] = HFILogAggregatedEntry(
                workspace_id=request_log.workspace_id,
                datasource_id=request_log.datasource_id,
                datasource_name=request_log.datasource_name,
                successful_rows=request_log.successful_rows,
                quarantined_rows=request_log.quarantined_rows,
                error=request_log.error,
                channel_ended=request_log.channel_state == "ended",
                gatherer=request_log.gatherer,
            )
