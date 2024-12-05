import asyncio
import dataclasses
import json
import logging
import re
from datetime import datetime
from typing import Optional, cast

import snowflake.connector.errors
import tinybird_cdk.errors
from tornado.web import url

import tinybird.data_connectors.services as connector_services
from tinybird.connector_settings import DynamoDBConnectorSetting
from tinybird.data_connectors.credentials import ConnectorCredentials, IAMRoleAWSCredentials, S3ConnectorCredentials
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.guess_analyze import analyze
from tinybird.ingest.cdk_utils import InvalidRole, get_env_for_snowflake, get_gcs_bucket_uri, validate_snowflake_role
from tinybird.ingest.data_connectors import (
    ConnectorContext,
    ConnectorException,
    ConnectorParameters,
    GCSSAConnectorCredentials,
    GCSSAConnectorParameters,
    S3ConnectorParameters,
    S3IAMConnectorParameters,
)
from tinybird.ingest.external_datasources.connector import (
    SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT,
    InvalidGCPCredentials,
    get_connector,
)
from tinybird.ingest.external_datasources.inspection import ExternalTableDatasource, list_resources
from tinybird.ingest.preview_connectors.amazon_s3_connector import S3PreviewConnector
from tinybird.ingest.preview_connectors.amazon_s3_iam_connector import S3IAMPreviewConnector
from tinybird.ingest.preview_connectors.gcs_sa_connector import GCSSAPreviewConnector
from tinybird.kafka_utils import KafkaTbUtils
from tinybird.limits import Limit
from tinybird.ndjson import extend_json_deserialization
from tinybird.plan_limits.cdk import CDKLimits
from tinybird.providers.aws.dynamodb import scan_table
from tinybird.providers.aws.exceptions import AWSClientException
from tinybird.providers.aws.session import AWSSession
from tinybird.sql import parse_table_structure
from tinybird.views.api_data_connections import cdk_to_http_errors
from tinybird.views.base import check_rate_limit
from tinybird.views.json_deserialize_utils import (
    SchemaJsonpathMismatch,
    json_deserialize_merge_schema_jsonpaths,
    parse_augmented_schema,
)
from tinybird.views.ndjson_importer import dynamodb_preview

from ..data_connector import (
    DataConnector,
    DataConnectors,
    DuplicatedConnectorNameException,
    InvalidSettingsException,
    KafkaSettings,
)
from ..feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from .api_errors.data_connectors import (
    DataConnectorsClientErrorBadRequest,
    DataConnectorsClientErrorForbidden,
    DataConnectorsClientErrorNotFound,
    DataConnectorsUnprocessable,
    DynamoDBPreviewError,
)
from .base import ApiHTTPError, BaseHandler, authenticated, requires_write_access, with_scope_admin

CONNECTOR_PARAMS = ("token", "name", "service")
PASSWORD_MASKED = "******"
LINKER_FORBIDDEN_KEYS = ("clickhouse_host", "clickhouse_table", "token")
CONNECTOR_MASKED_KEYS = (
    "kafka_sasl_plain_password",
    "kafka_schema_registry_url",
    "kafka_ssl_ca_pem",
    "password",
    "gcs_hmac_secret",
    "s3_access_key_id",
    "s3_secret_access_key",
    "gcs_private_key_id",
    "gcs_client_id",
    "gcs_client_email",
    "gcs_private_key",
)


def clean_data_connector(connector: dict) -> dict:
    for linker in connector["linkers"]:
        for key in LINKER_FORBIDDEN_KEYS:
            if key in linker["settings"]:
                del linker["settings"][key]
    for key in CONNECTOR_MASKED_KEYS:
        if key in connector["settings"] and connector["settings"][key]:
            connector["settings"][key] = PASSWORD_MASKED

    return connector


def sanitize_snowflake_account(account: str) -> str:
    # Sanitizing the account is used because Snowflake's option to copy the
    # account identifier in their UI uses a dot '.' instead of the required
    # hyphen '-' to separate the fields. Thus, this is a small UX improvement to
    # ease the life of the users.
    """
    >>> sanitize_snowflake_account('evnxbin.ca56448')
    'evnxbin-ca56448'
    """
    return account.replace(".", "-")


