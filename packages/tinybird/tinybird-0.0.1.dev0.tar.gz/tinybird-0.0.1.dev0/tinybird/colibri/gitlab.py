import os
import re
from typing import Optional

import requests

from .logging import log_info

TINYBIRD_PROJECTID = 6576720
GITLAB_API = f"https://gitlab.com/api/v4/projects/{TINYBIRD_PROJECTID}"
ISSUES_API = f"{GITLAB_API}/issues"
BRANCH_API = f"{GITLAB_API}/repository/branches"
COMMIT_API = f"{GITLAB_API}/repository/commits"
MERGE_API = f"{GITLAB_API}/merge_requests"


def create_gitlab_ticket(title: str, description: str, labels: str) -> Optional[str]:
    headers = {"Authorization": "Bearer glpat-9rQ7nsQK5RjoToa6nUjW"}
    content = {"title": title, "description": description, "labels": labels}
    r = requests.post(ISSUES_API, headers=headers, json=content)
    if not r.ok:
        return None
    return str(r.json()["web_url"])


def create_upgrade_ticket(cluster: str, version: str, hosts: str) -> Optional[str]:
    title = f"Upgrade Clickhouse cluster {cluster} to version {version}"
    labels = "ClickHouse Upgrade"

    description = f"""
The Clickhouse cluster needs to be upgraded to the current version {version}

The hosts that are in this cluster are {hosts}

You will need to validate that the new version is not problematic on this environments, for
that you will need to use the [ClickHouse Validator](https://wiki.tinybird.co/doc/how-to-upgrade-clickhouse-p53Dgqe8Uz).

The validation itself is a safe procedure. The upgrade itself, should be done assisted by
[Colibri](https://wiki.tinybird.co/doc/colibri-DIyk5pBTIu)"""
    return create_gitlab_ticket(title, description, labels)


def create_gitlab_branch(token: str, branch: str) -> None:
    headers = {"Authorization": f"Bearer {token}"}
    details = {"branch": branch, "ref": "master"}
    try:
        r = requests.post(BRANCH_API, headers=headers, json=details)
        if r.status_code == 201:
            log_info(f"Branch '{branch}' created successfully.")
    except Exception as e:
        log_info(f"Failed to create branch. {e}")


def create_gitlab_commit(token: str, branch: str, commit_message: str, path: str, content: str) -> None:
    headers = {"Authorization": f"Bearer {token}"}
    details = {
        "branch": branch,
        "commit_message": commit_message,
        "actions": [
            {
                "action": "update",
                "file_path": path,
                "content": content,
            }
        ],
    }
    try:
        r = requests.post(COMMIT_API, headers=headers, json=details)
        if r.status_code == 201:
            log_info("Commit successful.")
    except Exception as e:
        log_info(f"Error performing commit into branch: {e}")


def create_gitlab_mr(token: str, branch: str, title: str, description: str, labels: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    details = {
        "source_branch": branch,
        "target_branch": "master",
        "title": title,
        "description": description,
        "labels": labels,
    }

    try:
        r = requests.post(MERGE_API, headers=headers, json=details)
        # Check if the response is successful
        if r.status_code == 201:
            log_info("Merge request created successfully.")
            return str(r.json()["web_url"])
        else:
            return None
    except Exception as e:
        log_info(f"Error opening MR: {e}")
        return None


def create_upgrade_mr(token: str, cluster: str, version: str, issue: Optional[str] = None) -> Optional[str]:
    cluster_name = "clickhouse_cluster_" + cluster
    labels = "ClickHouse Upgrade"
    # Create new branch
    new_branch = "upgrade_ch_" + cluster + "_" + version
    if issue is not None:
        new_branch = issue + "_" + new_branch

    create_gitlab_branch(token, new_branch)

    # Modify file
    file_path = os.path.join(os.getcwd(), "inventories", "02-clickhouse-config.yaml")
    with open(file_path, "r") as file:
        content = file.read()

    pattern = rf"({cluster_name}.*?clickhouse_version\s*:\s*)([^\n\r]*)"
    matches = list(re.finditer(pattern, content, re.DOTALL))

    # Only updates the second match, if there's two
    if matches:
        match = matches[-1]
        updated_content = content[: match.start(2)] + version + content[match.end(2) :]
    else:
        updated_content = content

    # Commit this file into a new branch
    title = f"Update Clickhouse version for {cluster} to {version}."
    description = f"{title} Closes #{issue}" if issue else title
    path = "/deploy/inventories/02-clickhouse-config.yaml"
    create_gitlab_commit(token, new_branch, description, path, updated_content)

    # Open MR
    mr_url = create_gitlab_mr(token, new_branch, title, description, labels)
    return mr_url
