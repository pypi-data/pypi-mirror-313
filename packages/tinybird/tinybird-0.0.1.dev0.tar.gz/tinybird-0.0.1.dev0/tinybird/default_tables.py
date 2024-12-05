# flake8: noqa: E501
from dataclasses import dataclass, field
from typing import List, Optional

from tinybird.feature_flags import FeatureFlagWorkspaces


@dataclass
class DefaultTable:
    """
    Attributes:
        ...
        fixed_name  if True, the table's redis_id = datasource_name. Otherwise, redis_id will be a random string
                    prefixed by the object type. Redis_id matches the name of the table in ClickHouse.
        ...
    """

    name: str
    schema: str
    engine: Optional[str] = None
    migrations: List[List[str]] = field(default_factory=lambda: [])
    fixed_name: bool = False
    engine_template: Optional[str] = None


@dataclass
class DefaultView:
    """
    Attributes:
        ...
        fixed_name  if True, the view's redis_id = datasource_name. Otherwise, redis_id will be a random string
                    prefixed by the object type. Redis_id matches the name of the view in ClickHouse.
        ...
    """

    name: str
    table: str
    query_template: str
    fixed_name: bool = False
    engine: Optional[str] = None
    populate_view: bool = True
    datasource_name: Optional[str] = None


DEFAULT_TABLES = [
    # kafka_ops_log:
    # new_messages: new messages available at Kafka
    # processed_messages: messages processed, committed or not
    # processed_bytes: bytes processed, commited or not
    # committed_messages:
    # time_read: time spent in polling Kafka
    # time_process: time spent in processing messages
    # time_write: time spent in pushing messages to TB
    # msg:
    # msg_internal: errors that we don't want to show users
    DefaultTable(
        "kafka_ops_log",
        """timestamp DateTime,
         agent LowCardinality(String),
         user_id LowCardinality(String),
         datasource_id LowCardinality(String),
         topic LowCardinality(String),
         partition Int16,
         msg_type LowCardinality(String),
         lag Int64,
         new_messages Int32,
         processed_messages Int32,
         processed_bytes Int32,
         committed_messages Int32,
         time_read Float32,
         time_process Float32,
         time_write Float32,
         msg String,
         msg_internal String
         """,
        "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY",
        fixed_name=True,
    ),
    DefaultTable(
        "data_guess",
        """
         user_id LowCardinality(String),
         datasource_id LowCardinality(String),
         timestamp DateTime,

         path LowCardinality(String),
         type LowCardinality(String),
         num Float64,
         str String
         """,
        "MergeTree() ORDER BY (user_id, datasource_id, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 1 DAY",
        [
            [
                "MODIFY COLUMN IF EXISTS num Float64",
            ]
        ],
        fixed_name=True,
    ),
]


DEFAULT_METRICS_CLUSTER_TABLES = [
    DefaultTable(
        "bi_connector_log",
        """
        start_datetime DateTime,
        query_id String,
        database String,
        host String,
        query String,
        query_normalized String,
        exception_code Int32,
        exception String,
        duration UInt64,
        read_rows UInt64,
        read_bytes UInt64,
        result_rows UInt64,
        result_bytes UInt64,
        databases Array(LowCardinality(String)),
        tables Array(LowCardinality(String)),
        columns Array(LowCardinality(String)),
        projections Array(LowCardinality(String)),
        views Array(LowCardinality(String))
    """,
        engine="""MergeTree() ORDER BY (database, cityHash64(query_normalized), start_datetime) TTL start_datetime + INTERVAL 7 DAY""",
        fixed_name=True,
    ),
    DefaultTable(
        "bi_connector_stats",
        """
        date Date,
        database String,
        query_normalized String,
        view_count UInt64,
        error_count UInt64,
        avg_duration_state AggregateFunction(avg, Float32),
        quantile_timing_state AggregateFunction(quantilesTiming(0.9, 0.95, 0.99), Float64),
        read_bytes_sum UInt64,
        read_rows_sum UInt64,
        avg_result_rows_state AggregateFunction(avg, Float32),
        avg_result_bytes_state  AggregateFunction(avg, Float32)""",
        engine="""SummingMergeTree() ORDER BY (database, cityHash64(query_normalized), date) PARTITION BY toYYYYMM(date)""",
        fixed_name=True,
    ),
    DefaultTable(
        "materializations_log",
        """
        event_time DateTime,
        host String,
        initial_query_id String,
        view_name String,
        view_target String,
        view_duration_ms UInt64,
        read_rows UInt64,
        read_bytes UInt64,
        written_rows UInt64,
        written_bytes UInt64,
        peak_memory_usage Int64,
        exception_code Int32,
        exception String""",
        engine="""MergeTree() ORDER BY (initial_query_id, event_time) TTL event_time + INTERVAL 8 HOUR""",
        fixed_name=True,
    ),
    DefaultTable(
        "processed_usage_log",
        """
        date Date,
        database String,
        host String,
        version String,
        user_agent LowCardinality(String),
        read_bytes UInt64,
        written_bytes UInt64,
        __inserted_at AggregateFunction(max, DateTime64(6))""",
        engine="""SummingMergeTree() PARTITION BY toYYYYMM(date) ORDER BY (database, user_agent, host, version, date)""",
        fixed_name=True,
    ),
    DefaultTable(
        "billing_processed_usage_log",
        """
        date Date,
        database String,
        read_bytes UInt64,
        written_bytes UInt64,
        __inserted_at AggregateFunction(max, DateTime64(6))""",
        engine="""SummingMergeTree() PARTITION BY toYYYYMM(date) ORDER BY (database, date)""",
        fixed_name=True,
    ),
]