class APIDataConnectorsBase(BaseHandler):
    """
    This class is a base to support getting arguments from JSON requests the same way
    we take them from Tornado's using the convenient `get_argument` which reads args
    both from the query and from the body.

    This class overrides the `get_argument` method returning the argument from the
    JSON given if available, falling back to Tornado's one if not found.
    """

    async def prepare(self):
        super().prepare()
        self.json_args = None
        if "Content-Type" in self.request.headers and self.request.headers["Content-Type"].startswith(
            "application/json"
        ):
            # Let's keep the args as bytes because internal args are stored this way. Then, we'll use
            # decode_argument to convert them to str.
            self.json_args = {k: str(v).encode("utf-8") for k, v in json.loads(self.request.body).items()}

    def get_argument(self, name: str, default=None):
        if name != "token" and hasattr(self, "json_args") and self.json_args is not None:
            value = self.decode_argument(self.json_args.get(name), name)
            if value is None:
                value = super().get_argument(name, default)
            return value
        return super().get_argument(name, default)

    @property
    def request_arguments(self):
        args = self.request.arguments
        if hasattr(self, "json_args") and self.json_args is not None:
            args.update(self.json_args)
        return args


class APIDataConnectorsHandler(APIDataConnectorsBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self):
        """
        Get the list of connectors

        .. sourcecode:: bash
            :caption: Getting the connectors

            curl "https://api.tinybird.co/v0/connectors?token=$TOKEN"

        .. sourcecode:: json
            :caption: Response

            {
                "connectors": [{
                    "id": "1234",
                    "name" "my_connector",
                    "service": "kafka",
                    "settings": {
                        ...
                    }
                }, {
                    ...
                }],
                "limits": {
                    "max_topics": 5
                }
            }
        """
        workspace = self.get_workspace_from_db()

        # If we are on a release or a branch, we will use the origin workspace to get the connectors
        origin_workspace = workspace.get_main_workspace()
        origin_workspace_id = origin_workspace.id
        data_connectors = DataConnector.get_user_data_connectors(origin_workspace_id)
        data_connectors = [clean_data_connector(connector) for connector in data_connectors]

        service = self.get_argument("service", None)
        if service is not None:
            data_connectors = [connector for connector in data_connectors if connector["service"] == service]

        response = {"connectors": data_connectors}

        self.write_json(response)

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_create)
    async def post(self):
        """
        Add a connector

        .. sourcecode:: bash
            :caption: Adding a connector

            curl \\
                -H "Authorization: Bearer $TOKEN" \\
                "http://api.tinybird.co/v0/connectors" \\
                --data-urlencode "name=my_connector" \\
                --data-urlencode "service=kafka" \\
                --data-urlencode "kafka_bootstrap_servers=kafka_server"

        .. sourcecode:: json
            :caption: Response

            {
                "id": "1234",
                "name" "my_connector",
                "service": "kafka",
                "settings": {
                    "kafka_bootstrap_servers": "kafka_server",
                }
            }
        """
        workspace = self.get_workspace_from_db()

        # Retrieve request args

        service: Optional[DataConnectors] = self.get_argument("service", None)
        name = self.get_argument("name", None)
        dry_run = self.get_argument("dry_run", "false").lower() == "true"

        settings = {
            setting: self.get_argument(setting)
            for setting in self.request_arguments.keys()
            if setting not in CONNECTOR_PARAMS
        }
        if service == DataConnectors.KAFKA:
            settings["kafka_sasl_mechanism"] = self.get_argument("kafka_sasl_mechanism", "PLAIN")
        settings["tb_endpoint"] = self.application.settings["api_host"]

        if dry_run is True:
            try:
                buckets_list = await connector_services.dry_run(service, settings)
            except connector_services.DryRunNotSupported as err:
                raise ApiHTTPError(400, str(err))
            except InvalidSettingsException as err:
                req_error = DataConnectorsClientErrorBadRequest.invalid_settings(message=err)
                raise ApiHTTPError.from_request_error(req_error) from err
            except DuplicatedConnectorNameException as err:
                req_error = DataConnectorsClientErrorBadRequest.invalid_settings(message=err)
                raise ApiHTTPError.from_request_error(req_error) from err
            self.write(json.dumps(buckets_list))
        else:
            try:
                data_connector = await connector_services.create_data_connector(
                    workspace, name, service, settings, self.application.settings
                )
            except connector_services.GCPServiceAccountCreationFailed as err:
                # There's not much the user can do here as it's our internal setup with GCP that failed so 502 Bad Gateway.
                raise ApiHTTPError(502, "Connector creation failed") from err
            except connector_services.SnowflakeIntegrationFailed as err:
                req_err = DataConnectorsClientErrorBadRequest.snowflake_integration_failed()
                raise ApiHTTPError.from_request_error(req_err) from err
            except InvalidSettingsException as err:
                req_error = DataConnectorsClientErrorBadRequest.invalid_settings(message=err)
                raise ApiHTTPError.from_request_error(req_error) from err
            except DuplicatedConnectorNameException as err:
                req_error = DataConnectorsClientErrorBadRequest.invalid_settings(message=err)
                raise ApiHTTPError.from_request_error(req_error) from err

            response = clean_data_connector(data_connector.to_json())
            self.write_json(response)


