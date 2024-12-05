import logging
import math
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Callable, List, Optional, Tuple

from tinybird.constants import BillingPlans
from tinybird.views.api_errors.datasources import ClientErrorEntityTooLarge
from tinybird_shared.redis_client.redis_client import async_redis

MB = 1024**2
GB = 1024**3
SECONDS = 1
HOURS = 3600

MAX_SIZE_URL_FILE = 32
MAX_SIZE_URL_PARQUET_FILE = 5
MAX_SIZE_URL_FILE_DEV = 10
MAX_SIZE_URL_PARQUET_FILE_DEV = 1
MAX_SIZE_URL_FILE_UNITS = "GB"
MAX_SIZE_URL_FILE_BYTES = MAX_SIZE_URL_FILE * GB
MAX_SIZE_URL_FILE_DEV_BYTES = MAX_SIZE_URL_FILE_DEV * GB
MAX_SIZE_URL_PARQUET_FILE_BYTES = MAX_SIZE_URL_PARQUET_FILE * GB
MAX_SIZE_URL_PARQUET_FILE_DEV_BYTES = MAX_SIZE_URL_PARQUET_FILE_DEV * GB
DEFAULT_MAX_POPULATE_JOB_TTL_IN_HOURS = 48
DEFAULT_MAX_COPY_JOB_TTL_IN_HOURS = 48
DEFAULT_MAX_SINK_JOB_TTL_IN_HOURS = 48
DEFAULT_MAX_IMPORT_JOB_TTL_IN_HOURS = 48
DEFAULT_CDK_VERSION = "v0.17"


class FileSizeException(Exception):
    pass


def get_url_file_size_checker(
    ws_file_size_limit: Optional[int], ws_plan: str, ws_name: str, ds_name: Optional[str], is_parquet: bool = False
) -> Callable[[int], None]:
    def f(file_size: int) -> None:
        if ws_file_size_limit is None:
            max_size_url_file_bytes, max_size_url_file_dev_bytes = (
                (MAX_SIZE_URL_PARQUET_FILE_BYTES, MAX_SIZE_URL_PARQUET_FILE_DEV_BYTES)
                if is_parquet
                else (MAX_SIZE_URL_FILE_BYTES, MAX_SIZE_URL_FILE_DEV_BYTES)
            )
            file_size_limit = (
                max_size_url_file_dev_bytes
                if ws_plan == BillingPlans.DEV or ws_plan is None
                else max_size_url_file_bytes
            )
        else:
            file_size_limit = ws_file_size_limit
        if file_size >= file_size_limit:
            max_file_size_gb = f"{(file_size_limit / GB):.2f}"
            error = ClientErrorEntityTooLarge.entity_too_large_url(
                file_size=f"{(file_size / GB):.2f}",
                file_size_unit="GB",
                max_import_url=max_file_size_gb,
                max_import_url_unit=MAX_SIZE_URL_FILE_UNITS,
            )
            ds_name_msg = f".{ds_name}" if ds_name else ""
            logging.warning(f"Import file too big in {ws_name}{ds_name_msg}: {error.message}")
            raise FileSizeException(error.message)

    return f


class RateLimitConfig:
    def __init__(
        self,
        key,
        count_per_period: int,
        period: int,
        max_burst: int = 0,
        quantity: int = 1,
        msg_error: Optional[str] = None,
        documentation: Optional[str] = None,
    ):
        self.key = key
        self.max_burst = max_burst
        self.count_per_period = count_per_period
        self.period = period
        self.quantity = quantity
        self.msg_error = "Too many requests: retry after {retry} seconds" if msg_error is None else msg_error
        self.documentation = "/api-reference/api-reference.html#limits" if documentation is None else documentation

    def __str__(self):
        return f"""rl:{self.key} burst={self.max_burst} count={self.count_per_period} period={self.period} quantity={self.quantity}"""


class PlanRateLimitConfig(RateLimitConfig):
    """
    >>> drl_config = PlanRateLimitConfig('foo', BillingPlans.DEV, 10, 3, 1)
    >>> drl_config.key == f'foo_{datetime.now().strftime("%Y%m%d")}'
    True
    >>> 0 < drl_config.period < 3600* 24
    True
    """

    def __init__(self, key_base: str, plan: str, count_per_period: int, max_burst: int = 0, quantity: int = 1):
        self.key_base = key_base
        self.plan = plan
        super().__init__(
            None,
            count_per_period,
            None,  # type: ignore
            max_burst,
            quantity,
            msg_error="Too many requests: {workspace_name} quota exceeded. Learn more {workspace_settings_url}",
        )

    @property
    def key(self):
        t_now = datetime.now()
        return f"{self.key_base}_{t_now.strftime('%Y%m%d')}"

    @key.setter
    def key(self, value):
        pass

    @property
    def period(self):
        t_now = datetime.now()
        tomorrow = t_now + timedelta(days=1)
        remaining_daily_period = datetime.combine(tomorrow, time.min) - t_now
        return int(remaining_daily_period.total_seconds())

    @period.setter
    def period(self, value):
        pass

    def is_applicable(self, workspace, from_ui):
        return not from_ui and workspace.plan == self.plan


