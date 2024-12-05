import asyncio
import base64
import logging
import os
import time
import timeit
import traceback
import zlib
from collections import namedtuple
from io import BytesIO
from math import ceil, floor
from typing import Any, Dict, List, NamedTuple, Optional, Tuple
from urllib.parse import urlparse

import orjson
import sentry_sdk
from cachetools import TTLCache
from sentry_sdk import Hub
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import ClientDisconnect, Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Route

from tinybird import context
from tinybird.ch_utils.exceptions import clickhouse_parse_code_error
from tinybird.distributed import LockTimeoutError, distributed_lock
from tinybird.guess_analyze import analyze
from tinybird.hfi.ch_multiplexer import AnalyzeError, force_flush_ch_multiplexer
from tinybird.hfi.circuit_breakers import CircuitBreakersException, get_circuit_breaker_id, global_hfi_circuit_breakers
from tinybird.hfi.circuit_breakers_rate_limit import global_hfi_circuit_breakers_rate_limit
from tinybird.hfi.errors import APIError
from tinybird.hfi.hfi_defaults import (
    DEFAULT_HFI_MAX_REQUEST_MB,
    DEFAULT_HFI_RATE_LIMIT_BURST,
    DEFAULT_HFI_RATE_LIMIT_PACE,
    DEFAULT_HFI_SEMAPHORE_COUNTER,
    DEFAULT_HFI_SEMAPHORE_TIMEOUT,
    DEFAULT_HTTP_ERROR,
    HFI_CACHE_DURATION,
    HFI_CACHE_DURATION_ON_ERROR,
    HFI_CACHE_RETRY_DURATION_ON_ERROR,
    HFI_SAMPLING_BUCKET,
    HFI_SEMAPHORE_MINIMUM_CHECK_SIZE,
    LAG_MONITOR_THRESHOLD_IN_SECS,
    RATE_LIMITS_TOKENS_PER_REQUEST,
    REDIS_TIMEOUT,
)
from tinybird.hfi.hfi_log import HFILogPoint, hfi_log
from tinybird.hfi.hfi_settings import hfi_settings
from tinybird.hfi.utils import get_error_message_and_http_code_for_ch_error_code
from tinybird.ingest.datasource_creation import DatasourceCreationError, create_datasource
from tinybird.lag_monitor import LagMonitor
from tinybird.limits import MB
from tinybird.model import RedisModel
from tinybird.ndjson import UnsupportedType, extend_json_deserialization
from tinybird.python_orphan_task_workaround import workaround_orphan_task
from tinybird.redis_config import get_redis_config
from tinybird.sql import parse_table_structure
from tinybird.syncasync import sync_to_async
from tinybird.token_scope import scopes
from tinybird.tokens import token_decode, token_decode_unverify
from tinybird.tracker import DatasourceOpsTrackerRegistry
from tinybird.user import DatasourceLimitReached, ResourceAlreadyExists, User, UserAccount
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.block_tracker import DummyBlockLogTracker
from tinybird.views.gzip_utils import GZIP_MAGIC_CODE, has_gzip_magic_code
from tinybird.views.json_deserialize_utils import json_deserialize_merge_schema_jsonpaths, parse_augmented_schema
from tinybird.views.ndjson_importer import NDJSONIngester, UnimplementedFormat
from tinybird.views.utils import split_ndjson
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisReplicaClientSync, async_redis

SemaphoreData = namedtuple("SemaphoreData", ["semaphore", "counter", "timeout"])

global_hfi_cache: Dict[str, dict] = dict()
global_hfi_token_cache: TTLCache = TTLCache(maxsize=1000, ttl=HFI_CACHE_DURATION)
global_hfi_semaphore: TTLCache = TTLCache(maxsize=100_000, ttl=300)
redis_client = None
lag_monitor: Optional[LagMonitor] = None
concurrent_active_requests: TTLCache = TTLCache(maxsize=10_000, ttl=300)
concurrent_wait_requests: TTLCache = TTLCache(maxsize=10_000, ttl=300)


class UnexpectedHFICondition(Exception):
    pass


# Note that we may have to add exceptions also in exception_workaround() below
expected_exceptions = (
    UnimplementedFormat,
    AnalyzeError,
    ResourceAlreadyExists,
    UnexpectedHFICondition,
    LockTimeoutError,
    UnsupportedType,
)
expected_exception_http_codes = {
    UnimplementedFormat: 501,
    AnalyzeError: 400,
    ResourceAlreadyExists: 409,
    UnexpectedHFICondition: 422,
    LockTimeoutError: 503,
    UnsupportedType: 400,
}
RATE_LIMIT_MSG = "Too many requests\n"
RATE_LIMIT_HTTP_CODE = 429
INITIAL_LOOKUP_SIZE = 64 * 1024
ACQUIRE_LOCK_TIMEOUT = 10


class HfiConfig(NamedTuple):
    current_config: Optional[asyncio.Task]
    last_successful_config: Optional[Dict[str, Any]]


def statsd_request_monitor(func):
    async def inner_func(*args, **kwargs):
        t0 = time.monotonic()
        response = await func(*args, **kwargs)
        status_code = response.status_code
        region_machine = statsd_client.region_machine
        workspace_id = context.workspace_id.get("unknown")
        statsd_client.incr(
            f"tinybird-hfi.requests.{region_machine}.{workspace_id}.{context.table_id.get('unknown')}.{status_code}.{context.origin.get('unknown')}"
        )
        statsd_client.timing(f"tinybird-hfi.requests_time.{region_machine}.{workspace_id}", time.monotonic() - t0)
        return response

    return inner_func


