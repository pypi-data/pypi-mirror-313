from typing import Any, cast

from tinybird.data_connector import DataConnectors
from tinybird.data_connectors.credentials import ConnectorCredentials
from tinybird.ingest.data_connectors import ConnectorParameters, GCSSAConnectorCredentials, GCSSAConnectorParameters
from tinybird.ingest.preview_connectors.base_connector import BasePreviewConnector, PreviewConnectorMock


class GCSSAPreviewConnector(BasePreviewConnector):
    def __init__(self):
        super().__init__()
        self.connector = DataConnectors.GCLOUD_STORAGE

    def make_credentials(self, credentials: ConnectorCredentials) -> dict[str, Any]:
        return {
            "projectId": cast(GCSSAConnectorCredentials, credentials).project_id,
            "credentials": {
                "private_key_id": cast(GCSSAConnectorCredentials, credentials).private_key_id,
                "client_x509_cert_url": cast(GCSSAConnectorCredentials, credentials).client_x509_cert_url,
                "project_id": cast(GCSSAConnectorCredentials, credentials).project_id,
                "client_id": cast(GCSSAConnectorCredentials, credentials).client_id,
                "client_email": cast(GCSSAConnectorCredentials, credentials).client_email,
                "private_key": cast(GCSSAConnectorCredentials, credentials)
                .private_key.encode("utf-8")
                .decode("unicode_escape"),
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "type": "service_account",
            },
        }

    def make_parameters(self, parameters: ConnectorParameters) -> dict[str, Any]:
        params = {
            "bucketUrl": cast(GCSSAConnectorParameters, parameters).bucket_uri,
        }
        if (from_time := cast(GCSSAConnectorParameters, parameters).from_time) is not None:
            params["from"] = from_time
        if (file_format := cast(GCSSAConnectorParameters, parameters).file_format) is not None:
            params["format"] = file_format
        return params


class GCSSAPreviewConnectorMock(PreviewConnectorMock):
    pass
