import json
import logging
import uuid
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar
from urllib.parse import urlparse

import aiohttp
from multidict import CIMultiDictProxy

T = TypeVar("T")
DEFAULT_AIOHTTP_TIMEOUT = 300

DEFAULT_HTTP_PORT = 8123
DEFAULT_TCP_PORT = 9000


def get_query_id() -> str:
    return str(uuid.uuid4())


@dataclass(frozen=True)
class CHHost:
    hostname: str
    http_port: int = DEFAULT_HTTP_PORT
    tcp_port: int = DEFAULT_TCP_PORT
    secure: bool = False

    @property
    def url(self) -> str:
        protocol = "https" if self.secure else "http"
        return f"{protocol}://{self.hostname}:{self.http_port}"

    @property
    def http_host(self) -> str:
        return f"{self.hostname}:{self.http_port}"

    @property
    def tcp_host(self) -> str:
        return f"{self.hostname}:{self.tcp_port}"

    @classmethod
    def from_url(cls, url: str) -> "CHHost":
        """
        >>> CHHost.from_url('localhost')
        CHHost(hostname='localhost', http_port=8123, tcp_port=9000, secure=False)
        >>> CHHost.from_url('http://localhost')
        CHHost(hostname='localhost', http_port=8123, tcp_port=9000, secure=False)
        >>> CHHost.from_url('http://localhost:1234')
        CHHost(hostname='localhost', http_port=1234, tcp_port=9000, secure=False)
        >>> CHHost.from_url('https://localhost:1234')
        CHHost(hostname='localhost', http_port=1234, tcp_port=9000, secure=True)
        """
        # Defensive programming to ensure what we pass here is an URL and not an endpoint
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        components = urlparse(url)
        if components.hostname is None:
            raise RuntimeError(f"Invalid url '{url}' missing hostname")

        return cls(
            hostname=components.hostname,
            http_port=components.port or DEFAULT_HTTP_PORT,
            secure=components.scheme == "https",
        )


class CHException(Exception):
    def __init__(self, status_code: int, exception_code: int, text: str, query_id: Optional[str] = None) -> None:
        self.status_code = status_code
        self.exception_code = exception_code
        self.text = text
        self.query_id = query_id
        super().__init__(str(self))

    def __str__(self):
        return f"query_id: {self.query_id}, status code: {self.status_code}, exception_code: {self.exception_code}, text: '{self.text}'"


@dataclass(frozen=True)
class CHQueryStats:
    read_rows: int
    read_bytes: int
    written_rows: int
    written_bytes: int
    total_rows_to_read: int
    result_rows: int
    result_bytes: int


@dataclass(frozen=True)
class CHResponse:
    query_id: str
    data: bytes
    stats: CHQueryStats
    server: Optional[str]

    def json(self) -> dict[str, Any]:
        output: dict[str, Any] = json.loads(self.data)  # Hack to make mypy happy
        return output

    def text(self) -> str:
        return self.data.decode("utf-8").rstrip("\n")


@dataclass(frozen=True)
class CHQueryResults(Generic[T]):
    query_id: str
    data: T
    stats: CHQueryStats
    server: Optional[str]