@dataclass
class EndpointLimit:
    name: str
    default_value: int


class EndpointLimits:
    max_concurrent_queries = EndpointLimit("max_concurrent_queries", 0)
    max_threads = EndpointLimit("max_threads", 0)
    analyzer = EndpointLimit("analyzer", 0)
    backend_hint = EndpointLimit("backend_hint", 0)
    max_rps = EndpointLimit("max_rps", 20)
    max_bytes_before_external_group_by = EndpointLimit("max_bytes_before_external_group_by", 0)

    @staticmethod
    def get_all_settings() -> List[EndpointLimit]:
        return [
            EndpointLimits.max_concurrent_queries,
            EndpointLimits.max_threads,
            EndpointLimits.analyzer,
            EndpointLimits.backend_hint,
            EndpointLimits.max_rps,
            EndpointLimits.max_bytes_before_external_group_by,
        ]

    @staticmethod
    def prefix() -> str:
        return "endpoint_limit"

    @staticmethod
    def get_limit_key(endpoint: str, limit: EndpointLimit) -> str:
        return f"{EndpointLimits.prefix()}_{endpoint}_{limit.name}"


class Limit:
    ch_max_execution_time = 10 * SECONDS
    ch_max_estimated_execution_time = 0 * SECONDS
    ch_timeout_before_checking_execution_speed = 0 * SECONDS
    ch_max_threads = 0
    ch_max_insert_threads = 2
    ch_max_result_bytes = 100 * MB
    ch_max_memory_usage = 16 * GB
    ch_chunk_max_execution_time = 30 * SECONDS
    ch_max_mutations_seconds_to_wait = 360
    ch_lock_acquire_timeout = 120 * SECONDS
    ch_max_execution_time_replace_partitions = 30 * SECONDS
    ch_max_wait_for_replication_seconds = 180 * SECONDS
    # This limits will be used for all the DDL operations (CREATE, ALTER, DROP, etc)
    ch_ddl_max_execution_time = 30 * SECONDS
    api_datasources_create_append_replace = RateLimitConfig("api_datasources_create_append_replace", 5, 60, max_burst=3)
    api_datasources_create_schema = RateLimitConfig("api_datasources_create_schema", 25, 60, max_burst=25)
    api_datasources_list = RateLimitConfig("api_datasources_list", 10, 1, max_burst=10)
    api_datasources_hfi = RateLimitConfig("api_datasources_hfi", 1000, 1, max_burst=2000)
    build_plan_api_requests = PlanRateLimitConfig("build_plan_api_requests", BillingPlans.DEV, 1000, max_burst=1000)
    workspace_api_requests = RateLimitConfig(
        "workspace_api_requests", 1000, 1, max_burst=1000
    )  # Only applied when overriden Only applied when overriden
    api_branches_create = RateLimitConfig("api_branches_create", 2, 60, max_burst=1)
    api_branches_data = RateLimitConfig("api_branches_data", 2, 60, max_burst=2)
    api_branches_delete = RateLimitConfig("api_branches_delete", 3, 60, max_burst=3)
    api_variables = RateLimitConfig("api_variables", 5, 1, max_burst=5)
    api_variables_list = RateLimitConfig("api_variables", 60, 60, max_burst=60)
    api_connectors_list = RateLimitConfig("api_connectors_list", 20, 60, max_burst=10)
    api_connectors_create = RateLimitConfig("api_connectors_create", 5, 60, max_burst=5)
    api_connectors_preview = RateLimitConfig("api_connectors_preview", 20, 60, max_burst=10)
    api_workspace_users_invite = RateLimitConfig("api_workspace_users_invite", 15, 60, max_burst=1)
    materialize_performance_validation_limit = 2000
    materialize_performance_validation_seconds = 1
    materialize_performance_validation_threads = 2
    max_seats = 90
    max_workspaces = 90
    max_owned = 90
    kafka_max_topics = 5
    requests_connect_timeout = 3600
    requests_bytes_between_timeout = 3600
    pg_connect_timeout = 10
    pg_statement_timeout = 10000
    copy_join_algorithm = "auto"
    copy_max_bytes_before_external_group_by = 1442450940  # Coming from: clickhouse/steps/clickhouse.yaml
    copy_max_memory_usage = 0 * GB  # it won't be applied if it's 0
    copy_max_threads_query_limit_per_replica = 128
    copy_max_job_ttl_in_hours = DEFAULT_MAX_COPY_JOB_TTL_IN_HOURS

    # same as above
    branchcopy_max_bytes_before_external_group_by = 1442450940
    branchcopy_max_memory_usage = 0 * GB
    branchcopy_max_threads_query_limit_per_replica = 128
    branchcopy_max_job_ttl_in_hours = DEFAULT_MAX_COPY_JOB_TTL_IN_HOURS

    iterating_max_branches = 3
    iterating_attach_max_part_size = 50 * 1000000000  # 50 GB
    iterating_attach_parts_batch_number = 0  # 0 means no batch limit
    iterating_creation_concurrency = 10
    import_max_url_file_size_dev_gb = MAX_SIZE_URL_FILE_DEV
    import_max_url_file_size_no_dev_gb = MAX_SIZE_URL_FILE
    import_max_url_parquet_file_size_dev_gb = MAX_SIZE_URL_PARQUET_FILE_DEV
    import_max_url_parquet_file_size_no_dev_gb = MAX_SIZE_URL_PARQUET_FILE
    import_parquet_url_max_threads = None
    import_parquet_url_max_insert_threads = None  # We use ch_max_insert_threads by default on parquet url
    import_parquet_url_max_insert_block_size = None
    import_parquet_url_min_insert_block_size_rows = None
    import_parquet_url_min_insert_block_size_bytes = None
    import_parquet_url_max_memory_usage = None
    import_parquet_url_max_execution_time = 600
    import_parquet_url_input_format_parquet_max_block_size = None
    import_parquet_url_input_format_parquet_allow_missing_columns = 1
    import_parquet_url_input_format_null_as_default = 1
    import_parquet_url_max_partitions_per_insert_block = 12
    import_parquet_url_insert_deduplicate = 0
    import_parquet_url_date_time_overflow_behavior = "saturate"
    import_parquet_url_enable_url_encoding = 0
    import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference = 0
    import_csv_bytes_to_fetch = 1024 * 20
    import_max_job_ttl_in_hours = DEFAULT_MAX_IMPORT_JOB_TTL_IN_HOURS
    sinks_max_insert_delayed_streams_for_parallel_write = 1000
    sinks_max_bytes_before_external_group_by = 1442450940  # Coming from: clickhouse/steps/clickhouse.yaml
    sinks_max_bytes_before_external_sort = 10 * GB
    sinks_output_format_parallel_fomatting = 0
    sinks_render_internal_compression_in_binary_formats = 1
    sinks_output_format_parquet_string_as_string = 0
    sinks_max_job_ttl_in_hours = DEFAULT_MAX_SINK_JOB_TTL_IN_HOURS

    populate_max_threads = None
    populate_max_insert_threads = None  # We use ch_max_insert_threads by default on populates
    populate_move_parts_max_execution_time = None
    populate_max_insert_block_size = 1_048_449
    populate_min_insert_block_size_rows = None
    populate_min_insert_block_size_bytes = None
    populate_preferred_block_size_bytes = None
    populate_max_memory_usage = (
        None  # populate_max_memory_usage_percentage has prevalence over populate_max_memory_usage
    )
    populate_max_memory_usage_percentage = 0.5
    populate_max_estimated_execution_time = 0 * SECONDS
    populate_timeout_before_checking_execution_speed = 0 * SECONDS
    populate_min_memory_threshold = None
    populate_max_memory_threshold = None
    populate_min_cpu_threshold = None
    populate_max_cpu_threshold = None
    max_datasources = 100
    populate_max_concurrent_queries = None
    populate_max_job_ttl_in_hours = DEFAULT_MAX_POPULATE_JOB_TTL_IN_HOURS
    max_tokens = 100000
    gatherer_ch_max_insert_block_size = 200_000_000
    gatherer_ch_min_insert_block_size_rows = 100_000_000
    gatherer_ch_min_insert_block_size_bytes = 1_000_000_000
    gatherer_ch_max_threads = 32
    # Disable max_insert_threads until this issue gets clarified: https://github.com/ClickHouse/ClickHouse/issues/60746
    # gatherer_ch_max_insert_threads = 1
    gatherer_ch_optimize_on_insert = False
    gatherer_ch_max_block_size = 2_000_000
    gatherer_ch_preferred_block_size_bytes = 2_000_000_000
    gatherer_ch_insert_deduplicate = 0
    gatherer_multiwriter_enabled = False
    gatherer_multiwriter_type = "random"  # use hint to use backend-hint
    gatherer_multiwriter_tables = ""  # comma separated list of ids
    gatherer_multiwriter_tables_excluded = ""  # comma separated list of ids
    gatherer_multiwriter_hint_backend_ws = ""  # The name of the Varnish backend to use for the whole Workspace
    gatherer_multiwriter_hint_backend_tables = (
        ""  # A string "table1:backend1,table2:backend2" representing the Varnish backends to use for each table
    )

    release_max_number_of_total_releases = 5
    release_max_number_of_rollback_releases = 3
    release_max_number_of_preview_releases = 1
    release_max_number_of_total_releases_in_branches = 5
    cdk_version = DEFAULT_CDK_VERSION

    @classmethod
    def set_max_datasources(cls, limit: Optional[int]):
        if limit is not None:
            cls.max_datasources = limit


