import dataclasses
import logging
import uuid
from typing import Any, Optional, Protocol, runtime_checkable

import boto3
import botocore
from botocore.config import Config

from tinybird.providers.aws.credentials import AccessKeyCredentials, TemporaryAWSCredentials
from tinybird.providers.aws.exceptions import (
    CredentialsNotFound,
    ExpiredToken,
    InvalidClientTokenID,
    InvalidIdentityToken,
    InvalidRegionName,
    InvalidRoleARN,
    MalformedAWSAPIResponse,
    UnableToAssumeRole,
    UnexpectedBotoClientError,
)


@runtime_checkable
class AccessKey(Protocol):
    access_key_id: str
    secret_access_key: str


@dataclasses.dataclass(frozen=True)
class CallerIdentity:
    user_id: str
    account_id: str


@runtime_checkable
class AWSSession(Protocol):
    def client(
        self, service: str, region: Optional[str] = None, endpoint_url: Optional[str] = None
    ):  # No type because boto3 doesn't believe in them.
        ...

    def get_credentials(self) -> AccessKeyCredentials | TemporaryAWSCredentials: ...


class AuthenticatedAWSSession(AWSSession):
    def __init__(
        self, session: boto3.Session, session_name: Optional[str] = None, endpoint_url: Optional[str] = None
    ) -> None:
        self._session = session
        self._session_name = session_name or f"tb-session-{uuid.uuid4()}"
        self._endpoint_url = endpoint_url

    def with_endpoint_url(self, endpoint_url: Optional[str]) -> "AuthenticatedAWSSession":
        return AuthenticatedAWSSession(self._session, self._session_name, endpoint_url=endpoint_url)

    def client(self, service: str, region: Optional[str] = None, endpoint_url: Optional[str] = None):
        # Ensure that the session has some credentials by forcing a refresh
        if not self._session.get_credentials():
            raise CredentialsNotFound()
        return _build_client(self._session, service, region=region, endpoint_url=endpoint_url or self._endpoint_url)

    def assume_role(self, role_arn: str, external_id: Optional[str] = None) -> "AuthenticatedAWSSession":
        tmp_credentials = self._assume_role(role_arn, external_id=external_id)
        return self._session_from_tmp_credentials(tmp_credentials)

    def assume_role_with_web_identity(self, role_arn: str, web_identity_token: str) -> "AuthenticatedAWSSession":
        tmp_credentials = self._assume_role_with_web_identity(role_arn, web_identity_token)
        return self._session_from_tmp_credentials(tmp_credentials)

    def get_credentials(self) -> TemporaryAWSCredentials:
        frozen_credentials = self._session.get_credentials().get_frozen_credentials()
        return TemporaryAWSCredentials(
            access_key_id=frozen_credentials.access_key,
            secret_access_key=frozen_credentials.secret_key,
            session_token=frozen_credentials.token,
        )

    def get_caller_identity(self) -> CallerIdentity:
        try:
            res = self.client("sts").get_caller_identity()
        except botocore.exceptions.NoCredentialsError as err:
            raise CredentialsNotFound(err) from err
        try:
            return CallerIdentity(user_id=res["UserId"], account_id=res["Account"])
        except KeyError as err:
            raise MalformedAWSAPIResponse(err) from err

    def _assume_role(self, role_arn: str, external_id: Optional[str] = None) -> TemporaryAWSCredentials:
        sts = self.client("sts")
        args = {"RoleArn": role_arn, "RoleSessionName": self._session_name, "ExternalId": external_id}
        try:
            res = sts.assume_role(**{k: v for k, v in args.items() if v is not None})
        except botocore.exceptions.ParamValidationError as err:
            # Get only the second line of the error which contains the useful info
            err_msg = f"Invalid role ARN length: {len(role_arn)}. Min valid length: 20."
            raise InvalidRoleARN(err_msg) from err
        except botocore.exceptions.ClientError as err:
            _handle_assume_role_botocore_client_errors(err)

        return _parse_assume_role_response(res)

    def _assume_role_with_web_identity(self, role_arn: str, web_identity_token: str) -> TemporaryAWSCredentials:
        sts = _build_client(self._session, "sts", None, None)
        try:
            res = sts.assume_role_with_web_identity(
                RoleArn=role_arn,
                RoleSessionName=self._session_name,
                WebIdentityToken=web_identity_token,
            )
        except botocore.exceptions.ParamValidationError as err:
            # Get only the second line of the error which contains the useful info
            err_msg = f"Invalid role ARN length: {len(role_arn)}. Min valid length: 20."
            raise InvalidRoleARN(err_msg) from err
        except sts.exceptions.InvalidIdentityTokenException as err:
            raise InvalidIdentityToken(err) from err
        except sts.exceptions.ExpiredTokenException as err:
            raise ExpiredToken() from err
        except botocore.exceptions.ClientError as err:
            _handle_assume_role_botocore_client_errors(err)

        return _parse_assume_role_response(res)

    def _session_from_tmp_credentials(self, credentials: TemporaryAWSCredentials) -> "AuthenticatedAWSSession":
        assume_role_session = boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            aws_session_token=credentials.session_token,
        )
        return AuthenticatedAWSSession(assume_role_session, self._session_name, endpoint_url=self._endpoint_url)


