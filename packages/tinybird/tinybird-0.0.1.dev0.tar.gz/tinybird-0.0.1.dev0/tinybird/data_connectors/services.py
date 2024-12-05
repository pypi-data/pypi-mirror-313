from typing import Any, Dict, Optional

import googleapiclient.errors

from tinybird.connector_settings import DataConnectors, DataConnectorType, GCSConnectorSetting, S3ConnectorSetting
from tinybird.data_connector import DataConnector, InvalidHost, InvalidSettingsException
from tinybird.data_connectors.credentials import S3ConnectorCredentials
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.ingest.cdk_utils import (
    InvalidRole,
    get_env_for_snowflake,
    is_cdk_service_datasource,
    validate_snowflake_role,
)
from tinybird.ingest.data_connectors import (
    ConnectorContext,
    ConnectorCredentials,
    ConnectorException,
    GCSSAConnectorCredentials,
)
from tinybird.ingest.external_datasources.admin import get_or_create_workspace_service_account
from tinybird.ingest.external_datasources.connector import SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT, get_connector
from tinybird.ingest.preview_connectors.amazon_s3_connector import S3PreviewConnector
from tinybird.ingest.preview_connectors.gcs_sa_connector import GCSSAPreviewConnector
from tinybird.integrations.s3 import generate_external_id
from tinybird.user import User as Workspace


class GCPServiceAccountCreationFailed(Exception):
    pass


class SnowflakeIntegrationFailed(Exception):
    pass


class DryRunNotSupported(Exception):
    pass


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


async def create_data_connector(
    workspace: Workspace,
    name: str,
    service: DataConnectorType,
    settings: dict[str, Any],
    application_settings: Optional[Dict[str, Any]] = None,
) -> DataConnector:
    # Lazy initialization if needed of the GCP account
    main_workspace = workspace.get_main_workspace()

    if DataConnectorType.KAFKA == service and application_settings:
        try:
            if FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.VALIDATE_KAFKA_HOST, workspace.id, workspace.feature_flags
            ):
                await DataConnector.validate_kafka_host(
                    settings["kafka_bootstrap_servers"],
                    application_settings,
                )
        except InvalidHost as err:
            raise InvalidSettingsException(err) from err

    if DataConnectorType.GCLOUD_STORAGE_SA == service:
        try:
            account_details = await get_or_create_workspace_service_account(main_workspace)
        except googleapiclient.errors.HttpError as err:
            raise GCPServiceAccountCreationFailed() from err
        settings["account_email"] = account_details["service_account_id"]

    if is_cdk_service_datasource(service):
        try:
            await get_or_create_workspace_service_account(main_workspace)
        except googleapiclient.errors.HttpError as err:
            raise GCPServiceAccountCreationFailed() from err

    if service == DataConnectors.SNOWFLAKE:
        try:
            DataConnector.validate_service_settings(service, settings)
            validate_snowflake_role(settings["role"])
        except InvalidRole as err:
            raise InvalidSettingsException(err) from err

        settings["account"] = sanitize_snowflake_account(settings["account"])
        env = get_env_for_snowflake({})
        env.update(
            {
                "SF_ACCOUNT": settings["account"],
                "SF_USER": settings["username"],
                "SF_PWD": settings["password"],
                "SF_ROLE": settings["role"],
            }
        )
        cdk_connector = await get_connector(service, env)
        integrations = await cdk_connector.get_integrations()
        default_integration_name = SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT.format(role=env["SF_ROLE"])
        integration_name = settings.get("integration", default_integration_name) or default_integration_name
        integration_ok = any(entry.name == integration_name for entry in integrations)
        if not integration_ok:
            raise SnowflakeIntegrationFailed()

    if service == DataConnectors.AMAZON_S3_IAMROLE:
        settings["s3_iamrole_external_id"] = generate_external_id(main_workspace)

    if service == DataConnectors.AMAZON_DYNAMODB:
        settings["dynamodb_iamrole_external_id"] = generate_external_id(main_workspace)

    connector = DataConnector.add_connector(workspace=main_workspace, name=name, service=service, settings=settings)
    await DataConnector.publish(connector.id, connector.service)
    return connector


async def dry_run(service: DataConnectorType, settings_dict: dict[str, Any]) -> list[str]:
    settings = DataConnector.validate_service_settings(service, settings_dict)

    # We've already validated that the settings are well-formed so we access the values directly.
    # Otherwise MyPy complaints.
    if isinstance(settings, S3ConnectorSetting):
        ctx = ConnectorContext(S3PreviewConnector())
        s3_credentials = S3ConnectorCredentials(
            access_key_id=settings.s3_access_key_id,
            secret_access_key=settings.s3_secret_access_key,
            region=settings.s3_region,
        )
        return await _list_buckets(ctx, s3_credentials)
    elif isinstance(settings, GCSConnectorSetting):
        ctx = ConnectorContext(GCSSAPreviewConnector())
        gcs_credentials = GCSSAConnectorCredentials(
            private_key_id=settings.gcs_private_key_id,
            client_x509_cert_url=settings.gcs_client_x509_cert_url,
            project_id=settings.gcs_project_id,
            client_id=settings.gcs_client_id,
            client_email=settings.gcs_client_email,
            private_key=settings.gcs_private_key,
        )
        return await _list_buckets(ctx, gcs_credentials)
    else:
        raise DryRunNotSupported(f"Dry run is not supported for service '{service}'")


async def _list_buckets(connector_context: ConnectorContext, credentials: ConnectorCredentials) -> list[str]:
    try:
        return await connector_context.get_bucket_list(
            credentials=credentials,
            working_zone="gcp#europe-west2",
        )  # TODO: get working zone from request
    except ConnectorException as err:
        message = err.message
        if isinstance(message, dict):
            message = message.get("message", "Unknown error")
        raise InvalidSettingsException(message) from err
