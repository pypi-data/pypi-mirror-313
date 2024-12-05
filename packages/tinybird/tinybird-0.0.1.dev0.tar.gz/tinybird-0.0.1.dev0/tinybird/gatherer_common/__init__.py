import base64
import hashlib
import logging
from typing import Dict, Optional

from tinybird.ch import ch_table_details, ch_table_schema
from tinybird.sql import schema_to_sql_columns
from tinybird_shared.gatherer_settings import (
    GathererFlushConfiguration,
    build_table_comment,
    get_gatherer_config_hash,
    get_limit_flush_interval_ds_key,
)

SAFE_TAG = "safe"
UNSAFE_TAG = "unsafe"

GATHERER_KAFKA_SOURCE_TAG = "kafka"
GATHERER_DYNAMODBSTREAMS_SOURCE_TAG = "dynamodbstreams"
GATHERER_HFI_SOURCE_TAG = "hfi"
GATHERER_JOB_PROCESSOR_SOURCE_TAG = "job_processor"


def get_gatherer_config_from_workspace(workspace, ds_id: Optional[str] = None) -> Optional[GathererFlushConfiguration]:
    if not workspace:
        return None

    # Can't import User globally because it causes a circular dependency with data_connectors.py
    from tinybird.user import User

    assert isinstance(workspace, User)

    if (
        ds_id is not None
        and (flush_interval_ds := workspace.limits.get(get_limit_flush_interval_ds_key(ds_id), None)) is not None
    ):
        _, gatherer_flush_interval = flush_interval_ds
    else:
        gatherer_flush_interval = workspace.gatherer_flush_interval

    ws_gatherer_limits = workspace.get_limits(prefix="gatherer_ch")
    if (
        gatherer_flush_interval is not None
        or workspace.gatherer_deduplication is not None
        or (ws_gatherer_limits and len(ws_gatherer_limits) > 0)
    ):
        return GathererFlushConfiguration(gatherer_flush_interval, workspace.gatherer_deduplication, ws_gatherer_limits)

    return None


def render_gatherer_table_name(
    url: str,
    database: str,
    table: str,
    columns: list[str],
    columns_types: list[str],
    source: str,
    safety: str,
    gatherer_config: Optional[GathererFlushConfiguration] = None,
    additional_content_for_hash: Optional[str] = None,
) -> str:
    """
    >>> table_name = render_gatherer_table_name("http://aws-split-us-east-split:6081", "d_d3926a",
    ...    "t_09fd9ef81ce940ad9a099a8762213bea", ["first", "second"], ["str", "int"], "kafka", "safe",  None)
    >>> decoded = base64.b64decode(table_name).decode("utf-8").split("\\0")
    >>> len(decoded)
    7
    >>> decoded[1]
    'http://aws-split-us-east-split:6081'
    >>> decoded[6]
    'safe'
    """
    # Poor-man's check since we don't have mypy yet in HFI
    if type(columns) is not list or type(columns_types) is not list:
        raise RuntimeError(
            f"Cannot render a table name with columns ({type(columns)}) or columns_types ({type(columns_types)}) that are not a list"
        )

    if len(columns) != len(columns_types):
        logging.warning(
            f"Cannot render a table name  for {database}.{table} with different length in columns ({len(columns)}) and columns types ({len(columns_types)}). Columns: {', '.join(columns)}. Types: {', '.join(columns_types)}"
        )

    if url[-1] == "/":
        url = url[:-1]

    columns_and_types = ", ".join(columns + columns_types)
    config_hash = get_gatherer_config_hash(gatherer_config)
    content_to_hash = columns_and_types + "-" + config_hash
    if additional_content_for_hash is not None:
        content_to_hash += "-" + additional_content_for_hash
    content_hash = hashlib.sha256(content_to_hash.encode("utf-8")).hexdigest()[:8]
    decoded_table_name = "\0".join(["v0", url, database, table, content_hash, source, safety])

    return base64.b64encode(decoded_table_name.encode("utf-8")).decode("ascii")


def _build_order_by(sorting_key):
    """
    >>> _build_order_by(None)
    '(tuple())'
    >>> _build_order_by("tuple()")
    '(tuple())'
    >>> _build_order_by("")
    '(tuple())'
    >>> _build_order_by(" ")
    '(tuple())'
    >>> _build_order_by("a")
    '(a)'
    >>> _build_order_by(" a ")
    '(a)'
    >>> _build_order_by("a, b")
    '(a, b)'
    >>> _build_order_by(" a, b ")
    '(a, b)'
    >>> _build_order_by("tuple(a), tuple(b)")
    '(tuple(a), tuple(b))'
    >>> _build_order_by("(a, b)")
    '((a, b))'
    """
    if not sorting_key or not (sorting_key := sorting_key.strip()):
        sorting_key = "tuple()"

    return f"({sorting_key})"


def compose_gatherer_table_create_request_params(
    gatherer_database: str,
    gatherer_table: str,
    dest_url: str,
    dest_database: str,
    dest_table: str,
    gatherer_ch_config: Optional[GathererFlushConfiguration] = None,
    extra_comment: Optional[Dict[str, str]] = None,
) -> dict[str, str]:
    schema = ch_table_schema(dest_table, dest_url, dest_database)
    assert schema is not None
    columns_with_types = ", ".join(schema_to_sql_columns(schema))

    table_info = ch_table_details(dest_table, dest_url, dest_database)
    assert table_info.details is not None

    query_segments = [
        f"CREATE TABLE IF NOT EXISTS `{gatherer_database}`.`{gatherer_table}`",
        f"({columns_with_types})",
        "ENGINE = MergeTree()",
        f"ORDER BY {_build_order_by(table_info.sorting_key)}",
    ]
    if table_info.partition_key:
        query_segments.append(f"PARTITION BY {table_info.partition_key}")

    query_segments.append(
        "SETTINGS max_bytes_to_merge_at_max_space_in_pool = 0, max_bytes_to_merge_at_min_space_in_pool = 0"
    )

    comment = build_table_comment(
        destination_url=dest_url,
        destination_database=dest_database,
        destination_table_name=dest_table,
        gatherer_ch_config=gatherer_ch_config,
        extra_comment=extra_comment,
    )

    query_segments.append(f"COMMENT '{comment}'")

    request = {
        "database": gatherer_database,
        "query": " ".join(query_segments),
    }

    return request
