import asyncio
import datetime
import json
import logging
import os
import random
import tempfile
import time
import traceback
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Union
from uuid import uuid4

import orjson
import pyarrow.parquet as pq

from tinybird import context
from tinybird.ch import (
    ERROR_COLUMNS_SORTED_NAMES,
    ERROR_COLUMNS_SORTED_TYPES,
    CHSummary,
    create_quarantine_table_from_landing,
    get_fallback_partition_column_name,
)
from tinybird.ch_utils.exceptions import CHException
from tinybird.csv_tools import csv_from_python_object_async
from tinybird.hfi.ch_multiplexer import CHMultiplexerChannel, insert_chunk
from tinybird.hfi.hfi_gatherer import HFI_USER_AGENT
from tinybird.limits import GB, MB, Limit
from tinybird.ndjson import ExtendedJSONDeserialization, JSONToRowbinary
from tinybird.sampler import Guess, guess
from tinybird.timing import Timer
from tinybird.views.aiohttp_shared_session import aiohttpClient
from tinybird.views.block_tracker import DummyBlockLogTracker, NDJSONBlockLogTracker
from tinybird.views.ch_local import ch_local_query
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client

MAX_JSON_GUESS_SIZE = 32 * 1024
NDJSON_CONCURRENCY_LIMIT = 1
NDJSON_CHUNK_SIZE = 32 * MB
NDJSON_CHUNK_SIZE_COMPRESSED = 512 * 1024
PARQUET_CHUNK_SIZE = 32 * MB
NDJSON_CH_LOCAL_TIMEOUT = 10


class IngestionError(Exception):
    pass


class MaxFileSize(IngestionError):
    pass


class InvalidFile(IngestionError):
    pass


class IngestionInternalError(Exception):
    def __init__(self, msg, error_code=None):
        super().__init__(msg)
        self.error_code = error_code

    pass


class PushError(IngestionInternalError):
    def __init__(
        self,
        msg,
        error_code=None,
        ch_summaries: Optional[List[CHSummary]] = None,
        ch_summaries_quarantine: Optional[List[CHSummary]] = None,
    ):
        super().__init__(msg, error_code)
        self.ch_summaries = ch_summaries if ch_summaries is not None else []
        self.ch_summaries_quarantine = ch_summaries_quarantine if ch_summaries_quarantine is not None else []

    pass


class UnimplementedFormat(IngestionError):
    pass


class IngestionReporter:
    def __init__(self, format):
        self._format = format
        self._last_report_timestamp = time.time()
        self._work_id = uuid4()
        self._processed_bytes = 0
        self._successful_rows = 0
        self._quarantined_rows = 0

    def work(self, processed_bytes, successful_rows, quarantined_rows):
        self._track(processed_bytes, successful_rows, quarantined_rows)
        if time.time() - self._last_report_timestamp < 5:
            return
        self.report()

    def _track(self, processed_bytes, successful_rows, quarantined_rows):
        self._processed_bytes += processed_bytes
        self._successful_rows += successful_rows
        self._quarantined_rows += quarantined_rows

    def report(self):
        self._last_report_timestamp = time.time()
        if self._processed_bytes or self._successful_rows or self._quarantined_rows:
            statsd_client.set(
                f"tinybird-ingestion.concurrent_work.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{self._format}.{context.origin.get('unknown')}",
                self._work_id,
            )
            statsd_client.incr(
                f"tinybird-ingestion.successful-rows.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{self._format}.{context.origin.get('unknown')}",
                self._successful_rows,
            )
            statsd_client.incr(
                f"tinybird-ingestion.quarantined-rows.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{self._format}.{context.origin.get('unknown')}",
                self._quarantined_rows,
            )
            statsd_client.incr(
                f"tinybird-ingestion.bytes_processed.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{self._format}.{context.origin.get('unknown')}",
                self._processed_bytes,
            )
        self._processed_bytes = 0
        self._successful_rows = 0
        self._quarantined_rows = 0


