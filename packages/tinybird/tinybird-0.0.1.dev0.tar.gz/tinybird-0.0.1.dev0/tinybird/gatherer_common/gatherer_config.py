import hashlib
import heapq
import logging
import math
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

import cachetools.func
import orjson

from tinybird.model import RedisModel
from tinybird_shared.gatherer_settings import (
    GATHERERS_DISCOVERY_FAILOVER_TTL,
    GATHERERS_DISCOVERY_KEY,
    GATHERERS_DISCOVERY_TTL,
)
from tinybird_shared.metrics.statsd_client import statsd_client


@dataclass(frozen=True)
class GathererConfig:
    url: str
    database: str
    tcp_port: int
    top_tables_bandwidth: Dict[str, float] = field(default_factory=dict)


@cachetools.func.ttl_cache(ttl=0.1)
def get_region_gatherers_config(tb_region: str) -> list[GathererConfig]:
    now = int(time.time())

    def _get_config(key: bytes):
        try:
            obj = orjson.loads(key.decode("utf-8"))

            region = obj.get("region", None)
            url = obj.get("url")
            database = obj.get("database")
            tcp_port = obj.get("tcp_port", 9000)

            if not url or not database or (region and region != tb_region):
                return None

            top_tables_bandwidth: Dict[str, float] = {}
            bandwidth_stats = obj.get("bandwidth_stats")
            if bandwidth_stats:
                try:
                    bandwidth_stats_start = datetime.fromisoformat(bandwidth_stats["start"])
                    bandwidth_stats_end = datetime.fromisoformat(bandwidth_stats["end"])
                    bandwidth_stats_time = bandwidth_stats_end.timestamp() - bandwidth_stats_start.timestamp()

                    if bandwidth_stats_time > 0:
                        for table_obj in bandwidth_stats["top_tables"]:
                            table_name = table_obj["local_table"]
                            top_tables_bandwidth[table_name] = table_obj["incoming_bytes"] / bandwidth_stats_time

                except Exception as ex:
                    logging.exception(f"Error parsing gatherer tables bandwidth: {ex}")
                    top_tables_bandwidth = {}

            return GathererConfig(url, database, tcp_port, top_tables_bandwidth)
        except Exception as ex:
            logging.exception(ex)
            return None

    try:
        ttl = GATHERERS_DISCOVERY_TTL
        if RedisModel.redis_last_error and now - RedisModel.redis_last_error < GATHERERS_DISCOVERY_FAILOVER_TTL:
            ttl = GATHERERS_DISCOVERY_FAILOVER_TTL
        list_cfg = RedisModel.redis_client.zrangebyscore(GATHERERS_DISCOVERY_KEY, now - ttl, math.inf)
    except Exception as ex:
        logging.exception(ex)
        list_cfg = RedisModel.redis_replica_client.zrangebyscore(
            GATHERERS_DISCOVERY_KEY, now - GATHERERS_DISCOVERY_FAILOVER_TTL, math.inf
        )
        logging.info(f"Received {len(list_cfg)} gatherer keys from Redis replica")
        RedisModel.redis_last_error = now

    parsed_map = {(x.url, x.database, x.tcp_port): x for x in map(_get_config, list_cfg) if x is not None}

    # We need to sort based on the entry, rather than on the timestamp. Otherwise, we would jump between one
    # Gatherer and the other all the time. Been there, done that :)
    return [parsed_map[k] for k in sorted(parsed_map.keys())]


def get_gatherer_config(table: str, region: str) -> Optional[GathererConfig]:
    list_parsed = get_region_gatherers_config(region)

    if len(list_parsed) == 0:
        return None

    top_tables_bandwidth: Dict[str, float] = defaultdict(float)

    for gatherer_config in list_parsed:
        for top_table, bandwidth in gatherer_config.top_tables_bandwidth.items():
            top_tables_bandwidth[top_table] += bandwidth

    if table in top_tables_bandwidth:
        gatherer_bandwidths_heapq = [(0.0, i) for i in range(len(list_parsed))]
        heapq.heapify(gatherer_bandwidths_heapq)

        # Complexity is O(log(GT)*GT), where G=num_gatherers and T=num_top_tables_per_gatherer
        for top_table, bandwidth in sorted(top_tables_bandwidth.items(), key=lambda x: x[1], reverse=True):
            gatherer_bandwidth, gatherer_index = heapq.heappop(gatherer_bandwidths_heapq)
            if table == top_table:
                return list_parsed[gatherer_index]
            heapq.heappush(gatherer_bandwidths_heapq, (gatherer_bandwidth + bandwidth, gatherer_index))

    # We balance the load across the different gatherers evenly based on the table name to
    # maximize batching data for the same DS.
    _hash = int(hashlib.sha256(table.encode("utf-8")).hexdigest(), 16)
    gatherer_selected = list_parsed[_hash % len(list_parsed)]
    return gatherer_selected


def send_gatherer_routing_metrics(
    gatherer_config: Optional[GathererConfig],
    workspace_id: str,
    table_id: str,
    flushed_bytes: int,
):
    def sanitize_url(url: str):
        return "".join(c if c.isalnum() else "_" for c in url)

    prefix = f"tinybird-ingestion.gatherer-routing.{statsd_client.region}"
    suffix = f"{workspace_id}.{table_id}"
    if gatherer_config:
        statsd_client.timing(f"{prefix}.{sanitize_url(gatherer_config.url)}.{suffix}", flushed_bytes)