class CHErrorPythonWorkaround(Exception):
    def __init__(self, message, is_materialized_view, error_code: int, data_not_ingested: Optional[bool]):
        self.message = message
        self.is_materialized_view = is_materialized_view
        self.error_code = error_code
        self.data_not_ingested = data_not_ingested
        super().__init__(message)


class OrjsonResponse(JSONResponse):
    def render(self, content) -> bytes:
        return orjson.dumps(content)


class OriginType:
    EVENTS = "EVENTS"
    SNS = "SNS"
    KINESIS = "KINESIS"


def get_response(
    origin: str,
    http_code: int,
    request_id: str,
    successful_rows: int,
    quarantined_rows: int,
    headers: Optional[Dict[str, str]] = None,
):
    response_body = None
    if origin == OriginType.KINESIS:
        response_body = {
            "requestId": request_id,
            "timestamp": int(time.time() * 1000),
        }
    else:
        response_body = {
            "successful_rows": successful_rows,
            "quarantined_rows": quarantined_rows,
        }

    return OrjsonResponse(content=response_body, status_code=http_code, headers=headers)


def get_error_response(error_msg, http_code):
    logging.info(f"Sending response for HTTP code {http_code}, error message {error_msg}")
    origin = context.origin.get(OriginType.EVENTS)

    if origin == OriginType.KINESIS:
        request_id = context.request_id.get("")
        return OrjsonResponse(
            {"requestId": request_id, "timestamp": int(time.time() * 1000), "errorMessage": error_msg}, http_code
        )
    else:
        return PlainTextResponse(error_msg, http_code)


@statsd_request_monitor
async def hfi(request: Request, default_request_origin: str = OriginType.EVENTS) -> Response:
    t_0 = timeit.default_timer()
    try:
        return await hfi_impl(request, default_request_origin)
    except CircuitBreakersException as err:
        ch_error_code = clickhouse_parse_code_error(str(err), headers=None)
        if ch_error_code is None:
            return get_error_response(str(err), 503)
        else:
            error_msg, error_code = get_error_message_and_http_code_for_ch_error_code(
                str(err), ch_error_code, default_http_error=503
            )
            return get_error_response(error_msg, error_code)
    except CHErrorPythonWorkaround as err:
        if err.is_materialized_view:
            error_code = 503 if err.data_not_ingested else 422
            return get_error_response(str(err), error_code)
        else:
            error_msg, error_code = get_error_message_and_http_code_for_ch_error_code(str(err), err.error_code)
            return get_error_response(error_msg, error_code)
    except expected_exceptions as err:
        exception_type = type(err)
        http_code = expected_exception_http_codes.get(exception_type, DEFAULT_HTTP_ERROR)
        return get_error_response(str(err), http_code)
    except APIError as err:
        if err.status_code == RATE_LIMIT_HTTP_CODE and (workspace_id := context.workspace_id.get(None)) is not None:
            global_hfi_circuit_breakers_rate_limit.set_rate_limited(workspace_id)
        return get_error_response(err.response_text, err.status_code)
    except ClientDisconnect:
        t_exception = timeit.default_timer()
        elapsed_time = round((t_exception - t_0) * 1000, 3)
        workspace_id = context.workspace_id.get("unknown")
        table_id = context.table_id.get(None)
        if not table_id:
            table_id = request.query_params.get("name", "unknown")
        logging.info(
            f"Client disconnected. workspace_id: {workspace_id}. ds: {table_id}. Elapsed time: {elapsed_time}ms."
        )
        return get_error_response("", 499)  # 499 is what nginx returns for Client disconnected
    except Exception as e:
        error = f"Unhandled exception {e}.\nTraceback: {traceback.format_exc()}"
        logging.exception(error)
        return get_error_response(error, DEFAULT_HTTP_ERROR)


