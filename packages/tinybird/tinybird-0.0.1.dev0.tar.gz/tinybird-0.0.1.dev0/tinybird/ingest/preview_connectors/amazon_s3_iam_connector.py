import concurrent.futures
import logging
import math
import multiprocessing
import re
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, cast
from urllib.parse import urlparse

from botocore.exceptions import BotoCoreError, ClientError
from dateutil import parser

from tinybird.data_connector import DataConnectors
from tinybird.data_connectors.credentials import ConnectorCredentials, IAMRoleAWSCredentials
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.ingest.data_connectors import (
    ConnectorException,
    ConnectorParameters,
    S3ConnectorParameters,
    S3IAMConnectorParameters,
)
from tinybird.ingest.preview_connectors.base_connector import BasePreviewConnector, PreviewConnectorMock
from tinybird.ingest.preview_connectors.exceptions import RequestsLimitExceededException
from tinybird.integrations.s3 import get_aws_session_name
from tinybird.limits import (
    MAX_SIZE_URL_FILE_BYTES,
    MAX_SIZE_URL_FILE_DEV_BYTES,
    MAX_SIZE_URL_PARQUET_FILE_BYTES,
    MAX_SIZE_URL_PARQUET_FILE_DEV_BYTES,
)
from tinybird.providers.aws.session import AWSSession
from tinybird.user import User as Workspace


class S3IAMPreviewConnector(BasePreviewConnector):
    def __init__(self, custom_preview: bool = False):
        super().__init__()
        self.connector = DataConnectors.AMAZON_S3_IAMROLE
        self.custom_preview = custom_preview

    def make_credentials(self, credentials: ConnectorCredentials) -> dict[str, Any]:
        return {
            "role_arn": cast(IAMRoleAWSCredentials, credentials).role_arn,
            "external_id": cast(IAMRoleAWSCredentials, credentials).external_id,
            "region": cast(IAMRoleAWSCredentials, credentials).region,
        }

    def make_parameters(self, parameters: ConnectorParameters) -> dict[str, Any]:
        params = {
            "bucketUrl": cast(S3IAMConnectorParameters, parameters).bucket_uri,
        }
        if (from_time := cast(S3IAMConnectorParameters, parameters).from_time) is not None:
            params["from"] = from_time
        if (file_format := cast(S3IAMConnectorParameters, parameters).file_format) is not None:
            params["format"] = file_format
        if (sample_file_uri := cast(S3IAMConnectorParameters, parameters).sample_file_uri) is not None:
            params["sample_file_uri"] = sample_file_uri
        return params

    async def preview_summary(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, Any]:
        results: dict[str, Any] = {}
        if self.custom_preview:
            # TODO: change this value to a config chosen one
            max_workers = math.floor(multiprocessing.cpu_count() / 2)
            workspace = Workspace.get_by_id(workspace_id)
            # The 40 requests per thread limit is chosen considering that, worse case, one response could cost us 800 ms
            # to 1min depending on the region of the bucket and our cluster's region. Best case, seems to be 100 ms.
            # In order to avoid reaching nginx's limits we lowered the requests_limit to accommodate this delta
            results = await custom_preview_summary(
                credentials=credentials,
                parameters=parameters,
                match_limit=20,
                requests_limit=40,
                max_workers=max_workers,
                workspace=workspace,
            )
        else:
            results = await super().preview_summary(
                credentials=credentials,
                tb_token=tb_token,
                tb_endpoint=tb_endpoint,
                parameters=parameters,
                workspace_id=workspace_id,
                working_zone=working_zone,
            )
        return results


async def custom_preview_summary(
    credentials: ConnectorCredentials,
    parameters: ConnectorParameters,
    max_workers: int,
    workspace: Workspace,
    match_limit: int = -1,
    requests_limit: int = 40,
) -> dict[str, Any]:
    try:
        aws_session = cast(
            AWSSession,
            build_session_from_credentials(credentials=credentials, session_name=get_aws_session_name(workspace)),
        )
        s3_client = aws_session.client("s3", cast(IAMRoleAWSCredentials, credentials).region)

        bucket_uri = cast(S3ConnectorParameters, parameters).bucket_uri
        prefix, pattern = get_prefix_and_pattern(bucket_uri)

        file_format = (
            cast(S3IAMConnectorParameters, parameters).file_format
            if cast(S3IAMConnectorParameters, parameters).file_format is not None
            else get_file_extension(bucket_uri=bucket_uri)
        )

        from_time_str = cast(S3ConnectorParameters, parameters).from_time
        from_time: Optional[datetime] = None
        if from_time_str:
            # TODO: check how this is integrating with the UI
            from_time = parser.isoparse(from_time_str)
            if from_time.tzinfo is None:
                from_time = from_time.replace(tzinfo=timezone.utc)
            else:
                from_time = from_time.astimezone(timezone.utc)

        sample_file_uri = cast(S3IAMConnectorParameters, parameters).sample_file_uri
        results: dict[str, Any] = {"contents": []}
        if sample_file_uri:
            file_metadata = get_file_metadata(s3_client, sample_file_uri)
            if file_metadata:
                results["contents"].append(file_metadata)
        else:
            results = get_matching_files(
                s3_client=s3_client,
                bucket=get_bucket_name(bucket_uri),
                match_limit=match_limit,
                requests_limit=requests_limit,
                prefix=prefix,
                delimiter="/",
                pattern=pattern,
                workspace=workspace,
                file_format=file_format,
                from_time=from_time,
                max_workers=max_workers,
            )

        matching_files: dict[str, Any] = {
            "files": results["contents"][:match_limit] if match_limit > 0 else results["contents"],
            "errors": results["errors"] if results.get("errors") else [],
        }

        return matching_files
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error assuming IAM role: {e}")
        raise Exception(f"Failed to assume IAM role: {str(e)}")