class NDJSONIngester:
    def __init__(
        self,
        extended_json_deserialization: ExtendedJSONDeserialization,
        database_server: Optional[str] = None,
        database: Optional[str] = None,
        workspace_id: str = "",
        datasource_id: str = "",
        format: str = "ndjson",
        pusher: str = "lfi",
        sample_iterations: int = 10,
        sampler_sampling_rate: float = 1.0,
        import_id: str = "",
        block_tracker: Optional[Union[NDJSONBlockLogTracker, DummyBlockLogTracker]] = None,
        max_import_size: Optional[int] = None,
        cluster: Optional[str] = None,
        token_id: Optional[str] = None,
    ):
        self._workspace = workspace_id
        self._table_id = datasource_id
        context.workspace_id.set(workspace_id)
        context.table_id.set(datasource_id)
        self._ingestor_reporter = IngestionReporter(format)
        self._chunk_size = NDJSON_CHUNK_SIZE
        self._encoder = RowBinaryEncoder(extended_json_deserialization, import_id)
        self.database = database
        columns = ", ".join(extended_json_deserialization.query_columns)
        columns_list = extended_json_deserialization.query_columns
        columns_types_list = extended_json_deserialization.query_columns_types

        insertion_date_column = get_fallback_partition_column_name(extended_json_deserialization.query_columns)
        quarantine_columns = f'{columns},{", ".join(ERROR_COLUMNS_SORTED_NAMES)},{insertion_date_column}'  # type: ignore
        quarantine_columns_list = columns_list + ERROR_COLUMNS_SORTED_NAMES + [insertion_date_column]
        quarantine_columns_types_list = columns_types_list + ERROR_COLUMNS_SORTED_TYPES + ["DateTime"]
        log_comment = {"token": token_id} if token_id else {}
        if format == "ndjson":
            # Temporary description for temporary size warning
            self._chunker = NDJSONChunker(max_import_size, f"{workspace_id}.{datasource_id}")
            self._decoder = NDJSONDecoder(len(extended_json_deserialization.query_columns))
        elif format == "parquet":
            self._chunker = SingleChunker(max_import_size)  # type: ignore
            self._decoder = ParquetDecoder(len(extended_json_deserialization.query_columns))  # type: ignore
        else:
            raise UnimplementedFormat(f"Unimplemented format {format}")

        if pusher == "lfi":
            self._pusher = CHHTTPPusher(database_server, database, datasource_id, columns)
            self._pusher_quarantine = CHHTTPQuarantinePusher(
                database_server,
                database,
                quarantine_datasource_id=f"{datasource_id}_quarantine",
                original_datasource_id=datasource_id,
                columns=quarantine_columns,
                cluster=cluster,
            )
        elif pusher == "hfi":
            self._pusher = CHMultiplexedHTTPPusher(
                database_server, database, workspace_id, datasource_id, columns_list, columns_types_list, log_comment
            )  # type: ignore
            self._pusher_quarantine = CHMultiplexedHTTPPusher(
                database_server,
                database,
                workspace_id,
                f"{datasource_id}_quarantine",
                quarantine_columns_list,
                quarantine_columns_types_list,
                log_comment,
            )  # type: ignore

        if pusher == "dry":
            self._pusher = CHLocalDryRun(extended_json_deserialization)  # type: ignore
            self._pusher_quarantine = DiscardSink()  # type: ignore

        should_sample = sampler_sampling_rate > random.random()
        self._sampler = (
            AsyncSampler(workspace_id, datasource_id, sample_iterations, pusher) if should_sample else NullSampler()
        )
        self.written = False
        self.block_tracker = block_tracker
        self.successful_rows = 0
        self.quarantined_rows = 0
        self.processed_bytes = 0
        self.ch_written_bytes = 0
        self.ch_written_rows = 0

    def write(self, chunk):
        if chunk:
            self.written = True
        self._chunker.write(chunk)

    async def work(self, block=None):
        # Workaround Tornado spliting requests into multiple contexts
        context.workspace_id.set(self._workspace)
        context.table_id.set(self._table_id)
        if self._chunker.buffer_size() < self._chunk_size:
            return None
        return await self._work(block, last=False)

    async def finish(self, block=None):
        # Workaround Tornado spliting requests into multiple contexts
        context.workspace_id.set(self._workspace)
        context.table_id.set(self._table_id)
        statsd_client.timing(
            f"tinybird-hfi.request_size.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
            self._chunker.buffer_size(),
        )
        try:
            push_result, push_quarantine_result = await self._work(block, last=True)
            self._sampler.send_sample()
            self.successful_rows = self._encoder.successful_rows
            self.quarantined_rows = self._encoder.quarantined_rows
        finally:
            self._chunker.close()
            self._ingestor_reporter.report()
        return push_result, push_quarantine_result

    async def _work(self, block, last):
        push_result = None
        push_quarantine_result = None
        prev_successful_rows = self._encoder.successful_rows
        prev_quarantined_rows = self._encoder.quarantined_rows
        ch_summaries: List[CHSummary] = []
        quarantine_ch_summaries: List[CHSummary] = []
        with Timer() as timer:
            assert self.block_tracker is not None
            self.block_tracker.on_processing(block)
            chunk = self._chunker.get_chunk(last=last)
            if not chunk:
                return None, None
            self.block_tracker.track_offset(block, self._chunker.buffer_size())
            self.block_tracker.on_queued(block and block["block_id"])
            async for rows, quarantine_rows_decoder, raw_rows in self._decoder.decode(chunk):
                prev_chunk_successful_rows = self._encoder.successful_rows
                prev_chunk_quarantined_rows = self._encoder.quarantined_rows
                rb_chunk, rb_quarantine_chunk = await self._encoder.encode(
                    rows, quarantine_rows_decoder, meta_rows=None, raw_rows=raw_rows
                )
                s_rows = self._encoder.successful_rows - prev_chunk_successful_rows
                q_rows = self._encoder.quarantined_rows - prev_chunk_quarantined_rows
                self._ingestor_reporter.work(len(rb_chunk) + len(rb_quarantine_chunk), s_rows, q_rows)
                self.processed_bytes += len(rb_chunk) + len(rb_quarantine_chunk)
                self.block_tracker.on_inserting_chunk(block and block["block_id"])
                if rb_chunk:
                    push_result = await self._pusher.push(rb_chunk, ch_summaries)
                if rb_quarantine_chunk:
                    push_quarantine_result = await self._pusher_quarantine.push(
                        rb_quarantine_chunk, quarantine_ch_summaries
                    )
                self._sampler.sample(rows)

        successful_rows = self._encoder.successful_rows - prev_successful_rows
        quarantined_rows = self._encoder.quarantined_rows - prev_quarantined_rows
        total_rows = successful_rows + quarantined_rows
        self.block_tracker.on_done_inserting_chunk(
            block and block["block_id"],
            total_rows,
            quarantined_rows,
            timer.elapsed_seconds(),
            ch_summaries,
            quarantine_ch_summaries,
        )
        self.ch_written_bytes += sum([int(stat.summary.get("written_bytes", 0)) for stat in ch_summaries])
        self.ch_written_rows += sum([int(stat.summary.get("written_rows", 0)) for stat in ch_summaries])
        self.block_tracker.on_done(block and block["block_id"])
        return push_result, push_quarantine_result


