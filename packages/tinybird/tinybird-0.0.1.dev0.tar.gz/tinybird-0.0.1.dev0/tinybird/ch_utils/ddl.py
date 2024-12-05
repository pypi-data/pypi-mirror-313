import csv
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT = "null_status_on_timeout"

TSV_NULL = "\\N"


def is_null(value: str) -> bool:
    return value == TSV_NULL


@dataclass
class DDLQueryStatus:
    host: str
    port: int
    status: Optional[int]
    error: Optional[str]
    num_hosts_remaining: int
    num_hosts_active: int
    query_id: Optional[str]


class DDLQueryException(Exception):
    def __init__(self, err, response):
        self.response = response
        super().__init__(err)


class DDLQueryError(DDLQueryException):
    pass


class DDLQueryTimeout(DDLQueryException):
    pass


class DDLQueryUnkownError(DDLQueryException):
    pass


@dataclass
class DDLQueryStatusResponse:
    response: List[DDLQueryStatus]

    @classmethod
    def from_client_response(cls, headers: Dict[str, Any], body: bytes, query_id: Optional[str]) -> None:
        if headers["content-type"].startswith("application/json"):
            cls.from_query_data_response(headers, json.loads(body)["data"], query_id)
        elif headers["content-type"].startswith("text/tab-separated-values"):
            cls.from_tsv_response(headers, body, query_id)
        else:
            if body and headers:
                raise Exception("Not correct content-type")
            else:
                logging.warning("empty response skipped due to a KILL query")

    @classmethod
    def from_tsv_response(cls, headers: Dict[str, Any], body: bytes, query_id) -> None:
        ddl_query_status = []

        for response in csv.reader(body.decode("utf-8").splitlines(), delimiter="\t"):
            ddl_query_status.append(
                DDLQueryStatus(
                    host=response[0],
                    port=int(response[1]),
                    status=None if is_null(response[2]) else int(response[2]),
                    error=None if is_null(response[3]) else response[3],
                    num_hosts_remaining=int(response[4]),
                    num_hosts_active=int(response[5]),
                    query_id=query_id,
                )
            )
        status_response = cls(response=ddl_query_status)
        status_response.process(query_id)

    @classmethod
    def from_query_data_response(
        cls, headers: Dict[str, Any], data_response: List[Dict[str, Any]], query_id: Optional[str]
    ) -> None:
        ddl_query_status = []

        for response in data_response:
            if not response.get("host") or not response.get("port"):
                continue

            query_status = DDLQueryStatus(
                host=response.get("host", ""),
                port=int(response.get("port", 0)),
                status=None if not response.get("status") else int(response.get("status", 0)),
                error=response.get("error", ""),
                num_hosts_remaining=int(response.get("num_hosts_remaining", 0)),
                num_hosts_active=int(response.get("num_hosts_active", 0)),
                query_id=query_id,
            )

            ddl_query_status.append(query_status)

        status_response = cls(response=ddl_query_status)
        status_response.process(query_id)

    @property
    def ok(self) -> bool:
        return not any(status.status != 0 for status in self.response)

    @property
    def errors(self) -> List[DDLQueryStatus]:
        return list(filter(lambda x: x.error, self.response))

    @property
    def timeouts(self) -> List[DDLQueryStatus]:
        return list(filter(lambda x: x.status is None, self.response))

    def process(self, query_id: Optional[str] = ""):
        # for the moment just raise timeouts to keep current behavior
        try:
            query_id = f" - QUERY_ID {query_id}" if query_id else ""
            if not self.ok:
                if self.errors:
                    raise DDLQueryError(f"DDL Error: {self.errors}{query_id}", self.response)
                if self.timeouts:
                    raise DDLQueryTimeout(f"DDL Timeout: {self.timeouts}{query_id}", self.response)
                raise DDLQueryUnkownError("DDL Unknown Error", self.response)
        except DDLQueryTimeout as e:
            logging.warning(f"Skipping replica as it's down or slow {str(e)}{query_id}")
        except Exception as e:
            logging.exception(e)
            raise e