class APIDataConnectorPreviewHandler(APIDataConnectorsBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_preview)
    async def get(self, connector_id: str) -> None:
        """
        Preview a connector

        .. sourcecode:: bash
            :caption: Preview a connector

            curl \\
                -H "Authorization: Bearer $TOKEN" \\
                -G "http://127.0.0.1:8001/v0/connectors/784181e7-748f-44bb-a50f-ee810bc07dad/preview" \\
                --data-urlencode "max_records=3" \\
                --data-urlencode "preview_activity=true" \\
                --data-urlencode "preview_earliest_timestamp=true" \\
                --data-urlencode "preview_group=true" \\

        .. sourcecode:: json
            :caption: Response

            {
                "preview": [
                    {
                        "topic": "t_10",
                        "last_messages": [
                            {
                                "timestamp": "2021-05-11 12:18:35.190245",
                                "topic": "t_10",
                                "partition": 1,
                                "offset": 51197,
                                "message_key": "None",
                                "message_value": "b'{\"vendorid\": 2, \"tpep_pickup_datetime\": \"2017-01-01 00:01:06\", \"tpep_dropoff_datetime\": \"2017-01-01 00:25:44\", \"passenger_count\": 1, \"trip_distance\": 5.67, \"ratecodeid\": 1, \"store_and_fwd_flag\": \"N\", \"pulocationid\": 234, \"dolocationid\": 41, \"payment_type\": 2, \"fare_amount\": 21, \"extra\": 0.5, \"mta_tax\": 0.5, \"tip_amount\": 0, \"tolls_amount\": 0, \"improvement_surcharge\": 0.3, \"total_amount\": 22.3}'"
                            }
                        ],
                        "messages_in_last_hour": 0
                    }
                ]
            }
        """
        data_connector = DataConnector.get_by_id(connector_id)

        if not data_connector:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

        workspace = self.get_workspace_from_db()
        origin_workspace_id = workspace.origin if workspace.is_branch_or_release_from_branch else workspace.id

        connector_belongs_to_workspace = await asyncio.to_thread(
            DataConnector.is_owned_by, connector_id, origin_workspace_id
        )
        if not connector_belongs_to_workspace:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorForbidden.not_allowed())

        if data_connector.service == DataConnectors.KAFKA:
            kafka_group_id = self.get_argument("kafka_group_id", None)
            kafka_topic = self.get_argument("kafka_topic", None)
            max_records = int(self.get_argument("max_records", KafkaSettings.PREVIEW_MAX_RECORDS))
            preview_activity = self.get_argument("preview_activity", "true").lower() == "true"
            preview_earliest_timestamp = self.get_argument("preview_earliest_timestamp", "false").lower() == "true"
            preview_group = self.get_argument("preview_group", "false").lower() == "true"
            schema = self.get_argument("schema", None)

            if preview_group:
                response = await KafkaTbUtils.get_kafka_topic_group(
                    workspace, kafka_topic=kafka_topic, kafka_group_id=kafka_group_id, data_connector=data_connector
                )

            else:
                response = await KafkaTbUtils.get_kafka_preview(
                    workspace,
                    data_connector,
                    kafka_group_id,
                    kafka_topic=kafka_topic,
                    max_records=max_records,
                    preview_activity=preview_activity,
                    preview_earliest_timestamp=preview_earliest_timestamp,
                    schema=schema,
                )
            if response.get("error"):
                logging.error(f"Kafka preview error: {response['error']}")
                if response.get("error") == "not_exists":
                    raise ApiHTTPError.from_request_error(DataConnectorsUnprocessable.topic_not_exists())
                if response.get("error") == "consume_failed_auth_groupid_failed":
                    raise ApiHTTPError.from_request_error(DataConnectorsUnprocessable.auth_groupid_failed())
                if response.get("error") == "group_id_already_active_for_topic":
                    raise ApiHTTPError.from_request_error(DataConnectorsUnprocessable.auth_groupid_in_use())
                if response.get("error") == "metadata_protocol_error":
                    raise ApiHTTPError.from_request_error(DataConnectorsUnprocessable.metadata_protocol_error())
                elif response.get("error") == "message_not_produced_with_confluent_schema_registry":
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsUnprocessable.message_not_produced_with_confluent_schema_registry()
                    )
                elif type(response.get("error")) is str:
                    raise ApiHTTPError(422, response.get("error"))
                raise ApiHTTPError.from_request_error(
                    DataConnectorsUnprocessable.unable_to_connect(error=response["error"])
                )

            self.write_json(response)

        elif data_connector.service == DataConnectors.SNOWFLAKE:
            external_data_source = self.get_argument("external_data_source", None)
            if external_data_source is None:
                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.missing_param(param="external_data_source")
                )

            optional_env = {
                "SF_ACCOUNT": data_connector.settings.get("account"),
                "SF_USER": data_connector.settings.get("username"),
                "SF_PWD": data_connector.settings.get("password"),
                "SF_WAREHOUSE": data_connector.settings.get("warehouse"),
                "SF_ROLE": data_connector.settings.get("role"),
            }
            env = get_env_for_snowflake(optional_env)

            try:
                try:
                    self.cdk_connector = await get_connector(data_connector.service, env)
                except InvalidGCPCredentials as err:
                    # If we get here something has gone terribly wrong and the credentials might be invalid/corrupted
                    raise ApiHTTPError(401, "Something went terribly wrong. Please try again later") from err

                table = ExternalTableDatasource(self.cdk_connector, external_data_source.rsplit(".", 2))
                schema = await table.get_schema()
                sample = await table.get_sample()
                query = await table.get_extraction_query()
                preview_metadata = [{"name": col["name"], "type": col["recommended_type"]} for col in schema["columns"]]
                analyze_results = {
                    "analysis": schema,
                    "query": query,
                    "preview": {"meta": preview_metadata, "data": sample},
                }
                self.write(json.dumps(analyze_results, default=str, indent=4))
            except InvalidGCPCredentials as e:
                raise ApiHTTPError(401, "Invalid credentials") from e
            except snowflake.connector.errors.Error as e:
                raise ApiHTTPError(403, e.raw_msg) from e

        elif data_connector.service == DataConnectors.AMAZON_DYNAMODB:
            table_name: str = self.get_argument("dynamodb_table_arn")
            settings = cast(DynamoDBConnectorSetting, data_connector.validated_settings)
            session = cast(AWSSession, build_session_from_credentials(credentials=settings.credentials))

            def scan_dynamodb_table():
                return scan_table(session, table_name, settings.dynamodb_iamrole_region)

            try:
                raw_data = await asyncio.get_running_loop().run_in_executor(None, scan_dynamodb_table)
            except AWSClientException as err:
                raise ApiHTTPError.from_request_error(DynamoDBPreviewError.scan_error(error_message=str(err)))

            if len(raw_data) == 0:
                raise ApiHTTPError.from_request_error(
                    DynamoDBPreviewError.analyze_error(error_message="Table is empty")
                )

            try:
                analysis = await analyze(raw_data)
            except Exception as e:
                raise ApiHTTPError.from_request_error(DynamoDBPreviewError.analyze_error(error_message=str(e)))

            if not analysis:
                raise ApiHTTPError.from_request_error(
                    DynamoDBPreviewError.analyze_error(error_message="No analysis found")
                )

            augmented_schema = analysis["schema"]
            parsed_schema = parse_augmented_schema(augmented_schema)
            schema = parsed_schema.schema
            jsonpaths = parsed_schema.jsonpaths

            try:
                json_conf = json_deserialize_merge_schema_jsonpaths(parse_table_structure(schema), jsonpaths)
            except SchemaJsonpathMismatch:
                raise ApiHTTPError.from_request_error(
                    DynamoDBPreviewError.analyze_mismatch(schema=schema, jsonpaths=jsonpaths)
                )

            extended_json_deserialization = extend_json_deserialization(json_conf)
            preview = await dynamodb_preview(extended_json_deserialization, raw_data)
            return self.write_json({"preview": preview, "analysis": analysis})

        elif data_connector.service in [
            DataConnectors.AMAZON_S3,
            DataConnectors.GCLOUD_STORAGE,
            DataConnectors.AMAZON_S3_IAMROLE,
        ]:
            summary = self.get_argument("summary", "false").lower() == "true"
            credentials: ConnectorCredentials = ConnectorCredentials()
            parameters: ConnectorParameters = ConnectorParameters()
            bucket_uri = self.get_argument("bucket_uri", None)
            from_time = self.get_argument("from_time", None)
            file_format = self.get_argument("format", None)
            sample_file_uri = self.get_argument("sample_file_uri", None)

            if bucket_uri is None:
                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.missing_param(param="bucket_uri")
                )

            valid_extensions = [
                "csv",
                "csv.gz",
                "ndjson",
                "ndjson.gz",
                "jsonl",
                "jsonl.gz",
                "json",
                "json.gz",
                "parquet",
                "parquet.gz",
            ]

            if file_format is not None and file_format not in valid_extensions:
                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.format_not_supported(formats=["csv", "ndjson", "parquet"])
                )
            elif file_format is None and not bool(re.search(r"\.(" + "|".join(valid_extensions) + ")$", bucket_uri)):
                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.bucket_uri_not_supported(
                        extensions=valid_extensions, formats=["csv", "ndjson", "parquet"]
                    )
                )

            try:
                from_time = str(datetime.fromisoformat(from_time).isoformat()) if from_time is not None else None
            except ValueError:
                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.invalid_settings(
                        message=f"'{from_time}' isn't a valid value for parameter 'from_time'"
                    )
                )

            if data_connector.service == DataConnectors.AMAZON_S3:
                connector = ConnectorContext(S3PreviewConnector())

                credentials = S3ConnectorCredentials(
                    access_key_id=data_connector.settings.get("s3_access_key_id"),  # type: ignore
                    secret_access_key=data_connector.settings.get("s3_secret_access_key"),  # type: ignore
                    region=data_connector.settings.get("s3_region"),  # type: ignore
                )
                parameters = S3ConnectorParameters(bucket_uri=bucket_uri, from_time=from_time, file_format=file_format)

            if data_connector.service == DataConnectors.AMAZON_S3_IAMROLE:
                is_custom_preview_enabled = FeatureFlagsWorkspaceService.feature_for_id(
                    FeatureFlagWorkspaces.ENABLE_CUSTOM_PREVIEW_FOR_S3_CONNECTOR, workspace.id, workspace.feature_flags
                )
                connector = ConnectorContext(S3IAMPreviewConnector(custom_preview=is_custom_preview_enabled))

                credentials = IAMRoleAWSCredentials(
                    role_arn=data_connector.settings.get("s3_iamrole_arn"),  # type: ignore
                    external_id=data_connector.settings.get("s3_iamrole_external_id"),  # type: ignore
                    region=data_connector.settings.get("s3_iamrole_region"),  # type: ignore
                )

                parameters = S3IAMConnectorParameters(
                    bucket_uri=bucket_uri, from_time=from_time, file_format=file_format, sample_file_uri=sample_file_uri
                )

            if data_connector.service == DataConnectors.GCLOUD_STORAGE:
                connector = ConnectorContext(GCSSAPreviewConnector())

                credentials = GCSSAConnectorCredentials(
                    private_key_id=data_connector.settings.get("gcs_private_key_id"),  # type: ignore
                    client_x509_cert_url=data_connector.settings.get("gcs_client_x509_cert_url"),  # type: ignore
                    project_id=data_connector.settings.get("gcs_project_id"),  # type: ignore
                    client_id=data_connector.settings.get("gcs_client_id"),  # type: ignore
                    client_email=data_connector.settings.get("gcs_client_email"),  # type: ignore
                    private_key=data_connector.settings.get("gcs_private_key"),  # type: ignore
                )
                parameters = GCSSAConnectorParameters(
                    bucket_uri=bucket_uri, from_time=from_time, file_format=file_format
                )

            try:
                token = self._get_token()

                if token is None:
                    raise ConnectorException(message="Token not found")

                if summary:
                    response = await connector.get_preview_summary(
                        credentials=credentials,
                        tb_endpoint=self.request.host,
                        tb_token=token,
                        parameters=parameters,
                        working_zone="gcp#europe-west2",
                        workspace_id=workspace.id,
                    )  # TODO: get working zone from request
                else:
                    response = await connector.get_preview(
                        credentials=credentials,
                        tb_endpoint=self.request.host,
                        tb_token=token,
                        parameters=parameters,
                        working_zone="gcp#europe-west2",
                        workspace_id=workspace.id,
                    )  # TODO: get working zone from request

                self.write_json(response)
            except ConnectorException as e:
                message = e.message
                if isinstance(message, dict):
                    message = message.get("message", "Unknown error")

                if "Not all required params" in message:
                    raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.missing_params())

                if "Bucket does not exist" in message:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.invalid_settings(
                            message="The specified bucket does not exist"
                        )
                    )

                if "must be addressed using the specified endpoint" in message:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.invalid_settings(
                            message="Invalid connection parameters (maybe the region is wrong?)"
                        )
                    )

                if "Token not found" in message:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.invalid_settings(message="Token not found")
                    )

                raise ApiHTTPError.from_request_error(
                    DataConnectorsClientErrorBadRequest.invalid_settings(message=message)
                )

    def on_finish(self):
        super().on_finish()
        if hasattr(self, "cdk_connector"):
            self.cdk_connector.shutdown()