async def kafka_preview(extended_json_deserialization, messages, store_headers=False):
    topic = next((msg["__topic"] for msg in messages), None)
    encoder = RowBinaryEncoder(extended_json_deserialization, topic=topic, store_headers=store_headers)
    pusher = CHLocalDryRun(extended_json_deserialization, kafka=True, store_headers=store_headers)
    rows = []
    raw_rows = []
    meta_rows = []
    for msg in messages:
        try:
            obj = orjson.loads(msg["__value"])

            if isinstance(msg["__key"], bytes):
                key = msg["__key"]
            else:
                key = msg["__key"].encode("utf-8") if msg["__key"] is not None else b""

            meta_row = (
                msg["__value"].encode("utf-8"),
                msg["__partition"],
                msg["__offset"],
                msg["__timestamp"],
                key,
                msg["__headers"].encode("utf-8"),
            )

            rows.append(obj)
            raw_rows.append(msg["__value"])
            meta_rows.append(meta_row)
        except orjson.JSONDecodeError:
            pass
    rb_chunk, _rb_quarantine_chunk = await encoder.encode(rows, [], meta_rows, raw_rows, process_headers=True)
    preview = await pusher.push(rb_chunk)
    return preview


async def dynamodb_preview(extended_json_deserialization, rows):
    encoder = RowBinaryEncoder(extended_json_deserialization)
    pusher = CHLocalDryRun(extended_json_deserialization)
    rb_chunk, _rb_quarantine_chunk = await encoder.encode(rows, [], None, None)
    preview = await pusher.push(rb_chunk)
    return preview


