import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

import aiohttp

from tinybird.ch import url_from_host
from tinybird.constants import Incidents, Notifications
from tinybird.distributed import WorkingGroup
from tinybird.user import UserDoesNotExist, Users, public
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.redis_client.redis_client import async_redis

INGESTION_OBSERVER_POLL_SECONDS = 5 * 60
INGESTION_OBSERVER_SUB_POLL_SECONDS = 1
INGESTION_OBSERVER_INCIDENT_TTL_SECONDS = 24 * 60 * 60
INGESTION_OBSERVER_ERROR_LIMIT = 10
INTERNAL_SLACK_EMAIL = "e4i7t3o4z0g0f1n1@tinybirdworkspace.slack.com"
INGESTION_LAGGY_WINDOW = 5

# Redis structure
#
# Hash Table at `ingestion-observer:incidents:{WORKSPACE_ID}`
#   having keys like `{DATASOURCE_ID}`
#   having values like `{"time_first_detected": "{UNIX_EPOCH_SECONDS}",
#                        "time_last_detected": "{UNIX_EPOCH_SECONDS}"
#                        "errors": ["error1", "bla bla bla..."]
#                       }`


class IngestionObserver:
    def __init__(self, mailgun_service=None):
        self._mailgun_service = mailgun_service

    async def run(self):
        self._exit_flag = asyncio.Event()
        self._task = asyncio.create_task(self._action())

    async def _action(self):
        self._working_group = WorkingGroup("ingestion-observer", str(uuid4()))
        await self._working_group.init()
        while not self._exit_flag.is_set():
            await asyncio.sleep(INGESTION_OBSERVER_SUB_POLL_SECONDS)
            # try:
            #     await asyncio.wait_for(self._exit_flag.wait(), timeout=INGESTION_OBSERVER_SUB_POLL_SECONDS)
            #     return
            # except asyncio.TimeoutError:
            #     pass
            try:
                should_check, check_timestamp_start = await self._should_check_for_incidents()
                if not should_check:
                    continue

                observation_start_time = datetime.now(timezone.utc).timestamp()
                # Skip last 5 seconds to give a window for laggy inserts on ds_ops_log
                check_timestamp_end = int(datetime.now(timezone.utc).timestamp()) - INGESTION_LAGGY_WINDOW

                error_events = await self._get_errors_from_ds_ops_log(check_timestamp_start, check_timestamp_end)
                await self._process_error_events(error_events, check_timestamp_end)
                quarantine_events = await self._get_quarantine_from_ds_ops_log(
                    check_timestamp_start, check_timestamp_end
                )
                await self._process_quarantine_events(quarantine_events, check_timestamp_end)

                await async_redis.set("ingestion-observer:last_check", f"{check_timestamp_end}")

                observation_duration_time = datetime.now(timezone.utc).timestamp() - observation_start_time
                logging.info(f"obs time {observation_duration_time}")
                statsd_client.timing(
                    f"tinybird-ingestion-observer.{statsd_client.region_app_machine}.observation-duration-time",
                    observation_duration_time,
                )

            except Exception as e:
                logging.exception(e)
        await self._working_group.exit()
        logging.info("IngestionObserver exit")

    async def terminate(self):
        self._exit_flag.set()
        await self._task
        logging.info("IngestionObserver exited")

    async def _should_check_for_incidents(self):
        score_index = self._working_group.score_index("main")
        if score_index != 0:
            return False, 0
        # Check time of last pass on Redis (poll every 5 minutes), continue if too soon
        last_check = await async_redis.get("ingestion-observer:last_check")
        if last_check is None:
            # If this is the first time we observe for errors, ignore old errors
            last_check = int(datetime.now(timezone.utc).timestamp()) - 2 * INGESTION_OBSERVER_POLL_SECONDS
        last_check_seconds = int(last_check)
        if datetime.now(timezone.utc).timestamp() < last_check_seconds + INGESTION_OBSERVER_POLL_SECONDS:
            return False, 0
        # Plus 1 to avoid processing events twice due to SQL BETWEEN clause being inclusive
        return True, last_check_seconds + 1

    async def _store_incident(self, workspace_id: str, datasource_id: str, incident_type: str, incident: dict):
        incident_json = json.dumps(incident)
        await async_redis.hset(f"ingestion-observer:{incident_type}:{workspace_id}", datasource_id, incident_json)

    async def _get_errors_from_ds_ops_log(self, check_timestamp_start, check_timestamp_end):
        # Make the lookup query against ds_ops_log, set timeout to 5 seconds (query against 6 minutes)
        pu = public.get_public_user()
        table = next(x for x in pu.datasources if x["name"] == "datasources_ops_log")
        query = f"""
            SELECT timestamp, user_id, datasource_id, error FROM {pu.database}.{table['id']}
            WHERE timestamp BETWEEN FROM_UNIXTIME({check_timestamp_start})
                AND FROM_UNIXTIME({check_timestamp_end})
                AND result!='ok'
            ORDER BY user_id, datasource_id, error, timestamp DESC
            FORMAT JSON
        """
        url = url_from_host(pu.database_server)
        params = {
            "database": pu.database,
            "query": query,
            "max_execution_time": 5,
        }
        headers = {
            "User-Agent": "tb-ingestion-observer",
        }
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10, connect=2, sock_read=7)) as session:
            async with session.request("POST", url=url, params=params, headers=headers) as resp:
                result = await resp.content.read()
                if resp.status >= 400:
                    raise Exception(f"IngestionObserver CH error {resp.status}: {result.decode('utf-8')}")
                data = json.loads(result)["data"]
                return data if data else []

    async def _process_error_events(self, error_events, current_timestamp: int):
        incidents_by_datasource_id = {}  # type: ignore
        for event in error_events:
            datasource_id = event["datasource_id"]
            if datasource_id in incidents_by_datasource_id:
                incident = incidents_by_datasource_id[datasource_id]
            else:
                incident = {
                    "workspace_id": event["user_id"],
                    "datasource_id": datasource_id,
                    "errors": [],
                }
                incidents_by_datasource_id[datasource_id] = incident
            incident["errors"].append({"timestamp": event["timestamp"], "error": event["error"]})

        # Merge new incidents with incidents stored at Redis
        for new_incident in incidents_by_datasource_id.values():
            workspace_id = new_incident["workspace_id"]
            datasource_id = new_incident["datasource_id"]
            # Get old incident from Redis => default to empty incident
            old_incident_json = await async_redis.hget(
                f"ingestion-observer:{Incidents.ERROR}:{workspace_id}", datasource_id
            )
            if old_incident_json:
                old_incident = json.loads(old_incident_json)
                now = datetime.now(timezone.utc).timestamp()
                errors = [
                    error
                    for error in old_incident["errors"]
                    if isinstance(error, dict)
                    and error.get("timestamp", None)
                    and datetime.fromisoformat(f"{error['timestamp']}Z").timestamp()
                    > now - INGESTION_OBSERVER_INCIDENT_TTL_SECONDS
                ]
                old_incident["errors"] = errors
            else:
                old_incident = {"status": IncidentStatus.IDLE, "errors": [], "next_timestamp": 0}
            # Merge old and new incidents
            next_timestamp = int(old_incident.get("next_timestamp", 0))
            status = IncidentStatus.NEW if current_timestamp >= next_timestamp else IncidentStatus.PENDING
            incident = {
                "status": status,
                "errors": (old_incident["errors"] + new_incident["errors"])[-INGESTION_OBSERVER_ERROR_LIMIT:],
                "next_timestamp": next_timestamp,
            }

            # Sort incidents DESC from most recent to oldest
            incident["errors"] = sorted(
                incident["errors"], key=lambda x: datetime.fromisoformat(x["timestamp"]), reverse=True
            )

            # Store new incident
            await self._store_incident(workspace_id, datasource_id, Incidents.ERROR, incident)
            await self._process_incident(workspace_id, datasource_id, Incidents.ERROR, incident)

    async def _get_quarantine_from_ds_ops_log(self, check_timestamp_start: int, check_timestamp_end: int):
        public_user = public.get_public_user()
        table = next(
            datasource for datasource in public_user.datasources if datasource["name"] == "datasources_ops_log"
        )
        if not table:
            return []
        query = f"""
        SELECT user_id, datasource_id, rows_quarantine, timestamp
        FROM {public_user.database}.{table['id']}
        WHERE timestamp BETWEEN FROM_UNIXTIME({check_timestamp_start})
            AND FROM_UNIXTIME({check_timestamp_end})
            AND rows_quarantine > 0
        FORMAT JSON;
        """
        url = url_from_host(public_user.database_server)
        params = {
            "database": public_user.database,
            "query": query,
            "max_execution_time": 5,
        }
        headers = {
            "User-Agent": "tb-ingestion-observer",
        }
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10, connect=2, sock_read=7)) as session:
            async with session.request("POST", url=url, params=params, headers=headers) as resp:
                result = await resp.content.read()
                if resp.status >= 400:
                    raise Exception(f"IngestionObserver CH error {resp.status}: {result}")  # type: ignore
                data = json.loads(result)["data"]
                return data if data else []

    async def _process_quarantine_events(self, quarantine_events: List[dict], current_timestamp: int):
        incidents_by_datasource_id = {}  # type: ignore
        for event in quarantine_events:
            datasource_id = event["datasource_id"]
            if datasource_id in incidents_by_datasource_id:
                incident = incidents_by_datasource_id[datasource_id]
            else:
                incident = {
                    "workspace_id": event["user_id"],
                    "datasource_id": datasource_id,
                    "imports": 0,
                    "rows": 0,
                    "timeline": [],
                    "next_timestamp": 0,
                }
                incidents_by_datasource_id[datasource_id] = incident
            rows = int(event["rows_quarantine"])
            incident["imports"] += 1
            incident["rows"] += rows
            timeline_entry = {"timestamp": event["timestamp"], "rows": rows}
            incident["timeline"].append(timeline_entry)
        # Merge new incidents with incidents stored at Redis
        for new_incident in incidents_by_datasource_id.values():
            # Get old incident from Redis => default to empty incident
            datasource_id = new_incident["datasource_id"]
            workspace_id = new_incident["workspace_id"]
            old_incident_json = await async_redis.hget(
                f"ingestion-observer:{Incidents.QUARANTINE}:{workspace_id}", datasource_id
            )
            if old_incident_json:
                old_incident = json.loads(old_incident_json)
            else:
                old_incident = {
                    "status": IncidentStatus.IDLE,
                    "imports": 0,
                    "rows": 0,
                    "timeline": [],
                    "next_timestamp": 0,
                }
            # Merge old and new incidents
            next_timestamp = int(old_incident.get("next_timestamp", 0))
            incident = {
                "status": IncidentStatus.NEW if current_timestamp >= next_timestamp else IncidentStatus.PENDING,
                "imports": int(new_incident["imports"]) + int(old_incident["imports"]),
                "rows": int(new_incident["rows"]) + int(old_incident["rows"]),
                "timeline": (old_incident.get("timeline", []) + new_incident["timeline"])[
                    -INGESTION_OBSERVER_ERROR_LIMIT:
                ],
                "next_timestamp": next_timestamp,
            }
            # Store new incident
            await self._store_incident(workspace_id, datasource_id, Incidents.QUARANTINE, incident)
            await self._process_incident(workspace_id, datasource_id, Incidents.QUARANTINE, incident)

    async def _reset_incidents(self, workspace_id: str, datasource_id: str, incident_type: str):
        incident_by_type = {
            Incidents.ERROR: {"errors": []},
            Incidents.QUARANTINE: {"imports": 0, "rows": 0, "timeline": []},
        }[incident_type]

        incident = {
            **incident_by_type,  # type: ignore
            "status": IncidentStatus.SENT,
            "next_timestamp": int(datetime.now(timezone.utc).timestamp()) + INGESTION_OBSERVER_INCIDENT_TTL_SECONDS,
        }
        await self._store_incident(workspace_id, datasource_id, incident_type, incident)

    async def _process_incident(self, workspace_id: str, datasource_id: str, incident_type: str, incident: dict):
        is_incident_new = incident["status"] == IncidentStatus.NEW
        if not is_incident_new or not workspace_id or not datasource_id:
            return
        try:
            workspace = Users.get_by_id(workspace_id)
        except UserDoesNotExist:
            return
        datasource = Users.get_datasource(workspace, datasource_id)
        if not datasource:
            return
        emails = [
            member["email"]
            for member in workspace.members
            if member["active"] and Notifications.INGESTION_ERRORS in member["notifications"]
        ]
        if len(emails) > 0:
            emails.append(INTERNAL_SLACK_EMAIL)
        statsd_client.incr(
            f"tinybird-ingestion-observer.{statsd_client.region_machine}.{incident_type}.{workspace_id}.{datasource_id}"
        )
        await self._send_notification(emails, workspace, datasource, incident_type, incident)  # type: ignore
        await self._reset_incidents(workspace_id, datasource_id, incident_type)
        logging.info(f"IngestionObserver {incident_type}: {workspace_id} {datasource_id} {incident}")
        statsd_client.incr(
            f"tinybird-ingestion-observer.{statsd_client.region_machine}.{incident_type}.{workspace_id}.{datasource_id}"
        )

    async def _send_notification(
        self, emails: List[str], workspace: dict, datasource: dict, incident_type: str, incident: dict
    ):
        if not self._mailgun_service or len(emails) == 0:
            return
        action = {
            Incidents.ERROR: self._mailgun_service.send_notification_on_ingestion_incident,
            Incidents.QUARANTINE: self._mailgun_service.send_notification_on_quarantine_incident,
        }[incident_type]
        await action(emails, workspace, datasource, incident)


class IncidentStatus:
    IDLE = "idle"
    PENDING = "pending"
    NEW = "new"
    SENT = "sent"