class APIDataConnectorHandler(APIDataConnectorsBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self, connector_id: str) -> None:
        """
        Get a connector

        .. sourcecode:: bash
            :caption: Getting a single connector

            curl "https://api.tinybird.co/v0/connectors/<connector_id>?token=$TOKEN"

        .. sourcecode:: json
            :caption: Response

            {
                "id": "<connector_id>",
                "name" "my_connector",
                "service": "kafka",
                "settings": {
                    "endpoint": "http://api.tinybird.co",
                    "max_wait_seconds": "30",
                    "max_wait_records": "10000",
                    "max_wait_bytes": "8388608",
                    "kafka_bootstrap_servers": "kafka_server",
                },
                "linkers": [
                    {
                        "id": "<linker_id>",
                        "datasource": "datasource_id",
                        "settings": {
                            "token": "<token>",
                            "kafka_topic": "topic_1",
                            "kafka_group_id": "kafka_group"
                        }
                    }
                ]
            }
        """

        workspace = self.get_workspace_from_db()
        origin_workspace_id = workspace.origin if workspace.is_branch_or_release_from_branch else workspace.id

        data_connector = DataConnector.get_by_id(connector_id)
        if not data_connector:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

        if not DataConnector.is_owned_by(connector_id, origin_workspace_id):
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorForbidden.not_allowed())

        clean_dc = clean_data_connector(data_connector.to_json())
        self.write_json(clean_dc)

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_create)
    async def put(self, connector_id: str) -> None:
        """
        Modify a data connector. The 'service' field can not be updated.

        .. sourcecode:: bash
            :caption: Update name and settings

            curl \\
                -H "Authorization: Bearer $TOKEN" \\
                -X PUT "http://api.tinybird.co/v0/connectors/<connector_id>" \\
                -d "name=my_new_connector"

        .. sourcecode:: json
            :caption: Response

            {
                "id": "1234",
                "name" "my_new_connector",
                "connector": "kafka",
                "settings": {
                    "endpoint": "http://api.tinybird.co",
                    "kafka_bootstrap_servers": "kafka_server",
                }
            }
        """

        workspace = self.get_workspace_from_db()
        data_connector = DataConnector.get_by_id(connector_id)

        if not data_connector:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

        if not DataConnector.is_owned_by(connector_id, workspace.id):
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorForbidden.not_allowed())

        name = self.get_argument("name", None)

        with DataConnector.transaction(data_connector.id) as data_connector:
            try:
                if name:
                    data_connector.update_name(name)

                settings = {
                    setting: self.get_argument(setting)
                    for setting in self.request_arguments.keys()
                    if setting not in CONNECTOR_PARAMS
                }

                if data_connector.service == DataConnectors.SNOWFLAKE and "role" in settings:
                    try:
                        validate_snowflake_role(settings["role"])
                    except InvalidRole as e:
                        raise ApiHTTPError.from_request_error(
                            DataConnectorsClientErrorBadRequest.invalid_settings(message=e)
                        )
                data_connector.update_settings(settings)
            except InvalidSettingsException as e:
                raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.invalid_settings(message=e))
            except DuplicatedConnectorNameException as e:
                raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.invalid_settings(message=e))

        await DataConnector.publish(data_connector.id)
        response = clean_data_connector(data_connector.to_json())
        self.write_json(response)

    @authenticated
    @requires_write_access
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_create)
    async def delete(self, connector_id: str) -> None:
        """
        Delete a data connector. This operation can not be undone.

        .. sourcecode:: bash
            :caption: Delete request

            curl \\
                -H "Authorization: Bearer $TOKEN" \\
                -X DELETE "http://api.tinybird.co/v0/connectors/<connector_id>"
        """

        workspace = self.get_workspace_from_db()
        data_connector = DataConnector.get_by_id(connector_id)

        if not data_connector:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

        if not DataConnector.is_owned_by(connector_id, workspace.id):
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorForbidden.not_allowed())

        await data_connector.hard_delete()
        self.set_status(204)