class NDJSONChunker:
    def __init__(self, size_limit: Optional[int] = None, description: Optional[str] = None):
        self._json_buffer = BytesIO()
        self._size = 0
        self._size_limit = size_limit
        self._description = description

    def write(self, chunk):
        if self._size_limit and self._size <= self._size_limit and self._size + len(chunk) > self._size_limit:
            logging.warning(
                f"Max request size {self._size_limit / MB} MB reached for {self._description}, limit not enforced"
            )
        self._size += len(chunk)
        self._json_buffer.write(chunk)

    def buffer_size(self):
        return self._size

    def get_chunk(self, last=False):
        data = self._json_buffer.getvalue()
        if not data:
            return b""

        if not last:
            split_index = data.rfind(b"\n") + 1
            incomplete_data = data[split_index:]
            self._json_buffer.seek(0)
            self._json_buffer.truncate()
            self._json_buffer.write(incomplete_data)
        else:
            split_index = len(data)

        chunk = data[:split_index]
        return chunk

    def close(self):
        pass


class SingleChunker:
    def __init__(self, size_limit: Optional[int] = None):
        Path("/tmp/tinybird/parquet").mkdir(parents=True, exist_ok=True)
        self._file = tempfile.NamedTemporaryFile(
            mode="w+b", delete=False, prefix="parquet_", dir="/tmp/tinybird/parquet"
        )
        self._size = 0
        self._size_limit = size_limit if size_limit else Limit.import_max_url_parquet_file_size_dev_gb * GB

    def write(self, chunk):
        self._size += len(chunk)
        if self._size > self._size_limit:
            self._file.close()
            os.unlink(self._file.name)
            raise MaxFileSize(
                f"Max file size reached: {self._size_limit / MB} MB. Please split the file into smaller ones."
            )
        self._file.write(chunk)

    def buffer_size(self):
        return self._size

    def get_chunk(self, last=False):
        if not last or not self.buffer_size():
            return b""
        self._file.close()
        return self._file.name

    def head(self, size):
        self._file.seek(0)
        return self._file.read(size)

    def close(self):
        try:
            os.unlink(self._file.name)
        except Exception:
            pass

    def __del__(self):
        self.close()


class NDJSONDecoder:
    def __init__(self, hint_num_columns=10):
        self.hint_num_columns = hint_num_columns

    async def decode(self, chunk):
        quarantine_decoder_errors = []
        rows = []
        raw_rows = []
        yielder = AsyncioYielder(max_cost=10 * int(10000 / (self.hint_num_columns + 1)))
        for json_obj in BytesIO(chunk):
            try:
                obj = orjson.loads(json_obj)
                rows.append(obj)
                raw_rows.append(json_obj)
            except orjson.JSONDecodeError:
                res = json_obj.decode("utf-8", "replace").replace("\n", "")
                # we do not compute empty lines or just with spaces '  \n', ' '...
                if len(res.replace(" ", "")) == 0:
                    continue
                quarantine_decoder_errors.append(f"Line is not a valid JSON: '{res}'")
            await yielder.yield_if_needed(cost=len(json_obj))
        yield rows, quarantine_decoder_errors, raw_rows


