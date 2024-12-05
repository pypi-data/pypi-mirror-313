import base64
import logging
import os
from base64 import b64encode
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse

import aiohttp
import orjson
import pytz
import tornado.web
from nacl import encoding, public
from tornado.httpclient import AsyncHTTPClient
from tornado.template import Template

from tinybird.datasource import Datasource, SharedDatasource
from tinybird.git_settings import (
    CI_WORKFLOW_VERSION,
    DEFAULT_BRANCH,
    DEFAULT_INIT_FILES,
    DEFAULT_TINYENV_FILE,
    GITHUB_DATE_FORMAT,
    GITHUB_DEFAULT_EMPTY_TREE_HASH,
    GitHubResource,
    GitHubSettings,
    GitHubSettingsStatus,
    GitProviders,
    SemverVersions,
    bump_version,
    get_default_init_files_deploy,
)
from tinybird.pipe import Pipe
from tinybird.tokens import AccessToken
from tinybird.user import User, UserAccount, Users
from tinybird.views.base import WebBaseHandler, confirmed_account, cookie_domain
from tinybird.views.entities_datafiles import generate_datasource_datafile, generate_pipe_datafile
from tinybird_shared.retry.retry import retry_async

DEFAULT_TIMEOUT: float = 3600.0
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_SCOPE = "repo,workflow,read:org"

http_client = AsyncHTTPClient(defaults=dict(request_timeout=DEFAULT_TIMEOUT))


class GitHubException(Exception):
    pass


