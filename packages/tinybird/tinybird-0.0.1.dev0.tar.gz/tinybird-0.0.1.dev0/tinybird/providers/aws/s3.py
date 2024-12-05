import asyncio
import dataclasses
import datetime as dt
from typing import Optional
from urllib.parse import unquote, urlparse

import botocore
import requests

from tinybird.providers.aws.exceptions import (
    InvalidS3URL,
    MalformedAWSAPIResponse,
    NoSuchBucket,
    _handle_botocore_client_exception,
)
from tinybird.providers.aws.session import AWSSession

EXPIRES_IN_24H = 86400


@dataclasses.dataclass(frozen=True)
class S3Object:
    key: str
    size: int
    last_modified: dt.datetime
    body: botocore.response.StreamingBody | None = None


@dataclasses.dataclass(frozen=True)
class ObjectHead:
    metadata: dict[str, str]


def list_objects(
    session: AWSSession,
    bucket: str,
    prefix: Optional[str] = None,
    region: Optional[str] = None,
    max_keys: Optional[int] = None,
    start_after: Optional[str] = None,
) -> list[S3Object]:
    args = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if start_after is not None:
        args["StartAfter"] = start_after
    s3 = session.client("s3", region=region)
    try:
        # Filter out None values otheriwse boto complains
        res = s3.list_objects_v2(**{k: v for k, v in args.items() if v is not None})
    # Boto3 client exceptions are constructed dynamically so we need to get them from the client itself.
    except s3.exceptions.NoSuchBucket as err:
        raise NoSuchBucket(bucket) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)

    try:
        if 0 == res["KeyCount"]:  # Let's trust KeyCount
            return []
        return [S3Object(obj["Key"], obj["Size"], obj["LastModified"]) for obj in res["Contents"]]
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def get_signed_url(
    session: AWSSession, bucket_name: str, file_name: str, region: str, endpoint_url: str | None = ""
) -> tuple[str, str | None]:
    final_endpoint_url = endpoint_url
    if not final_endpoint_url:
        s3 = session.client("s3", region=region)
        final_endpoint_url = s3.meta.endpoint_url

    s3 = session.client("s3", region=region, endpoint_url=final_endpoint_url)

    try:
        url: str = s3.generate_presigned_url(
            "get_object", Params={"Bucket": bucket_name, "Key": file_name}, ExpiresIn=EXPIRES_IN_24H
        )
        return url, final_endpoint_url
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)


def head_object(session: AWSSession, bucket: str, key: str, region: Optional[str] = None) -> ObjectHead:
    s3 = session.client("s3", region=region)
    try:
        res = s3.head_object(Bucket=bucket, Key=key)
    except s3.exceptions.NoSuchBucket as err:
        raise NoSuchBucket(bucket) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)
    try:
        return ObjectHead(res["Metadata"])
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def get_object(session: AWSSession, bucket: str, key: str, region: Optional[str] = None) -> S3Object:
    s3 = session.client("s3", region=region)
    try:
        res = s3.get_object(Bucket=bucket, Key=key)
    except s3.exceptions.NoSuchBucket as err:
        raise NoSuchBucket(bucket) from err
    except botocore.exceptions.ClientError as err:
        _handle_botocore_client_exception(err)
    try:
        return S3Object(key=key, size=res["ContentLength"], last_modified=res["LastModified"], body=res["Body"])
    except KeyError as err:
        raise MalformedAWSAPIResponse(err) from err


def parse_s3_url(signed_url: str) -> tuple[str, str]:
    """
    >>> import pytest
    >>> s3_url = "https://my-bucket.s3.amazonaws.com/path/to/my/object.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=..."
    >>> parse_s3_url(s3_url)
    ('my-bucket', 'path/to/my/object.jpg')
    >>> s3_url = "https://my-bucket.s3.amazonaws.com/path/to/my/object.jpg"
    >>> parse_s3_url(s3_url)
    ('my-bucket', 'path/to/my/object.jpg')
    >>> s3_url = "https://my-bucket.s3.eu-west-1.amazonaws.com/path/to/my/object.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=..."
    >>> parse_s3_url(s3_url)
    ('my-bucket', 'path/to/my/object.jpg')
    >>> s3_url = "https://my-bucket.s3..eu-west-1.amazonaws.com/path/to/my/object.jpg"
    >>> parse_s3_url(s3_url)
    ('my-bucket', 'path/to/my/object.jpg')
    >>> no_hostname = "https://path/to/my/object.jpg"
    >>> with pytest.raises(InvalidS3URL, match="The URL provided does not contain a valid hostname for an S3 bucket."):
    ...     parse_s3_url(no_hostname)
    >>> no_bucket = "https://s3.amazonaws.com/path/to/my/object.jpg"
    >>> parse_s3_url(no_bucket)
    ('path', 'to/my/object.jpg')
    >>> no_bucket = "https://.s3.amazonaws.com/path/to/my/object.jpg"
    >>> parse_s3_url(no_bucket)
    ('path', 'to/my/object.jpg')
    >>> no_object = "https://my-bucket.s3.amazonaws.com/"
    >>> with pytest.raises(InvalidS3URL, match="The URL provided does not specify an object path within the bucket."):
    ...     parse_s3_url(no_object)
    >>> s3_url = "https://my-bucket.s3.amazonaws.com/path/to/my/tb-2024-07-17T19%3A13%3A53.826910559Z.parquet"
    >>> parse_s3_url(s3_url)
    ('my-bucket', 'path/to/my/tb-2024-07-17T19:13:53.826910559Z.parquet')
    """
    s3, amazon_service = "s3", "amazonaws.com"
    parsed_url = urlparse(signed_url)
    hostname = parsed_url.hostname
    invalid_hostname = not hostname or s3 not in hostname or amazon_service not in hostname
    if invalid_hostname:
        raise InvalidS3URL("The URL provided does not contain a valid hostname for an S3 bucket.")
    bucket_name = hostname.split(".")[0] if isinstance(hostname, str) and "." in hostname else None
    if not bucket_name or bucket_name == s3:
        path_parts = parsed_url.path.lstrip("/").split("/", 1)
        if len(path_parts) < 2 or not path_parts[0]:
            raise InvalidS3URL("The URL provided is missing a bucket name or object path.")
        bucket_name, object_path = path_parts[0], path_parts[1]
        if not bucket_name or not object_path:
            raise InvalidS3URL("The URL provided is missing a bucket name.")
        object_path = unquote(object_path)
        return bucket_name, object_path

    object_path = parsed_url.path.lstrip("/")
    if not object_path:
        raise InvalidS3URL("The URL provided does not specify an object path within the bucket.")
    object_path = unquote(object_path)

    return bucket_name, object_path


async def check_signed_s3_url(url):
    try:
        response = await asyncio.to_thread(requests.get, url, headers={"Range": "bytes=0-0"})
        response.raise_for_status()  # Raises a HTTPError if the status code is 4xx or 5xx
        return True, response.status_code
    except requests.exceptions.RequestException:
        return False, response.status_code