class ParquetDecoder:
    def __init__(self, hint_num_columns=10):
        self.limit_rows = None
        self.hint_num_columns = hint_num_columns

    async def decode(self, parquetData):
        try:
            pq_file = pq.ParquetFile(parquetData)
        except Exception as e:
            logging.error(f"Error on ParquetDecoder.decode. File is not a valid Parquet file: {e}")
            raise InvalidFile("File is not a valid Parquet file")
        batch_bytes = 0
        batch_rows = []
        for batch in pq_file.iter_batches(int(10000 / (self.hint_num_columns + 1)), use_threads=False):
            await asyncio.sleep(0)
            batch_rows += batch.to_pylist()
            batch_bytes += batch.nbytes

            if self.limit_rows is not None:
                yield batch_rows[: self.limit_rows], [], None
                return

            if batch_bytes >= PARQUET_CHUNK_SIZE:
                yield batch_rows, [], None
                batch_bytes = 0
                batch_rows.clear()

        if batch_rows:
            yield batch_rows, [], None


class AsyncioYielder:
    def __init__(self, max_cost=1):
        self._max_cost = max_cost
        self._cost = 0

    async def yield_if_needed(self, cost=1):
        self._cost += cost
        if self._cost >= self._max_cost:
            self._cost = 0
            await asyncio.sleep(0)


def create_json_to_rowbinary_encoder(
    extended_json_deserialization: ExtendedJSONDeserialization,
    topic=None,
    truncate_value=False,
    store_headers=False,
    store_binary_headers=False,
):
    return JSONToRowbinary(
        extended_json_deserialization,
        topic=topic,
        truncate_value=truncate_value,
        store_headers=store_headers,
        store_binary_headers=store_binary_headers,
    )


class RowBinaryEncoder:
    def __init__(
        self,
        extended_json_deserialization,
        import_id="",
        topic=None,
        store_headers=False,
    ):
        self._converter = create_json_to_rowbinary_encoder(
            extended_json_deserialization, topic=topic, store_headers=store_headers
        )
        self._import_id = import_id
        self.successful_rows = 0
        self.quarantined_rows = 0
        self._yielder = AsyncioYielder(max_cost=int(10000 / (len(extended_json_deserialization.query_columns) + 1)))

    async def encode(
        self,
        rows,
        quarantine_rows,
        meta_rows=None,
        raw_rows=None,
        process_headers=False,
    ):
        yielder = self._yielder
        for error in quarantine_rows:
            self._converter.append_to_quarantine(
                [""],
                [error],
                self._import_id,
                self._converter.extended_json_deserialization,
                self._converter.quarantine_buffer.write,
                {},
                self._converter.fast_leb_table,
                self._converter.leb128_buffer,
                True,
            )
            await yielder.yield_if_needed()
        if meta_rows:
            for obj, meta_row, raw_obj in zip(rows, meta_rows, raw_rows, strict=True):
                self._converter.convert(
                    obj=obj,
                    json_obj=raw_obj,
                    import_id=self._import_id,
                    metadata=meta_row,
                )
                await yielder.yield_if_needed()
        else:
            if not raw_rows:
                for obj in rows:
                    self._converter.convert(obj=obj, json_obj=b"", import_id=self._import_id)
                    await yielder.yield_if_needed()
            else:
                for obj, raw_obj in zip(rows, raw_rows, strict=True):
                    self._converter.convert(obj=obj, json_obj=raw_obj, import_id=self._import_id)
                    await yielder.yield_if_needed()
        data, quarantine_data = self._converter.flush()
        self.successful_rows = self._converter.total_rows - self._converter.quarantine_rows
        self.quarantined_rows = self._converter.quarantine_rows + len(quarantine_rows)
        return data, quarantine_data


