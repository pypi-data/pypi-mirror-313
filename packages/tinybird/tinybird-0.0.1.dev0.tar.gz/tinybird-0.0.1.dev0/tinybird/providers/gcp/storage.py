import dataclasses
import datetime as dt
from typing import Optional

from google.cloud import storage

from tinybird.providers.gcp.session import GCPSession


@dataclasses.dataclass(frozen=True)
class GCSBlob:
    name: str
    size: str
    created_at: dt.datetime
    last_modified: dt.datetime


def list_blobs(
    session: GCPSession, bucket: str, prefix: Optional[str] = None, max_results: Optional[int] = None
) -> list:
    credentials = session.get_credentials()
    gcs = storage.Client(credentials=credentials)

    blobs = gcs.list_blobs(bucket, prefix=prefix, max_results=max_results)
    return [GCSBlob(blob.name, blob.size, blob.time_created, blob.updated) for blob in blobs]