class StaticCredentialsAWSSession(AWSSession):
    """
    Wraps a set of long-lived credentials and allows creating clients & retrieving keys using them.
    """

    def __init__(self, session: boto3.Session, endpoint_url: Optional[str] = None) -> None:
        self._session = session
        self._endpoint_url = endpoint_url

    def client(self, service: str, region: Optional[str] = None, endpoint_url: Optional[str] = None):
        return _build_client(self._session, service, region=region, endpoint_url=endpoint_url or self._endpoint_url)

    def get_credentials(self) -> AccessKeyCredentials:
        frozen_credentials = self._session.get_credentials().get_frozen_credentials()
        return AccessKeyCredentials(
            access_key_id=frozen_credentials.access_key,
            secret_access_key=frozen_credentials.secret_key,
        )

    def with_endpoint_url(self, endpoint_url: Optional[str]) -> "StaticCredentialsAWSSession":
        return StaticCredentialsAWSSession(self._session, endpoint_url=endpoint_url)

    @classmethod
    def from_access_key(
        cls, access_key: AccessKey, endpoint_url: Optional[str] = None
    ) -> "StaticCredentialsAWSSession":
        boto3_session = boto3.Session(
            aws_access_key_id=access_key.access_key_id,
            aws_secret_access_key=access_key.secret_access_key,
        )
        return StaticCredentialsAWSSession(boto3_session, endpoint_url=endpoint_url)


def _build_client(session: boto3.Session, service: str, region: Optional[str], endpoint_url: Optional[str]):
    try:
        return session.client(
            service, region_name=region, endpoint_url=endpoint_url, config=Config(signature_version="v4")
        )
    except botocore.exceptions.InvalidRegionError as err:
        raise InvalidRegionName(err) from err


def _handle_assume_role_botocore_client_errors(err: botocore.exceptions.ClientError) -> None:
    err_code = err.response.get("Error", {}).get("Code")
    err_msg = err.response.get("Error", {}).get("Message")
    if "AccessDenied" == err_code:
        err_msg = "Access denied while attempting to assume role. Please ensure that the provided role ARN and external ID are correct."
        raise UnableToAssumeRole(err_msg) from err
    elif "ValidationError" == err_code:
        raise InvalidRoleARN("Invalid role ARN") from err
    elif "InvalidClientTokenId" == err_code:
        raise InvalidClientTokenID(err) from err
    else:
        logging.error(err_msg)
        raise UnexpectedBotoClientError() from err


def _parse_assume_role_response(res: dict[str, Any]) -> TemporaryAWSCredentials:
    try:
        return TemporaryAWSCredentials(
            access_key_id=res["Credentials"]["AccessKeyId"],
            secret_access_key=res["Credentials"]["SecretAccessKey"],
            session_token=res["Credentials"]["SessionToken"],
        )
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err