async def hfi_impl(request: Request, default_request_origin: str = OriginType.EVENTS) -> Response:
    token = get_token_from_params_or_header(request)
    secret = hfi_settings["jwt_secret"]
    if token is None:
        raise APIError(403, "Invalid token\n")
    try:
        token_decoded = global_hfi_token_cache.get(token)
        if token_decoded is None:
            token_decoded = token_decode(token, secret)
            global_hfi_token_cache[token] = token_decoded
        elif isinstance(token_decoded, Exception):
            raise token_decoded
    except Exception as err:
        global_hfi_token_cache[token] = err
        raise APIError(403, "Invalid token\n")
    workspace_id = token_decoded["u"]
    context.workspace_id.set(workspace_id)

    # The `tb_semver` parameter is used to specify the release version to use. This is for the Versions feature
    semver = request.query_params.get("__tb__semver", None)

    if global_hfi_circuit_breakers_rate_limit.is_rate_limited(workspace_id):
        return get_error_response(RATE_LIMIT_MSG, RATE_LIMIT_HTTP_CODE)

    global concurrent_active_requests, concurrent_wait_requests
    ds_name = request.query_params.get("name", None)
    format = request.query_params.get("format", "ndjson")
    if ds_name is None or not ds_name.strip():
        raise APIError(400, "Missing 'name' parameter\n")

    ds_name = ds_name.strip()
    request_origin, request_id = get_request_origin_and_id(request, default_request_origin)
    wait = request.query_params.get("wait", "false").lower() == "true" or request_origin == OriginType.KINESIS

    # Support AWS SNS
    # https://docs.aws.amazon.com/sns/latest/dg/SendMessageToHttp.prepare.html
    if request.headers.get("x-amz-sns-message-type", "") == "SubscriptionConfirmation":
        subscription_confirmation_msg = await request.json()
        logging.info(f"Received AWS SNS Subscription Confirmation request {subscription_confirmation_msg}")
        subscribe_url = subscription_confirmation_msg["SubscribeURL"]
        if hfi_settings.get("allow_unsafe_sns", False) is False:
            url = urlparse(subscribe_url)
            if url.scheme != "https" or not url.hostname.endswith(".amazonaws.com"):
                logging.error(f"Invalid unsafe URL: {subscribe_url}")
                return PlainTextResponse("", 400)
        async with get_shared_session().request("GET", url=subscribe_url) as resp:
            result = await resp.content.read()
            if resp.status >= 400:
                logging.error(
                    f"AWS SNS Subscription Confirmation request failed {resp.status} {result.decode('utf-8', 'replace')}"
                )
                return PlainTextResponse("", 400)
            else:
                logging.info(
                    f"AWS SNS Subscription Confirmation request success {resp.status} {result.decode('utf-8', 'replace')}"
                )
        return PlainTextResponse("", 200)

    context.origin.set(request_origin)
    context.request_id.set(request_id)
    context.wait_parameter.set(wait)

    sem_t0 = time.monotonic()
    semaphore = await hfi_acquire_semaphore(request, workspace_id, ds_name)
    statsd_client.timing(
        f"tinybird-hfi.semaphore_wait_time.{statsd_client.region_machine}.{workspace_id}.{ds_name}",
        time.monotonic() - sem_t0,
    )
    try:
        request_stream = RequestStreamWithLookup(request)
        now = time.monotonic()
        config = await get_hfi_config_with_cache(workspace_id, ds_name, request_stream, now, token, semver)

        response_headers = {}

        if config["error"]:
            # logging.warning(f"Error while getting config: {str(config['error'])}")
            if isinstance(config["error"], APIError):
                raise APIError(config["error"].status_code, config["error"].response_text)
            if isinstance(config["error"], AnalyzeError):
                raise APIError(
                    400,
                    "Analysis error, invalid data. We could not infer the schema, please create the datasource manually and try again or contact us at support@tinybird.co.",
                )
            if isinstance(config["error"], DatasourceLimitReached):
                raise APIError(400, str(config["error"]))
            if isinstance(config["error"], DatasourceCreationError):
                raise APIError(400, str(config["error"]))
            if "There is already a" in str(config["error"]):
                raise APIError(400, str(config["error"]))
            if isinstance(config["error"], LockTimeoutError):
                raise config["error"]
            if isinstance(config["error"], UnsupportedType):
                raise config["error"]
            raise Exception(str(config["error"]))
        if token not in config["valid_tokens"]:
            raise APIError(403, "Invalid token\n")
        if not config["extended_json_deserialization"]:
            raise APIError(400, "Data Source must be of type JSON\n")
        sample_iterations = ceil(config["sample_iterations"] / 2)

        if config["sample_iterations"] > 0:
            config["sample_iterations"] = floor(config["sample_iterations"] / 2)

        context.table_id.set(config["table_id"])
        # Let's refresh the id of the workspace in the context in case it was changed by the semver
        if config.get("workspace") is not None:
            context.workspace_id.set(config["workspace"].id)

        async with config["limits_lock"]:
            # Concurrent requests while 'limits_tokens' is depleted
            # should wait to the first one making the Redis request
            if config["limits_tokens"] == 0:
                if now - config["limits_rate_limited_timestamp"] < 0.05:
                    # Avoid HF requests to Redis while rate-limiting
                    raise APIError(RATE_LIMIT_HTTP_CODE, RATE_LIMIT_MSG)
                t0_throttle = time.monotonic()
                try:
                    throttle_task = async_redis.execute_command(
                        "CL.THROTTLE",
                        f"rl:hfi:{workspace_id}",
                        str(config["limits_burst"]),
                        str(config["limits_pace"]),
                        "1",
                        str(RATE_LIMITS_TOKENS_PER_REQUEST),
                    )

                    limited, limit, remaining, retry, reset = await asyncio.wait_for(throttle_task, REDIS_TIMEOUT)
                    config["limit"] = limit
                    config["remaining"] = remaining
                    config["retry"] = retry
                    config["reset"] = reset
                except Exception:
                    t_throttle = time.monotonic() - t0_throttle
                    statsd_client.timing(
                        f"tinybird-hfi.throttle_time.{statsd_client.region_machine}.{workspace_id}", t_throttle
                    )
                    limited = 0

                if limited:
                    config["limits_rate_limited_timestamp"] = now

                    response_headers["X-RateLimit-Limit"] = str(config.get("limit", 0))
                    response_headers["X-RateLimit-Remaining"] = str(
                        config.get("remaining", 0) + config["limits_tokens"]
                    )
                    response_headers["X-RateLimit-Reset"] = str(config.get("reset", 0))
                    response_headers["Retry-After"] = str(config.get("retry", 0))
                    raise APIError(RATE_LIMIT_HTTP_CODE, RATE_LIMIT_MSG)

                config["limits_tokens"] = RATE_LIMITS_TOKENS_PER_REQUEST
                config["limits_rate_limited_timestamp"] = 0

            config["limits_tokens"] -= 1

            response_headers["X-RateLimit-Limit"] = str(config.get("limit", 0))
            response_headers["X-RateLimit-Remaining"] = str(config.get("remaining", 0) + config["limits_tokens"])
            response_headers["X-RateLimit-Reset"] = str(config.get("reset", 0))

        config["performed_requests"] += 1

        hfi_frequency = (
            config["hfi_frequency"]
            if config["hfi_frequency"] is not None
            else hfi_settings["ch_ingestion_tokens_per_second_default"]
        )
        context.hfi_frequency.set(hfi_frequency)

        hfi_frequency_gatherer = (
            config["hfi_frequency_gatherer"]
            if config["hfi_frequency_gatherer"] is not None
            else hfi_settings["ch_ingestion_tokens_per_second_gatherer_default"]
        )
        context.hfi_frequency_gatherer.set(hfi_frequency_gatherer)

        context.workspace.set(config["workspace"])
        context.engine.set(config["datasource_engine"])
        concurrency_limit = config["hfi_concurrency_limit"]
        semaphore_timeout = config["hfi_concurrency_timeout"]
        max_request_mb = config["hfi_max_request_mb"]

        content_length = int(request.headers.get("Content-Length", 0))
        if content_length > max_request_mb * MB:
            # temporary warning, should be changed to HTTP 413 soon: https://gitlab.com/tinybird/analytics/-/issues/9723
            content_mb = int(content_length / MB)
            description = f"{config['workspace'].id}.{config['table_id']} {content_mb} MB"
            logging.warning(f"Max request size {max_request_mb} MB exceeded for {description}, limit not enforced")

        if semaphore and concurrency_limit > 0:
            check_replace_semaphore(workspace_id, ds_name, concurrency_limit, semaphore_timeout)

        # We use the timing stat to send a throughput to benefit from the metrics and usability of it. We can't use a counter or a gauge for this
        statsd_client.timing(
            f"tinybird-hfi.content_length.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
            content_length,
        )
        circuit_breaker_id = get_circuit_breaker_id(config["workspace"].id, config["table_id"])
        global_hfi_circuit_breakers.check(circuit_breaker_id)

        json_importer = NDJSONIngester(
            extended_json_deserialization=config["extended_json_deserialization"],
            database_server=config["database_server"],
            database=config["database"],
            workspace_id=workspace_id,
            datasource_id=config["table_id"],
            format=format,
            pusher="hfi",
            sample_iterations=sample_iterations,
            sampler_sampling_rate=0.2,
            block_tracker=DummyBlockLogTracker(),
            max_import_size=max_request_mb * MB,
            token_id=token_decoded.get("id") if token_decoded else None,
        )
        try:
            concurrent_active_requests[config["table_id"]] = concurrent_active_requests.get(config["table_id"], 0) + 1
            statsd_client.gauge(
                f"tinybird-hfi.concurrent_active_requests.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
                concurrent_active_requests.get(config["table_id"], 0),
            )

            work_time: float = 0
            first_chunk = True
            before_download = time.monotonic()
            _bytes = 0
            async for chunk in request_stream:
                json_importer.write(chunk)
                _bytes += len(chunk)
                before_work = time.monotonic()
                if await json_importer.work() is not None and first_chunk:
                    first_chunk = False
                    # We use the timing stat to send a throughput to benefit from the metrics and usability of it. We can't use a counter or a gauge for this
                    statsd_client.timing(
                        f"tinybird-hfi.receive_throughput.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
                        _bytes / max(before_work - before_download, 0.001),
                    )
                work_time += time.monotonic() - before_work

            if first_chunk:
                # We use the timing stat to send metrics to benefit from the usability of it: aggregates and percentiles. We can't use a counter or a gauge for this
                statsd_client.timing(
                    f"tinybird-hfi.receive_throughput.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
                    _bytes / max(time.monotonic() - before_download, 0.001),
                )

            before_finish = time.monotonic()
            await json_importer.finish()
            work_time += time.monotonic() - before_finish
            statsd_client.timing(
                f"tinybird-hfi.work_time.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
                work_time,
            )
        finally:
            concurrent_active_requests[config["table_id"]] = concurrent_active_requests.get(config["table_id"], 1) - 1
    finally:
        if semaphore is not None:
            semaphore.release()

    async def wait_and_log(ch):
        error = await ch.wait_for_flush_task
        if error:
            log_point = HFILogPoint(
                workspace_id=workspace_id,
                datasource_id=config["table_id"],
                successful_rows=json_importer.successful_rows,
                quarantined_rows=json_importer.quarantined_rows,
                datasource_name=config["datasource_name"],
                channel=ch,
                channel_state="ended",
                error=str(error),
                gatherer=ch.use_gatherer,
            )
            hfi_log(log_point)
            if not wait:
                # Nobody listening for it, don't raise
                return
            # Workaround for Python's bug https://bugs.python.org/issue45924
            # See related duplicated issue https://bugs.python.org/issue46954
            # We shouldn't re-raise the exception here to avoid the bug in Python
            raise CHErrorPythonWorkaround(
                error.message, error.is_materialized_view, error.code, error.data_not_ingested
            )
        log_point = HFILogPoint(
            workspace_id=workspace_id,
            datasource_id=config["table_id"],
            successful_rows=json_importer.successful_rows,
            quarantined_rows=json_importer.quarantined_rows,
            datasource_name=config["datasource_name"],
            channel=ch,
            channel_state="ended",
            error=None,
            gatherer=ch.use_gatherer,
        )
        hfi_log(log_point)

    if wait:
        try:
            concurrent_wait_requests[config["table_id"]] = concurrent_wait_requests.get(config["table_id"], 0) + 1
            statsd_client.gauge(
                f"tinybird-hfi.concurrent_wait_requests.{statsd_client.region_machine}.{context.workspace_id.get('unknown')}.{context.table_id.get('unknown')}.{context.origin.get('unknown')}",
                concurrent_wait_requests.get(config["table_id"], 0),
            )

            for _ch_type, ch in json_importer._pusher._channels:  # type: ignore
                await wait_and_log(ch)
        finally:
            concurrent_wait_requests[config["table_id"]] = concurrent_wait_requests.get(config["table_id"], 1) - 1
    else:
        for ch_type, ch in json_importer._pusher._channels:  # type: ignore
            if ch_type == "new":
                workaround_orphan_task(asyncio.create_task(wait_and_log(ch)))
            else:
                log_point = HFILogPoint(
                    workspace_id=workspace_id,
                    datasource_id=config["table_id"],
                    successful_rows=json_importer.successful_rows,
                    quarantined_rows=json_importer.quarantined_rows,
                    datasource_name=config["datasource_name"],
                    channel=ch,
                    channel_state="ongoing",
                    error=None,
                    gatherer=ch.use_gatherer,
                )
                hfi_log(log_point)

    disconnected = await request.is_disconnected()
    if disconnected:
        raise ClientDisconnect()

    response_http_code = 200 if wait else 202

    return get_response(
        origin=request_origin,
        http_code=response_http_code,
        request_id=request_id,
        successful_rows=json_importer.successful_rows,
        quarantined_rows=json_importer.quarantined_rows,
        headers=response_headers,
    )


