import asyncio
import logging
import traceback
from asyncio import AbstractEventLoop, Task
from typing import Dict, Optional

import aiohttp

from tinybird.ch import HTTPClient, url_from_host
from tinybird.ch_utils.exceptions import CHException
from tinybird.default_timeouts import socket_connect_timeout, socket_read_timeout, socket_total_timeout

# Dict of event loops, to support
# multiple loops
global_shared_session: Dict[AbstractEventLoop, aiohttp.ClientSession] = {}
global_shared_session_task: Dict[AbstractEventLoop, Task] = {}


def get_shared_session_task() -> Optional[Task]:
    global global_shared_session, global_shared_session_task
    loop = asyncio.get_running_loop()
    return global_shared_session_task.get(loop)


def get_shared_session() -> aiohttp.ClientSession:
    global global_shared_session, global_shared_session_task

    loop = asyncio.get_running_loop()

    session = global_shared_session.get(loop)
    if session:
        return session

    conn = aiohttp.TCPConnector(limit=32, force_close=True)
    global_shared_session[loop] = aiohttp.ClientSession(
        connector=conn,
        skip_auto_headers=["User-Agent", "Content-Type"],
        headers={"accept-encoding": "none"},
        auto_decompress=False,
        read_bufsize=4096,
        timeout=aiohttp.ClientTimeout(
            total=socket_total_timeout(), connect=socket_connect_timeout(), sock_read=socket_read_timeout()
        ),
    )

    # When the IO loop gets closed, it will cancel all pending tasks
    # This task is responsible for the session closing
    async def close_session_on_cancel():
        try:
            # wait forever
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            await global_shared_session[loop].close()
            raise

    # It's important to keep a reference to the task
    # If not, the GC will destroy it eventually,
    # causing "Task was destroyed but it is pending!" errors
    # and global_shared_session.close() won't be called on shutdown
    # See https://bugs.python.org/issue21163
    global_shared_session_task[loop] = asyncio.create_task(close_session_on_cancel())
    return global_shared_session[loop]


def reset_shared_session():
    global global_shared_session, global_shared_session_task
    for x in global_shared_session_task.values():
        try:
            x.cancel()
        except Exception:
            pass
    global_shared_session = {}
    global_shared_session_task = {}


class aiohttpClient:
    def __init__(self, host="localhost", database=None):
        self.http_client = HTTPClient(host, database)
        self.host = host
        self.database = database if database else "default"

    @property
    def endpoint(self):
        """
        >>> c = aiohttpClient()
        >>> c.endpoint
        'http://localhost:8123/'
        >>> c = aiohttpClient(host='http://1.2.3.4:8888/')
        >>> c.endpoint
        'http://1.2.3.4:8888/'
        >>> c = aiohttpClient(host='http://1.2.3.4:8888')
        >>> c.endpoint
        'http://1.2.3.4:8888/'
        """
        return url_from_host(self.host)

    def get_params(self, q, method="GET", query_id=None, extra_params=None):
        """
        >>> params, body = aiohttpClient().get_params('', extra_params={'max_execution_time': 30})
        >>> params['max_execution_time']
        30
        >>> params['lock_acquire_timeout']
        30
        """
        return self.http_client.get_params(q, method, query_id, extra_params)

    async def insert_chunk(self, query, chunk, dialect=None, max_execution_time=10, extra_params=None):
        headers = {
            "User-Agent": "tb-lfi",
        }
        session = get_shared_session()
        delimiter = "," if not dialect else dialect.get("delimiter", ",")
        max_execution_time = max_execution_time or 10
        extra_params = {
            "format_csv_delimiter": delimiter,
            "input_format_defaults_for_omitted_fields": 1,
            "max_execution_time": max_execution_time,
            **(extra_params or {}),
        }
        params, _ = self.get_params(
            query, method="GET", extra_params=extra_params
        )  # use get to avoid using the body to send the query
        retry = 0
        while True:
            try:
                async with session.post(self.endpoint, params=params, data=chunk, headers=headers) as resp:
                    result = await resp.content.read()
                    if resp.status >= 400:
                        # log here the error, when working with varnish the response could be totally different to what
                        # CH reports and therefore the CHException parsing will not work
                        logging.error(
                            f"insert chunk failed {len(chunk)} in clickhouse: {resp.status}, {resp.raw_headers} {result.decode('utf-8', 'replace')}"
                        )
                        try:
                            error_result = result.decode("utf-8", "replace")
                        except AttributeError:
                            error_result = str(result)
                        raise CHException(error_result, headers=resp.headers)

                    return resp.headers, result
            except aiohttp.client_exceptions.ClientOSError as e:
                retry += 1
                if retry >= 2:
                    raise
                logging.error(f"Retrying aiohttp exception: {e}.\n{traceback.format_exc()}")
                await asyncio.sleep(0.2)
                continue
