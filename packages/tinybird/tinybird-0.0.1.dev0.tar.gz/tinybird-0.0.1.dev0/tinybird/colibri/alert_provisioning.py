import functools
import json
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator, Tuple
from urllib.parse import quote

import _jsonnet
import requests

GRAFANA_URL = "https://grafana.tinybird.app"
GRAFANA_TOKEN = "glsa_II91nMKda29GYf9OKJ90DlfiJnxSHBoF_4da76104"

ALERTS_FOLDER = "DQg3Rtqnk"


@functools.cache
def get_datasources() -> dict[str, dict[str, str]]:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}"}
    r = requests.get(f"{GRAFANA_URL}/api/datasources", headers=headers)
    r.raise_for_status()
    response = r.json()
    return {ds["name"]: {"type": ds["type"], "uid": ds["uid"]} for ds in response}


def generate_alert_json(alert_file: str, datasource: str, extra_vars: Any = None) -> str:
    base_path = Path(alert_file)
    while base_path.name != "grafana":
        base_path = base_path.parent
    alert_json: str = _jsonnet.evaluate_file(
        alert_file,
        jpathdir=[str(base_path / "vendor"), str(base_path / "lib")],
        ext_vars={"datasources": json.dumps(get_datasources()), "datasource": datasource} | (extra_vars or {}),
    )
    return alert_json


def post_alert(alert_json: str) -> requests.Response:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    r = requests.post(
        f"{GRAFANA_URL}/api/v1/provisioning/alert-rules", headers=headers, data=alert_json.encode("utf-8")
    )
    r.raise_for_status()
    return r


def get_alert_group(alert_group: str, folder_uid: str = ALERTS_FOLDER) -> Any:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    r = requests.get(
        f"{GRAFANA_URL}/api/v1/provisioning/folder/{folder_uid}/rule-groups/{quote(alert_group, safe='')}",
        headers=headers,
    )
    if r.status_code == 404:
        return None

    r.raise_for_status()
    return r.json()


def delete_alert(alert_id: str) -> None:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    r = requests.delete(f"{GRAFANA_URL}/api/v1/provisioning/alert-rules/{alert_id}", headers=headers)
    r.raise_for_status()


def get_alerts_status(group_name: str = "CH Upgrades") -> Any:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    r = requests.get(f"{GRAFANA_URL}/api/prometheus/grafana/api/v1/rules", headers=headers)
    r.raise_for_status()

    json_response = r.json()

    # equivalent to jq '.data.groups[] | select(.name == "<group_name>") | .rules[] | select(.alerts !=  null) | .alerts[]'
    rules: Any = [rule for g in json_response["data"]["groups"] if g["name"] == group_name for rule in g["rules"]]
    alerts: Any = [alert for r in rules if r.get("alerts") for alert in r["alerts"]]

    return alerts


def silence_ch_is_down_for_instance(instance: str, duration: timedelta | None = None) -> Tuple[str, Any]:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    duration = duration or timedelta(minutes=30)
    body = {
        "startsAt": datetime.utcnow().isoformat(),
        "endsAt": (datetime.utcnow() + duration).isoformat(),
        "comment": "created by colibri",
        "createdBy": "colibri",
        "matchers": [
            {"name": "__alert_rule_uid__", "value": "88gqgp37k", "isEqual": True, "isRegex": False},
            {"name": "name", "value": f".*{instance}.*", "isEqual": True, "isRegex": True},
        ],
    }

    r = requests.post(
        f"{GRAFANA_URL}/api/alertmanager/grafana/api/v2/silences",
        headers=headers,
        data=json.dumps(body).encode("utf-8"),
    )
    r.raise_for_status()

    return str(r.json()["silenceID"]), body


def modify_silence_duration_ch_is_down(silence_id: str, body: Any, until: datetime) -> None:
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
    body["endsAt"] = until.isoformat()
    body["id"] = silence_id

    r = requests.post(
        f"{GRAFANA_URL}/api/alertmanager/grafana/api/v2/silences",
        headers=headers,
        data=json.dumps(body).encode("utf-8"),
    )
    r.raise_for_status()


@contextmanager
def ch_is_down_silenced(instance: str) -> Iterator[None]:
    try:
        silence_id, request_body = silence_ch_is_down_for_instance(instance)
        yield
    finally:
        modify_silence_duration_ch_is_down(silence_id, request_body, until=datetime.utcnow() + timedelta(minutes=5))