class Base64StreamDecoder:
    def __init__(self):
        self._acc = None

    def decode(self, chunk: bytes) -> bytes:
        # base64 encoders usually put a newline every 72 characters
        # ignore them
        chunk = chunk.replace(b"\n", b"")

        # base64 encoding encodes 3 bytes in 4 characters
        # if we receive a chunk with length non a multiple of 4
        # we need to cut the ending bytes, and accumulate them for
        # next chunks
        if self._acc:
            chunk = self._acc + chunk
            self._acc = None
        extra = len(chunk) % 4
        if extra != 0:
            offset = len(chunk) - extra
            self._acc = chunk[offset:]
            chunk = chunk[:offset]
        return base64.decodebytes(chunk)

    def flush(self) -> bytes:
        if self._acc:
            # base64.decodebytes decoder requires padding characters
            # we add them here if necessary
            # https://datatracker.ietf.org/doc/html/rfc4648.html#section-4
            b = base64.decodebytes((self._acc + b"==")[:4])
            self._acc = None
            return b
        return b""


class RequestStreamWithLookup:
    def __init__(self, request: Request):
        self._request = request
        self._request_stream = request.stream()
        self._lookup_buffer = BytesIO()
        self._decompressor: Optional[zlib._Decompress] = None
        self._first_chunk = True
        self._base64: Optional[Base64StreamDecoder] = None

    def _process_chunk(self, chunk: bytes) -> bytes:
        if self._first_chunk:
            self._first_chunk = False
            if "gzip" in self._request.headers.get("Content-Encoding", "") or has_gzip_magic_code(chunk):
                self._decompressor = zlib.decompressobj(wbits=16 + 15)
            elif has_gzip_base64_magic_code(chunk):
                self._base64 = Base64StreamDecoder()
                self._decompressor = zlib.decompressobj(wbits=16 + 15)
        if self._base64:
            chunk = self._base64.decode(chunk)
        if self._decompressor:
            chunk = self._decompressor.decompress(chunk)
        return chunk

    def _flush(self) -> bytes:
        if self._base64:
            chunk = self._base64.flush()
            self._base64 = None
            if self._decompressor:
                chunk1 = self._decompressor.decompress(chunk)
                chunk2 = self._decompressor.flush()
                self._decompressor = None
                return chunk1 + chunk2
            raise UnexpectedHFICondition(
                "Unexpected exception. Base64 is only supported in combination with gzip decompression"
            )
        elif self._decompressor:
            chunk = self._decompressor.flush()
            self._decompressor = None
            return chunk
        else:
            return b""

    async def lookup(self, lookup_size=INITIAL_LOOKUP_SIZE) -> bytes:
        async for chunk in self._request_stream:
            chunk = self._process_chunk(chunk)
            self._lookup_buffer.write(chunk)
            if self._lookup_buffer.tell() >= lookup_size:
                return self._lookup_buffer.getvalue()
        chunk = self._flush()
        self._lookup_buffer.write(chunk)
        return self._lookup_buffer.getvalue()

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._lookup_buffer.tell() > 0:
            chunk = self._lookup_buffer.getvalue()
            self._lookup_buffer.seek(0)
            self._lookup_buffer.truncate()
            return chunk
        try:
            chunk = await self._request_stream.__anext__()
            chunk = self._process_chunk(chunk)
            return chunk
        except StopAsyncIteration:
            # StopAsyncIteration is raised by self._request_stream.__anext__()
            # when there are no more chunks in the request stream
            # we still may have to flush base64/gzip buffers though
            chunk = self._flush()
            if chunk:
                return chunk
            raise


