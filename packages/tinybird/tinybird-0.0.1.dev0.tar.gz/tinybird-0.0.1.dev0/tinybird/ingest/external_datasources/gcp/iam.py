import base64
import logging

import googleapiclient.errors
from googleapiclient.discovery import build as build_gcp_service


class GCPIAMClient:
    AUTH_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

    def __init__(self, project_id: str, credentials):
        self._project_id = project_id
        self._iam = build_gcp_service("iam", "v1", credentials=credentials)
        self._cloud_identity = build_gcp_service("cloudidentity", "v1", credentials=credentials)

    def get_or_create_service_account(self, name: str, display_name: str) -> str:
        req = (
            self._iam.projects()
            .serviceAccounts()
            .create(
                name=f"projects/{self._project_id}",
                body={"accountId": name, "serviceAccount": {"displayName": display_name}},
            )
        )
        try:
            return req.execute()["email"]
        except googleapiclient.errors.HttpError as httpe:
            if httpe.status_code == 409:  # Resource already exists
                return f"{name}@{self._project_id}.iam.gserviceaccount.com"
            logging.exception("Service account creation failed")
            raise

    def delete_service_account(self, account_email: str) -> None:
        """
        Deletes a service account. If the account doesn't exist then this is a no-op.
        Be careful not to call this twice or you might get a 403 error while the account is being deleted.
        """
        req = (
            self._iam.projects()
            .serviceAccounts()
            .delete(name=f"projects/{self._project_id}/serviceAccounts/{account_email}")
        )
        try:
            return req.execute()

        except googleapiclient.errors.HttpError as httperr:
            # If the account doesn't already exist then we're good
            if httperr.status_code == 404:
                return
            logging.exception("Service account creation failed")
            raise

    def generate_account_key(self, account_email: str) -> str:
        req = (
            self._iam.projects()
            .serviceAccounts()
            .keys()
            .create(
                name=f"projects/{self._project_id}/serviceAccounts/{account_email}",
                body={},
            )
        )
        res = req.execute()
        return base64.b64decode(res["privateKeyData"]).decode("utf-8")

    def add_account_to_group(self, group_email: str, account_email: str) -> None:
        group_name_req = self._cloud_identity.groups().lookup()
        # This is a terrible way to build the HTTP query but that's how it's done in google docs so :shrug:
        group_name_req.uri += f"&groupKey.id={group_email}"
        group_name = group_name_req.execute()["name"]  # If this is malformed blow up loudly
        membership = {"preferredMemberKey": {"id": account_email}, "roles": {"name": "MEMBER"}}
        req = self._cloud_identity.groups().memberships().create(parent=group_name, body=membership)
        try:
            req.execute()  # If we get a 409 then the account is already in the group
        except googleapiclient.errors.HttpError as httpe:
            if httpe.status_code == 409:  # Resource already exists
                return
            logging.exception("Unable to add account to group")
            raise


def get_iam_client(project_id: str, credentials_provider):
    credentials = credentials_provider(scopes=GCPIAMClient.AUTH_SCOPES)
    return GCPIAMClient(project_id, credentials)