class Limits:
    disable_rate_limits = False

    @classmethod
    def config(cls, disable_rate_limits=False):
        cls.disable_rate_limits = disable_rate_limits

    @classmethod
    async def rate_limit(cls, config: RateLimitConfig) -> Tuple[int, int, int, int, int]:
        """
        >>> import asyncio
        >>> from tinybird_shared.redis_client.redis_client import async_redis
        >>> from tinybird_shared.redis_client.redis_client import TBRedisConfig
        >>> from tinybird.limits import Limits, RateLimitConfig
        >>> import uuid
        >>> async_redis.init(TBRedisConfig())
        >>> key=str(uuid.uuid4().hex)
        >>> rl_config = RateLimitConfig(f"foo_{key}", 10, 10, 10)
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (0, 11, 10, -1, 2)
        >>> Limits.config()
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (0, 11, 9, -1, 2)
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (0, 11, 8, -1, 3)
        >>> rl_config = RateLimitConfig(f"bar_{key}", 2, 1)
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (0, 1, 0, -1, 1)
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (1, 1, 0, 1, 1)
        >>> asyncio.run(Limits.rate_limit(rl_config))
        (1, 1, 0, 1, 1)

        """

        try:
            [limited, limit, remaining, retry, reset] = await async_redis.execute_command(
                "CL.THROTTLE",
                f"rl:{config.key}",
                config.max_burst,
                config.count_per_period,
                config.period,
                config.quantity,
            )

            # Please, remove the following adjustments when
            #
            #     https://github.com/brandur/redis-cell/issues/56
            #
            # gets fixed.
            if limited:
                retry += 1
            reset += 1

            if cls.disable_rate_limits:
                return 0, limit, remaining, retry, reset
            return limited, limit, remaining, retry, reset
        except Exception as e:
            logging.exception(f"Could not retrieve rate limit for key={config.key}. Reason: {e}")
            limited, limit, remaining, retry, reset = (
                0,
                config.max_burst + 1,
                config.count_per_period,
                -1,
                math.ceil(config.period / config.count_per_period),
            )
            return limited, limit, remaining, retry, reset

    @staticmethod
    def max_threads(
        workspace: Optional[float],
        endpoint_cheriff: Optional[int],
        request: Optional[int],
        template: Optional[int],
    ) -> Optional[int]:
        """Determines how many threads to use based on the user config, HTTP request, and template.
        Rules:
        - None or Zero values are ignored and considered as unlimited in ClickHouse = number of physical CPU cores.
        - Priorities:
            1. If the limit at workspace level is defined, it's the upper limit for max_threads and it is the default value used.
            2. And in case request, template and cheriff is defined, it will be selected in that order

        >>> Limits.max_threads(None, None, None, None)
        >>> Limits.max_threads(0, 0, 0, 0)
        >>> Limits.max_threads(0, 0, 6, 10)
        6
        >>> Limits.max_threads(0, 0, 0, 10)
        10
        >>> Limits.max_threads(None, None, None, 10)
        10
        >>> Limits.max_threads(2, 0, 6, 10)
        2
        >>> Limits.max_threads(20, 0, 6, 10)
        6
        >>> Limits.max_threads(20, 0, 0, 10)
        10
        >>> Limits.max_threads(20, 0, None, 10)
        10
        >>> Limits.max_threads(20, 0, None, None)
        20
        >>> Limits.max_threads(20, None, None, 0)
        20
        >>> Limits.max_threads(None, 0, 10, 6)
        10
        >>> Limits.max_threads(20, 0, 6, 1)
        6
        >>> Limits.max_threads(20, None, 6, 1)
        6
        >>> Limits.max_threads(None, 2, 6, 1)
        6
        >>> Limits.max_threads(None, 2, 0, 0)
        2
        >>> Limits.max_threads(3, 2, 0, 0)
        2
        """
        workspace = workspace or float("inf")
        request_or_template = request or template or endpoint_cheriff or float("inf")

        _max_threads = min(workspace, request_or_template)
        if _max_threads == float("inf"):
            return None

        return int(_max_threads)