async def get_config_from_redis_and_fill_cache(
    workspace_id: str,
    ds_name: str,
    request_stream: RequestStreamWithLookup,
    workspace_hfi_cache: Dict[str, HfiConfig],
    last_successful_config: Optional[Dict[str, Any]],
    token: str,
    semver: Optional[str] = None,
) -> Dict[str, Any]:
    now = time.monotonic()
    config_task = get_hfi_config_from_redis(workspace_id, ds_name, request_stream, token, semver)
    workspace_hfi_cache[ds_name] = HfiConfig(config_task, last_successful_config)
    new_config = await config_task

    if not new_config["error"]:
        workspace_hfi_cache[ds_name] = HfiConfig(config_task, new_config)

    elapsed_read_config = time.monotonic() - now
    statsd_client.timing(
        f"tinybird-hfi.read_config_time.{statsd_client.region_machine}.{workspace_id}.{ds_name}", elapsed_read_config
    )

    return new_config


async def get_hfi_config_with_cache(
    workspace_id: str,
    ds_name: str,
    request_stream: RequestStreamWithLookup,
    now: float,
    token: str,
    semver: Optional[str] = None,
) -> Dict[str, Any]:
    global global_hfi_cache

    # In case of semver, we need to use the workspace_id of the release. So, create a cache key with the semver
    cache_key = f"{workspace_id}.{semver}" if semver else workspace_id
    workspace_hfi_cache = global_hfi_cache.get(cache_key, None)

    cached_config_task: Optional[asyncio.Task[Dict[str, Any]]] = None
    last_successful_config: Optional[Dict[str, Any]] = None

    if workspace_hfi_cache is None:
        workspace_hfi_cache = {}
        global_hfi_cache[cache_key] = workspace_hfi_cache
    else:
        cached_config_task, last_successful_config = workspace_hfi_cache.get(ds_name, HfiConfig(None, None))

    if cached_config_task is None:
        return await get_config_from_redis_and_fill_cache(
            workspace_id, ds_name, request_stream, workspace_hfi_cache, last_successful_config, token, semver
        )

    config = await cached_config_task

    if (not config["error"] and config["timestamp"] < (now - HFI_CACHE_DURATION)) or (
        config["error"] and config["timestamp"] < (now - HFI_CACHE_RETRY_DURATION_ON_ERROR)
    ):
        config = await get_config_from_redis_and_fill_cache(
            workspace_id, ds_name, request_stream, workspace_hfi_cache, last_successful_config, token, semver
        )

    if (
        config["error"]
        and last_successful_config
        and last_successful_config["timestamp"] > (now - HFI_CACHE_DURATION_ON_ERROR)
    ):
        return last_successful_config

    return config


