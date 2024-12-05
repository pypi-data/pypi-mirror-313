import dataclasses
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional

import botocore

from tinybird.integrations.dynamodb.transform import from_dynamodb_to_json_raw
from tinybird.providers.aws.exceptions import (
    MalformedAWSAPIResponse,
    NoSuchDynamoDBTable,
    PITRExportNotAvailable,
    _handle_botocore_client_exception,
)
from tinybird.providers.aws.session import AWSSession
from tinybird_shared.retry.retry import retry_sync

DYNAMODB_MANDATORY_COLUMNS = [
    "`_event_name` LowCardinality(String)",
    "`_timestamp` DateTime64(3)",
    "`_record` String",
    "`_is_deleted` UInt8",
]
DYNAMODB_MANDATORY_COLUMNS_JSONPATHS = [
    "$.eventName",
    "$.ApproximateCreationDateTime",
    "$.NewImage",
    "$._is_deleted",
]
DYNAMODB_OLD_RECORD_COLUMN = "`_old_record` Nullable(String) `json:$.OldImage`"


@dataclasses.dataclass(frozen=True)
class DynamoDBTableKeySchema:
    key_type: str
    attribute_name: str


@dataclasses.dataclass(frozen=True)
class DynamoDBAttributeDefinition:
    name: str
    type: str


@dataclasses.dataclass(frozen=True)
class DynamoDBTable:
    key_schemas: list[DynamoDBTableKeySchema]
    attribute_definitions: list[DynamoDBAttributeDefinition]
    stream_enabled: bool = False
    stream_view_type: str = ""
    table_size_bytes: Optional[int] = None
    table_write_capacity_units: Optional[int] = None

    def get_key_schemas_by_type(self) -> dict[str, DynamoDBTableKeySchema]:
        return {key_schema.key_type: key_schema for key_schema in self.key_schemas}

    def has_streams_enabled(self) -> bool:
        return self.stream_enabled and (
            self.stream_view_type == DynamoDBStreamsType.NEW_AND_OLD_IMAGES
            or self.stream_view_type == DynamoDBStreamsType.NEW_IMAGE
        )


@dataclasses.dataclass(frozen=True)
class DynamoDBExportConfiguration:
    table_arn: str
    export_time: datetime
    bucket: str
    export_type: str = "FULL_EXPORT"


@dataclasses.dataclass(frozen=True)
class DynamoDBExportDescription:
    table_arn: str
    export_arn: str
    export_time: datetime
    bucket: str


@dataclasses.dataclass(frozen=True)
class DynamoDBFinishedExportDescription:
    table_arn: str
    export_arn: str
    export_time: datetime
    bucket: str
    export_status: str
    export_manifest: str
    failure_code: str
    failure_message: str


class DynamoDBStreamsType(StrEnum):
    NEW_IMAGE = "NEW_IMAGE"
    NEW_AND_OLD_IMAGES = "NEW_AND_OLD_IMAGES"


def get_dynamodb_datasource_columns(stream_type: DynamoDBStreamsType, table_schema: str):
    columns = [
        f"{column} `json:{jsonpath}`"
        for column, jsonpath in zip(DYNAMODB_MANDATORY_COLUMNS, DYNAMODB_MANDATORY_COLUMNS_JSONPATHS)
    ]

    if stream_type == DynamoDBStreamsType.NEW_AND_OLD_IMAGES and DYNAMODB_OLD_RECORD_COLUMN not in table_schema:
        columns.insert(-1, DYNAMODB_OLD_RECORD_COLUMN)

    return ", ".join(columns)


@retry_sync(NoSuchDynamoDBTable, tries=2, delay=3)
def describe_table(session: AWSSession, table: str, region: Optional[str] = None) -> DynamoDBTable:
    dynamodb = session.client("dynamodb", region=region)

    try:
        # Table Name can be the table name or the table ARN
        res = dynamodb.describe_table(TableName=table)
    except dynamodb.exceptions.ResourceNotFoundException as err:
        raise NoSuchDynamoDBTable(table) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)

    try:
        table_definition: dict[str, Any] = res["Table"]
        stream_definition: dict[str, Any] = table_definition.get("StreamSpecification", {})

        # Try to get the write capacity units from a provisioned instance
        write_capacity_units = table_definition.get("ProvisionedThroughput", {}).get("WriteCapacityUnits", None)
        if write_capacity_units is None:
            # The table is on-demand, try to get capacity units for this specific case.
            # MaxWriteRequestUnits is optional depending on if the user enforces a threshold. If the threshold is
            # not defined, the throughput is unlimited.
            write_capacity_units = table_definition.get("OnDemandThroughput", {}).get("MaxWriteRequestUnits", None)

        return DynamoDBTable(
            key_schemas=[
                DynamoDBTableKeySchema(attribute_name=key_schema["AttributeName"], key_type=key_schema["KeyType"])
                for key_schema in table_definition["KeySchema"]
            ],
            attribute_definitions=[
                DynamoDBAttributeDefinition(name=attribute.get("AttributeName"), type=attribute.get("AttributeType"))
                for attribute in table_definition["AttributeDefinitions"]
            ],
            stream_enabled=stream_definition.get("StreamEnabled", False),
            stream_view_type=stream_definition.get("StreamViewType", ""),
            table_size_bytes=table_definition.get("TableSizeBytes", None),
            table_write_capacity_units=write_capacity_units,
        )
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def scan_table(session: AWSSession, table: str, region: Optional[str] = None) -> List[Dict[str, Any]]:
    dynamodb = session.client("dynamodb", region=region)

    try:
        res = dynamodb.scan(TableName=table, Limit=20)
    except dynamodb.exceptions.ResourceNotFoundException as err:
        raise NoSuchDynamoDBTable(table) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)

    try:
        # Extract and deserialize the items
        return [from_dynamodb_to_json_raw(item) for item in res["Items"]]
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def export_table_to_point_in_time(
    session: AWSSession, export_configuration: DynamoDBExportConfiguration, region: str
) -> DynamoDBExportDescription:
    dynamodb = session.client("dynamodb", region=region)

    try:
        res = dynamodb.export_table_to_point_in_time(
            TableArn=export_configuration.table_arn,
            ExportTime=export_configuration.export_time,
            S3Bucket=export_configuration.bucket,
            ExportFormat="DYNAMODB_JSON",
        )
    except dynamodb.exceptions.PointInTimeRecoveryUnavailableException as err:
        raise PITRExportNotAvailable(export_configuration.table_arn) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)

    try:
        export: dict[str, Any] = res["ExportDescription"]
        return DynamoDBExportDescription(
            table_arn=export["TableArn"],
            export_arn=export["ExportArn"],
            export_time=export["ExportTime"],
            bucket=export["S3Bucket"],
        )
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def describe_export(session: AWSSession, export_arn: str, region: str) -> DynamoDBFinishedExportDescription:
    dynamodb = session.client("dynamodb", region=region)

    try:
        res = dynamodb.describe_export(ExportArn=export_arn)
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)

    try:
        export: dict[str, Any] = res["ExportDescription"]
        return DynamoDBFinishedExportDescription(
            table_arn=export["TableArn"],
            export_arn=export["ExportArn"],
            export_status=export["ExportStatus"],
            export_time=export["ExportTime"],
            export_manifest=export.get("ExportManifest", ""),
            bucket=export["S3Bucket"],
            failure_code=export.get("FailureCode", ""),
            failure_message=export.get("FailureMessage", ""),
        )
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err
