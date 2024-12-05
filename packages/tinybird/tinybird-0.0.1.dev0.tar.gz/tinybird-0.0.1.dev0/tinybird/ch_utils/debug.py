import json
import logging
import re
from io import StringIO

from clickhouse_driver import Client

from tinybird.syncasync import sync_to_async

from ..ch import ch_flush_logs_on_all_replicas, host_port_from_url, url_from_host


class LoggingCapturer:
    def __init__(self, logger_name, level):
        self.old_stdout_handlers = []
        self.logger = logging.getLogger(logger_name)
        self.level = level
        super().__init__()

    def __enter__(self):
        self.buffer = StringIO()
        self.new_handler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.new_handler)
        self.old_logger_level = self.logger.level
        self.logger.setLevel(self.level)

        return self

    def __exit__(self, *exc_info):
        self.logger.setLevel(self.old_logger_level)
        self.logger.removeHandler(self.new_handler)

    def get_raw_lines(self):
        v = self.buffer.getvalue()
        # remove not used info from the start to the first ">"
        return "\n".join([re.sub(".*>", "", x) for x in v.split("\n")])


async def get_trace_info(client, q: str, host: str, query_id: str, **extra_params):
    """
    this function captures the server log with trace level.
    It uses the native library because the HTTP interface does not support sending logs to the client
    """
    # request hostname trough http first to see if we go through a proxy
    headers, body = await client.query("select hostname()", max_execution_time=1)
    if "X-Varnish" not in headers:
        host, _ = host_port_from_url(url_from_host(host))
    else:
        host = body.decode().strip()

    with LoggingCapturer("clickhouse_driver.log", "INFO") as buffer:
        extra_params.update({"send_logs_level": "trace"})
        client = Client(host)
        await sync_to_async(client.execute)(q, settings=extra_params, query_id=query_id)
        return buffer.get_raw_lines()


async def get_execution_info(client, query_id, database_server, cluster=None):
    await ch_flush_logs_on_all_replicas(database_server, cluster)

    table = "system.query_log"
    if cluster:
        table = f"clusterAllReplicas('{cluster}', system.query_log)"

    _, content = await client.query(
        f"""
    select * from {table}
    where query_id = '{query_id}'
    and event_date = today()
    and event_time >= now() - interval 1 hour
    and type = 'QueryFinish'
    format JSON
    """
    )
    data = json.loads(content)["data"]
    if data:
        data = data[0]
        info = []
        for name, value in data.items():
            if "." not in name and name != "query":
                info.append((name, value))
        for name, value in data["ProfileEvents"].items():
            info.append((name, value))
        for name, value in data["Settings"].items():
            info.append((name, value))
        return info
    return None


async def get_query_explain(client, query, **extra_params):
    logging.info(f"get_query_explain {query}")
    _, content = await client.query("EXPLAIN indexes=1 " + query, **extra_params)
    if content:
        return content.decode()
    return ""
