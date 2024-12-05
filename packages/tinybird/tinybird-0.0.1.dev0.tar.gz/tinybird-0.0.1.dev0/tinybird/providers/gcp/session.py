import typing

import google.auth.exceptions
import google.auth.impersonated_credentials
import google.auth.transport.requests
import google.oauth2.service_account

ImpersonatedGCPCredentials: typing.TypeAlias = google.auth.impersonated_credentials.Credentials
ServiceAccountGCPCredentials: typing.TypeAlias = google.oauth2.service_account.Credentials

GCPCredentials = ServiceAccountGCPCredentials | ImpersonatedGCPCredentials

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


class GCPSession:
    def __init__(self, credentials: GCPCredentials) -> None:
        self._credentials = credentials

    def impersonate_service_account(self, account_email: str) -> "GCPSession":
        credentials = ImpersonatedGCPCredentials(
            source_credentials=self._credentials,
            target_principal=account_email,
            target_scopes=DEFAULT_SCOPES,
        )
        req = google.auth.transport.requests.Request()
        # Throws: google.auth.exceptions.RefreshError
        credentials.refresh(req)  # Refresh to ensure that it works
        return GCPSession(credentials)

    def get_credentials(self) -> GCPCredentials:
        return self._credentials