def get_hfi_config_from_redis(
    workspace_id: str,
    ds_name: str,
    request_stream: RequestStreamWithLookup,
    raw_token: str,
    semver: Optional[str] = None,
) -> asyncio.Task:
    async def get_config_async(raw_token: str, workspace_id: str) -> Dict[str, Any]:
        workspace: Optional[User] = await sync_to_async(User.get_by_id)(workspace_id)

        if workspace is None:
            token_attrs: Dict[str, Any] = token_decode_unverify(raw_token)
            token_region = token_attrs.get("host")
            current_region = hfi_settings.get("tb_region") or os.environ.get("TB_REGION")

            msg: str
            if not token_region:
                # Legacy tokens don't have the host attribute
                msg = "Invalid token. Verify you are making the request to the correct region. You can find the valid regions at https://www.tinybird.co/docs/api-reference/api-reference.html."
            elif token_region == current_region:
                # We're in the same region as the token, so probably the
                # token was removed/is invalid, but let's not say that to
                # the user
                msg = "Invalid token. Verify you are using the correct token for this region. Please, refer to https://www.tinybird.co/docs/api-reference/api-reference.html for more info."
            else:
                # We're in a different region than the token. Let's give
                # a hint to the user
                if current_region:
                    msg = f"You made a request to the {current_region} region, but the provided token belongs to the {token_region} region."
                else:
                    msg = f"The provided token belongs to the {token_region} region."

                token_region_info: Dict[str, Any] = hfi_settings.get("all_regions", {}).get(token_region, {})
                url: Optional[str] = token_region_info.get("api_host") or token_region_info.get("host")
                if url:
                    msg += f" You should make your requests to {url}."
            raise APIError(404, msg)

        if not workspace.is_active:
            msg = "Workspace not found"
            raise APIError(404, msg)

        if semver is not None:
            release = workspace.get_release_by_semver(semver)
            if not release:
                raise APIError(404, f"Release {semver} not found in workspace {workspace.name}.")
            release_metadata = release.metadata
            if not release_metadata:
                raise APIError(404, f"Release {semver} not found in workspace {workspace.name}.")

            workspace = release_metadata
            workspace_id = workspace.id

        # Let's do the read-only check only for "master" workspaces with the FF enabled
        if not workspace.origin:
            # Try to identify the user (if any) of this token
            # to check if it has write permissions.
            access_tok = next(
                (t for t in workspace.get_tokens() if t.token == raw_token and t.has_scope(scopes.ADMIN_USER)),
                None,
            )
            if access_tok:
                user_id: Optional[str] = next((r for r in access_tok.get_resources_for_scope(scopes.ADMIN_USER)), None)
                if user_id:
                    user: Optional[UserAccount] = UserAccount.get_by_id(user_id)
                    if user is not None and not UserWorkspaceRelationship.user_can_write(
                        user_id=user_id, workspace_id=workspace.id
                    ):
                        raise APIError(
                            403,
                            "Invalid token for HFI append. You have the Viewer role. Please contact your Workspace administrator.",
                        )

        datasource = workspace.get_datasource(ds_name)
        if datasource is None:
            token_obj = next((token_obj for token_obj in workspace.tokens if token_obj.token == raw_token), None)
            if token_obj is None:
                raise APIError(403, "Invalid token\n")
            elif not token_obj.may_create_ds(ds_name):
                raise APIError(403, "Invalid token for DS autocreation\n")

            async with distributed_lock(workspace_id, acquire_timeout=ACQUIRE_LOCK_TIMEOUT):
                # Re-check to ensure DS was not created before acquiring the lock
                workspace = await sync_to_async(User.get_by_id)(workspace_id)
                if not workspace:
                    raise APIError(404, "Workspace not found")

                datasource = workspace.get_datasource(ds_name)
                if datasource is None:
                    schema, json_conf = await analyze_request_stream(request_stream)
                    datasource = await create_datasource(workspace, ds_name, schema, json_conf)

        valid_tokens = [token.token for token in workspace.tokens if token.may_append_ds(datasource.id)]
        database = workspace["database"]
        database_server = workspace["hfi_database_server"] or workspace["database_server"]
        hfi_concurrency_limit = (
            workspace["hfi_concurrency_limit"]
            if hasattr(workspace, "hfi_concurrency_limit") and workspace["hfi_concurrency_limit"]
            else DEFAULT_HFI_SEMAPHORE_COUNTER
        )
        hfi_concurrency_timeout = (
            workspace["hfi_concurrency_timeout"]
            if hasattr(workspace, "hfi_concurrency_timeout") and workspace["hfi_concurrency_timeout"]
            else DEFAULT_HFI_SEMAPHORE_TIMEOUT
        )
        hfi_max_request_mb = (
            workspace["hfi_max_request_mb"]
            if hasattr(workspace, "hfi_max_request_mb") and workspace["hfi_max_request_mb"]
            else DEFAULT_HFI_MAX_REQUEST_MB
        )
        table_id = datasource.id
        if datasource.json_deserialization:
            extended_json_deserialization = extend_json_deserialization(datasource.json_deserialization)
        else:
            # Data Source is not of type JSON
            extended_json_deserialization = None
        limits_pace = DEFAULT_HFI_RATE_LIMIT_PACE
        limits_burst = DEFAULT_HFI_RATE_LIMIT_BURST
        custom_limits = workspace["limits"].get("api_datasources_hfi", None)
        if custom_limits:
            limits_pace = int(custom_limits[1] / custom_limits[2])
            limits_burst = int(custom_limits[3])
        config = {
            "timestamp": time.monotonic(),
            "valid_tokens": valid_tokens,
            "extended_json_deserialization": extended_json_deserialization,
            "database_server": database_server,
            "database": database,
            "table_id": table_id,
            "datasource_name": datasource.name,
            "datasource_engine": datasource.engine.get("engine", None),
            "sample_iterations": HFI_SAMPLING_BUCKET,
            "performed_requests": 0,
            "limits_pace": limits_pace,
            "limits_burst": limits_burst,
            "limits_tokens": 0,
            "limits_rate_limited_timestamp": 0,
            "error": None,
            "hfi_frequency": workspace.hfi_frequency,
            "hfi_frequency_gatherer": workspace.hfi_frequency_gatherer,
            "workspace": workspace,
            "hfi_concurrency_limit": hfi_concurrency_limit,
            "hfi_concurrency_timeout": hfi_concurrency_timeout,
            "hfi_max_request_mb": hfi_max_request_mb,
        }
        config["limits_lock"] = asyncio.Lock()
        return config

    return asyncio.create_task(exception_workaround(get_config_async(raw_token, workspace_id)))