def get_matching_files(
    s3_client,
    bucket: str,
    match_limit: int,
    requests_limit: int,
    max_workers: int,
    pattern: str,
    workspace: Workspace,
    file_format: str,
    prefix: str = "",
    delimiter: str = "/",
    from_time: Optional[datetime] = None,
) -> Dict[str, List[Any]]:
    objects = []
    processed_prefixes = set()
    tasks = set()

    total_matches = [0]
    matches_found_event = threading.Event()
    thread_requests: Dict[int, int] = {}
    lock = threading.Lock()
    limit_reached = False
    size_limit_reached = False
    file_size_limit = get_file_size_limit(workspace, file_format)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks.add(
            executor.submit(
                list_objects,
                s3_client,
                bucket,
                prefix,
                delimiter,
                pattern,
                from_time,
                match_limit,
                requests_limit,
                total_matches,
                matches_found_event,
                thread_requests,
                lock,
                file_size_limit,
            )
        )

        while tasks and not matches_found_event.is_set():
            done, _ = concurrent.futures.wait(tasks, return_when=concurrent.futures.FIRST_COMPLETED)

            for future in done:
                try:
                    result = future.result()
                    if result.get("error"):
                        errors: List[str] = cast(List[str], result.get("error"))
                        raise ConnectorException(errors[0] if errors else "")
                except RequestsLimitExceededException:
                    logging.debug(f"A thread exceeded its requests limit for: {thread_requests}")
                    limit_reached = True
                    continue

                if result.get("size_limit_reached"):
                    size_limit_reached = True

                objects.extend(result["Contents"])

                if 0 < match_limit <= total_matches[0]:
                    matches_found_event.set()
                    break

                new_tasks = set()
                for common_prefix in result["CommonPrefixes"]:
                    next_prefix = common_prefix["Prefix"]
                    if next_prefix not in processed_prefixes:
                        processed_prefixes.add(next_prefix)
                        new_tasks.add(
                            executor.submit(
                                list_objects,
                                s3_client,
                                bucket,
                                next_prefix,
                                delimiter,
                                pattern,
                                from_time,
                                match_limit,
                                requests_limit,
                                total_matches,
                                matches_found_event,
                                thread_requests,
                                lock,
                                file_size_limit,
                            )
                        )

                tasks.update(new_tasks)
            tasks -= done

    results = {"contents": objects}
    errors = []

    if limit_reached and not objects:
        errors.append(
            "Exceeded requests limit before finding any matches. "
            "Consider broadening your pattern to capture more files."
        )
    elif limit_reached and len(objects) < match_limit:
        errors.append(
            "Preview limit reached: Showing partial results. Proceeding with the setup will "
            "process all matching files without limits. Adjust your pattern for a more complete preview."
        )

    if size_limit_reached and not objects:
        errors.append(
            "Exceeded file size limits before finding any matches. "
            "Check our documentation to see file size limits per plan."
        )
    elif size_limit_reached and len(objects) <= match_limit:
        errors.append(
            "Preview limit reached: Showing partial results. Proceeding with the setup will process all matching"
            " files that comply with your plan's size limits. Check size limits"
        )

    if errors:
        results["errors"] = errors

    return results


