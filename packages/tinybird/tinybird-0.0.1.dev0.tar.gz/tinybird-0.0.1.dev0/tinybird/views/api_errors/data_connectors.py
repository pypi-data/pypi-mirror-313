from tinybird.data_connector import DataConnectors

from . import request_error

DATA_CONNECTORS_AVAILABLE = [DataConnectors.KAFKA, DataConnectors.GCLOUD_SCHEDULER]


class DataConnectorsClientErrorForbidden:
    not_allowed = request_error(
        403,
        "Not allowed. Data Connectors created from a Branch belong to the main Workspace. Try again from the Workspace.",
    )


class DataConnectorsClientErrorNotFound:
    no_data_connector = request_error(404, "Data Connector not found")
    no_data_connector_token_found = request_error(
        404, "No token with scope DATASOURCES_CREATE. Please create one and retry or contact us at support@tinybird.co"
    )
    no_data_connector_type = request_error(404, "Data Connector type not supported")
    no_data_linker = request_error(404, "Data Linker not found")


class DataConnectorsClientErrorBadRequest:
    invalid_settings = request_error(400, "{message}")
    invalid_mode = request_error(400, "Invalid mode: {invalid}. Only {valid} supported")
    missing_connector_param = request_error(
        400, f"'connector' param is mandatory, allowed connectors are: {', '.join(DATA_CONNECTORS_AVAILABLE)}"
    )
    missing_param = request_error(400, "Missing param: {param}")
    missing_params = request_error(400, "Missing params")
    file_extension_not_supported = request_error(
        400, "File extension not supported. Valid extensions are: {extensions}. Valid data formats are: {formats}"
    )
    bucket_uri_not_supported = request_error(
        400,
        "Bucket path must include the file extension, example: s3://events-daily/*.csv. Valid extensions are: {extensions}. Valid data formats are: {formats}",
    )
    format_not_supported = request_error(
        400,
        "Format not supported. Valid data formats are: {formats}",
    )
    connector_can_not_be_updated = request_error(400, "'connector' can not be updated")
    data_linker_other_type = request_error(404, "Data Source has already another Linker of other type")
    snowflake_integration_failed = request_error(403, "Remember to execute the SQL statement from an Admin account")


class DataConnectorsUnprocessable:
    unable_to_connect = request_error(
        422,
        "Unable to connect to Kafka server due to error: {error}. Check bootstrap server address, auth settings and firewalls.",
    )
    topic_not_exists = request_error(422, "Topic not exists.")
    auth_groupid_failed = request_error(
        422,
        "Cannot consume from this group ID with these credentials. Check this auth settings have access to consume from this group ID.",
    )
    auth_groupid_in_use = request_error(422, "Group ID already in active use for this topic.")
    metadata_protocol_error = request_error(422, "Metadata protocol error. Contact support@tinybird.co.")
    message_not_produced_with_confluent_schema_registry = request_error(
        422,
        "Unable to deserialize message. Please verify if this message was produced with Schema Registry, uncheck 'Decode messages with Schema Registry' otherwise",
    )


class KafkaPreviewError:
    connection_error = request_error(500, "Error connecting to Kafka broker. Contact support@tinybird.co.")


class PreviewConnectorError:
    connection_error = request_error(500, "Error connecting to preview service. Contact support@tinybird.co.")
    timeout_error = request_error(
        408,
        "Error connecting to preview service due to a timeout. Please retry and if the problem persists contact support@tinybird.co.",
    )


class S3SourceError:
    invalid_bucket_name_error = request_error(
        400,
        "The bucket name is not valid. See guidelines: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html",
    )


class DynamoDBConnectorError:
    invalid_bucket_name_error = request_error(
        400,
        "The bucket name is not valid. See guidelines: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html",
    )


class DynamoDBPreviewError:
    scan_error = request_error(400, "Unable to scan DynamoDB table: {error_message}")
    analyze_error = request_error(
        400, "Unable to analyze DynamoDB table and generate compatible schema: {error_message}"
    )
    analyze_mismatch = request_error(
        400, "Analyze mismatch between schema and jsonpath parameters: schema={schema} jsonpath={jsonpaths}"
    )