class CHConnection:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        settings: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        self._session = session
        self._url = url
        self._settings = settings or {}
        self._headers = headers or {}
        self._default_timeout = aiohttp.ClientTimeout(total=DEFAULT_AIOHTTP_TIMEOUT)

    async def run_query(self, query: str, database: Optional[str] = None, read_query: bool = False) -> CHResponse:
        query_id = get_query_id()
        logging.debug(f"Running query with id {query_id}: {self._format_query_single_line(query)}")

        params = {**self._get_encoded_settings(), "query": query, "query_id": query_id}
        if database:
            params["database"] = database

        headers = self._headers
        if read_query:
            headers |= {"X-TB-Read-Cluster": "true"}

        try:
            async with self._session.get(self._url, params=params, headers=headers) as res:
                data = await res.read()
                if res.status != 200:
                    exception_code = res.headers.get("X-ClickHouse-Exception-Code", None)
                    raise CHException(
                        status_code=res.status,
                        exception_code=int(exception_code) if exception_code is not None else -1,
                        text=await res.text(),
                        query_id=query_id,
                    )
                return self._build_response(res.headers, data)
        except Exception as ex:
            # Remove carriage return to avoid Loki splitting the log into several entries
            query_str = self._format_query_single_line(query)
            ex_str = str(ex).replace("\n", " ")
            logging.warning(f"Error running query '{query_str}' in {self._url} with query_id {query_id}: {ex_str}")
            raise ex

    async def run_command(
        self,
        stmt: str,
        database: Optional[str] = None,
        timeout: Optional[aiohttp.ClientTimeout] = None,
        query_id: Optional[str] = None,
    ) -> CHResponse:
        if not query_id:
            query_id = get_query_id()

        logging.debug(f"Running command with id {query_id}: {self._format_query_single_line(stmt)}")
        params = {**self._get_encoded_settings(), "query_id": query_id}
        if database:
            params["database"] = database

        if timeout is None:
            timeout = self._default_timeout

        try:
            async with self._session.post(
                self._url, data=stmt, params=params, headers=self._headers, timeout=timeout
            ) as res:
                text = await res.text()
                if res.status != 200:
                    exception_code = res.headers.get("X-ClickHouse-Exception-Code", None)
                    raise CHException(
                        status_code=res.status,
                        exception_code=int(exception_code) if exception_code is not None else -1,
                        text=text,
                        query_id=query_id,
                    )
                return self._build_response(res.headers, b"")
        except Exception as ex:
            # Remove carriage return to avoid Loki splitting the log into several entries
            stmt_str = self._format_query_single_line(stmt)
            ex_str = str(ex).replace("\n", " ")
            logging.warning(
                f"Error running ClickHouse command '{stmt_str}' in {self._url} with query_id {query_id}: {ex_str}"
            )
            raise ex

    def _get_encoded_settings(self) -> dict[str, Any]:
        return {k: str(v) for k, v in self._settings.items()}

    def _build_response(self, headers: CIMultiDictProxy[str], data: bytes) -> CHResponse:
        query_id = headers.get("X-ClickHouse-Query-Id", "")
        server = headers.get("X-ClickHouse-Server-Display-Name")
        stats = self._parse_headers(headers)
        return CHResponse(query_id, data, stats, server)

    @staticmethod
    def _format_query_single_line(query: str) -> str:
        return " ".join(query.split())

    @staticmethod
    def _parse_headers(raw_header: CIMultiDictProxy[str]) -> CHQueryStats:
        stats = json.loads(raw_header["X-ClickHouse-Summary"])
        return CHQueryStats(
            read_rows=int(stats["read_rows"]),
            read_bytes=int(stats["read_bytes"]),
            written_rows=int(stats["written_rows"]),
            written_bytes=int(stats["written_bytes"]),
            total_rows_to_read=int(stats["total_rows_to_read"]),
            result_rows=int(stats["result_rows"]),
            result_bytes=int(stats["result_bytes"]),
        )


class CHSession:
    def __init__(self, timeout: Optional[aiohttp.ClientTimeout] = None, limit: int = 100) -> None:
        if timeout is None:
            timeout = aiohttp.ClientTimeout(total=DEFAULT_AIOHTTP_TIMEOUT)

        tcp_connector = aiohttp.TCPConnector(force_close=True, limit=limit)
        self._session = aiohttp.ClientSession(timeout=timeout, connector=tcp_connector)

    # Async to ensure we're running inside a loop
    async def connect(
        self, url: str, settings: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None
    ) -> CHConnection:
        return CHConnection(self._session, url, settings, headers)

    async def close(self) -> None:
        await self._session.close()
