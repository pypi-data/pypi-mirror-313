import asyncio
import functools
import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict

import google.api_core.exceptions
import google.auth
import google.auth.exceptions
import google.cloud.storage
import googleapiclient.errors
from google.auth.transport.requests import AuthorizedSession

from tinybird.ingest.cdk_utils import CDKUtils
from tinybird.ingest.external_datasources.gcp.iam import get_iam_client
from tinybird.user import User as Workspace
from tinybird.user import Users as Workspaces


class ExternalDatasourceIntegrationProvisioningFailed(Exception):
    pass


def generate_account_name(workspace_id: str):
    return f"cdk-E-{workspace_id[:16]}-{hashlib.sha224(workspace_id.encode()).hexdigest()[:6]}"


def grant_bucket_write_permissions_to_account(
    credentials_provider, project_id: str, bucket_name: str, account_email: str
) -> None:
    credentials = credentials_provider(scopes=["https://www.googleapis.com/auth/devstorage.full_control"])
    bucket = google.cloud.storage.Client(credentials=credentials, project=project_id).bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": "roles/storage.admin", "members": {f"serviceAccount:{account_email}"}})
    bucket.set_iam_policy(policy)


def create_composer_pool(credentials_provider, webserver_url: str, name: str) -> None:
    session = AuthorizedSession(credentials_provider(scopes=["https://www.googleapis.com/auth/cloud-platform"]))
    res = session.post(f"{webserver_url}/api/v1/pools", json={"name": f"{name}_pool", "slots": 5})
    if res.status_code == 409:  # If the pool already exists just return
        return
    res.raise_for_status()


def schedule(pool: ThreadPoolExecutor, func: Callable):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        prepared_func = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(pool, prepared_func)

    return inner


async def _provision_workspace_service_account(workspace: Workspace) -> Dict:
    iam = get_iam_client(CDKUtils.get_project_id(), CDKUtils.get_credentials_provider())
    account_name = generate_account_name(workspace.id)
    with ThreadPoolExecutor(1) as pool:
        account_email = await schedule(pool, iam.get_or_create_service_account)(account_name, workspace.id)
        # NOTICE: to be able to do that, the service account used to create the iam client above
        # needs to have `Manager` permissions in the group email defined by `CDKUtils.get_group_email()`
        # here: https://console.cloud.google.com/iam-admin/groups
        await schedule(pool, iam.add_account_to_group)(CDKUtils.get_group_email(), account_email)
        await schedule(pool, create_composer_pool)(
            CDKUtils.get_credentials_provider(), CDKUtils.cdk_webserver_url, workspace.id
        )
        key_info = await schedule(pool, iam.generate_account_key)(account_email)
    account_details = {"service_account_id": account_email, "key": key_info}
    return account_details


async def provision_workspace_service_account(workspace: Workspace) -> Dict:
    try:
        account_details = await _provision_workspace_service_account(workspace)
    except (
        google.auth.exceptions.GoogleAuthError,  # Credentials are wrong
        google.api_core.exceptions.GoogleAPICallError,  # 4xx & 5xx from the google cloud api client
        googleapiclient.errors.Error,  # Anything from the google legacy api client
    ) as err:
        logging.exception("External datasource integration provisioning failed")  # Log the exception
        raise ExternalDatasourceIntegrationProvisioningFailed() from err
    Workspaces.alter_cdk_gcp_service_account(workspace, account_details)
    return account_details


async def get_or_create_workspace_service_account(workspace: Workspace) -> Dict:
    if not (account_info := workspace.cdk_gcp_service_account):
        account_info = await provision_workspace_service_account(workspace)
    return account_info


async def delete_workspace_service_account(workspace: Workspace) -> None:
    if not (account_info := workspace.cdk_gcp_service_account):
        logging.info(
            f"GCP Service account deletion was requested for workspace '{workspace.id}' but it did not have an associated account.",
        )
        return

    email = workspace.cdk_gcp_service_account.get("client_email")
    iam = get_iam_client(CDKUtils.get_project_id(), CDKUtils.get_credentials_provider())
    with ThreadPoolExecutor(1) as pool:
        await schedule(pool, iam.delete_service_account)(account_info["service_account_id"])

    logging.info(
        f"GCP Service account '{email}' was deleted for workspace '{workspace.id}'.",
    )
    Workspaces.alter_cdk_gcp_service_account(workspace, None)