DEFAULT_METRICS_CLUSTER_VIEWS = [
    DefaultView(
        name="billing_processed_usage_log_view",
        table="billing_processed_usage_log",
        query_template="""
            SELECT
                date as date,
                database as database,
                sum(if((version < '22' AND user_agent != 'tb-materialization') OR (version >= '22' AND user_agent IN ('tb-materialization', 'tb-api-query', 'tb-postgres', 'tb-karman-query', 'tb-delete-condition', 'tb-copy-query', 'tb-datasink-query')), read_bytes, 0)) as read_bytes,
                sum(if(user_agent NOT IN ('tb-materialization', 'tb-datasink-query'), written_bytes, 0)) as written_bytes,
                maxState(now64(6)) __inserted_at
            FROM {metrics_database}.processed_usage_log
            WHERE
                startsWith(user_agent, 'tb')
                AND user_agent NOT IN ('tb-internal-query', 'tb-ui-query')
            GROUP BY database, date
        """,
        fixed_name=True,
    ),
    DefaultView(
        name="bi_connector_stats_view",
        table="bi_connector_stats",
        query_template="""
            SELECT
                toDate(start_datetime) date,
                database,
                query_normalized,
                count() view_count,
                countIf(exception_code > 0 or notEmpty(exception)) error_count,
                avgState(toFloat32(duration)) avg_duration_state,
                quantilesTimingState(0.9, 0.95, 0.99) (toFloat64(duration)) quantile_timing_state,
                sum(read_bytes) read_bytes_sum,
                sum(read_rows) read_rows_sum,
                avgState(toFloat32(result_rows)) avg_result_rows_state,
                avgState(toFloat32(result_bytes)) avg_result_bytes_state
            FROM {metrics_database}.bi_connector_log
            GROUP BY database, query_normalized, date
        """,
        populate_view=False,
    ),
    DefaultView(
        name="billing_bi_connector_log_view",
        table="billing_processed_usage_log",
        query_template="""
        SELECT
            date,
            database,
            sum(read_bytes) as read_bytes,
            0 as written_bytes,
            maxState(now64(6)) __inserted_at
        FROM {metrics_database}.bi_connector_log
        WHERE start_datetime > toDateTime('2022-11-30 23:59:59')
        GROUP BY toDate(start_datetime) as date, database
    """,
        fixed_name=True,
    ),
]

