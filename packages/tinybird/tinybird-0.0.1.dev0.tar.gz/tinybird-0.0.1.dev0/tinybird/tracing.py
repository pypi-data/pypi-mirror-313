import json
import logging
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, fields
from threading import Timer
from typing import Any, List, Optional
from urllib.parse import urlparse

import requests
from basictracer import BasicTracer
from basictracer.recorder import SpanRecorder
from opentracing.scope_managers.tornado import TornadoScopeManager, tracer_stack_context

from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.retry.retry import retry_sync

from .ch import CHException, HTTPClient
from .csv_tools import csv_from_python_object


class BufferedInsert:
    """
    insert data into clickhouse database, table
    """

    def __init__(
        self,
        wait,
        max_size,
        host,
        database,
        table,
        columns: Optional[List[str]] = None,
        async_insert: Optional[bool] = False,
    ):
        self.host = host
        self.database = database
        self.table = table
        self.max_size = max_size
        self.wait = wait  # s
        self.client = HTTPClient(host, database)
        self.buffer: List[Any] = []
        self.timer: Optional[Timer] = None
        self.buffer_lock = threading.Lock()
        self.columns = columns or []
        self.async_insert = async_insert

    def append(self, row):
        with self.buffer_lock:
            self.buffer.append(row)
            insert = len(self.buffer) >= self.max_size

        if not insert:
            if not self.timer:
                self.timer = Timer(self.wait, self.insert_buffer)
                self.timer.name = "buffered_insert_tracer"
                self.timer.start()
        else:
            if self.timer:
                self.timer.cancel()
            self.insert_buffer()

    def insert_buffer(self):
        with self.buffer_lock:
            buffer = self.buffer
            self.buffer = []

        # Let's just try to insert data if we have data
        if buffer:
            # enable a different context so we don't have a infinite loop
            # because we don't want to trace this call
            with tracer_stack_context():
                try:
                    columns = f"({', '.join(self.columns)})" if self.columns else ""

                    @retry_sync((CHException, requests.exceptions.ConnectionError), tries=4, delay=1)
                    def insert_chunk(query, chunk):
                        extra_params = {"async_insert": 1} if self.async_insert else {}
                        self.client.insert_chunk(query, chunk, log_as_error=False, extra_params=extra_params)

                    insert_chunk(f"insert into `{self.table}` {columns} FORMAT CSV", csv_from_python_object(buffer))
                except Exception as exc:
                    logging.exception(f"Spans insertion error: {exc}")
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def clear(self):
        with self.buffer_lock:
            self.buffer = []


class ClickhouseTracer(BasicTracer):
    def __init__(self, enable_logger: bool = False):
        logger = logging.getLogger("span_logging")
        logger.setLevel(logging.INFO)
        hndlr = logging.StreamHandler(sys.stdout)
        hndlr.setFormatter(logging.Formatter("[%(levelname)-8s] %(name)s: %(message)s"))
        logger.addHandler(hndlr)

        self.recorder = LogSpanRecorder(logger=logger if enable_logger else None, enable_statsd=True)
        BasicTracer.__init__(self, recorder=self.recorder, scope_manager=TornadoScopeManager())

    def set_logging_clickhouse(self, host, database, table, async_insert=False):
        self.register_required_propagators()
        self.recorder.set_logging_clickhouse(host, database, table, async_insert)


@dataclass
class SpanRecord:
    span_id: str
    operation_name: str
    start_datetime: int
    start_time: Any
    duration: Any
    parent_id: Optional[str]
    component: str
    kind: str
    user: Optional[str]
    user_email: Optional[str]
    workspace: str
    workspace_name: str
    token: str
    token_name: str
    url: Optional[str]
    method: Optional[str]
    status_code: str
    error: Any
    logs: List[str]
    tags: str

    @classmethod
    def get_columns(cls):
        return [field.name for field in fields(cls)]

    def values(self):
        return [getattr(self, field.name) for field in fields(self)]


