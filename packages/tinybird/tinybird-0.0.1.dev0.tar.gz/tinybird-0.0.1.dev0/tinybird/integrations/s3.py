import asyncio
import dataclasses
import logging
import random
import re
import uuid
from typing import Any, List, Optional, Tuple, cast

from tinybird.connector_settings import S3ConnectorSetting, S3IAMConnectorSetting
from tinybird.data_connector import DataConnector, DataLinker
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.providers.auth import get_auth_provider
from tinybird.providers.aws.s3 import check_signed_s3_url, get_signed_url, list_objects, parse_s3_url
from tinybird.providers.aws.session import AWSSession
from tinybird.user import User as Workspace

S3_REGEXP = r"s3://([^/]+)/"


class S3IntegrationException(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class AWSAccountPrincipal:
    account_id: str

    def render(self) -> str:
        return f"arn:aws:iam::{self.account_id}:root"


def _render_aws_policy(statements: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "Version": "2012-10-17",
        "Statement": statements,
    }


@dataclasses.dataclass(frozen=True)
class AWSRoleSettings:
    principal: AWSAccountPrincipal
    external_id: str

    def to_dict(self) -> dict:
        return {"principal": self.principal.render(), "external_id": self.external_id}


@dataclasses.dataclass(frozen=True)
class AWSAssumeRoleTrustPolicy:
    role_settings: AWSRoleSettings

    def render(self) -> dict[str, Any]:
        statement = {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Principal": {"AWS": self.role_settings.principal.render()},
            "Condition": {"StringEquals": {"sts:ExternalId": self.role_settings.external_id}},
        }
        return _render_aws_policy([statement])


@dataclasses.dataclass(frozen=True)
class AWSS3AccessWritePolicy:
    bucket: Optional[str] = None

    def render(self) -> dict[str, Any]:
        bucket = self.bucket or "<bucket>"
        bucket_statement = {
            "Effect": "Allow",
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": f"arn:aws:s3:::{bucket}",
        }
        contents_statement = {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject", "s3:PutObjectAcl"],
            "Resource": f"arn:aws:s3:::{bucket}/*",
        }
        statements = [bucket_statement, contents_statement]
        return _render_aws_policy(statements)


@dataclasses.dataclass(frozen=True)
class AWSS3AccessReadPolicy:
    bucket: Optional[str] = None

    def render(self) -> dict[str, Any]:
        bucket = self.bucket or "<bucket>"
        statements = [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    f"arn:aws:s3:::{bucket}",
                    f"arn:aws:s3:::{bucket}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:ListAllMyBuckets"],
                "Resource": "*",
            },
        ]
        return _render_aws_policy(statements)


def generate_external_id(workspace: Workspace) -> str:
    return _generate_deterministic_id_from_workspace(workspace, "external-id")


def get_aws_session_name(workspace: Workspace) -> str:
    return _generate_deterministic_id_from_workspace(workspace, "session-name")


async def get_assume_role_trust_policy(workspace: Workspace) -> AWSAssumeRoleTrustPolicy:
    role_settings = await get_s3_role_settings(workspace)
    return AWSAssumeRoleTrustPolicy(role_settings)


async def get_s3_role_settings(workspace: Workspace) -> AWSRoleSettings:
    aws_account_id = await asyncio.get_running_loop().run_in_executor(None, _get_aws_account_id)
    external_id = generate_external_id(workspace)
    principal = AWSAccountPrincipal(aws_account_id)
    return AWSRoleSettings(principal, external_id)


def get_s3_access_write_policy(bucket: Optional[str] = None) -> AWSS3AccessWritePolicy:
    return AWSS3AccessWritePolicy(bucket)


def get_s3_access_read_policy(bucket: Optional[str] = None) -> AWSS3AccessReadPolicy:
    return AWSS3AccessReadPolicy(bucket)


def validate_s3_bucket_name(bucket_name: str) -> bool:
    """
    Validate an S3 bucket name according to AWS S3 naming rules.

    Args:
        bucket_name (str): The S3 bucket name to validate.

    Returns:
        bool: True if the bucket name is valid, False otherwise.

    >>> validate_s3_bucket_name("my-bucket")
    True
    >>> validate_s3_bucket_name("my_bucket")
    True
    >>> validate_s3_bucket_name("s3://my-bucket")
    False
    >>> validate_s3_bucket_name("my-bucket")
    True
    >>> validate_s3_bucket_name("my.bucket")
    False
    >>> validate_s3_bucket_name("192.168.5.4")
    False
    >>> validate_s3_bucket_name("xn--my-bucket")
    False
    >>> validate_s3_bucket_name("sthree-my-bucket")
    False
    >>> validate_s3_bucket_name("my-bucket-s3alias")
    False
    >>> validate_s3_bucket_name("my-bucket--ol-s3")
    False
    >>> validate_s3_bucket_name("my.bucket.com")
    False
    >>> validate_s3_bucket_name("")
    False
    """

    # Check if bucket name starts with s3://
    if bucket_name.startswith("s3://"):
        return False

    # Check length
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Check if bucket name starts or ends with a dot
    if bucket_name.startswith(".") or bucket_name.endswith("."):
        return False

    # Check if bucket name contains two adjacent periods
    if ".." in bucket_name:
        return False

    # Check if bucket name starts with the prefix xn--
    if bucket_name.startswith("xn--"):
        return False

    # Check if bucket name starts with the prefix sthree- or sthree-configurator
    if bucket_name.startswith("sthree-") or bucket_name.startswith("sthree-configurator"):
        return False

    # Check if bucket name ends with the suffix -s3alias or --ol-s3
    if bucket_name.endswith("-s3alias") or bucket_name.endswith("--ol-s3"):
        return False

    # Check if bucket name is formatted as an IP address
    ip_pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    if ip_pattern.match(bucket_name):
        return False

    # Check if bucket name starts and ends with a letter or number
    if not bucket_name[0].isalnum() or not bucket_name[-1].isalnum():
        return False

    # Check if bucket name contains dots when used with Transfer Acceleration
    if "." in bucket_name:
        # Assume that Transfer Acceleration is enabled
        return False

    return True