class GitHubWorkspaceSettings:
    def __init__(
        self,
        owner: str,
        access_token: str,
        remote: Optional[str] = "",
        name: Optional[str] = "",
        branch: Optional[str] = DEFAULT_BRANCH,
        owner_type: Optional[str] = "",
        project_path: Optional[str] = "",
        last_commit_sha: Optional[str] = "",
    ):
        if not name and remote:
            parsed_remote = urlparse(remote)
            name = parsed_remote.path.split("/")[-1].replace(".git", "")

        self.owner = owner
        self.owner_type = owner_type
        self.name = name
        self.access_token = access_token
        self.remote = remote
        self.branch = branch
        self.default_headers = GitHubInterface.DEFAULT_HEADERS
        self.default_headers["Authorization"] = f"token {access_token}"
        self.project_path = self.parse_valid_path_string(project_path)
        self.last_commit_sha = last_commit_sha

    def parse_valid_path_string(self, project_path: Optional[str] = "") -> str:
        """
        >>> GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", project_path="//invalid_path").project_path
        Traceback (most recent call last):
        ...
        Exception: Invalid project path //invalid_path
        >>> GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", project_path="/valid_path").project_path
        'valid_path'
        >>> GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", project_path="valid_path").project_path
        'valid_path'
        >>> GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git").project_path
        ''
        """
        if not project_path:
            return ""

        original_project_path = f"{project_path}"
        project_path = project_path[1:] if project_path.startswith("/") else project_path
        if os.path.isabs(project_path):
            raise Exception(f"Invalid project path {original_project_path}")
        return project_path

    @property
    def user_orgs_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.user_orgs_api_url
        'https://api.github.com/user/orgs'
        """
        return f"{GitHubInterface.API_URL}/user/orgs"

    @property
    def user_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.user_api_url
        'https://api.github.com/user'
        """
        return f"{GitHubInterface.API_URL}/user"

    @property
    def branch_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.branch_api_url
        'https://api.github.com/repos/owner/myremote/git/ref/heads/main'
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.branch_api_url
        'https://api.github.com/repos/owner/myremote/git/ref/heads/my_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/ref/heads/{self.branch}"

    def get_branch_api_url(self, branch):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_branch_api_url(branch="another_branch")
        'https://api.github.com/repos/owner/myremote/git/ref/heads/another_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/ref/heads/{branch}"

    @property
    def create_branch_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.create_branch_api_url
        'https://api.github.com/repos/owner/myremote/git/refs'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/refs"

    @property
    def update_branch_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.update_branch_api_url
        'https://api.github.com/repos/owner/myremote/git/refs/heads/main'
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.update_branch_api_url
        'https://api.github.com/repos/owner/myremote/git/refs/heads/my_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/refs/heads/{self.branch}"

    @property
    def trees_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.trees_api_url
        'https://api.github.com/repos/owner/myremote/git/trees'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/trees"

    @property
    def branch_trees_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.branch_trees_api_url
        'https://api.github.com/repos/owner/myremote/git/trees/main'
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.branch_trees_api_url
        'https://api.github.com/repos/owner/myremote/git/trees/my_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/trees/{self.branch}"

    @property
    def default_blobs_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.default_blobs_api_url
        'https://api.github.com/repos/owner/myremote/git/blobs'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/blobs"

    @property
    def defaul_commits_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.defaul_commits_api_url
        'https://api.github.com/repos/owner/myremote/git/commits'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/commits"

    @property
    def branch_commits_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="abc")
        >>> gh.branch_commits_api_url
        'https://api.github.com/repos/owner/myremote/commits/abc'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/commits/{self.branch}"

    def get_branch_commits_api_url(self, branch: Optional[str] = None):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="abc")
        >>> gh.get_branch_commits_api_url(branch="def")
        'https://api.github.com/repos/owner/myremote/commits/def'
        """
        branch = branch if branch else self.branch
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/commits/{branch}"

    def get_commits_api_url_sha(self, commit_sha: str):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.get_commits_api_url_sha('abc')
        'https://api.github.com/repos/owner/myremote/git/commits/abc'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/commits/{commit_sha}"

    def contents_api_url(self, resource: str):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.contents_api_url('path/to/file')
        'https://api.github.com/repos/owner/myremote/contents/path/to/file'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/contents/{resource}"

    def get_files_api_url_sha(self, commit_sha: str):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.get_files_api_url_sha('abc')
        'https://api.github.com/repos/owner/myremote/git/trees/abc?recursive=1'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/git/trees/{commit_sha}?recursive=1"

    @property
    def pull_request_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.pull_request_api_url
        'https://api.github.com/repos/owner/myremote/pulls?head=owner:my_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/pulls?head={self.owner}:{self.branch}"

    def get_pull_request_base_api_url(self, branch: Optional[str] = ""):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_pull_request_base_api_url(branch="origin_branch")
        'https://api.github.com/repos/owner/myremote/pulls?base=origin_branch'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/pulls?base={branch}"

    @property
    def create_pull_request_api_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.create_pull_request_api_url
        'https://api.github.com/repos/owner/myremote/pulls'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/pulls"

    def get_compare_api_url(self, base_branch: str):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_compare_api_url(base_branch="main")
        'https://github.com/owner/myremote/compare/main...my_branch'
        """
        return f"{GitHubInterface.UI_URL}/{self.owner}/{self.name}/compare/{base_branch}...{self.branch}"

    def get_branch_url(self, branch: Optional[str] = ""):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_branch_url(branch="another_branch")
        'https://github.com/owner/myremote/tree/another_branch'
        """
        return f"{GitHubInterface.UI_URL}/{self.owner}/{self.name}/tree/{branch}"

    @property
    def get_repositories_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", owner_type="organization", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_repositories_url
        'https://api.github.com/orgs/owner/repos'
        >>> gh = GitHubWorkspaceSettings(owner="owner", owner_type="user", access_token="123", remote="path/myremote.git", branch="my_branch")
        >>> gh.get_repositories_url
        'https://api.github.com/user/repos'
        """
        path = f"orgs/{self.owner}/repos" if self.owner_type == "organization" else "user/repos"
        return f"{GitHubInterface.API_URL}/{path}"

    @property
    def secret_key_url(self):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.secret_key_url
        'https://api.github.com/repos/owner/myremote/actions/secrets/public-key'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/actions/secrets/public-key"

    def repository_secret_url(self, secret_name: str):
        """
        >>> gh = GitHubWorkspaceSettings(owner="owner", access_token="123", remote="path/myremote.git")
        >>> gh.repository_secret_url(secret_name="TB_TOKEN")
        'https://api.github.com/repos/owner/myremote/actions/secrets/TB_TOKEN'
        """
        return f"{GitHubInterface.API_URL}/repos/{self.owner}/{self.name}/actions/secrets/{secret_name}"