class LogSpanRecorder(SpanRecorder):
    """Records spans by printing them to a log
    Fields:
        - logger (Logger): Logger used to display spans
    """

    def __init__(self, logger: Optional[logging.Logger], enable_statsd: bool):
        self.logger = logger
        self.buffer: Optional[BufferedInsert] = None
        self.max_size = float(os.environ.get("SPANS_MAX_SIZE_BYTES", "1048576"))
        self.pool: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="log_span_recorder")
        self.statsd = enable_statsd

    def __del__(self):
        self.pool.shutdown(wait=True)
        if self.buffer:
            self.buffer.insert_buffer()
            # "Cancel the interval flush as we are leaving
            if self.buffer.timer:
                self.buffer.timer.cancel()

    def set_logging_clickhouse(self, host, database, table, async_insert=False):
        self.buffer = BufferedInsert(
            5, self.max_size, host, database, table, columns=SpanRecord.get_columns(), async_insert=async_insert
        )

    def flush(self):
        """
        Only intended to be used for testing purposes.
        """

        # We submit an empty function and wait to be completed
        # As we have only 1 worker in the threadpool, once this method finished means the rest of the threads did as well.
        def do_nothing():
            pass

        self.pool.submit(do_nothing).result()
        if self.buffer:
            self.buffer.insert_buffer()

    def clear(self):
        if self.buffer:
            self.buffer.clear()
        self.pool.shutdown()

    def _send_statsd(self, spans_row: SpanRecord) -> None:
        try:
            if spans_row.kind == "server":
                statsd_client.timing(
                    f"tinybird-server.handlers.{statsd_client.region}.unknown.{spans_row.method}."
                    f"{spans_row.operation_name}.{spans_row.workspace_name or 'unknown'}."
                    f"unknown.{spans_row.status_code}.duration",
                    spans_row.duration,
                )
                if spans_row.operation_name == "APIPipeDataHandler":
                    tags = json.loads(spans_row.tags)
                    if "pipe_id" in tags and (
                        match_pipe_name := re.match(r"/v0/pipes/(?P<pipe_name>.*)\.", str(urlparse(spans_row.url).path))
                    ):
                        statsd_client.timing(
                            f"tinybird-server.pipe_endpoints.{statsd_client.region}."
                            f"{spans_row.workspace_name or 'unknown'}.unknown."
                            f"{match_pipe_name['pipe_name']}.unknown."
                            f"{spans_row.status_code}.duration",
                            spans_row.duration,
                        )
        except Exception as exc:
            logging.exception(f"Exception sending spans to statsd {exc}")

    """
    Private method to record spans in a different thread so that any processing (and request to ClickHouse) isn't
    handled in the main loop
    """

    def _record_span(self, span, exc_info=None):
        bracket_items = []  # Information to put in log tag brackets

        error = None
        error_obj = None
        has_error = span.tags.get("error", False)
        if has_error:
            # extract error from span logs
            error_objs = [
                log.key_values["error.object"] for log in span.logs if log.key_values.get("event", "") == "error"
            ]
            if error_objs:
                error_obj = error_objs[0]
                error = str(error_obj)
            else:
                error = has_error

        from tinybird.views.base import ApiHTTPError

        status_code = span.tags.get(
            "http.status_code", error_obj.status_code if isinstance(error_obj, ApiHTTPError) else 500
        )

        row = SpanRecord(
            span_id=str(span.context.span_id),
            operation_name=span.operation_name,
            start_datetime=int(span.start_time),
            start_time=span.start_time,
            duration=span.duration,
            parent_id=str(span.parent_id) if span.parent_id else None,
            component=span.tags.get("component"),
            kind=span.tags.get("span.kind"),
            user=span.tags.pop("user", "") or "",
            user_email=span.tags.pop("user_email", "") or "",
            workspace=span.tags.pop("workspace", "") or "",
            workspace_name=span.tags.pop("workspace_name", "") or "",
            token=span.tags.pop("token", "") or "",
            token_name=span.tags.pop("token_name", "") or "",
            # the following ones are tags only send by
            # tornado spans, but they are so frequent that makes
            # sense to have them as nullable columns
            url=span.tags.get("http.url", None),
            method=span.tags.get("http.method", None),
            status_code=status_code,
            error=error,
            logs=[
                json.dumps(dict(timestamp=log.timestamp, values=log.key_values), skipkeys=True, default=lambda x: None)
                for log in span.logs
            ],
            tags=json.dumps(
                {
                    x: span.tags[x]
                    for x in span.tags
                    if x not in ("component", "span.kind", "http.url", "http.method", "http.status_code", "error")
                },
                skipkeys=True,
                default=lambda x: None,
            ),
        )

        if self.buffer:
            self.buffer.append(row.values())

        if self.statsd:
            self._send_statsd(row)

        if self.logger:
            # Time
            duration_str = "{0:.2f} S".format(span.duration)

            if span.duration < 0:
                duration_str = "{0:.2e} S".format(span.duration)

            bracket_items.append(duration_str)

            # Parent ID
            if span.parent_id is not None:
                bracket_items.append("parent={}".format(span.parent_id))

            # Tags
            tags_strs = ["{}={}".format(tag, span.tags[tag]) for tag in span.tags]
            bracket_items.extend(tags_strs)

            # Create logger for span
            bracket_str = " ".join(bracket_items)

            span_logger = self.logger.getChild(
                "{}.{}[{}]".format(span.operation_name, span.context.span_id, bracket_str)
            )

            # Print span logs
            if len(span.logs) > 0:
                for log in span.logs:
                    log_str = " ".join(["{}={}".format(log_key, log.key_values[log_key]) for log_key in log.key_values])

                    span_logger.debug(log_str)
            else:
                # If no span logs exist simply print span finished
                span_logger.debug("finished")

    def record_span(self, span):
        self.pool.submit(LogSpanRecorder._record_span, self, span, exc_info=sys.exc_info())
