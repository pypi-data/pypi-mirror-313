from typing import Any, Dict, List

from pydantic import BaseModel

from tinybird.providers.aws.dynamodb import DynamoDBAttributeDefinition


class DynamoDBTableConfiguration(BaseModel):
    dynamodb_table_arn: str
    dynamodb_export_bucket: str


class DynamoDBLinkerConfiguration(DynamoDBTableConfiguration):
    tb_clickhouse_table: str
    tb_datasource: str
    json_deserialization: List[Dict[str, Any]]
    attribute_definitions: list[DynamoDBAttributeDefinition]
    initial_export_arn: str
    dynamodb_export_time: str
    dynamodb_sleep_closed_shards: float = 0.1
    dynamodb_sleep_open_shards: float = 0.1
    dynamodb_max_records_read: float = 1000
    linker_workers: int = 1
    dynamodb_sleep_closed_shard_cursor: float = 0
    dynamodb_sleep_open_shard_cursor: float = 0
    dynamodb_min_time_between_iterations: float = 1.5
    dynamodb_max_shards_read_from_redis: int = 15000


class DynamoDBExportFile(BaseModel):
    dataFileS3Key: str
    itemCount: int
