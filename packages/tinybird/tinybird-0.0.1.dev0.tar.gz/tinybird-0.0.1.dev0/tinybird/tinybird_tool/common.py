import asyncio
import json
import os
import subprocess
from functools import wraps
from typing import Any, Coroutine, Dict, List, Optional, Tuple, cast

import click
import tornado.ioloop

from tinybird.ch import HTTPClient
from tinybird.ingest.cdk_utils import CDKUtils
from tinybird.ingest.preview_connectors.yepcode_utils import set_yepcode_configuration
from tinybird.job import Job
from tinybird.model import RedisModel
from tinybird.redis_config import get_redis_config
from tinybird.user import User as Workspace
from tinybird.user import UserAccount
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig

DEFAULT_CONFIG_PATH = "/mnt/disks/tb/tinybird/pro.py"
KUBERNETES_CONFIG_PATH = "/app/config/app.py"
CONFIG_HELP = f"Configuration filepath. Defaults to {DEFAULT_CONFIG_PATH}"


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def run_until_complete(fn_result: Coroutine[Any, Any, Any]) -> Any:
    loop = tornado.ioloop.IOLoop.current()
    return loop.asyncio_loop.run_until_complete(fn_result)


def running_on_container():
    """Returns true if the app is running on an individual container"""
    return "KUBERNETES_SERVICE_HOST" in os.environ and os.path.isfile(KUBERNETES_CONFIG_PATH)


def setup_redis_client(
    config: Optional[click.Path],
) -> Tuple[Dict[str, Any], TBRedisClientSync]:
    import tinybird.app

    if not config and running_on_container():
        config = cast(click.Path, KUBERNETES_CONFIG_PATH)

    if not config and os.path.isfile(DEFAULT_CONFIG_PATH):
        config = cast(click.Path, DEFAULT_CONFIG_PATH)

    conf: Dict[str, Any] = tinybird.app.get_config(config_file=config)
    redis_config: TBRedisConfig = get_redis_config(conf)
    redis_client: TBRedisClientSync = TBRedisClientSync(redis_config)
    Workspace.config(redis_client, conf["jwt_secret"], secrets_key=conf["secrets_key"], replace_executor=None)
    UserAccount.config(redis_client, conf["jwt_secret"])
    Job.config(redis_client)
    RedisModel.config(redis_client)

    return conf, redis_client


def setup_connectors_config(conf: Dict[Any, Any]) -> None:
    CDKUtils.config(
        conf["cdk_gcs_export_bucket"],
        conf["cdk_gcs_composer_bucket"],
        conf["api_host"],
        conf["cdk_project_id"],
        conf["cdk_webserver_url"],
        conf["cdk_service_account_key_location"],
        conf["cdk_group_email"],
    )

    set_yepcode_configuration(conf.get("yepcode_environment", ""), conf.get("yepcode_token", ""))


async def execute_on_remote(host: str, query: str, client: Optional[HTTPClient] = None) -> str:
    output: bytes

    if client is not None:
        _, output = await client.query(query, read_only=True)
    else:
        query = query.replace("\n", " ")
        command: List[str] = ["clickhouse", "client", "--query", f'"{query}"']
        if host != "localhost" and host != "127.0.0.1":
            # Use ssh for remote hosts
            command_param: str = " ".join(command)
            command = ["ssh", host, command_param]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)  # noqa: ASYNC221
        except subprocess.CalledProcessError as ex:
            raise Exception((ex.stderr or ex.stdout).decode())
    return output.decode()


async def get_all_hosts(host: str, clusters: List[str], client: Optional[HTTPClient] = None) -> Dict[str, List[str]]:
    """Returns a mapping `cluster name` -> `host list` for all reachable clusters."""

    QUERY: str = f"""
        SELECT
            cluster,
            groupUniqArray(host_address) hosts
        FROM (
            SELECT
                cluster,
                host_address
            FROM
                system.clusters
            WHERE
                cluster in ('{"','".join(clusters)}')
            ORDER BY
                cluster,
                host_address
        )
        GROUP BY
            cluster
        ORDER BY cluster ASC
        FORMAT JSON
    """
    items: List[Dict[str, Any]] = json.loads(await execute_on_remote(host, QUERY, client=client))["data"]
    return dict((item["cluster"], item["hosts"]) for item in items)


async def get_all_clusters(host: str, client: Optional[HTTPClient] = None) -> List[str]:
    """Returns a list with all cluster names available."""
    return (await execute_on_remote(host, "SHOW clusters", client)).split("\n")


async def get_hostnames(host: str, clusters: List[str], client: Optional[HTTPClient] = None) -> Dict[str, str]:
    """Returns a mapping between `ip address` -> `hostname` for all reachable hosts."""

    result: Dict[str, str] = {}

    for cluster in clusters:
        hostnames_query: str = f"""
            SELECT
                hostname() as host_name,
                host_address
            FROM
                 clusterAllReplicas('{cluster}', system.clusters)
            WHERE
                is_local == 1
            ORDER BY
                host_name ASC
            FORMAT JSON
        """
        result.update(
            dict(
                (item["host_address"], item["host_name"])
                for item in json.loads(await execute_on_remote(host, hostnames_query, client))["data"]
            )
        )

    return result


async def get_cluster_members_with_ports(
    host: str, cluster: str, client: Optional[HTTPClient] = None
) -> list[dict[str, str | int]]:
    """Returns the list of members of a cluster with its hostname, address, tcp port and http port."""

    query = f"""
        SELECT
            hostname() as host_name,
            host_address,
            getServerPort('tcp_port') AS tcp_port,
            getServerPort('http_port') AS http_port
        FROM
             clusterAllReplicas('{cluster}', system.clusters)
        WHERE
            cluster == '{cluster}' AND
            is_local == 1
        ORDER BY
            host_name ASC
        FORMAT JSON
    """

    return sorted(json.loads(await execute_on_remote(host, query, client))["data"], key=lambda h: h["host_name"])
