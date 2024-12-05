from typing import Any, cast

from tinybird.data_connector import DataConnectors
from tinybird.data_connectors.credentials import ConnectorCredentials, S3ConnectorCredentials
from tinybird.ingest.data_connectors import ConnectorParameters, S3ConnectorParameters
from tinybird.ingest.preview_connectors.base_connector import BasePreviewConnector, PreviewConnectorMock


class S3PreviewConnector(BasePreviewConnector):
    def __init__(self):
        super().__init__()
        self.connector = DataConnectors.AMAZON_S3

    def make_credentials(self, credentials: ConnectorCredentials) -> dict[str, Any]:
        return {
            "accessKeyId": cast(S3ConnectorCredentials, credentials).access_key_id,
            "secretAccessKey": cast(S3ConnectorCredentials, credentials).secret_access_key,
            "region": cast(S3ConnectorCredentials, credentials).region,
        }

    def make_parameters(self, parameters: ConnectorParameters) -> dict[str, Any]:
        params = {
            "bucketUrl": cast(S3ConnectorParameters, parameters).bucket_uri,
        }
        if (from_time := cast(S3ConnectorParameters, parameters).from_time) is not None:
            params["from"] = from_time
        if (file_format := cast(S3ConnectorParameters, parameters).file_format) is not None:
            params["format"] = file_format
        return params


class S3PreviewConnectorMock(PreviewConnectorMock):
    pass