# Workaround for Python's bug https://bugs.python.org/issue45924
# See related duplicated issue https://bugs.python.org/issue46954
async def exception_workaround(async_iofuture) -> Any:
    def _return_error(e):
        return {
            "timestamp": time.monotonic(),
            "error": e,
        }

    try:
        return await async_iofuture
    except (
        APIError,
        ResourceAlreadyExists,
        AnalyzeError,
        DatasourceLimitReached,
        LockTimeoutError,
        UnsupportedType,
    ) as e:
        return _return_error(e)
    except Exception as e:
        logging.exception(f"exception_on_return_value: {e}\nTraceback: {traceback.format_exc()}")
        return _return_error(e)


async def analyze_request_stream(request_stream: RequestStreamWithLookup) -> Tuple[Any, Any]:
    lookup_size = INITIAL_LOOKUP_SIZE
    max_lookup_size = DEFAULT_HFI_MAX_REQUEST_MB * MB
    schema = None
    json_conf = None
    while not schema and not json_conf and lookup_size <= max_lookup_size:
        try:
            lookup = await request_stream.lookup(lookup_size)
            schema, json_conf = await hfi_analyze(lookup)
        except AnalyzeError as e:
            if lookup_size < max_lookup_size:
                lookup_size *= 2
                if lookup_size > max_lookup_size:
                    lookup_size = max_lookup_size
            else:
                raise e

    return schema, json_conf


async def hfi_analyze(data) -> Tuple[Any, List[Dict[str, Any]]]:
    lines = split_ndjson(data)
    rows = []
    for line in lines:
        try:
            rows.append(orjson.loads(line))
        except orjson.JSONDecodeError:
            pass
    analysis = await analyze(rows)
    if not analysis:
        raise AnalyzeError("NDJSON couldn't be analyzed")
    if not analysis["columns"]:
        raise AnalyzeError("No valid columns were found")
    augmented_schema = analysis["schema"]
    parsed_schema = parse_augmented_schema(augmented_schema)
    schema = parsed_schema.schema
    jsonpaths = parsed_schema.jsonpaths
    json_conf = json_deserialize_merge_schema_jsonpaths(parse_table_structure(schema), jsonpaths)
    return analysis["schema"], json_conf


def get_token_from_params_or_header(request) -> Optional[str]:
    token = request.query_params.get("token", None)
    if not token:
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            auth_header_parts = auth_header.split(" ")
            if auth_header_parts and len(auth_header_parts) == 2 and auth_header_parts[0] == "Bearer":
                token = auth_header_parts[1]
    return token


def has_gzip_base64_magic_code(chunk) -> bool:
    try:
        return base64.decodebytes(chunk[:4])[: len(GZIP_MAGIC_CODE)] == GZIP_MAGIC_CODE
    except Exception:
        return False


def get_semaphore_id(workspace_id: str, ds_name: str) -> str:
    return workspace_id + ds_name