DEFAULT_METRICS_TABLES = [
    DefaultTable(
        "distributed_bi_connector_log",
        """
        start_datetime DateTime,
        query_id String,
        host String,
        database String,
        query String,
        query_normalized String,
        exception_code Int32,
        exception String,
        duration UInt64,
        read_rows UInt64,
        read_bytes UInt64,
        result_rows UInt64,
        result_bytes UInt64,
        databases Array(LowCardinality(String)),
        tables Array(LowCardinality(String)),
        columns Array(LowCardinality(String)),
        projections Array(LowCardinality(String)),
        views Array(LowCardinality(String))
    """,
        engine_template="Distributed('{cluster}', '{database}', 'bi_connector_log', rand())",
        fixed_name=True,
    ),
    DefaultTable(
        "distributed_bi_connector_stats",
        """
        date Date,
        database String,
        query_normalized String,
        view_count UInt64,
        error_count UInt64,
        avg_duration_state AggregateFunction(avg, Float32),
        quantile_timing_state AggregateFunction(quantilesTiming(0.9, 0.95, 0.99), Float64),
        read_bytes_sum UInt64,
        read_rows_sum UInt64,
        avg_result_rows_state AggregateFunction(avg, Float32),
        avg_result_bytes_state  AggregateFunction(avg, Float32)""",
        engine_template="Distributed('{cluster}', '{database}', 'bi_connector_stats', rand())",
        fixed_name=True,
    ),
    DefaultTable(
        "distributed_materializations_log",
        """
        event_time DateTime,
        host String,
        initial_query_id String,
        view_name String,
        view_target String,
        view_duration_ms UInt64,
        read_rows UInt64,
        read_bytes UInt64,
        written_rows UInt64,
        written_bytes UInt64,
        peak_memory_usage Int64,
        exception_code Int32,
        exception String
    """,
        engine_template="Distributed('{cluster}', '{database}', 'materializations_log', rand())",
        fixed_name=True,
    ),
    DefaultTable(
        "distributed_processed_usage_log",
        """
        date Date,
        database String,
        host String,
        version String,
        user_agent LowCardinality(String),
        read_bytes UInt64,
        written_bytes UInt64,
        __inserted_at AggregateFunction(max, DateTime64(6))""",
        engine_template="Distributed('{cluster}', '{database}', 'processed_usage_log', rand())",
        fixed_name=True,
    ),
    DefaultTable(
        "distributed_billing_processed_usage_log",
        """
        date Date,
        database String,
        read_bytes UInt64,
        written_bytes UInt64,
        __inserted_at AggregateFunction(max, DateTime64(6))""",
        engine_template="Distributed('{cluster}', '{database}', 'billing_processed_usage_log', rand())",
        fixed_name=True,
    ),
]

DEFAULT_METRICS_VIEWS = [
    DefaultView(
        name="bi_connector_log_view",
        table="distributed_bi_connector_log",
        query_template="""
        SELECT
            event_time_microseconds as start_datetime,
            current_database as database,
            query_id as query_id,
            hostName() as host,
            query as query,
            normalizeQuery(query) as query_normalized,
            exception_code as exception_code,
            exception as exception,
            query_duration_ms as duration,
            read_bytes as read_bytes,
            read_rows as read_rows,
            result_bytes as result_bytes,
            result_rows as result_rows,
            databases as databases,
            tables as tables,
            columns as columns,
            projections as projections,
            views as views
        FROM system.query_log
        WHERE
            type > 1
            AND current_database not in ('default', 'system')
            AND http_user_agent = 'postgres'
""",
        fixed_name=True,
    ),
    DefaultView(
        name="materializations_log_view",
        table="distributed_materializations_log",
        query_template="""
            SELECT
                event_time,
                hostName() as host,
                initial_query_id,
                view_name,
                view_target,
                view_duration_ms,
                read_rows,
                read_bytes,
                written_rows,
                written_bytes,
                peak_memory_usage,
                exception_code,
                exception
            FROM system.query_views_log
            WHERE
                view_type = 2
                AND status > 1
        """,
        fixed_name=True,
    ),
    DefaultView(
        name="processed_usage_log_from_query_log_view",
        table="distributed_processed_usage_log",
        query_template="""
        SELECT
            event_date as date,
            current_database as database,
            hostName() as host,
            version() as version,
            toLowCardinality(http_user_agent) as user_agent,
            sum(read_bytes) as read_bytes,
            sum(written_bytes) as written_bytes,
            maxState(now64(6)) __inserted_at
        FROM system.query_log
        WHERE
            type > 1
            AND current_database not in ('default', 'system')
            AND notEmpty(http_user_agent)
        GROUP BY database, user_agent, host, date
""",
        fixed_name=True,
    ),
    DefaultView(
        name="processed_usage_log_from_query_views_log_view",
        table="distributed_processed_usage_log",
        query_template="""
        SELECT
            event_date as date,
            splitByChar('.', view_name)[1] as database,
            hostName() as host,
            version() as version,
            if(match(splitByChar('.', view_name)[2], '^t_[0-9a-f]*$'), toLowCardinality('tb-materialization'), toLowCardinality('no-tb-internal-materialization')) as user_agent,
            sum(read_bytes) as read_bytes,
            sum(written_bytes) as written_bytes,
            maxState(now64(6)) __inserted_at
        FROM system.query_views_log
        WHERE
            view_type = 2
            AND status > 1
            AND splitByChar('.', view_name)[1] not in ('default', 'system') AND (view_name NOT LIKE '%public.')
        GROUP BY database, user_agent, host, date
""",
        fixed_name=True,
    ),
]


@dataclass
class FeaturedColumns:
    feature_flag: FeatureFlagWorkspaces
    columns: str


def c(*columns: str) -> str:
    return ",".join(columns)
