import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, cast
from urllib.parse import urljoin, urlparse

from tinybird.connector_settings import (
    GCSHmacConnectorSetting,
    GCSServiceAccountConnectorSetting,
    S3ConnectorSetting,
    S3IAMConnectorSetting,
    SinkConnectorSettings,
)
from tinybird.data_connectors.credentials import (
    ConnectorCredentials,
    GCSServiceAccountCredentials,
    IAMRoleAWSCredentials,
    S3ConnectorCredentials,
)
from tinybird.data_connectors.exceptions import MissingBucketPathOrSchemeException
from tinybird.providers.auth import get_auth_provider
from tinybird.providers.aws.session import AccessKey, AWSSession, StaticCredentialsAWSSession
from tinybird.providers.gcp.session import GCPSession
from tinybird.views.api_errors.pipes import DataSinkError


@dataclass(frozen=True)
class BucketInfo:
    name: str
    prefix: str
    url: str


@dataclass(frozen=True)
class BucketFileInfo:
    path: str
    last_modification: datetime
    size: int

    def is_modified_after(self, modified_after: datetime) -> bool:
        last_modified_date = self.last_modification.replace(tzinfo=timezone.utc)
        modified_after_date = modified_after.replace(tzinfo=timezone.utc)
        return last_modified_date > modified_after_date


class Connector(ABC):
    @abstractmethod
    def get_bucket_info(self, credentials: ConnectorCredentials, path: str) -> BucketInfo:
        pass


class GCSLocalConnector(Connector):
    def __init__(self, endpoint_url: str):
        self._endpoint_url = endpoint_url

    def get_bucket_info(self, _: ConnectorCredentials, path: str) -> BucketInfo:
        parsed_bucket_url = urlparse(path)
        bucket_service = parsed_bucket_url.scheme
        bucket_name = parsed_bucket_url.netloc

        # Check to see if there is a bucket specified or not
        if len(bucket_service) <= 0 or len(bucket_name) <= 0:
            raise MissingBucketPathOrSchemeException(DataSinkError.invalid_gcs_bucket_path(path=path).message)

        # Bucket Path needs to be relative because it's not
        # actually a FS path, but some string prefixes.
        # Stripping the leading / here coming from urlparse
        bucket_prefix = parsed_bucket_url.path[1:] if bucket_name else ""
        bucket_url = urljoin(self._endpoint_url, f"{bucket_name}{parsed_bucket_url.path}")
        return BucketInfo(name=bucket_name, prefix=bucket_prefix, url=bucket_url)


class S3LocalConnector(Connector):
    def __init__(self, endpoint_url: Optional[str] = None):
        self._endpoint_url = endpoint_url

    def get_bucket_info(self, credentials: ConnectorCredentials, path: str) -> BucketInfo:
        s3_credentials = cast(S3ConnectorCredentials, credentials)
        parsed_bucket_url = urlparse(path)
        bucket_service = parsed_bucket_url.scheme
        bucket_name = parsed_bucket_url.netloc

        # Check to see if there is a bucket specified or not
        if len(bucket_service) <= 0 or len(bucket_name) <= 0:
            raise MissingBucketPathOrSchemeException(DataSinkError.invalid_s3_bucket_path(path=path).message)

        # Bucket Path needs to be relative because it's not
        # actually a FS path, but some string prefixes.
        # Stripping the leading / here coming from urlparse
        bucket_prefix = parsed_bucket_url.path[1:] if bucket_name else ""
        if self._endpoint_url:
            url = "/".join(filter(None, [self._endpoint_url, bucket_name, bucket_prefix]))
        else:
            base_url = f"https://{bucket_name}.s3.{s3_credentials.region}.amazonaws.com"
            url = urljoin(base_url, parsed_bucket_url.path)
        return BucketInfo(name=bucket_name, prefix=bucket_prefix, url=url)


def build_longest_static_prefix_of_destination(prefix: str, file_template: str) -> str:
    folders = file_template.split("/")
    folder = folders[:-1]
    if "{" in file_template:
        last_static_item = next((i for i, part in enumerate(folders) if "{" in part), len(folders) - 1)
        folder = folder[:last_static_item]

    return os.path.join(prefix, *folder)


def local_connector_from_settings(settings: SinkConnectorSettings) -> Connector:
    if isinstance(settings, S3ConnectorSetting) or isinstance(settings, S3IAMConnectorSetting):
        return S3LocalConnector(endpoint_url=settings.endpoint_url)
    elif isinstance(settings, GCSHmacConnectorSetting) or isinstance(settings, GCSServiceAccountConnectorSetting):
        return GCSLocalConnector(endpoint_url=settings.endpoint_url)
    else:
        raise TypeError(f"Unsupported connector type: '{type(settings)}'")


def build_session_from_credentials(
    credentials: ConnectorCredentials,
    session_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> AWSSession | GCPSession:
    match credentials:
        case AccessKey():
            return StaticCredentialsAWSSession.from_access_key(credentials, endpoint_url=endpoint_url)
        case IAMRoleAWSCredentials(role_arn, external_id):
            aws_session = get_auth_provider().get_aws_session(session_name)
            return aws_session.assume_role(role_arn, external_id=external_id).with_endpoint_url(endpoint_url)
        case GCSServiceAccountCredentials(account_email):
            gcp_session = get_auth_provider().get_gcp_session()
            return gcp_session.impersonate_service_account(account_email)
        case _:
            raise TypeError(f"Unsupported credential type: {type(credentials)}")
