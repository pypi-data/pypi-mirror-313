import json
import logging
import time
from queue import Empty as QueueEmpty
from queue import Queue
from typing import Generic, Optional, Tuple, TypeVar
from urllib.parse import urljoin

from pydantic import BaseModel
from pydantic.json import pydantic_encoder
from requests import ReadTimeout, Response, exceptions, post

from tinybird.internal_thread import InternalThread
from tinybird.user import public

DATASOURCE_BATCHER_HFI_TIMEOUT_SECONDS: int = 4
DATASOURCE_BATCHER_SHUTDOWN_WAIT_TIMEOUT_SECONDS: int = 30

DataSourceRecord = TypeVar("DataSourceRecord", bound=BaseModel)


class DataSourceRecordsBatcher(Generic[DataSourceRecord], InternalThread):
    def __init__(self, datasource_name: str):
        super().__init__(name=f"dataSourceRecordsBatcher-{datasource_name}", exit_queue_timeout=10.0)
        self.job_records: Queue[DataSourceRecord] = Queue()
        self.datasource_name = datasource_name
        self.api_host = ""
        self.send_batched_records = True

    def init(self, api_host: str, token: str | None = None, send_batched_records: bool = True) -> None:
        self.api_host = api_host
        self.token = token or get_datasource_append_token(self.datasource_name) or get_internal_admin_token()
        self.send_batched_records = send_batched_records

    def is_enabled(self) -> bool:
        return self.send_batched_records and bool(self.api_host) and bool(self.token)

    def append_record(self, record: DataSourceRecord) -> None:
        self.job_records.put_nowait(record)

    def action(self) -> Tuple[bool, Optional[str]]:
        job_records = self.get_job_records()

        if len(job_records) == 0:
            return True, None

        logging.warning(f"{self.name} - There are {len(job_records)} remaining to flush")
        return self.send_records(job_records)

    def send_records(self, records: list[DataSourceRecord]) -> Tuple[bool, Optional[str]]:
        url = self._get_append_url()
        headers = {"Authorization": f"Bearer {self.token}"}
        parameters = {"name": self.datasource_name, "wait": "true"}
        body = self._serialize_records(records)

        try:
            request: Response = post(
                url=url, headers=headers, params=parameters, data=body, timeout=DATASOURCE_BATCHER_HFI_TIMEOUT_SECONDS
            )
        except ReadTimeout as e:
            logging.warning(f"{self.name}: ReadTimeout while sending {len(records)}")
            self._add_job_records(records)
            return False, str(e)
        except exceptions.RequestException as e:
            logging.exception(f"{self.name}: Error while sending {len(records)}. Text: {e}")
            self._add_job_records(records)
            return False, str(e)

        if request.status_code not in (200, 202):
            logging.exception(f"{self.name}: Error while sending {len(records)}. Text: {request.text}")
            self._add_job_records(records)
            return False, request.text

        return True, None

    def get_job_records(self) -> list[DataSourceRecord]:
        items = []
        while not self.job_records.empty():
            try:
                item = self.job_records.get_nowait()
                items.append(item)
            except QueueEmpty:
                break
        return items

    def _add_job_records(self, job_records: list[DataSourceRecord]) -> None:
        for item in job_records:
            self.job_records.put_nowait(item)

    def _get_append_url(self) -> str:
        return urljoin(self.api_host, "/v0/events")

    def _serialize_records(self, records: list[DataSourceRecord]) -> bytes:
        return "\n".join(
            json.dumps(record, default=pydantic_encoder, separators=(",", ":")) for record in records
        ).encode(errors="replace")

    def shutdown(self) -> None:
        logging.warning(f"{self.name} - Starting shutdown...")
        self._terminate_thread()

        # Once we've reached this point the thread is dead so we don't need to worry about concurrency
        wait_start = time.perf_counter()
        while self.job_records.qsize() > 0:
            self.action()

            if (time.perf_counter() - wait_start) >= DATASOURCE_BATCHER_SHUTDOWN_WAIT_TIMEOUT_SECONDS:
                self._print_unflushed_records()
                raise TimeoutError(f"{self.name} DatasourceBatcher Shutdown Timeout")
        logging.warning(f"{self.name} - Finished shutdown")

    def _terminate_thread(self) -> None:
        logging.warning(f"{self.name} - Terminating {self.name} thread...")
        self.terminate()
        self.join()
        logging.warning(f"{self.name} - Thread terminated")

    def _print_unflushed_records(self) -> None:
        records = self.get_job_records()
        for record in records:
            logging.warning(f"{self.name} - Unflushed record: {record.model_dump_json()}")


def get_datasource_append_token(datasource_name: str) -> str:
    """
    This is used in tests to get the token to append data to the datasource.
    """
    internal_workspace = public.get_public_user()
    access_token = internal_workspace.get_token(f"{datasource_name} (Data Source append)")
    if not access_token:
        logging.warning(f"No {datasource_name} token found for the 'Internal' workspace")
        access_token = internal_workspace.get_token("admin token")
        if not access_token:
            logging.warning("No admin token found for the 'Internal' workspace")
            return ""
    return access_token.token


def get_internal_admin_token() -> str:
    """
    This is used for local dev since datasource token might not be available.
    Also for tests to query the contents of the datasources.
    """
    internal_workspace = public.get_public_user()
    access_token = internal_workspace.get_token("admin token")
    if not access_token:
        raise Exception("No admin token found for the 'Internal' workspace")
    return access_token.token