class CHHTTPPusher:
    def __init__(
        self,
        database_server: Optional[str],
        database: Optional[str],
        datasource_id: str,
        columns: str,
    ):
        self._client = aiohttpClient(database_server, database)
        self._format = "RowBinaryWithDefaults"
        self._request_params = {
            "query": f"INSERT INTO {database}.{datasource_id}({columns}) FORMAT {self._format}",
        }

    async def push(self, rowbinary_chunk, ch_summaries: Optional[List[CHSummary]] = None):
        query_id = str(uuid4())
        extra_params = {
            "insert_deduplicate": 0,
            "max_partitions_per_insert_block": 12,
            "query_id": query_id,
        }
        try:
            headers, result = await self._client.insert_chunk(
                self._request_params["query"],
                rowbinary_chunk,
                dialect=None,
                # We had to set a timeout because the default one is 10 seconds and it's not enough for zero copy without hot disk
                max_execution_time=30,
                extra_params=extra_params,
            )
            if ch_summaries is not None:
                ch_summary = headers.get("X-Clickhouse-Summary")
                ch_summaries.append(
                    CHSummary(
                        query_id=query_id,
                        summary=json.loads(ch_summary) if ch_summary else {},
                    )
                )
        except CHException as e:
            if e.headers and ch_summaries is not None:
                x_ch_summary = e.headers.get("X-Clickhouse-Summary")
                ch_summaries.append(
                    CHSummary(
                        query_id=query_id,
                        summary=json.loads(x_ch_summary) if x_ch_summary else {},
                    )
                )
            raise PushError(f"Tinybird internal error: {e}", e.code, ch_summaries)
        except Exception as e:
            raise PushError(f"Tinybird internal error: {e}")


class CHHTTPQuarantinePusher(CHHTTPPusher):
    """
    This class expects to push to a quarantine table. If the table does not exist it, it will generate it
    """

    def __init__(
        self,
        database_server: Optional[str],
        database: Optional[str],
        quarantine_datasource_id: str,
        original_datasource_id: str,
        columns: str,
        cluster: Optional[str] = None,
    ):
        self._database_server = database_server or "localhost"
        self._database = database or "default"
        self._datasource_id = quarantine_datasource_id
        self._original_datasource_id = original_datasource_id
        self._cluster = cluster
        self._columns = columns

        super().__init__(database_server, database, quarantine_datasource_id, columns)

    async def create_quarantine_table(self) -> bool:
        try:
            await create_quarantine_table_from_landing(
                self._original_datasource_id,
                self._database_server,
                self._database,
                self._cluster,
            )
            return True
        except Exception as e:
            logging.error(f"Unable to create quarantine table: {str(e)}")
            return False

    async def push(self, rowbinary_chunk, ch_summaries: Optional[List[CHSummary]] = None):
        try:
            return await super().push(rowbinary_chunk, ch_summaries)
        except PushError as e:
            # If the quarantine table does not exist, we create it and retry the push
            if e.error_code == CHErrors.UNKNOWN_TABLE:
                created = await self.create_quarantine_table()
                if created:
                    return await super().push(rowbinary_chunk, ch_summaries)
            else:
                # track summaries for quarantine
                e.ch_summaries_quarantine = e.ch_summaries
                e.ch_summaries = []
                raise e


class CHMultiplexedHTTPPusher:
    def __init__(
        self,
        database_server,
        database,
        workspace_id,
        table_id,
        columns_list,
        columns_types_list,
        log_comment,
    ):
        self._database_server = database_server
        self._database = database
        self._table_id = table_id
        self._columns_list = columns_list
        self._columns_types_list = columns_types_list
        self._format = "RowBinaryWithDefaults"
        self._extra_params: Dict[str, str | int] = {
            "insert_deduplicate": 0,
            "max_partitions_per_insert_block": 12,
        }
        if log_comment:
            self._extra_params.update({"log_comment": json.dumps(log_comment)})
        self._channels: list[CHMultiplexerChannel] = []
        self._workspace_id = workspace_id

    async def push(self, rowbinary_chunk, _ch_summaries: Optional[List[CHSummary]] = None):
        ch = await insert_chunk(
            self._database_server,
            self._database,
            self._workspace_id,
            self._table_id,
            self._columns_list,
            self._columns_types_list,
            self._format,
            rowbinary_chunk,
            user_agent=HFI_USER_AGENT,
            extra_params=self._extra_params,
        )
        self._channels.append(ch)


def safe_sql_column(column_name: str):
    if "`" in column_name:
        raise Exception("Invalid column name containing the backtick (`) character")
    return f"`{column_name}`"