def list_objects(
    s3_client,
    bucket: str,
    prefix: str,
    delimiter: str,
    pattern: str,
    from_time: Optional[datetime],
    match_limit: int,
    requests_limit: int,
    total_matches: List[int],
    matches_found_event: threading.Event,
    thread_requests: Dict[int, int],
    lock: threading.Lock,
    file_size_limit: int,
) -> Dict[str, List[Any]]:
    paginator = s3_client.get_paginator("list_objects_v2")
    objects = []
    prefixes = []
    thread_id = threading.get_ident()
    size_limit_reached = False

    with lock:
        current_thread_requests = thread_requests.get(thread_id, 0)
        if current_thread_requests >= requests_limit:
            raise RequestsLimitExceededException(
                f"Thread exceeded its requests limit ({requests_limit}) before finding sufficient matches."
            )
    try:
        for response in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter):
            with lock:
                thread_requests[thread_id] = thread_requests.get(thread_id, 0) + 1

            if matches_found_event.is_set():
                break

            for obj in response.get("Contents", []):
                key = obj["Key"]
                last_modified = obj["LastModified"]
                size = obj["Size"]

                if from_time and last_modified < from_time:
                    continue

                if not full_match(key, pattern):
                    continue

                if size <= file_size_limit:
                    objects.append({"name": key, "size": size})
                    with lock:
                        total_matches[0] += 1
                        if 0 < match_limit <= total_matches[0]:
                            # This set() seems redundant because we are already doing it in the caller.
                            # matches_found_event.set()
                            break
                else:
                    size_limit_reached = True
                    continue

            prefixes.extend(response.get("CommonPrefixes", []))
    except ClientError as e:
        # There is no other, more granular way to distinguish between client errors.
        # AWS documentation states that this is how errors are supposed to be processed for granularity.
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html#discerning-useful-information-from-error-responses
        if e.response["Error"]["Code"] == "NoSuchBucket":
            message = f"Bucket does not exist : {bucket}"
        else:
            message = f"Error listing objects in bucket {bucket}. {e.response['Error']['Message']}"
        return {"error": [message]}
    except BotoCoreError as e:
        message = f"Error listing objects for prefix {prefix} in bucket {bucket}"
        logging.error(f"{message} : {e}")
        return {"error": [message]}
    if size_limit_reached:
        return {"Contents": objects, "CommonPrefixes": prefixes, "size_limit_reached": [str(size_limit_reached)]}

    return {"Contents": objects, "CommonPrefixes": prefixes}


def get_file_metadata(s3_client, file_uri: str) -> Optional[Dict[str, Any]]:
    parsed_uri = urlparse(file_uri)
    bucket_name = parsed_uri.netloc
    key = parsed_uri.path.lstrip("/")
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=key)
        metadata = {
            "name": key,
            "size": response["ContentLength"],
        }
        return metadata
    except s3_client.exceptions.NoSuchKey:
        logging.error(f"Sample file {file_uri} does not exist.")
    return None


def get_file_size_limit(workspace: Workspace, file_format: str) -> int:
    size_limit = None
    if file_format in ("parquet", "parquet.gz"):
        size_limit = MAX_SIZE_URL_PARQUET_FILE_BYTES if workspace.plan != "dev" else MAX_SIZE_URL_PARQUET_FILE_DEV_BYTES
    else:
        size_limit = MAX_SIZE_URL_FILE_BYTES if workspace.plan != "dev" else MAX_SIZE_URL_FILE_DEV_BYTES

    return size_limit


def get_bucket_name(bucket_uri: str) -> str:
    parsed = urlparse(bucket_uri)
    return parsed.netloc


def get_file_extension(bucket_uri: str) -> str:
    last_part = bucket_uri.split("/")[-1]

    if "." in last_part:
        return ".".join(last_part.split(".")[1:])

    # TODO: this should return an error to the user
    return ""


def get_prefix_and_pattern(bucket_uri: str) -> Tuple[str, str]:
    parsed = urlparse(bucket_uri)
    path = parsed.path.lstrip("/")
    if not path:
        return "", "*"
    wildcard_match = re.search(r"[\*\?]", path)
    if wildcard_match:
        wildcard_index = wildcard_match.start()
        prefix = path[:wildcard_index]
        pattern = path
    else:
        prefix = path
        pattern = path
    return prefix, glob_to_regex(pattern)


def full_match(key, pattern) -> bool:
    """
    TODO: replace this and glob_to_regex with full_match when migrating to a >= 3.13 python version
    Both methods are a simplified version of this chain https://github.com/python/cpython/blob/main/Lib/glob.py#L323 and
    https://github.com/python/cpython/blob/main/Lib/glob.py#L267
    """
    return re.match(pattern, key) is not None


def glob_to_regex(pat):
    res = ""
    i, n = 0, len(pat)
    while i < n:
        if pat[i] == "*":
            if i + 1 < n and pat[i + 1] == "*":
                i += 1
                if i + 1 < n and pat[i + 1] == "/":
                    i += 1
                    res += "(?:.*/)?"
                else:
                    res += ".*"
            else:
                res += "[^/]*"
        elif pat[i] == "?":
            res += "[^/]"
        elif pat[i] == "/":
            res += "/"
        else:
            res += re.escape(pat[i])
        i += 1
    return "^" + res + "$"


class S3IAMPreviewConnectorMock(PreviewConnectorMock):
    pass
