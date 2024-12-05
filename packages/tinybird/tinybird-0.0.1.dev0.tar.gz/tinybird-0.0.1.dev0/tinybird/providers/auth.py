import logging
import uuid
from typing import Optional, Protocol

import boto3
from google.oauth2.service_account import Credentials as ServiceAccountGCPCredentials

from tinybird.providers.aws.exceptions import AWSClientException
from tinybird.providers.aws.session import AuthenticatedAWSSession
from tinybird.providers.gcp.auth import get_id_token_from_metadata_server
from tinybird.providers.gcp.exceptions import AuthenticationFailed as GCPAuthenticationFailed
from tinybird.providers.gcp.session import GCPSession

AWS_STS_TARGET_AUDIENCE = "sts.amazonaws.com"


class AuthProviderException(Exception):
    pass


class AuthProviderNotSet(AuthProviderException):
    pass


class UnableToCreateAWSSession(AuthProviderException):
    pass


class AuthenticationProvider(Protocol):
    def get_aws_session(self, session_name: Optional[str] = None) -> AuthenticatedAWSSession: ...

    def get_gcp_session(self) -> GCPSession: ...


class GCPAuthenticationProvider(AuthenticationProvider):
    def __init__(self, deputy_aws_role_arn: str, deputy_gcp_service_account_credentials_file: str) -> None:
        self._deputy_aws_role_arn = deputy_aws_role_arn
        self._deputy_gcp_service_account_credentials_file = deputy_gcp_service_account_credentials_file

    def get_aws_session(self, session_name: Optional[str] = None) -> AuthenticatedAWSSession:
        base_session = AuthenticatedAWSSession(boto3.Session(), session_name or _generate_random_session_name())
        try:
            id_token = get_id_token_from_metadata_server(AWS_STS_TARGET_AUDIENCE)
            return base_session.assume_role_with_web_identity(
                role_arn=self._deputy_aws_role_arn,
                web_identity_token=id_token,
            )
        except (GCPAuthenticationFailed, AWSClientException) as err:
            logging.exception("Unable to build AWS session for instance")
            raise UnableToCreateAWSSession() from err

    def get_gcp_session(self) -> GCPSession:
        credentials = ServiceAccountGCPCredentials.from_service_account_file(
            self._deputy_gcp_service_account_credentials_file
        )
        return GCPSession(credentials)


class AWSAuthenticationProvider(AuthenticationProvider):
    def get_aws_session(self, session_name: Optional[str] = None) -> AuthenticatedAWSSession:
        session = AuthenticatedAWSSession(boto3.Session(), session_name or _generate_random_session_name())
        try:
            session.client("sts")  # Spawn a client to force a credential refresh and trigger any exceptions
        except AWSClientException as err:
            logging.exception("Unable to build AWS session for instance")
            raise UnableToCreateAWSSession("Unable to build AWS session for instance") from err
        return session

    def get_gcp_session(self) -> GCPSession:
        raise NotImplementedError()


class UnsetAuthProvider(AuthenticationProvider):
    def get_aws_session(self, _: Optional[str] = None) -> AuthenticatedAWSSession:
        raise NotImplementedError()

    def get_gcp_session(self) -> GCPSession:
        raise NotImplementedError()


_auth_provider: AuthenticationProvider = UnsetAuthProvider()


def register_auth_provider(provider: AuthenticationProvider) -> None:
    global _auth_provider
    _auth_provider = provider


def unregister_auth_provider() -> None:
    global _auth_provider
    _auth_provider = UnsetAuthProvider()


def get_auth_provider() -> AuthenticationProvider:
    if isinstance(_auth_provider, UnsetAuthProvider):
        raise AuthProviderNotSet()
    else:
        return _auth_provider


def _generate_random_session_name() -> str:
    return f"tb-session-{uuid.uuid4()}"