def create_semaphore(semaphore_id: str, concurrency_limit: int, timeout: int) -> asyncio.Semaphore:
    semaphore = asyncio.Semaphore(concurrency_limit)
    global_hfi_semaphore[semaphore_id] = SemaphoreData(semaphore, concurrency_limit, timeout)
    return semaphore


def check_replace_semaphore(workspace_id: str, ds_name: str, new_concurrency_limit: int, new_timeout: int) -> None:
    semaphore_id = get_semaphore_id(workspace_id, ds_name)
    cached_semaphore = global_hfi_semaphore.get(semaphore_id)
    if not cached_semaphore:
        create_semaphore(semaphore_id, new_concurrency_limit, new_timeout)
        return
    semaphore, prev_concurrency_limit, prev_timeout = cached_semaphore
    if new_concurrency_limit != prev_concurrency_limit:
        create_semaphore(semaphore_id, new_concurrency_limit, new_timeout)
    elif new_timeout != prev_timeout:
        global_hfi_semaphore[semaphore_id] = SemaphoreData(semaphore, prev_concurrency_limit, new_timeout)


async def hfi_acquire_semaphore(request: Request, workspace_id: str, ds_name: str) -> Optional[asyncio.Semaphore]:
    # Smallish requests shouldn't be limited by the semaphore
    try:
        content_length = request.headers["Content-Length"]
        if int(content_length) < HFI_SEMAPHORE_MINIMUM_CHECK_SIZE:
            return None
    except Exception:
        pass

    semaphore_id = get_semaphore_id(workspace_id, ds_name)
    semaphore_data = global_hfi_semaphore.get(semaphore_id)

    if semaphore_data is None:
        timeout = DEFAULT_HFI_SEMAPHORE_TIMEOUT
        semaphore = create_semaphore(semaphore_id, DEFAULT_HFI_SEMAPHORE_COUNTER, timeout)
    else:
        semaphore, _, timeout = semaphore_data

    try:
        await asyncio.wait_for(semaphore.acquire(), timeout)
    except asyncio.TimeoutError:
        semaphore = None  # type: ignore
        statsd_client.incr(f"tinybird-hfi.semaphore_timeout.{statsd_client.region_machine}.{workspace_id}.{ds_name}", 1)
        raise APIError(503, "Service temporarily unavailable, no data ingested, please retry again\n")
    return semaphore


def ping(request: Request) -> Response:
    return PlainTextResponse("ok", 200)


def get_request_origin_and_id(request: Request, default_request_origin: str = OriginType.EVENTS) -> Tuple[str, str]:
    if id := request.headers.get("x-amz-sns-message-id"):
        return (OriginType.SNS, id)
    elif id := request.headers.get("X-Amz-Firehose-Request-Id"):
        return (OriginType.KINESIS, id)
    return (default_request_origin, "")


def conf_sentry(conf):
    sentry_conf = conf.get("sentry")
    if sentry_conf and sentry_conf.get("hfi_dsn"):
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )
        # Get release version
        try:
            from . import revision  # type: ignore[attr-defined]

            release = revision
        except ImportError:
            logging.warning("Release tag not found")
            release = "unknown_release"

        def traces_sampler(sampling_context):
            return float(sentry_conf.get("traces_sample_rate", 0))

        sentry_sdk.init(
            sentry_conf.get("hfi_dsn"),
            environment=sentry_conf.get("environment"),
            release=release,
            traces_sampler=traces_sampler,
            integrations=[sentry_logging, StarletteIntegration(), RedisIntegration(), AioHttpIntegration()],
        )


async def startup():
    global lag_monitor
    logging.warning("HFI app startup initiated")

    conf_sentry(hfi_settings)

    redis_config = get_redis_config(hfi_settings)
    redis_client = TBRedisClientSync(redis_config)
    redis_replica_client = TBRedisReplicaClientSync(redis_config)
    secrets_key = ""  # Used only in pipes for now
    User.config(redis_client, hfi_settings["jwt_secret"], replace_executor=None, secrets_key=secrets_key)
    RedisModel.config(redis_client)
    RedisModel.config_replica(redis_replica_client)
    async_redis.init(redis_config)
    hfi_settings["app_name"] = hfi_settings.get("app_name", "hfi")
    statsd_client.init(hfi_settings)
    lag_monitor = LagMonitor()
    await lag_monitor.init(LAG_MONITOR_THRESHOLD_IN_SECS)
    datasources_ops_log_delay = hfi_settings.get(
        "datasources_ops_log_delay", DatasourceOpsTrackerRegistry.DEFAULT_DELAY
    )
    DatasourceOpsTrackerRegistry.create(
        datasources_ops_log_delay,
        sleep_time=hfi_settings.get("datasources_ops_log_sleep_time", 4.0),
        monitoring_context="tinybird-hfi",
    )
    logging.warning("HFI app startup finished")


async def shutdown():
    global lag_monitor
    logging.warning("HFI app shutdown initiated")
    await force_flush_ch_multiplexer()
    if lag_monitor:
        logging.warning("HFI: stopping lag monitor")
        await lag_monitor.stop()
    logging.warning("HFI: stopping datasourceops tracker registry")
    DatasourceOpsTrackerRegistry.stop(5.0)
    client = Hub.current.client
    if client is not None:
        logging.warning("HFI: closing hub current client")
        client.close(timeout=2.0)
    logging.warning("HFI app shutdown finished")


routes = [
    Route("/v0/events", endpoint=hfi, methods=["POST"]),
    Route("/ping", endpoint=ping, methods=["GET"]),
]

middleware = [Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"], allow_headers=["*"])]

app = Starlette(debug=False, routes=routes, middleware=middleware, on_startup=[startup], on_shutdown=[shutdown])
