import hashlib
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

import orjson

GB = 1024**3

DEFAULT_PUSH_QUERY_SETTINGS = [
    ("max_insert_block_size", 200_000_000, "rows"),
    ("min_insert_block_size_rows", 100_000_000, "rows"),
    ("min_insert_block_size_bytes", 1_000_000_000, "bytes"),
    ("max_threads", 32, "threads"),
    ("optimize_on_insert", False, "bool"),
    ("max_block_size", 2_000_000, "rows"),
    ("preferred_block_size_bytes", 2_000_000_000, "bytes"),
    ("insert_deduplicate", 0, "bool"),
]

OPTIONAL_PUSH_QUERY_SETTINGS = [("max_memory_usage", 16 * GB, "bytes")]

MANDATORY_PUSH_QUERY_SETTINGS = {"max_insert_threads": 1}

GATHERERS_DISCOVERY_KEY: str = "gatherers:discovery"
GATHERERS_DISCOVERY_TTL: int = 3  # in seconds
GATHERERS_DISCOVERY_FAILOVER_TTL: int = 10  # to use when Redis fails over
GATHERERS_BANDWIDTH_TOP_N: int = 5  # store bandwidth for top5

SETTINGS_CONFIG = "config"
SETTINGS_RETRY_STATUS = "retry_status"
SETTINGS_FLUSH_INTERVAL = "flush_interval"
SETTINGS_CH_LIMITS = "ch_limits"

PREFIX_FLUSH_INTERVAL_DS = "flush_time_"


def get_limit_flush_interval_ds_key(ds_id):
    return f"{PREFIX_FLUSH_INTERVAL_DS}{ds_id}"


class GathererDefaults:
    USE_GATHERER = True
    ALLOW_GATHERER_FALLBACK = False
    ALLOW_S3_BACKUP_ON_USER_ERRORS = True
    FLUSH_INTERVAL = 4
    DEDUPLICATION = None  # None defers the decision to the Gatherer, True/False forces the value for the workspace


@dataclass(frozen=False)
class RetryStatus:
    block_id: str = field(default_factory=lambda: str(uuid.uuid4().hex))
    last_query_id: Optional[str] = None
    last_error: int = -1
    retry_count: int = 0
    last_error_epoch: int = 0
    last_error_timestamp: int = 0
    initial_error_timestamp: int = 0
    retry_wait: int = 0


@dataclass(frozen=True)
class GathererFlushConfiguration:
    flush_interval: Optional[float]
    deduplication: Optional[bool]
    ch_limits: Optional[dict[str, Any]]


def get_gatherer_config_hash(config: Optional[GathererFlushConfiguration]) -> str:
    key = b"{}" if config is None else orjson.dumps(asdict(config))
    return hashlib.sha256(key).hexdigest()[:8]


def build_extra_info(destination_url: str, destination_database: str, destination_table_name: str) -> dict[str, Any]:
    return {
        "url": destination_url,
        "database": destination_database,
        "table": destination_table_name,
    }


def build_settings_from_partition_data(
    extra_info: dict[str, Any], config: Optional[GathererFlushConfiguration], retry_status: Optional[RetryStatus]
) -> dict[str, Any]:
    settings = extra_info.copy() if extra_info else {}
    if config:
        settings[SETTINGS_CONFIG] = asdict(config)
    if retry_status:
        settings[SETTINGS_RETRY_STATUS] = asdict(retry_status)

    return settings


def build_table_comment(
    destination_url: str,
    destination_database: str,
    destination_table_name: str,
    gatherer_ch_config: Optional[GathererFlushConfiguration],
    retry_status: Optional[RetryStatus] = None,
    extra_comment: Optional[Dict[str, str]] = None,
) -> str:
    extra_info = build_extra_info(destination_url, destination_database, destination_table_name)
    if extra_comment:
        extra_info.update(extra_comment)
    return build_comment_from_partition_data(extra_info, gatherer_ch_config, retry_status)


def build_comment_from_partition_data(
    extra_info: dict[str, Any], config: Optional[GathererFlushConfiguration], retry_status: Optional[RetryStatus]
) -> str:
    settings = build_settings_from_partition_data(extra_info, config, retry_status)

    return orjson.dumps(settings).decode("utf-8")


def parse_configuration_from_comment(metadata: dict[str, Any]) -> Optional[GathererFlushConfiguration]:
    try:
        configuration = metadata.get("config", {})
        flush_interval = configuration.get("flush_interval", None)
        deduplication = configuration.get("deduplication", None)
        ch_limits = configuration.get("ch_limits", None)
        if flush_interval is None and deduplication is None and ch_limits is None:
            return None
        return GathererFlushConfiguration(
            flush_interval=flush_interval, ch_limits=ch_limits, deduplication=deduplication
        )
    except Exception:
        return None


def parse_retry_status_from_comment(metadata: dict[str, Any]) -> Optional[RetryStatus]:
    if not metadata:
        retry_status_dict = None
    else:
        try:
            retry_status_dict = metadata.get(SETTINGS_RETRY_STATUS, None)
        except Exception:
            retry_status_dict = None
    return RetryStatus(**retry_status_dict) if retry_status_dict else RetryStatus()


def parse_extra_info_from_comment(metadata: dict[str, Any], url: str, database: str, table: str) -> dict[str, Any]:
    if not metadata:
        return build_extra_info(url, database, table)

    known_keys = {SETTINGS_CONFIG, SETTINGS_RETRY_STATUS}
    return {key: value for key, value in metadata.items() if key not in known_keys}