class APISnowflakeHandler(APIDataConnectorsBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_list)
    async def post(self, details):
        account = self.get_argument("account", None)
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        role = self.get_argument("role", None)
        stage = self.get_argument("stage", None)
        integration = self.get_argument("integration", None)

        mandatory_arguments = {
            "account": account,
            "username": username,
            "password": password,
        }

        for key, value in mandatory_arguments.items():
            if value is None:
                raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.missing_param(param=key))

        if role:
            try:
                validate_snowflake_role(role)
            except InvalidRole as e:
                raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.invalid_settings(message=e))

        account = sanitize_snowflake_account(account)

        env = {
            "SF_ACCOUNT": account,
            "SF_USER": username,
            "SF_PWD": password,
            "SF_ROLE": role,
            "SF_STAGE": stage,
            "SF_INTEGRATION": integration,
        }
        env = get_env_for_snowflake(env)

        try:
            self.cdk_connector = await get_connector(DataConnectors.SNOWFLAKE, env)

            if details == "roles":
                roles = await self.cdk_connector.get_roles()
                self.write_json({"roles": [role.name for role in roles]})
            elif details == "warehouses":
                if role is None:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.missing_param(param="role")
                    )
                warehouses = await self.cdk_connector.get_warehouses()
                self.write_json({"warehouses": [dataclasses.asdict(warehouse) for warehouse in warehouses]})
        except snowflake.connector.errors.Error as e:
            raise ApiHTTPError(403, e.raw_msg) from e
        except tinybird_cdk.errors.SnowflakeConnectionError:
            raise ApiHTTPError(
                403,
                "Failed to connect to DB. Incoming request is not allowed to access Snowflake. Contact your account admin",
            )

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self):
        role = self.get_argument("role", None)
        stage = self.get_argument("stage", None)
        integration = self.get_argument("integration", None)

        if role is None:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.missing_param(param="role"))

        try:
            validate_snowflake_role(role)
        except InvalidRole as e:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.invalid_settings(message=e))

        workspace = self.get_workspace_from_db()
        origin_workspace_id = workspace.origin if workspace.is_branch_or_release_from_branch else workspace.id
        gcs_bucket_uri = get_gcs_bucket_uri(origin_workspace_id)
        env = get_env_for_snowflake({"SF_ROLE": role, "SF_STAGE": stage, "SF_INTEGRATION": integration})
        cdk_connector = await get_connector(DataConnectors.SNOWFLAKE, env)

        integration = integration or SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT.format(role=role)
        query = await cdk_connector.get_integration_query(gcs_bucket_uri, integration)

        response = {
            "steps": [
                {
                    "description": "Execute this SQL statement in Snowflake using your Admin account to create the connection. Edit <your_database> and add yours:",
                    "action": query,
                }
            ]
        }

        self.write_json(response)

    def on_finish(self):
        super().on_finish()
        if hasattr(self, "cdk_connector"):
            self.cdk_connector.shutdown()