class GitHubInterface:
    API_URL = "https://api.github.com"
    UI_URL = "https://github.com"
    ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API_URL = "https://api.github.com/user"

    DEFAULT_HEADERS = {
        "User-Agent": "Tinybird (tinybird.co)",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    @classmethod
    async def _fetch_repositories(
        self,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        page: int = 1,
        per_page: int = 100,
        sort: Optional[str] = "updated",
        order: Optional[str] = "desc",
    ):
        try:
            params = {
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "direction": order,
                "type": "all" if github_settings.owner_type == "organization" else "owner",
            }

            async with session.get(
                f"{github_settings.get_repositories_url}?{urlencode(params)}",
                headers=github_settings.default_headers,
            ) as response:
                result = (await response.content.read()).decode()
                data = orjson.loads(result)

                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    if "Validation Failed" in error:
                        raise Exception("GitHub error: GitHub verification is not supported")
                    raise Exception(f"Error searching repositories: {error}")

                next_data = []
                if "next" in response.links:
                    next_data = await self._fetch_repositories(
                        github_settings=github_settings,
                        session=session,
                        page=page + 1,
                        per_page=per_page,
                        sort=sort,
                        order=order,
                    )

                return data + next_data
        except Exception as e:
            logging.exception(e)
            raise Exception("There was an error while connecting to GitHub")

    @classmethod
    async def get_account_information(
        cls, workspace: User, github_settings: GitHubWorkspaceSettings, session: aiohttp.ClientSession
    ):
        owners: List[Dict[str, str]] = []
        error: Optional[str] = None

        try:
            async with session.get(
                github_settings.user_orgs_api_url, headers=github_settings.default_headers
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error getting information: {error}")
                owners = [{"owner": d.get("login"), "owner_type": "organization"} for d in data]
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception("There was an error while connecting to GitHub")

        try:
            async with session.get(github_settings.user_api_url, headers=github_settings.default_headers) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error getting information: {error}")
                owners.append({"owner": data.get("login"), "owner_type": "user"})
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception("There was an error while connecting to GitHub")
        return {"owners": owners}

    @classmethod
    async def get_access_token(cls, client_id: str, client_secret: str, code: str):
        params = {"client_id": client_id, "client_secret": client_secret, "code": code}
        response = await http_client.fetch(
            cls.ACCESS_TOKEN_URL,
            method="POST",
            body=urlencode(params).encode("utf-8"),
            headers={"Accept": "application/json"},
        )
        data = orjson.loads(response.body)
        access_token = data.get("access_token")
        if not access_token:
            logging.error(f"Could not connect to GitHub: {data}")
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )
        return access_token

    @classmethod
    async def get_owner_info(cls, access_token: str):
        response = await http_client.fetch(
            cls.USER_API_URL,
            method="GET",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        data = orjson.loads(response.body)
        owner = data.get("login")

        if not owner:
            logging.error(f"Could not connect to GitHub: {data}")
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

        owner_type = data.get("type", "").lower()
        return {"owner": owner, "owner_type": owner_type}

    @classmethod
    async def generate_resources(
        cls,
        workspace: User,
        github_settings: GitHubWorkspaceSettings,
        pipes: Optional[List[Pipe]],
        datasources: Optional[List[Datasource]],
        session: aiohttp.ClientSession,
        extra_files: Optional[Dict[str, str]] = None,
        tinybird_token: Optional[AccessToken] = None,
    ) -> List[GitHubResource]:
        project_path = github_settings.project_path
        pipes = pipes or []
        datasources = datasources or []

        resources = await parse_resources_to_datafiles(
            workspace=workspace,
            pipes=pipes,
            datasources=datasources,
            project_path=project_path,
            tinybird_token=tinybird_token,
        )
        github_resources = []

        for resource_id, resource_name, resource_type, path, content, origin in resources:
            blob_sha = await cls.generate_blob_sha(github_settings, path, content, session)
            resource = GitHubResource(
                resource_id=resource_id,
                resource_name=resource_name,
                resource_type=resource_type,
                path=path,
                sha=blob_sha,
                origin=origin,
            )
            github_resources.append(resource)

        if extra_files:
            for name, content in extra_files.items():
                blob_sha = await cls.generate_blob_sha(github_settings, name, content, session)
                path_file = os.path.join(project_path or "", name) if name in DEFAULT_INIT_FILES else name
                resource = GitHubResource(
                    resource_id=name,
                    resource_name=name,
                    resource_type="extra_file",
                    path=path_file,
                    sha=blob_sha,
                    mode="100755" if name.startswith("scripts/") else "100644",
                )
                github_resources.append(resource)

        return github_resources

    @classmethod
    async def get_last_commit(
        cls, github_settings: GitHubWorkspaceSettings, session: aiohttp.ClientSession, branch: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            async with session.get(
                github_settings.get_branch_commits_api_url(branch=branch), headers=github_settings.default_headers
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    if error in ["Git Repository is empty.", "Not Found"]:
                        return {}
                    raise Exception(error)

                updated_at = data.get("commit", {}).get("author", {}).get("date", {})
                updated_at = (
                    str(datetime.strptime(updated_at, GITHUB_DATE_FORMAT).replace(tzinfo=pytz.utc))
                    if updated_at
                    else ""
                )

                return {
                    "sha": data.get("sha", ""),
                    "message": data.get("commit", {}).get("message", ""),
                    "updated_at": updated_at,
                    "updated_by": data.get("commit", {}).get("author", {}).get("email", ""),
                }
        except Exception as e:
            branch = branch or github_settings.branch
            if "No commit found for SHA" in str(e):
                raise Exception(
                    f"Branch {branch} does not exist in GitHub: {e}. Make sure the Workspace is connected to GitHub. Contact as at support@tinybird.co if you need help."
                ) from e
            raise Exception(f"Error getting last commit from GitHub: {e}.") from e

    @classmethod
    async def get_last_tree_sha(
        cls,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        last_commit_sha: Optional[str] = "",
    ) -> str:
        try:
            if not last_commit_sha:
                return GITHUB_DEFAULT_EMPTY_TREE_HASH

            async with session.get(
                github_settings.get_commits_api_url_sha(last_commit_sha), headers=github_settings.default_headers
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")
                if data.get("tree"):
                    return data.get("tree", {}).get("sha", "")
                return data.get("sha", "")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def create_tree(
        cls,
        github_settings: GitHubWorkspaceSettings,
        tree: List[GitHubResource],
        last_tree_sha: str,
        session: aiohttp.ClientSession,
    ):
        parsed_tree = []

        try:
            parsed_tree = [{"mode": r.mode, "path": r.path, "sha": r.sha, "type": r.type} for r in tree]
            async with session.post(
                github_settings.trees_api_url,
                headers=github_settings.default_headers,
                json={"base_tree": last_tree_sha, "tree": parsed_tree},
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")
                return data.get("sha", "")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(f"{e}, tree: {parsed_tree}")
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def create_commit(
        cls,
        github_settings: GitHubWorkspaceSettings,
        message: str,
        tree_sha: str,
        parent_commit_sha: str,
        email: str,
        session: aiohttp.ClientSession,
    ):
        try:
            async with session.post(
                github_settings.defaul_commits_api_url,
                headers=github_settings.default_headers,
                json={
                    "message": message,
                    "parents": [parent_commit_sha],
                    "tree": tree_sha,
                    "author": {"name": email, "email": email},
                },
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")
                return data.get("sha", "")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def create_first_commit(
        cls, github_settings: GitHubWorkspaceSettings, session: aiohttp.ClientSession, workspace_name: Optional[str]
    ) -> str:
        title = workspace_name or "Tinybird Project"
        return await cls.push_file(
            github_settings=github_settings,
            file_name="README.md",
            commit_message=f"Initialize {title}",
            file_content=f"# {title}",
            session=session,
        )

    @classmethod
    async def update_branch(
        cls,
        github_settings: GitHubWorkspaceSettings,
        commit_sha: str,
        resources: List[GitHubResource],
        session: aiohttp.ClientSession,
    ):
        try:
            async with session.patch(
                github_settings.update_branch_api_url,
                headers=github_settings.default_headers,
                json={"sha": commit_sha},
            ) as response:
                data = orjson.loads(await response.read())

                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")

                if data.get("object"):
                    data = data.get("object", {})

                return {"url": data.get("url", ""), "commit": data.get("sha", ""), "resources": resources}
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def push_file(
        cls,
        github_settings: GitHubWorkspaceSettings,
        commit_message: str,
        file_name: str,
        file_content: str,
        session: aiohttp.ClientSession,
        branch: Optional[str] = None,
    ) -> str:
        try:
            resource = (
                os.path.join(github_settings.project_path or "", file_name)
                if file_name in DEFAULT_INIT_FILES.keys()
                else file_name
            )
            async with session.put(
                github_settings.contents_api_url(resource),
                headers=github_settings.default_headers,
                json={
                    "message": commit_message,
                    "content": base64.b64encode(file_content.encode("utf-8")).decode(),
                    "branch": branch or github_settings.branch,
                },
            ) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")
                return data.get("commit", {}).get("sha", "")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(f"Error pushing file {file_name} to GitHub: {e}.")

    @classmethod
    async def push_multiple_files(
        cls,
        workspace: User,
        user: UserAccount,
        github_settings: GitHubWorkspaceSettings,
        message: str,
        pipes: Optional[List[Pipe]],
        datasources: Optional[List[Datasource]],
        host: str,
        session: aiohttp.ClientSession,
        include_templates: Optional[bool] = False,
        last_commit_sha: Optional[str] = "",
        tinybird_token: Optional[AccessToken] = None,
        extra_files: Optional[Dict[str, str]] = None,
        tinyenv_version: Optional[str] = None,
    ):
        data_project_dir = (github_settings.project_path or "").strip("/") or "."

        template_params = {
            "data_project_dir": data_project_dir,
            "tb_host": host,
            "workflow_version": CI_WORKFLOW_VERSION,
            "workspace_name": workspace.name,
            "tb_admin_token_name": f"TB_{workspace.name.upper()}_ADMIN_TOKEN",
        }

        files_to_initialize = dict(DEFAULT_INIT_FILES)

        file_shas: Dict[str, Any] = {}
        extra_files = {} if not extra_files else extra_files

        # 1. Get Last Commit SHA
        try:
            if not last_commit_sha:
                commit = await cls.get_last_commit(github_settings, session)
                last_commit_sha = commit.get("sha", "")
        except Exception:
            pass

        # 2. Get the Tree SHA of the latest commit
        last_tree_sha = await cls.get_last_tree_sha(github_settings, session, last_commit_sha)
        if not last_tree_sha or last_tree_sha == GITHUB_DEFAULT_EMPTY_TREE_HASH:
            last_commit_sha = await cls.create_first_commit(
                github_settings=github_settings, session=session, workspace_name=workspace.name
            )
            last_tree_sha = await cls.get_last_tree_sha(github_settings, session, last_commit_sha)

        if include_templates:
            files_to_initialize.update(get_default_init_files_deploy(workspace.name))

            if last_commit_sha:
                file_shas = await cls.get_files_sha_for_commit(
                    github_settings=github_settings,
                    commit_sha=last_commit_sha,
                    session=session,
                )

            for file_name, file_content in files_to_initialize.items():
                file_sha = file_shas.get(file_name, "")
                if file_sha:
                    continue

                extra_files[file_name] = Template(file_content).generate(**template_params).decode()

        if tinyenv_version and tinyenv_version != SemverVersions.CURRENT.value:
            version = workspace.current_release.semver if workspace.current_release else "0.0.0"
            version = bump_version(version=version, next_version=tinyenv_version)
            tinyenv_content_file = DEFAULT_TINYENV_FILE
            updated_lines = []
            for line in tinyenv_content_file.split("\n"):
                if line.startswith("VERSION="):
                    updated_lines.append(f"VERSION={version}\n")
                else:
                    updated_lines.append(line)
            file_content = "\n".join(updated_lines)
            extra_files[".tinyenv"] = Template(file_content).generate(**template_params).decode()

        # 3. Create a new Tree
        resources = await cls.generate_resources(
            workspace=workspace,
            github_settings=github_settings,
            pipes=pipes,
            datasources=datasources,
            session=session,
            extra_files=extra_files,
            tinybird_token=tinybird_token,
        )

        if not resources:
            return {"commit": last_commit_sha}

        new_tree_sha = await cls.create_tree(github_settings, resources, last_tree_sha, session)

        # 4. Create a new Commit
        assert isinstance(last_commit_sha, str)
        new_commit_sha = await cls.create_commit(
            github_settings,
            message=message,
            tree_sha=new_tree_sha,
            parent_commit_sha=last_commit_sha,
            session=session,
            email=user.email,
        )

        # 5. Update Branch
        branch = await cls.update_branch(
            github_settings=github_settings, commit_sha=new_commit_sha, resources=resources, session=session
        )

        # 6. Update resources
        Users.update_last_commit(workspace, last_commit=branch.get("commit"), resources=resources)

        return {"url": branch.get("url"), "commit": branch.get("commit")}

    @classmethod
    @retry_async(GitHubException, tries=3, delay=0.5)
    async def generate_blob_sha(
        cls, github_settings: GitHubWorkspaceSettings, path: str, content: str, session: aiohttp.ClientSession
    ):
        try:
            file_content = base64.b64encode(content.encode("utf-8")).decode()
            async with session.post(
                github_settings.default_blobs_api_url,
                headers=github_settings.default_headers,
                json={"content": file_content, "encoding": "base64"},
            ) as response:
                error: Optional[str]
                try:
                    raw_data = await response.read()
                    data = orjson.loads(raw_data)
                except orjson.JSONDecodeError:
                    error = "Failed to decode JSON from response."
                    raise GitHubException(f"Error pushing file: {error}")
                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error pushing file: {error}")
                return data.get("sha", "")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error pushing file {path}: {e}.")

    @classmethod
    async def get_default_branch_for_repo(
        cls, repository_url: str, github_token: str, session: aiohttp.ClientSession
    ) -> Optional[str]:
        url_parts = urlparse(repository_url)
        req_url = f"https://api.github.com/repos{url_parts.path}"

        result = None

        try:
            headers = GitHubInterface.DEFAULT_HEADERS
            headers["Authorization"] = f"token {github_token}"

            async with session.get(req_url, headers=headers) as resp:
                r_limit = int(resp.headers.get("x-ratelimit-remaining", -1))
                if r_limit > 0 and r_limit <= 1000 and r_limit % 100 == 0:  # warn every 100 changes
                    logging.warning(
                        f"Github API request limit almost exhaust ({r_limit} remaining): x-ratelimit-reset={resp.headers.get('x-ratelimit-reset', '<unknown>')}"
                    )
                elif r_limit == 0:
                    logging.warning(
                        f"Github API request limit exhausted: x-ratelimit-reset={resp.headers.get('x-ratelimit-reset', '<unknown>')}"
                    )

                if resp.status == 200:
                    repo_info = orjson.loads(await resp.read())
                    result = repo_info.get("default_branch", None)
        except Exception as ex:
            logging.exception(ex)

        return result or DEFAULT_BRANCH

    @classmethod
    async def get_files_sha_for_commit(
        cls, github_settings: GitHubWorkspaceSettings, commit_sha: str, session: aiohttp.ClientSession
    ) -> Dict[str, Any]:
        files_sha_url = github_settings.get_files_api_url_sha(commit_sha=commit_sha)

        try:
            async with session.get(files_sha_url, headers=github_settings.default_headers) as response:
                data = orjson.loads(await response.read())
                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error getting files: {error}")

                file_blob_shas = {file["path"]: file["sha"] for file in data.get("tree") if file["type"] == "blob"}
                return file_blob_shas
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(f"Error getting files: {e}")

    @classmethod
    async def get_pull_request(
        cls, github_settings: GitHubWorkspaceSettings, session: aiohttp.ClientSession, base_branch: Optional[str] = None
    ) -> dict[Any, dict[str, Any]]:
        try:
            error: Optional[str] = ""
            if base_branch:
                async with session.get(
                    github_settings.pull_request_api_url, headers=github_settings.default_headers
                ) as response:
                    data = orjson.loads(await response.read())
                    if response.status >= 400:
                        error = data.get("message")
                        if not error:
                            error = data
                        raise GitHubException(f"Error getting files: {error}")

                    url = (
                        data[0].get("html_url")
                        if data
                        else github_settings.get_compare_api_url(base_branch=base_branch)
                    )
                    title = data[0].get("title") if data else ""
                    return {"url": url, "title": title}  # type: ignore
            else:
                async with session.get(
                    github_settings.get_pull_request_base_api_url(branch=github_settings.branch),
                    headers=github_settings.default_headers,
                ) as response:
                    data = orjson.loads(await response.read())
                    if response.status >= 400:
                        error = data.get("message")
                        if not error:
                            error = data
                        raise GitHubException(f"Error getting files: {error}")

                    pull_requests = {}
                    for pr in data:
                        name = pr.get("head").get("ref")
                        pull_requests[name] = {"url": pr.get("url"), "title": pr.get("title")}
                    return pull_requests
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def create_pull_request(
        cls,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        base_branch: str,
        title: str,
        description: Optional[str] = "",
    ) -> Dict[str, Any]:
        try:
            pull_request_data = {
                "title": title,
                "body": description,
                "head": github_settings.branch,
                "base": base_branch,
            }

            async with session.post(
                github_settings.create_pull_request_api_url,
                headers=github_settings.default_headers,
                json=pull_request_data,
            ) as response:
                data = orjson.loads(await response.read())

                if response.status >= 400:
                    error: Optional[str] = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error getting files: {error}")

                pull_request = data[0] if data else {}
                return {
                    "url": pull_request.get("html_url", ""),
                    "state": pull_request.get("state", ""),
                    "title": pull_request.get("title", ""),
                }
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def create_branch(
        cls,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        base_branch: Optional[str] = "",
        target_branch: Optional[str] = "",
        commit_sha: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            target_branch = target_branch if target_branch else github_settings.branch
            base_branch = base_branch if base_branch else github_settings.branch

            if target_branch == base_branch:
                raise GitHubException("Base branch and target branch can not be the same")

            if not commit_sha:
                commit = await cls.get_last_commit(github_settings, session, base_branch)
                commit_sha = commit.get("sha", "")

            branch_data = {"ref": f"refs/heads/{target_branch}", "sha": commit_sha}

            async with session.post(
                github_settings.create_branch_api_url,
                headers=github_settings.default_headers,
                json=branch_data,
            ) as response:
                data = orjson.loads(await response.read())
                error: Optional[str] = ""

                if response.status == 422:
                    error = data.get("message", "There was an error with GitHub. Please try again.")
                    raise GitHubException(f"Error creating branch, {error}")

                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(f"Error creating branch, {error}")

                return {
                    "url": github_settings.get_branch_url(branch=target_branch),
                    "commit_sha": data.get("object", {}).get("sha"),
                }
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

    @classmethod
    async def get_repositories(
        cls,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        sort: Optional[str] = "updated",
        order: Optional[str] = "desc",
    ):
        try:
            data = await cls._fetch_repositories(
                github_settings=github_settings, session=session, sort=sort, order=order
            )

            return {"items": data}
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception("There was an error while connecting to GitHub")

    @classmethod
    async def create_secret_in_repo(
        cls,
        github_settings: GitHubWorkspaceSettings,
        session: aiohttp.ClientSession,
        secret_name: str,
        secret_value: str,
    ) -> str:
        key = ""
        key_id = ""

        # 1. Get the public key to be able to generate secrets
        try:
            async with session.get(
                f"{github_settings.secret_key_url}", headers=github_settings.default_headers
            ) as response:
                result = (await response.content.read()).decode()
                data = orjson.loads(result)

                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(error)

                key = data.get("key")
                key_id = data.get("key_id")
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception("There was an error while connecting to GitHub")

        # 2. Try to delete the secret if it exists. Needed to link after unlink.
        try:
            async with session.delete(
                f"{github_settings.repository_secret_url(secret_name=secret_name)}",
                headers=github_settings.default_headers,
            ) as response:
                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(error)
        except Exception as e:
            logging.warning(f"Error deleting secret: {e}")

        # 3. Add the secret
        try:
            encrypted_value = encrypt_secret_value(key, secret_value)

            async with session.put(
                f"{github_settings.repository_secret_url(secret_name=secret_name)}",
                headers=github_settings.default_headers,
                json={
                    "encrypted_value": encrypted_value,
                    "key_id": key_id,
                },
            ) as response:
                if response.status >= 400:
                    error = data.get("message")
                    if not error:
                        error = data
                    raise GitHubException(error)
                return secret_name
        except GitHubException:
            raise
        except Exception as e:
            logging.exception(e)
            # FIXME better exception message
            raise Exception("There was an error while connecting to GitHub")


class GitHubIntegrationRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    async def get(self, *args):
        code: str = self.get_argument("code", "")
        github_config = self.settings.get("github_integration")

        if not github_config or not code:
            self.set_status(404)
            self.render("404.html")
            return

        client_id: str = github_config["client_id"]
        client_secret: str = github_config["client_secret"]

        access_token = await GitHubInterface.get_access_token(
            client_id=client_id, client_secret=client_secret, code=code
        )

        owner_info = await GitHubInterface.get_owner_info(access_token)
        owner = owner_info.get("owner")
        params = {
            "provider": GitProviders.GITHUB.value,
            "access_token": access_token,
            "owner": owner,
            "owner_type": owner_info.get("owner_type"),
        }

        # 1. save params in cookie
        domain = cookie_domain(self)
        is_https = self.application.settings.get("host", "").startswith("https")
        self.set_secure_cookie("github_params", orjson.dumps(params), domain=domain, secure=is_https, httponly=True)

        # 2. get saved region from cookie to redirect -> init handler
        origin = self.get_secure_cookie("github_origin")
        if not origin:
            logging.error(f"Could handle GitHub redirection for owner: {owner}")
            raise Exception(
                "There was an error while connecting to GitHub. Please, retry or contact us at support@tinybird.co"
            )

        url = f"{origin.decode()}/git-integrations/github-init"
        return self.redirect(url)


class GitHubIntegrationInitHandler(WebBaseHandler):
    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args):
        user = self.get_current_user()
        if not user:
            self.redirect("/login")
            return

        workspace = self.get_current_workspace()
        if not workspace:
            self.redirect("/dashboard")
            return

        # 1. get saved params in cookie
        params = self.get_secure_cookie("github_params")
        if not params:
            self.redirect("/dashboard")
            return

        params = orjson.loads(params)

        # 2. save to remote
        remote_settings = GitHubSettings(
            provider=params.get("provider"),
            access_token=params.get("access_token"),
            owner=params.get("owner"),
            owner_type=params.get("owner_type"),
            status=GitHubSettingsStatus.LINKED.value,
        )

        workspace = await Users.update_remote(workspace, remote=remote_settings)
        domain = cookie_domain(self)

        # 3. remove cookies
        self.clear_cookie("github_params", domain=domain)
        self.clear_cookie("github_origin", domain=domain)

        # 4. redirect
        return self.redirect(self.reverse_url("workspace_git", workspace.id))


class GitHubIntegrationAuthorizeHandler(WebBaseHandler):
    @tornado.web.authenticated
    async def get(self, *args):
        github_config = self.settings.get("github_integration")

        if not github_config:
            self.set_status(404)
            self.render("404.html")
            return

        client_id: str = github_config["client_id"]

        params = {"client_id": client_id, "scope": GITHUB_SCOPE}

        origin = self.settings.get("host")
        domain = cookie_domain(self)
        is_https = origin.startswith("https")
        self.set_secure_cookie("github_origin", origin, domain=domain, secure=is_https, httponly=True)

        url = f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}"
        self.redirect(url)


def get_pipe_path(project_path, name):
    path = f"{project_path}/pipes/{name}.pipe"
    if path[0] == "/":
        path = path[1:]
    return path


async def parse_pipe_datafile(workspace: User, pipe: Pipe, project_path: Optional[str] = ""):
    path = get_pipe_path(project_path, pipe.name)
    content = await generate_pipe_datafile(pipe=pipe, workspace=workspace, format=True)
    origin = workspace.name
    return path, content, origin


def get_datasource_path(project_path, datasource):
    if project_path and project_path[0] == "/":
        project_path = project_path[1:]

    path = f"{project_path}"

    if isinstance(datasource, SharedDatasource):
        path = (
            f"{path}/vendor/{datasource.original_workspace_name}/datasources/{datasource.original_ds_name}.datasource"
        )
    else:
        path = f"{path}/datasources/{datasource.name}.datasource"

    if path[0] == "/":
        path = path[1:]

    return path


async def parse_datasource_datafile(
    workspace: User,
    datasource: Datasource,
    project_path: Optional[str] = "",
    tinybird_token: Optional[AccessToken] = None,
):
    path = get_datasource_path(project_path, datasource)
    content = await generate_datasource_datafile(
        workspace=workspace, ds_meta=datasource, current_token=tinybird_token, format=True
    )
    origin = datasource.original_workspace_name if isinstance(datasource, SharedDatasource) else workspace.name
    return path, content, origin


async def parse_resources_to_datafiles(
    workspace: User,
    pipes: List[Pipe],
    datasources: List[Datasource],
    project_path: Optional[str] = "",
    tinybird_token: Optional[AccessToken] = None,
):
    resources = []
    for pipe in pipes:
        path, content, origin = await parse_pipe_datafile(workspace, pipe, project_path)
        resources.append((pipe.id, pipe.name, "pipe", path, content, origin))

    for datasource in datasources:
        path, content, origin = await parse_datasource_datafile(workspace, datasource, project_path, tinybird_token)
        resources.append((datasource.id, datasource.name, "datasource", path, content, origin))

    return resources


def encrypt_secret_value(public_key, secret_value) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key=public_key.encode("utf-8"), encoder=encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")