def _get_aws_account_id() -> str:
    session = get_auth_provider().get_aws_session()
    return session.get_caller_identity().account_id


def _generate_deterministic_id_from_workspace(workspace: Workspace, name: str) -> str:
    rnd = random.Random()
    # We use workspace.origin if available
    # to generate the same External ID for
    # the main workspace and all their envs
    workspace_id = workspace.origin if workspace.origin else workspace.id
    seed_str = f"tb-{name}-{workspace_id}"
    rnd.seed(seed_str)
    return str(uuid.UUID(int=rnd.getrandbits(128), version=4))


async def sign_s3_url(connector_id: str, workspace: Workspace, url: str, job_id: Optional[str] = None) -> str | None:
    data_connector = DataConnector.get_by_id(connector_id)
    if not data_connector:
        return None
    settings = cast(S3IAMConnectorSetting, data_connector.validated_settings)
    bucket_name, file_name = parse_s3_url(url)
    session = build_session_from_credentials(settings.credentials, session_name=get_aws_session_name(workspace))
    if isinstance(session, AWSSession):
        signed_url, endpoint_url = await asyncio.to_thread(
            get_signed_url,
            session=session,
            bucket_name=bucket_name,
            file_name=file_name,
            region=settings.s3_iamrole_region
            if isinstance(settings, S3IAMConnectorSetting)
            else cast(S3ConnectorSetting, settings).s3_region,
            endpoint_url=settings.endpoint_url,
        )
        signed, status = await check_signed_s3_url(signed_url)
        if not signed:
            logging.warning(
                f"s3 URL workspace_id={workspace.id} job_id={job_id or ''} connector_id={connector_id} status_code={status} - endpoint_url={endpoint_url} signed_url={signed_url}"
            )
        else:
            return signed_url
    # we still need to implement this for GCS https://gitlab.com/tinybird/analytics/-/issues/14206
    return None


def get_data_connector(workspace: Workspace, datasource_id: str) -> Tuple[DataConnector, DataLinker]:
    datasource = workspace.get_datasource(datasource_id)
    if datasource is None:
        raise ValueError(f"Data Source not found: {datasource_id}")

    data_linker = datasource.get_data_linker()
    if data_linker is None or data_linker.data_connector_id is None:
        raise ValueError(f"Data Linker for Data Source not found: {datasource_id}")

    data_connector = DataConnector.get_by_id(data_linker.data_connector_id)
    if data_connector is None:
        raise ValueError(f"Data Connector for Data Linker not found: {datasource_id} - {data_linker.id}")
    return data_connector, data_linker


async def get_files_in_bucket(workspace_id: str, datasource_id: str):
    files: List[dict[str, Any]] = []
    workspace = Workspace.get_by_id(workspace_id)
    assert isinstance(workspace, Workspace)
    data_connector, data_linker = get_data_connector(workspace, datasource_id)

    settings = cast(S3IAMConnectorSetting, data_connector.validated_settings)
    session = await asyncio.to_thread(
        build_session_from_credentials, settings.credentials, session_name=get_aws_session_name(workspace)
    )
    assert isinstance(session, AWSSession)
    bucket_uri = data_linker.settings["bucket_uri"]
    if not bucket_uri:
        raise ValueError("bucket_uri is empty")
    # !! change to gc:// if using google cloud
    try:
        matches = re.match(S3_REGEXP, bucket_uri)
        if not matches:
            raise S3IntegrationException(
                f"Error parsing bucket_uri in workspace_id={workspace_id}, and datasource_id={datasource_id} for {data_linker.settings['bucket_uri']}"
            )
        bucket_name = matches.group(1)
        prefix = "/".join(bucket_uri.split("//")[1].split("/")[1:-1])
    except AttributeError as e:
        logging.exception(e)
        raise S3IntegrationException(
            f"Error parsing bucket_uri in workspace_id={workspace_id}, and datasource_id={datasource_id} for {data_linker.settings['bucket_uri']}"
        )

    logging.info(f"Getting list of files for {workspace.name} in bucket {bucket_name}/{prefix}...")
    region = (
        settings.s3_iamrole_region
        if isinstance(settings, S3IAMConnectorSetting)
        else cast(S3ConnectorSetting, settings).s3_region
    )
    listed = await asyncio.to_thread(list_objects, session, bucket_name, prefix, region=region)
    for obj in listed:
        files.append(
            {
                "key": obj.key,
                "last_modified": obj.last_modified.isoformat(),
                "workspace_id": workspace_id,
                "datasource_id": datasource_id,
                "bucket_uri": bucket_uri,
            }
        )

    while len(listed) == 1000:
        start_after = listed[-1].key
        listed = await asyncio.to_thread(
            list_objects, session, bucket_name, prefix, region=settings.s3_iamrole_region, start_after=start_after
        )
        for obj in listed:
            files.append(
                {
                    "key": obj.key,
                    "last_modified": obj.last_modified,
                    "workspace_id": workspace_id,
                    "datasource_id": datasource_id,
                    "bucket_uri": bucket_uri,
                }
            )
    logging.info(f"Listed files under <1000 => len listed={len(listed)}")
    return files