class APIDataConnectorResourcesHandler(APIDataConnectorsBase):
    @authenticated
    @with_scope_admin
    @cdk_to_http_errors
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self, connector_id: str, *scope: str) -> None:
        workspace = self.get_workspace_from_db()
        origin_workspace_id = workspace.origin if workspace.is_branch_or_release_from_branch else workspace.id
        data_connector = DataConnector.get_by_id(connector_id)

        if not data_connector:
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

        if not DataConnector.is_owned_by(connector_id, origin_workspace_id):
            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorForbidden.not_allowed())

        env = {}
        if data_connector.service == DataConnectors.SNOWFLAKE:
            env.update(
                {
                    "SF_ACCOUNT": data_connector.settings.get("account"),
                    "SF_USER": data_connector.settings.get("username"),
                    "SF_PWD": data_connector.settings.get("password"),
                    "SF_WAREHOUSE": data_connector.settings.get("warehouse"),
                    "SF_ROLE": data_connector.settings.get("role"),
                    "SF_STAGE": data_connector.settings.get("stage", None),
                    "SF_INTEGRATION": data_connector.settings.get("integration", None),
                }
            )
            env = get_env_for_snowflake(env)

        try:
            try:
                self.cdk_connector = await get_connector(data_connector.service, env)
            except NotImplementedError as err:
                raise ApiHTTPError(501, err.args[0]) from err

            resources = await list_resources(self.cdk_connector, scope)
            row_limit = CDKLimits.max_row_limit.get_limit_for(self.current_workspace)

            if len(scope) >= 2:
                resources = [
                    {
                        **table,
                        "row_limit": row_limit,
                        "row_limit_exceeded": (
                            CDKLimits.max_row_limit.has_reached_limit_in(row_limit, {"rows": table["num_rows"]})
                            if table.get("num_rows", None) is not None
                            else False
                        ),
                    }
                    for table in resources
                ]
            self.write_json({"resources": resources})
        except snowflake.connector.errors.Error as e:
            raise ApiHTTPError(403, e.raw_msg) from e

    def on_finish(self):
        super().on_finish()
        if hasattr(self, "cdk_connector"):
            self.cdk_connector.shutdown()


def handlers():
    return [
        url(r"/v0/connectors/?", APIDataConnectorsHandler),
        url(r"/v0/connectors/snowflake/(roles|warehouses)", APISnowflakeHandler),
        url(r"/v0/connectors/snowflake/instructions", APISnowflakeHandler),
        url(r"/v0/connectors/([^/]+)/preview", APIDataConnectorPreviewHandler),
        url(r"/v0/connectors/([^/]+)/resources", APIDataConnectorResourcesHandler),
        url(r"/v0/connectors/([^/]+)/resources/([^/]+)", APIDataConnectorResourcesHandler),
        url(r"/v0/connectors/([^/]+)/resources/([^/]+)/([^/]+)", APIDataConnectorResourcesHandler),
        url(r"/v0/connectors/([^/]+)/?", APIDataConnectorHandler),
    ]