class CHLocalDryRun:
    def __init__(self, extended_json_deserialization, kafka=False, store_headers=False):
        original_columns = ", ".join(safe_sql_column(x) for x in extended_json_deserialization.original_order_columns)
        self._query = f"SELECT {original_columns} FROM input_table"
        self._format = "RowBinaryWithDefaults"
        conf = extended_json_deserialization
        self._schema = ", ".join(
            [
                f"{safe_sql_column(conf.query_columns[i])} {conf.query_columns_types[i]}"
                for i in range(len(conf.query_columns))
            ]
        )
        if kafka:
            schema = "__value String, __topic String, __partition Int16, __offset Int64, __timestamp DateTime, __key String, "
            if store_headers:
                schema += "__headers String, "
            self._schema = f"{schema}{self._schema}"

    async def push(self, rowbinary_chunk, _ch_summaries: Optional[List[CHSummary]] = None):
        ch_result = await ch_local_query(
            self._query,
            rowbinary_chunk or b"",
            self._format,
            self._schema,
            timeout=NDJSON_CH_LOCAL_TIMEOUT,
            input_random_access_table="input_table",
        )
        result = json.loads(ch_result)
        return result


class DiscardSink:
    async def push(self, _rowbinary_chunk, _ch_summaries: Optional[List[CHSummary]] = None):
        pass


class NullSampler:
    def sample(self, _):
        pass

    def send_sample(self):
        pass


class AsyncSampler:
    def __init__(self, workspace_id, datasource_id, sample_iterations, pusher):
        self._workspace_id = workspace_id
        self._datasource_id = datasource_id
        self._sample_iterations = sample_iterations
        self._pusher = pusher
        self._guess_list: List[tuple] = []
        self._guess_keys: set = set()
        self._random = random.Random()

    def sample(self, rows):
        try:
            if not rows or self._sample_iterations <= 0:
                return
            t = datetime.datetime.now()
            date_formatted = "%04d-%02d-%02d %02d:%02d:%02d" % (
                t.year,
                t.month,
                t.day,
                t.hour,
                t.minute,
                t.second,
            )
            self._random.seed(len(rows))
            iterations = min(len(rows), self._sample_iterations)
            self._sample_iterations -= iterations
            sample = self._random.sample(rows, k=iterations)
            guess_list: List[Guess] = []
            for obj in sample:
                guess(
                    self._workspace_id,
                    self._datasource_id,
                    guess_list,
                    obj,
                    date_formatted,
                )
            if self._pusher == "hfi":
                # Only filter in hfi mode due to new ingestion will happen very frequently
                self._append_each_column_once(guess_list)
            else:
                self._guess_list += guess_list
        except Exception as e:
            logging.warning(f"sample() failed with an unexpected exception: {e}\n{traceback.format_exc()}")

    def _append_each_column_once(self, guess_list: List[Guess]):
        try:
            # Append only non-existing guessed columns
            # This is to avoid a big growing of data_guess table. Only store the columns once per sampling.
            for item in guess_list:
                # key : workspace_id#ds_id#json_path#type
                # Not take into account: timestamp (2), numeric_value(5), str_value(6)
                key = f"{item[0]}#{item[1]}#{item[3]}#{item[4]}"
                if key not in self._guess_keys:
                    self._guess_keys.add(key)
                    self._guess_list.append(item)
        except Exception as e:
            logging.warning(
                f"_append_each_column_once() failed with an unexpected exception: {e}\n{traceback.format_exc()}"
            )

    def send_sample(self):
        if not self._guess_list:
            return
        asyncio.create_task(self._send_sample_coro())  # noqa: RUF006

    async def _send_sample_coro(self):
        try:
            from tinybird.user import public

            pu = public.get_public_user()
            sample_csv = await csv_from_python_object_async(self._guess_list)
            sample_csv_bytes = sample_csv.encode("utf-8")
            server = pu.database_server
            columns_list = ["user_id", "datasource_id", "timestamp", "path", "type", "num", "str"]
            columns_types_list = ["String", "String", "Nullable(String)", "String", "String", "Float32", "String"]
            format = "CSV"
            await insert_chunk(
                server,
                pu.database,
                pu.id,
                "data_guess",
                columns_list,
                columns_types_list,
                format,
                sample_csv_bytes,
                user_agent="tb-data-guess-sampler",
            )
        except Exception as err:
            logging.warning(f"send_sample failed with an unexpected exception {err}\n{traceback.format_exc()}")
