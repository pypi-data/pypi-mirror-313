from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import logging
import os
import random
import re
import traceback
import typing
import unicodedata
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from functools import partial
from typing import Any, Coroutine, Dict, FrozenSet, List, Optional, Set, Tuple, Type, TypeVar, Union, cast
from urllib.parse import urlparse

from nacl.encoding import Base64Encoder
from passlib.hash import pbkdf2_sha256
from toposort import CircularDependencyError
from tornado.ioloop import IOLoop

from tinybird.ch import (
    HTTPClient,
    ch_database_exists,
    ch_databases_tables_schema_async,
    ch_drop_database,
    ch_finalize_aggregations,
    ch_many_tables_details_async,
    ch_server_is_reachable_and_has_cluster,
    ch_table_dependent_views_async,
)
from tinybird.ch_utils.constants import (
    CH_SETTINGS_JOIN_ALGORITHM_AUTO,
    CH_SETTINGS_JOIN_ALGORITHM_HASH,
    COPY_ENABLED_TABLE_FUNCTIONS,
    ENABLED_SYSTEM_TABLES,
    ENABLED_TABLE_FUNCTIONS,
    RESERVED_DATABASE_NAMES,
    SQL_KEYWORDS,
)
from tinybird.ch_utils.ddl import DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT
from tinybird.ch_utils.engine import TableDetails
from tinybird.constants import WORKSPACE_COLORS, BillingPlans, CHCluster, Notifications, Relationships
from tinybird.context import api_host, ff_preprocess_parameters_circuit_breaker, ff_split_to_array_escape
from tinybird.data_connector import DataConnector, DataSink
from tinybird.datasource import (
    DATASOURCE_CONNECTOR_TYPES,
    BranchDatasource,
    BranchSharedDatasource,
    Datasource,
    KafkaBranchDatasource,
    SharedDatasource,
    get_datasources_internal_ids,
)
from tinybird.default_secrets import DEFAULT_DOMAIN
from tinybird.exploration import Exploration, Explorations
from tinybird.feature_flags import FeatureFlag, FeatureFlagsService, FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.git_settings import GitHubResource, GitHubSettings, GitHubSettingsStatus
from tinybird.integrations.integration import IntegrationInfo
from tinybird.internal import get_by_pipe_endpoint
from tinybird.iterating.release import (
    DeleteRemoteException,
    LiveReleaseProtectedException,
    MaxNumberOfReleasesReachedException,
    Release,
    ReleaseStatus,
    ReleaseStatusException,
    validate_semver,
    validate_semver_greater_than_workspace_releases,
)
from tinybird.limits import EndpointLimit, EndpointLimits, Limit, RateLimitConfig
from tinybird.model import (
    RedisModel,
    retry_transaction_in_case_of_concurrent_edition_error_async,
    retry_transaction_in_case_of_concurrent_edition_error_sync,
)
from tinybird.pg import PGService
from tinybird.pipe import (
    DependentCopyPipeException,
    DependentMaterializedNodeException,
    DependentMaterializedNodeOnUpdateException,
    NodeNotFound,
    Pipe,
    PipeNode,
    PipeNodeTags,
    PipeNodeTypes,
    PipeTypes,
)
from tinybird.playground.playground import Playground, Playgrounds
from tinybird.replacements import REPLACEMENTS, Replacement
from tinybird.resource import ForbiddenWordException, Resource
from tinybird.snapshot import Snapshot
from tinybird.sql_template import CH_PARAM_PREFIX, TemplateExecutionResults, secret_template_key
from tinybird.sql_toolset import (
    VALID_REMOTE,
    InvalidFunction,
    InvalidResource,
    _separate_as_tuple_if_contains_database_and_table,
    replace_tables,
    sql_get_used_tables,
)
from tinybird.syncasync import sync_to_async
from tinybird.tag import ResourceTag, Tag
from tinybird.tb_secrets import Secret, secret_decrypt
from tinybird.token_origin import Origins, TokenOrigin
from tinybird.token_scope import ScopeException, scopes
from tinybird.tokens import AccessToken
from tinybird.tracing import ClickhouseTracer
from tinybird.user_workspace import (
    UserWorkspaceNotifications,
    UserWorkspaceNotificationsHandler,
    UserWorkspaceRelationship,
    UserWorkspaceRelationshipDoesNotExist,
    UserWorkspaceRelationships,
)
from tinybird_shared.gatherer_settings import GathererDefaults
from tinybird_shared.redis_client.redis_client import TBRedisClientSync

if typing.TYPE_CHECKING:
    from tinybird.views.mailgun import MailgunService


T = TypeVar("T", bound="User")


ENCRYPT_SETTINGS = dict(rounds=200000, salt_size=16)
MAX_SECRETS = 100


class TokenNotFound(Exception):
    pass


class SecretNotFound(Exception):
    pass


class TagNotFound(Exception):
    pass


class TokenUsedInConnector(Exception):
    pass


class WrongScope(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class UserAccountDoesNotExist(Exception):
    pass


class UserAccountAlreadyExists(Exception):
    pass


class ResourceDoesNotExist(Exception):
    pass


class UnreachableOrgCluster(Exception):
    pass


class WorkspaceAlreadyBelongsToOrganization(Exception):
    def __init__(self, workspace_id: str, organization_id: str, *args: Any, **kwargs: Any) -> None:
        self.workspace_id = workspace_id
        self.organization_id = organization_id
        super().__init__(*args, **kwargs)


class UserAccountAlreadyBelongsToOrganization(Exception):
    def __init__(self, user_id: str, organization_id: str, *args: Any, **kwargs: Any) -> None:
        self.user_id = user_id
        self.organization_id = organization_id
        super().__init__(*args, **kwargs)


class NameAlreadyTaken(Exception):
    def __init__(self, name_taken: str):
        super().__init__()
        self.name_taken = name_taken


class DatabaseNameCollisionError(Exception):
    pass


class WorkspaceNameIsNotValid(Exception):
    pass


class PipeNotFound(Exception):
    pass


class EndpointNotFound(Exception):
    pass


class CopyNodeNotFound(Exception):
    pass


class SinkNodeNotFound(Exception):
    pass


class StreamNodeNotFound(Exception):
    pass


class PipeIsMaterialized(Exception):
    pass


class PipeIsCopy(Exception):
    pass


class PipeIsDataSink(Exception):
    pass


class PipeIsStream(Exception):
    pass


class PipeIsNotDefault(Exception):
    pass


class PipeIsNotCopy(Exception):
    pass


class PipeIsNotDataSink(Exception):
    pass


class DataSourceNotFound(ValueError):
    def __init__(self, datasource_name: str):
        super().__init__()
        self.datasource_name = datasource_name


class DataSourceIsReadOnly(ValueError):
    pass


class CreateTokenError(Exception):
    pass


class CreateSecretError(Exception):
    pass


class CreateTagError(Exception):
    pass


class ResourceAlreadyExists(ValueError):
    pass


class DatasourceLimitReached(ValueError):
    pass


class DatasourceAlreadySharedWithWorkspace(ValueError):
    def __init__(self, datasource_name: str, workspace_id: str):
        super().__init__()
        self.datasource_name = datasource_name
        self.workspace_id = workspace_id


class DatasourceIsNotSharedWithThatWorkspace(ValueError):
    pass


class DataSourceIsNotASharedOne(ValueError):
    pass


class QueryNotAllowed(ValueError):
    def __init__(self, msg: str):
        def contains_fn_name(s, substring):
            pattern = rf"(?<![a-zA-Z_\d]){re.escape(substring)}(?![a-zA-Z_\d])"
            return bool(re.search(pattern, s))

        not_allowed = [fn for fn in COPY_ENABLED_TABLE_FUNCTIONS if contains_fn_name(msg, fn)]
        if any(not_allowed):
            _msg = ", ".join(not_allowed)
            msg = f"The {_msg} table function is only allowed in Copy Pipes. {msg}"
        super().__init__(msg)


class QueryNotAllowedForToken(ValueError):
    pass


class ServicesDataSourcesError(ValueError):
    pass


class PipeWithoutEndpoint(ValueError):
    pass


class WorkspaceException(Exception):
    pass


def simplify_characters(string: str) -> str:
    """
    >>> simplify_characters("abcáé123Ña")
    'abcae123Na'
    """
    nfkd_form = unicodedata.normalize("NFKD", string)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_token_name(connector_name: str, datasource_name: str) -> str:
    return f"{connector_name}_{datasource_name}"


class WorkspaceName:
    """
    >>> WorkspaceName('example name')
    Traceback (most recent call last):
    ...
    tinybird.user.WorkspaceNameIsNotValid: 'example name' is not a valid Workspace name. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use name_.
    >>> WorkspaceName('tinybird')
    Traceback (most recent call last):
    ...
    tinybird.user.WorkspaceNameIsNotValid: tinybird is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use tinybird_.
    >>> WorkspaceName('d_431241')
    Traceback (most recent call last):
    ...
    tinybird.user.WorkspaceNameIsNotValid: 'd_431241' can't be used as Workspace names can't start with 'd_'.
    >>> wn = WorkspaceName('SELECT')
    Traceback (most recent call last):
    ...
    tinybird.user.WorkspaceNameIsNotValid: SELECT is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use SELECT_.
    >>> wn = WorkspaceName('example_name')
    >>> str(wn)
    'example_name'
    >>> new_normalized_name = str(WorkspaceName.create_from_not_normalized_name('test.email@gmail.com'))
    >>> workspace_name_correctly_created_and_not_raising_exception = WorkspaceName(new_normalized_name)
    """

    def __init__(self, workspace_name: str) -> None:
        self.validate(workspace_name)
        self.workspace_name = workspace_name

    @staticmethod
    def validate(name: str) -> None:
        try:
            is_valid = Resource.validate_name(name)
        except ForbiddenWordException as e:
            raise WorkspaceNameIsNotValid(str(e))
        if not is_valid:
            raise WorkspaceNameIsNotValid(f"'{name}' is not a valid Workspace name. {Resource.name_help('name')}")
        if name in RESERVED_DATABASE_NAMES or name.lower() in SQL_KEYWORDS:
            raise WorkspaceNameIsNotValid(f"'{name}' can't be used as it's a reserved word.")
        if name.startswith("d_"):
            raise WorkspaceNameIsNotValid(f"'{name}' can't be used as Workspace names can't start with 'd_'.")

    def __str__(self) -> str:
        return self.workspace_name

    @classmethod
    def create_from_not_normalized_name(
        cls, unnormalized_name: str, random_string_at_the_end: bool = True, custom_random_string: Optional[str] = None
    ) -> "WorkspaceName":
        """
        >>> str(WorkspaceName.create_from_not_normalized_name('test.email.áccÈnt.Ññ@gmail.com', custom_random_string='a1b2c3'))
        'test_email_accEnt_Nn_gmail_com_a1b2c3'
        >>> str(WorkspaceName.create_from_not_normalized_name('test.email', random_string_at_the_end=False))
        'test_email'
        """

        name_without_accents = simplify_characters(unnormalized_name)
        normalized_name = Resource.normalize_name(name_without_accents, prefix="workspace")

        if random_string_at_the_end:
            suffix = custom_random_string if custom_random_string is not None else str(uuid.uuid4()).split("-")[-1]
            normalized_name += "_" + suffix
        return WorkspaceName(normalized_name)


class BranchName(WorkspaceName):
    def __init__(self, branch_name: str, main_name: str) -> None:
        self.validate(branch_name)
        self.branch_name = branch_name
        self.main_name = main_name
        super().__init__(f"{self.main_name}_{self.branch_name}")


@dataclass
class WorkspaceMember:
    email: str
    id: str
    role: str


class Users:
    """
    >>> u = UserAccount.register('test_users_class@example.com', 'pass')
    >>> w = User.register('test_users_class', admin=u.id)
    >>> w = User.get_by_id(w.id)
    >>> w['pipes']
    []
    >>> t = Users.add_pipe_sync(w, 'pipe', 'select * from table', description='my first pipe')
    >>> t.name
    'pipe'
    >>> t.description
    'my first pipe'
    >>> Users.get_pipe(w, t.id).name
    'pipe'
    >>> Users.get_by_id(w.id)['pipes'][0]['name']
    'pipe'
    >>> Users.drop_pipe(w, 'pipe')
    True
    >>> Users.drop_pipe(w, 'pipe')
    False
    >>> Users.get_tokens_for_resource(w, 'pipe', scopes.PIPES_READ)
    []
    >>> t = Users.get_token_for_scope(w, scopes.ADMIN)
    >>> t != ''
    True
    >>> t2 = Users.get_token_for_scope(w, scopes.DATASOURCES_CREATE)
    >>> t2 == None
    False
    >>> asyncio.run(Users.delete(w))
    True
    """

    _mailgun_service: MailgunService

    @dataclass
    class RollbackInfo:
        release_ids: List[str]
        pipes: List[Dict[str, Any]]
        datasources: List[Dict[str, Any]]
        tokens: List[AccessToken]

    @classmethod
    def config(cls, mailgun_service: MailgunService) -> None:
        cls._mailgun_service = mailgun_service

    @staticmethod
    def change_pg_password(workspace: User, password: str) -> bool:
        return workspace.change_pg_password(password)

    @staticmethod
    def set_name(workspace: User, name: WorkspaceName) -> User:
        with User.transaction(workspace.id) as user:
            user.set_name(name)
            return user

    @staticmethod
    def set_is_read_only(workspace: User, is_read_only: bool) -> User:
        with User.transaction(workspace.id) as user:
            user.set_is_read_only(is_read_only)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_endpoint_limit(workspace: User, name, value, endpoint, limit) -> User:
        with User.transaction(workspace.id) as user:
            user.limits[name] = (endpoint, limit, value)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def delete(workspace: User) -> bool:
        with User.transaction(workspace.id) as user:
            await user.delete()
        return True

    @staticmethod
    def get_by_id(workspace_id: str) -> User:
        user = User.get_by_id(workspace_id)
        if not user:
            raise UserDoesNotExist("workspace does not exist")
        return user

    @staticmethod
    def get_by_name(name: str) -> User:
        return User.get_by_name(name)

    @staticmethod
    def get_by_id_or_name(workspace_id_or_name: str) -> User:
        try:
            user = Users.get_by_id(workspace_id_or_name)
        except UserDoesNotExist:
            user = User.get_by_name(workspace_id_or_name)
        if not user:
            raise UserDoesNotExist("workspace does not exist")
        return user

    @staticmethod
    def get_by_database(database: str) -> User:
        return User.get_by_database(database)

    @staticmethod
    def confirmed_account(user: UserAccount) -> bool:
        return user.confirmed_account

    @staticmethod
    def get_datasource(
        workspace: User, ds_name_or_id: Optional[str], include_used_by: bool = False, include_read_only: bool = False
    ) -> Optional[Datasource]:
        """
        >>> u = UserAccount.register('test_get_datasource@example.com', 'pass')
        >>> w = User.register('test_get_datasource', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_datasource_sync(w, 'test')
        >>> Users.get_datasource(w, 'test').id == t.id
        True
        >>> Users.get_datasource(w, t.id).name == t.name
        True
        >>> Users.get_datasource(w, "t_vaya_tela_marinera_" + t.id.split('_')[-1]).name == t.name
        True
        >>> Users.get_datasource(w, "t_vaya_tela_marinera." + t.id.split('_')[-1]).name == t.name
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        user = User.get_by_id(workspace.id)
        return user.get_datasource(ds_name_or_id, include_used_by, include_read_only)

    @staticmethod
    def get_datasource_used_by(workspace: User, ds: Datasource, pipes: Optional[List[Pipe]] = None) -> List[Pipe]:
        user = User.get_by_id(workspace.id)
        return user.get_datasource_used_by(ds, pipes)

    @classmethod
    def get_datasource_dependencies(
        cls, workspace: User, ds_id: str, include_shared_with: bool = True
    ) -> Dict[str, Any]:
        ds = workspace.get_datasource(ds_id, include_used_by=True, include_read_only=True)
        dependencies: Any = {"pipes": []}

        if ds:
            shared_workspaces = [User.get_by_id(ws_id) for ws_id in ds.shared_with] if include_shared_with else []
            workspace_to_explore = [workspace, *shared_workspaces]
            for workspace in workspace_to_explore:
                ws_dependencies_indexed_by_pipe = cls._get_dependencies_in_workspace(workspace, ds)
                dependencies["pipes"].extend(ws_dependencies_indexed_by_pipe)

        return dependencies

    @classmethod
    def _get_dependencies_in_workspace(cls, workspace: User, ds: Datasource) -> List[Dict[str, Any]]:
        all_nodes_dependencies_to_datasources = cls.get_node_dependencies_to_all_datasources(workspace)
        dependencies_indexed_by_pipe = []
        pipes = workspace.get_pipes()

        for pipe in ds.used_by:
            if pipe.pipe_type == PipeTypes.COPY:
                pipe_object = pipe.to_json(attrs=["id", "name", "type"])

                copy_node = pipe.pipeline.get_node(pipe.copy_node)
                pipe_object["nodes"] = [copy_node.to_json(attrs=["id", "name", "sql", "params"])] if copy_node else []
                pipe_object["workspace"] = workspace.name
                dependencies_indexed_by_pipe.append(pipe_object)

        for pipe in pipes:
            pipe_object = pipe.to_json(attrs=["id", "name", "type"])
            pipe_object["nodes"] = []
            for node in pipe.pipeline.nodes:
                node_ds_deps = all_nodes_dependencies_to_datasources[node.id]["downstream_datasources_ids"]
                node_ds_deps.update(all_nodes_dependencies_to_datasources[node.id]["upstream_datasources_ids"])
                if ds.id in node_ds_deps:
                    node = workspace.get_node(node.id).to_json(attrs=["id", "name", "materialized", "sql"])  # type: ignore
                    pipe_object["nodes"].append(node)
            if pipe_object["nodes"]:
                pipe_object["workspace"] = workspace.name
                dependencies_indexed_by_pipe.append(pipe_object)

        return dependencies_indexed_by_pipe

    @classmethod
    def get_node_dependencies_to_all_datasources(self, workspace: "User"):
        def recursive_node_dependencies(all_nodes_dependencies_to_datasources: Dict, node: PipeNode, pipe: Pipe):
            if not all_nodes_dependencies_to_datasources.get(node.id):
                all_nodes_dependencies_to_datasources[node.id] = {
                    "downstream_datasources_ids": set(),
                    "upstream_datasources_ids": set(),
                }

            if node.materialized:
                all_nodes_dependencies_to_datasources[node.id]["downstream_datasources_ids"].add(node.materialized)

            # Check if all the node dependencies are data sources, i.e. there are no nodes in node.dependencies
            no_nodes_in_dependencies = [
                dependency for dependency in node.dependencies if dependency not in pipe.pipeline.node_names
            ]
            if no_nodes_in_dependencies:
                # A node where all dependencies are datasources is the base case, we can just add the datasources to
                # the upstream dependencies set and return
                downstream_datasources_ids = set([_ds_names_to_ids.get(ds_name) for ds_name in node.dependencies])
                all_nodes_dependencies_to_datasources[node.id]["upstream_datasources_ids"] = downstream_datasources_ids
                return

            # If there are nodes in the node.dependencies field, we check each dependency
            for dependency_name in node.dependencies:
                # If it is a datasource, add it to downstream dependencies set
                if ds_id := _ds_names_to_ids.get(dependency_name):
                    all_nodes_dependencies_to_datasources[node.id]["upstream_datasources_ids"].add(ds_id)
                    continue

                dependency_id = _node_index[f"{pipe.name}.{dependency_name}"]
                # If it is not a datasource, it must be a node
                if dependency_id not in all_nodes_dependencies_to_datasources.keys():
                    # If it is an explored node, explore it
                    unexplored_node = self.get_node(workspace, dependency_id)
                    recursive_node_dependencies(all_nodes_dependencies_to_datasources, unexplored_node, pipe)  # type: ignore
                explored_node_dependencies = all_nodes_dependencies_to_datasources[dependency_id]
                # If a node depends on another node, it should inherit all its upstream dependencies
                all_nodes_dependencies_to_datasources[node.id]["upstream_datasources_ids"].update(
                    explored_node_dependencies["upstream_datasources_ids"]
                )
                # And the depended node should inherit all current node downstream dependencies
                explored_node_dependencies["downstream_datasources_ids"].update(
                    all_nodes_dependencies_to_datasources[node.id]["downstream_datasources_ids"]
                )
            return

        all_nodes_dependencies_to_datasources: Dict = {}
        pipes = workspace.get_pipes()
        _ds_names_to_ids = {ds.name: ds.id for ds in Users.get_datasources(workspace)}
        _node_index = {}
        for pipe in pipes:
            _node_index.update({f"{pipe.name}.{node.name}": node.id for node in pipe.pipeline.nodes})

        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                if node.id not in all_nodes_dependencies_to_datasources:
                    recursive_node_dependencies(all_nodes_dependencies_to_datasources, node, pipe)
        return all_nodes_dependencies_to_datasources

    @staticmethod
    def get_source_workspace(workspace: User, source_datasource: Optional[Datasource]) -> User:
        if source_datasource and hasattr(source_datasource, "original_workspace_id"):
            return Users.get_by_id(source_datasource.original_workspace_id)
        else:
            return workspace

    @staticmethod
    def is_valid_cluster(u: User, cluster: Optional[str]) -> bool:
        if not cluster:
            return True
        return cluster in u.clusters

    @staticmethod
    def _add_datasource(
        u: User,
        ds_name: str,
        stats=None,
        cluster=None,
        tags=None,
        prefix="t",
        fixed_name=False,
        json_deserialization=None,
        description="",
        fixed_id: Optional[str] = None,
        origin_connector_id: Optional[str] = None,
        service_name=None,
        service_conf=None,
    ) -> Datasource:
        origin = User.get_by_id(u.origin) if u.is_branch and u.origin else None
        origin_database = origin.database if origin else None
        with User.transaction(u.id) as user:
            return user.add_datasource(
                ds_name,
                stats,
                cluster,
                tags,
                prefix,
                fixed_name=fixed_name,
                json_deserialization=json_deserialization,
                description=description,
                fixed_id=fixed_id,
                origin_database=origin_database,
                origin_connector_id=origin_connector_id,
                service_name=service_name,
                service_conf=service_conf,
            )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_many_datasources(u: User, datasources: List[Tuple[str, bool]], cluster=None, tags=None):
        created = []
        with User.transaction(u.id) as user:
            for ds_name, ds_fixed_name in datasources:
                created.append(user.add_datasource(ds_name, fixed_name=ds_fixed_name, cluster=cluster, tags=tags))
        return created

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_organization_id(workspace: User, organization_id: Optional[str]) -> None:
        if organization_id and workspace.organization_id and workspace.organization_id != organization_id:
            raise WorkspaceAlreadyBelongsToOrganization(workspace.id, workspace.organization_id)
        with User.transaction(workspace.id) as wksp:
            wksp.organization_id = organization_id

    @staticmethod
    async def add_users_to_workspace_async(
        workspace_id: str, users_emails: List[str], role: Optional[str] = None
    ) -> User:
        """
        >>> from tinybird.user import Users, UserAccount
        >>> u = UserAccount.register('test_workspace_add_users@example.com', 'pass')
        >>> w = User.register('test_workspace_add_users', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> u1 = UserAccount.register('test_users1_add@example.com', 'pass')
        >>> u1 = UserAccount.get_by_id(u1.id)
        >>> u2 = UserAccount.register('test_users2_add@example.com', 'pass')
        >>> u2 = UserAccount.get_by_id(u2.id)
        >>> u3 = UserAccount.register('test_users3_add@example.com', 'pass')
        >>> u3 = UserAccount.get_by_id(u3.id)
        >>> u4 = UserAccount.register('test_users4_add@example.com', 'pass')
        >>> u4 = UserAccount.get_by_id(u4.id)
        >>> _ = asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_users1_add@example.com', 'test_users2_add@example.com']))
        >>> 'test_users1_add@example.com' in w.user_accounts_emails
        True
        >>> 'test_users2_add@example.com' in w.user_accounts_emails
        True
        >>> len(asyncio.run(u1.get_workspaces()))
        1
        >>> len(asyncio.run(u2.get_workspaces()))
        1
        >>> _ = asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_users4_add@example.com'], role='admin'))
        >>> 'test_users4_add@example.com' in w.user_accounts_emails
        True
        >>> asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_users1_add@example.com']))
        Traceback (most recent call last):
        ...
        tinybird.user.WorkspaceException: User test_users1_add@example.com already belongs to test_workspace_add_users's workspace
        >>> _ = asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_users3_add@example.com', 'test_users3_add@example.com']))
        >>> 'test_users3_add@example.com' in w.user_accounts_emails
        True
        >>> _ = w.remove_users_from_workspace(['test_users1_add@example.com', 'test_users2_add@example.com', 'test_users3_add@example.com'])
        >>> w.set_max_seats_limit(2)
        >>> w.save()
        >>> _ = asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_users1_add@example.com', 'test_users2_add@example.com', 'test_users3_add@example.com']))
        Traceback (most recent call last):
        ...
        tinybird.user.WorkspaceException: Workspace maximum number of users is 2
        """

        @retry_transaction_in_case_of_concurrent_edition_error_async()
        async def update_workspace(user: UserAccount) -> User:
            with User.transaction(workspace_id) as wksp:
                wksp.create_workspace_access_token(user.id)
                UserWorkspaceRelationships.rename_user_token_by_role(user.id, wksp, role)
            return wksp

        workspace = User.get_by_id(workspace_id)

        user_emails_set = set(users_emails)

        if len(workspace.user_accounts_emails) + len(user_emails_set) > workspace.max_seats_limit:
            raise WorkspaceException(f"Workspace maximum number of users is {workspace.max_seats_limit}")

        for user_email in user_emails_set:
            user = UserAccounts.get_by_email(user_email)

            if len(await user.get_workspaces(with_environments=False)) + 1 >= user.max_workspaces_limit:
                raise WorkspaceException(
                    f"User {user.email} reached the maximum number of workspaces it can belong to ({user.max_workspaces_limit})"
                )

            if UserWorkspaceRelationship.user_has_access(user.id, workspace.id):
                raise WorkspaceException(f"User {user.email} already belongs to {workspace.name}'s workspace")

            UserWorkspaceRelationship.create_relationship(
                user_id=user.id, workspace_id=workspace.id, relationship=role or Relationships.VIEWER
            )

            workspace = await update_workspace(user)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_datasource_async(
        u: User,
        ds_name: str,
        stats=None,
        cluster=None,
        tags=None,
        prefix="t",
        fixed_name=False,
        json_deserialization=None,
        description="",
        fixed_id: Optional[str] = None,
        origin_connector_id: Optional[str] = None,
        service_name=None,
        service_conf=None,
    ) -> Datasource:
        return Users._add_datasource(
            u,
            ds_name,
            stats=stats,
            cluster=cluster,
            tags=tags,
            prefix=prefix,
            fixed_name=fixed_name,
            json_deserialization=json_deserialization,
            description=description,
            fixed_id=fixed_id,
            origin_connector_id=origin_connector_id,
            service_name=service_name,
            service_conf=service_conf,
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_datasource_sync(
        u: User,
        ds_name: str,
        stats=None,
        cluster=None,
        tags=None,
        prefix="t",
        fixed_name=False,
        json_deserialization=None,
        description="",
        fixed_id: Optional[str] = None,
        origin_connector_id: Optional[str] = None,
        service_name=None,
        service_conf=None,
    ) -> Datasource:
        return Users._add_datasource(
            u,
            ds_name,
            stats=stats,
            cluster=cluster,
            tags=tags,
            prefix=prefix,
            fixed_name=fixed_name,
            json_deserialization=json_deserialization,
            description=description,
            fixed_id=fixed_id,
            origin_connector_id=origin_connector_id,
            service_name=service_name,
            service_conf=service_conf,
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_pipe_async(
        u: User,
        name: str,
        edited_by: Optional[str],
        sql: Optional[str] = None,
        nodes: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        fixed_id: Optional[str] = None,
    ) -> Pipe:
        return Users._add_pipe(u, name, sql, nodes, description, fixed_id=fixed_id, edited_by=edited_by)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_pipe_sync(
        u: User, name: str, sql=None, nodes=None, description=None, fixed_id: Optional[str] = None
    ) -> Pipe:
        return Users._add_pipe(u, name, sql, nodes, description, fixed_id=fixed_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def clone_pipe(
        u: User,
        pipe: Pipe,
        fixed_id: Optional[str] = None,
    ) -> Pipe:
        with User.transaction(u.id) as user:
            new_pipe = user.add_pipe(
                pipe.name, None, [node.to_dict() for node in pipe.pipeline.clone().nodes], pipe.description, fixed_id
            )
            # legacy pipes published as endpoints and with materialized nodes
            if pipe.pipe_type == PipeTypes.ENDPOINT and not pipe.get_materialized_tables():
                user.set_node_of_pipe_as_endpoint(new_pipe.id, pipe.endpoint, pipe.edited_by)
            elif pipe.pipe_type == PipeTypes.COPY and pipe.copy_node:
                node = pipe.pipeline.get_node(pipe.copy_node)
                mode = node.mode if node else None
                user.set_node_of_pipe_as_copy(
                    new_pipe.id, pipe.copy_node, pipe.copy_target_datasource, user.id, mode, pipe.edited_by
                )
                user.set_source_copy_pipes_tag(pipe.copy_target_datasource, new_pipe.id)
            elif pipe.pipe_type == PipeTypes.DATA_SINK and pipe.sink_node:
                user.set_node_of_pipe_as_datasink(
                    pipe_name_or_id=new_pipe.id, node_name_or_id=pipe.sink_node, edited_by=pipe.edited_by
                )
            return new_pipe

    @staticmethod
    def _add_pipe(
        u: User,
        name: str,
        sql: Optional[str] = None,
        nodes: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        fixed_id: Optional[str] = None,
        edited_by: Optional[str] = None,
    ) -> Pipe:
        """
        >>> u = UserAccount.register('test_add_pipe@example.com', 'pass')
        >>> w = User.register('test_add_pipe', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> pipe = Users.add_pipe_sync(w, 'test_pipe', 'select * from table')
        >>> Users.get_pipe(w, 'test_pipe').id == pipe.id
        True
        >>> tokens = Users.get_tokens_for_resource(w, pipe.id, scopes.PIPES_READ)
        >>> len(tokens)
        0
        >>> with User.transaction(w.id) as user:
        ...     _ = user.add_token("Read Pipe '%s'" % pipe.name, scopes.PIPES_READ, pipe.id)
        >>> tokens = Users.get_tokens_for_resource(w, pipe.id, scopes.PIPES_READ)
        >>> len(tokens)
        1
        >>> pipe.id in Users.get_token_access_info(w, tokens[0]).get_resources()
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        with User.transaction(u.id) as user:
            return user.add_pipe(name, sql, nodes, description, fixed_id, edited_by=edited_by, workspace_id=user.id)

    @staticmethod
    def drop_token(u: "User", token: str) -> bool:
        """
        >>> u = UserAccount.register('drop_token@example.com', 'pass')
        >>> w = User.register('drop_token', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> # Test 1
        >>> t = Users.add_token(w, 'test', None)
        >>> Users.drop_token(w, t)
        True
        >>> # Test 2
        >>> t = Users.add_token(w, 'test2', None)
        >>> tk_info = Users.get_token_access_info(w, t)
        >>> tk_info != None
        True
        >>> Users.drop_token(w, tk_info.id)
        True
        >>> # Test 3
        >>> t = Users.add_token(w, 'test3', None)
        >>> tk_info = Users.get_token_access_info(w, t)
        >>> tk_info != None
        True
        >>> Users.drop_token(w, tk_info.name)
        True
        >>> # Test 4
        >>> tk_info = Users.get_token_access_info(w, t)
        >>> tk_info == None
        True
        >>> Users.drop_token(w, t)
        False
        >>> # Cleanup
        >>> asyncio.run(Users.delete(w))
        True
        """
        with User.transaction(u.id) as user:
            return user.drop_token(token)

    @staticmethod
    def drop_secret(u: "User", name: str) -> bool:
        result = False
        with User.transaction(u.id) as user:
            result = user.drop_secret(name)
        return result

    @staticmethod
    def drop_tag(u: "User", tag_id_or_name: str) -> bool:
        result = False
        with User.transaction(u.id) as user:
            result = user.drop_tag(tag_id_or_name)
        return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_secret(u: "User", name: str, value: str, edited_by: Optional[str]) -> Secret:
        with User.transaction(u.id) as user:
            secret = user.update_secret(name, value, edited_by)
            return secret

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_tag(
        u: "User", tag_id_or_name: str, name: Optional[str], resources: Optional[List[Dict[str, str]]]
    ) -> ResourceTag:
        with User.transaction(u.id) as user:
            tag = user.update_tag(tag_id_or_name, name, resources)
            return tag

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_resource_from_tags(u: "User", resource_id: str, resource_name: str) -> bool:
        with User.transaction(u.id) as user:
            return user.remove_resource_from_tags(resource_id, resource_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_token_async(u: "User", token: str) -> bool:
        return Users.drop_token(u, token)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_secret_async(u: "User", name: str) -> bool:
        return Users.drop_secret(u, name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_tag_async(u: "User", tag_id_or_name: str) -> bool:
        return Users.drop_tag(u, tag_id_or_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_token(u: User, name: str, scope: str, resource=None, origin: Optional[TokenOrigin] = None) -> str:
        """
        >>> u = UserAccount.register('test_add_token@example.com', 'pass')
        >>> w = User.register('test_add_token', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_token(w, 'test', None)
        >>> t = Users.add_token(w, 'test', None)
        Traceback (most recent call last):
        ...
        tinybird.user.CreateTokenError: Token with name "test" already exists
        """
        with User.transaction(u.id) as user:
            return user.add_token(name, scope, resource, origin)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_secret(u: User, name: str, value: str, edited_by: Optional[str]) -> Secret:
        """
        >>> User.secrets_key = Base64Encoder.decode("T67++TQ85w+bJH5jHKkdenvQyloztdipgP8F1q+w4CY=".encode())
        >>> u = UserAccount.register('test_add_secret@example.com', 'pass')
        >>> w = User.register('test_add_secret', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = await Users.add_secret(w, 'test', '1234', None)
        >>> t = await Users.add_secret(w, 'test', '1235', None)
        Traceback (most recent call last):
        ...
        tinybird.user.CreateSecretError: Secret with name "test" already exists
        """
        with User.transaction(u.id) as user:
            secret = user.add_secret(name, value, edited_by)
            return secret

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_tag(u: User, name: str, resources: List[Dict[str, str]]) -> ResourceTag:
        """
        >>> u = UserAccount.register('test_add_tag@example.com', 'pass')
        >>> w = User.register('test_add_tag', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = await Users.add_tag(w, 'test', [{'id': 'p_1', 'name': 'pipe_1', 'type': 'pipe'}])
        >>> t = await Users.add_tag(w, 'test', [{'id': 'p_1', 'name': 'pipe_1', 'type': 'pipe'}])
        Traceback (most recent call last):
        ...
        tinybird.user.CreateTagError: Tag with name "test" already exists
        """
        with User.transaction(u.id) as user:
            tag = user.add_tag(name, resources)
            return tag

    @staticmethod
    def add_scope_to_token(u, token, scope=None, resource=None, filters=None):
        with User.transaction(u.id) as user:
            return user.add_scopes_to_token(token, [(scope, resource, filters)])

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def create_new_token(
        workspace: "User",
        token_name: str,
        new_scopes: List[str],
        origin: TokenOrigin,
        description: Optional[str] = None,
    ) -> str:
        with User.transaction(workspace.id) as workspace:
            if workspace.get_token(token_name):
                raise CreateTokenError(f'Auth token with name "{token_name}" already exists')

            token = workspace.add_token(token_name, None, description=description, origin=origin)
            scope_details: List[Tuple[str, Optional[str], Optional[str]]] = []

            for s in new_scopes:
                scope, name_or_uid, _filter = AccessToken.parse(s)
                if not scope:
                    continue

                resource_id = None
                if name_or_uid:
                    resource_id = workspace.get_resource_id_for_scope(scope, name_or_uid)
                scope_details.append((scope, resource_id, _filter))

            try:
                workspace.add_scopes_to_token(token, scope_details)
            except ScopeException as e:
                raise CreateTokenError(str(e))

        return token

    @staticmethod
    def get_token_for_scope(u, scope, resource_id: Optional[str] = None) -> Optional[str]:
        u = User.get_by_id(u.id)
        return u.get_token_for_scope(scope, resource_id)

    @staticmethod
    def get_access_token_for_scope(u, scope, resource_id: Optional[str] = None) -> Optional[AccessToken]:
        u = User.get_by_id(u.id)
        return u.get_access_token_for_scope(scope, resource_id)

    @staticmethod
    def get_access_tokens_for_resource(u, resource: str, scope) -> List[AccessToken]:
        u = User.get_by_id(u.id)
        return u.get_access_tokens_for_resource(resource, scope)

    @staticmethod
    def get_tokens_for_resource(u, resource, scope):
        """
        >>> u = UserAccount.register('get_tokens_for_resource@example.com', 'pass')
        >>> w = User.register('get_tokens_for_resource', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_token(w, "test", scopes.DATASOURCES_READ, "test")
        >>> Users.get_tokens_for_resource(w, 'test', scopes.DATASOURCES_READ)[0] == t
        True
        >>> Users.get_tokens_for_resource(w, 'test2', scopes.DATASOURCES_READ)
        []
        >>> Users.get_tokens_for_resource(w, 'test', scopes.DATASOURCES_APPEND)
        []
        >>> _ = Users.add_token(w, "test 2", scopes.DATASOURCES_READ, "test")
        >>> len(Users.get_tokens_for_resource(w, 'test', scopes.DATASOURCES_READ))
        2
        >>> asyncio.run(Users.delete(w))
        True
        """
        u = User.get_by_id(u.id)
        return u.get_tokens_for_resource(resource, scope)

    @staticmethod
    def get_token_access_info(u: User, token: str, tokens: Optional[List[AccessToken]] = None) -> Optional[AccessToken]:
        """
        >>> u = UserAccount.register('test_token_access_info@example.com', 'pass')
        >>> w = User.register('test_token_access_info', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> tk = Users.add_token(w, "test name", scopes.ADMIN)
        >>> tk_info = Users.get_token_access_info(w, tk)
        >>> tk_info != None
        True
        >>> tk == tk_info.token
        True
        >>> tk_info.has_scope(scopes.ADMIN)
        True
        >>> tk2 = Users.add_token(w, "test name 2", scopes.DATASOURCES_CREATE)
        >>> tk != tk2
        True
        >>> tk_info2 = Users.get_token_access_info(w, tk2)
        >>> tk_info.token != tk_info2.token
        True
        >>> tk_info2.has_scope(scopes.DATASOURCES_CREATE)
        True
        >>> tk_info2.has_scope(scopes.ADMIN)
        False
        >>> asyncio.run(Users.delete(w))
        True
        """
        u = User.get_by_id(u.id)
        return u.get_token_access_info(token, tokens)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def refresh_token(workspace: "User", token_id: str) -> AccessToken:
        with User.transaction(workspace.id) as workspace:
            workspace.check_connector_token(token_id)
            tk = workspace.get_token_access_info(token_id)
            if not tk:
                raise TokenNotFound(404, "Auth token not found")
            tk.refresh(User.secret, workspace.id)
        return tk

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def change_workspace_plan(cls, workspace: "User", new_plan: str) -> "User":
        with User.transaction(workspace.id) as workspace:
            workspace.plan = new_plan
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_stripe_subscription(workspace: "User"):
        with User.transaction(workspace.id) as workspace:
            workspace.remove_stripe_subscription()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_stripe_settings(
        workspace: "User",
        stripe_customer_id=None,
        stripe_email=None,
        stripe_subscription_id=None,
        stripe_client_secret=None,
        stripe_setup_intent=None,
    ) -> User:
        with User.transaction(workspace.id) as user:
            user.set_stripe_settings(
                stripe_customer_id=stripe_customer_id,
                stripe_email=stripe_email,
                stripe_subscription_id=stripe_subscription_id,
                stripe_client_secret=stripe_client_secret,
                stripe_setup_intent=stripe_setup_intent,
            )
        return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_profile(workspace: "User", profile_name: str, profile_value: str) -> User:
        with User.transaction(workspace.id) as workspace:
            workspace.add_profile(profile_name=profile_name, profile_value=profile_value)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_profile(workspace: "User", profile_name: str, profile_value: str) -> User:
        with User.transaction(workspace.id) as workspace:
            workspace.update_profile(profile_name=profile_name, profile_value=profile_value)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def delete_profile(workspace: "User", profile_name: str) -> User:
        with User.transaction(workspace.id) as workspace:
            workspace.delete_profile(profile_name=profile_name)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_last_commit(workspace: "User", last_commit: str, resources: List[GitHubResource]) -> User:
        with User.transaction(workspace.id) as workspace:
            workspace.update_last_commit(last_commit=last_commit, resources=resources)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_remote(workspace: "User", remote: GitHubSettings) -> User:
        with User.transaction(workspace.id) as workspace:
            await workspace.update_remote(remote=remote)
        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def delete_remote(workspace: "User", force: Optional[bool] = False) -> User:
        with User.transaction(workspace.id) as workspace:
            await workspace.delete_remote(force=force)

        return workspace

    @staticmethod
    def get_pipes(u: User) -> List[Pipe]:
        user = User.get_by_id(u.id)
        return user.get_pipes()

    @staticmethod
    def get_resource(u: User, name_or_id: str) -> Optional[Union[Datasource, Pipe, PipeNode]]:
        """
        >>> u = UserAccount.register('test_get_resource@example.com', 'pass')
        >>> w = User.register('test_get_resource', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> ds = Users.add_datasource_sync(w, 'test_ds')
        >>> Users.get_resource(w, 'test_ds').id == ds.id
        True
        >>> Users.get_resource(w, ds.id).name == ds.name
        True
        >>> pipe = Users.add_pipe_sync(w, 'test_pipe', 'select * from test_ds')
        >>> Users.get_resource(w, 'test_pipe').id == pipe.id
        True
        >>> Users.get_resource(w, pipe.id).name == pipe.name
        True
        >>> node = pipe.pipeline.last()
        >>> Users.get_resource(w, node.id).name == node.name
        True
        >>> Users.get_resource(w, node.name).id == node.id
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        user = User.get_by_id(u.id)
        return user.get_resource(name_or_id)

    @staticmethod
    def get_pipe_by_node(u: User, node_name_or_uid: str) -> Optional[Pipe]:
        """
        >>> u = UserAccount.register('test_get_pipe_by_node@example.com', 'pass')
        >>> w = User.register('test_get_pipe_by_node', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> pipe = Users.add_pipe_sync(w, 'test_pipe', 'select * from test_ds')
        >>> node = pipe.append_node(PipeNode('node_1', 'select 1'))
        >>> Users.update_pipe(w, pipe)
        True
        >>> Users.get_pipe_by_node(w, node.name).id == pipe.id
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        user = User.get_by_id(u.id)
        return user.get_pipe_by_node(node_name_or_uid)

    @staticmethod
    def get_node(u: User, node_name_or_uid: str) -> Optional[PipeNode]:
        """
        >>> u = UserAccount.register('test_get_node@example.com', 'pass')
        >>> w = User.register('test_get_node', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> pipe = Users.add_pipe_sync(w, 'test_pipe', 'select * from test_ds')
        >>> node = pipe.append_node(PipeNode('node_1', 'select 1'))
        >>> Users.update_pipe(w, pipe)
        True
        >>> Users.get_node(w, node.name).id == node.id
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        user = User.get_by_id(u.id)
        return user.get_node(node_name_or_uid)

    @staticmethod
    def get_node_by_materialized(
        u: User, mv_uid: str, pipe_id: Optional[str] = None, i_know_what_im_doing: Optional[bool] = False
    ) -> Optional[PipeNode]:
        """
        >>> u = UserAccount.register('test_get_node_mat@example.com', 'pass')
        >>> w = User.register('test_get_node_mat', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> ds = Users.add_datasource_sync(w, 'test_materialized')
        >>> pipe = Users.add_pipe_sync(w, 'test_pipe', 'select * from test_ds')
        >>> node = pipe.append_node(PipeNode('node_1', 'select 1', materialized=ds.id))
        >>> Users.update_pipe(w, pipe)
        True
        >>> Users.get_node_by_materialized(w, ds.id, pipe.id).id == node.id
        True
        >>> asyncio.run(Users.delete(w))
        True
        """

        user = User.get_by_id(u.id)
        return user.get_node_by_materialized(mv_uid, pipe_id, i_know_what_im_doing)

    @staticmethod
    def get_tokens(u: "User") -> List[AccessToken]:
        user = User.get_by_id(u.id)
        return user.get_tokens()

    @staticmethod
    def get_token(u: "User", name: str) -> Optional[AccessToken]:
        user = User.get_by_id(u.id)
        return user.get_token(name)

    @staticmethod
    def get_workspace_users(u: User) -> List[Dict[str, Any]]:
        user = User.get_by_id(u.id)
        return user.get_workspace_users()

    @staticmethod
    def get_datasources(u: User) -> List[Datasource]:
        user = User.get_by_id(u.id)
        return user.get_datasources()

    @staticmethod
    def get_pipe(u: User, pipe_name_or_id: str) -> Optional[Pipe]:
        """
        >>> u = UserAccount.register('test_get_pipe@example.com', 'pass')
        >>> w = User.register('test_get_pipe', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_pipe_sync(w, 'test', 'select * from table')
        >>> Users.get_pipe(w, 'test').id == t.id
        True
        >>> Users.get_pipe(w, t.id).name == t.name
        True
        >>> Users.get_pipe(w, "t_vaya_tela_marinera_" + t.id.split('_')[-1]).name == t.name
        True
        >>> Users.get_pipe(w, "t_vaya_tela_marinera." + t.id.split('_')[-1]).name == t.name
        True
        >>> Users.get_pipe(w, None) is None
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        user = User.get_by_id(u.id)
        return user.get_pipe(pipe_name_or_id)

    @staticmethod
    def update_pipe(u, pipe) -> bool:
        with User.transaction(u.id) as user:
            return user.update_pipe(pipe)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_node_in_pipe_async(
        u: User,
        edited_by: Optional[str],
        pipe_name_or_id: str,
        node_name_or_id: str,
        sql: Optional[str] = None,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
        ignore_sql_errors: bool = False,
        mode: Optional[str] = None,
    ) -> Pipe:
        with User.transaction(u.id) as user:
            pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(pipe, Pipe)
            node = pipe.update_node(node_name_or_id, sql, new_name, new_description, mode, edited_by=edited_by)

            node.ignore_sql_errors = ignore_sql_errors
            user.update_pipe(pipe)

            updated_pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(updated_pipe, Pipe)

            return updated_pipe

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def mark_node_as_materializing(
        u: User, pipe_name_or_id: str, node_name_or_id: str, edited_by: Optional[str]
    ) -> Pipe:
        with User.transaction(u.id) as user:
            pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(pipe, Pipe)

            pipe.set_node_tag(node_name_or_id, PipeNodeTags.MATERIALIZING, value=True, edited_by=edited_by)
            user.update_pipe(pipe)

            updated_pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(updated_pipe, Pipe)

            return updated_pipe

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def unmark_node_as_materializing(
        u: User, pipe_name_or_id: str, node_name_or_id: str, edited_by: Optional[str]
    ) -> Pipe:
        with User.transaction(u.id) as user:
            pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(pipe, Pipe)
            pipe.set_node_tag(node_name_or_id, PipeNodeTags.MATERIALIZING, value=False, edited_by=edited_by)
            user.update_pipe(pipe)

            updated_pipe = user.get_pipe(pipe_name_or_id)
            assert isinstance(updated_pipe, Pipe)

            return updated_pipe

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_node_from_pipe_async(
        u, pipe_name_or_id: str, node_name_or_id: str, edited_by: Optional[str]
    ) -> PipeNode:
        with User.transaction(u.id) as user:
            result = user.drop_node_from_pipe(pipe_name_or_id, node_name_or_id, edited_by)
            return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_node_of_pipe_as_endpoint_async(
        user_id: str, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> User:
        with User.transaction(user_id) as user:
            user.set_node_of_pipe_as_endpoint(pipe_name_or_id, node_id, edited_by)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_node_of_pipe_as_datasink_async(
        workspace_id: str,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            workspace.set_node_of_pipe_as_datasink(pipe_name_or_id, node_name_or_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_node_of_pipe_as_stream_async(
        workspace_id: str,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            workspace.set_node_of_pipe_as_stream(pipe_name_or_id, node_name_or_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_node_of_pipe_as_copy_async(
        workspace_id: str,
        pipe_name_or_id: str,
        node_name_or_id: str,
        target_datasource_id: str,
        mode: Optional[str],
        edited_by: Optional[str],
        target_workspace_id: Optional[str] = None,
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            target_workspace_id = target_workspace_id if target_workspace_id else workspace_id
            workspace.set_node_of_pipe_as_copy(
                pipe_name_or_id, node_name_or_id, target_datasource_id, target_workspace_id, mode, edited_by
            )
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_copy_target_async(
        workspace_id: str,
        pipe_name_or_id: str,
        target_datasource_id: str,
        edited_by: Optional[str],
        target_workspace_id: Optional[str] = None,
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            target_workspace_id = target_workspace_id if target_workspace_id else workspace_id
            workspace.update_copy_pipe_target(pipe_name_or_id, target_datasource_id, target_workspace_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_endpoint_of_pipe_node_async(
        user_id: str, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> User:
        with User.transaction(user_id) as user:
            user.drop_endpoint_of_pipe_node(pipe_name_or_id, node_id, edited_by)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_copy_of_pipe_node_async(
        workspace_id: str, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            workspace.drop_copy_of_pipe_node(pipe_name_or_id, node_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_sink_of_pipe_node_async(
        workspace_id: str, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            await workspace.drop_sink_of_pipe_node(pipe_name_or_id, node_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_stream_of_pipe_node_async(
        workspace_id: str, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> User:
        with User.transaction(workspace_id) as workspace:
            await workspace.drop_stream_of_pipe_node(pipe_name_or_id, node_id, edited_by)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_node_of_pipe(user_id: str, pipe_name_or_id: str, node: PipeNode, edited_by: Optional[str]):
        with User.transaction(user_id) as user:
            user.update_node(pipe_name_or_id, node, edited_by)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def append_node_to_pipe_async(user_id: str, node: PipeNode, pipe_id: str, edited_by: Optional[str]) -> User:
        with User.transaction(user_id) as user:
            user.append_node_to_pipe(pipe_id, node, edited_by)
            return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_data_source_connector_token_async(user_id: str, datasource: Datasource, connector_name: str):
        with User.transaction(user_id) as user:
            return user.add_data_source_connector_token(datasource, connector_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def change_node_position_async(
        u: "User", pipe_name_or_id: str, node_name_or_id: str, new_position: str, edited_by: Optional[str]
    ) -> Pipe:
        with User.transaction(u.id) as workspace:
            pipe = workspace.get_pipe(pipe_name_or_id)
            if pipe is None:
                raise ValueError("pipe not found")
            try:
                position = int(new_position)
            except ValueError:
                raise ValueError("New position must be an integer.")
            pipe.change_node_position(node_name_or_id, position, edited_by)
            workspace.update_pipe(pipe)
        return pipe

    @staticmethod
    def update_datasource(u, ds):
        with User.transaction(u.id) as user:
            return user.update_datasource(ds)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_datasource_sync(workspace: User, ds: Datasource):
        return Users.update_datasource(workspace, ds)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_datasource_async(workspace: User, ds: Datasource):
        return await asyncio.to_thread(Users.update_datasource, workspace, ds)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_dependent_datasource_tag(u, source_datasource_id, target_datasource_id, workspace_id, engine):
        with User.transaction(u.id) as user:
            return user.set_dependent_datasource_tag(source_datasource_id, target_datasource_id, workspace_id, engine)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_dependent_datasource_tag(u, source_datasource_id, target_datasource_id):
        with User.transaction(u.id) as user:
            return user.update_dependent_datasource_tag(source_datasource_id, target_datasource_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_source_copy_pipes_tag(workspace_id: str, target_datasource_id: str, source_pipe_id: str) -> User:
        with User.transaction(workspace_id) as workspace:
            return workspace.set_source_copy_pipes_tag(target_datasource_id, source_pipe_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_source_copy_pipes_tag(workspace_id: str, target_datasource_id: str, source_pipe_id: str) -> User:
        with User.transaction(workspace_id) as workspace:
            return workspace.remove_source_copy_pipes_tag(target_datasource_id, source_pipe_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_source_copy_pipes_tag(
        target_workspace_id: str,
        target_datasource_id: str,
        former_workspace_id: str,
        former_datasource_id: str,
        source_pipe_id: str,
    ) -> User:
        if former_workspace_id == target_workspace_id:
            with User.transaction(target_workspace_id) as workspace:
                workspace.remove_source_copy_pipes_tag(former_datasource_id, source_pipe_id)
                return workspace.set_source_copy_pipes_tag(target_datasource_id, source_pipe_id)
        else:
            with User.transaction(former_workspace_id) as former_workspace:
                former_workspace.remove_source_copy_pipes_tag(former_datasource_id, source_pipe_id)
            with User.transaction(target_workspace_id) as target_workspace:
                return target_workspace.set_source_copy_pipes_tag(target_datasource_id, source_pipe_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def cache_delimiter_used_in_datasource_async(u, ds, delimiter):
        with User.transaction(u.id) as user:
            datasource = user.get_datasource(ds.name)
            if not datasource:
                return False

            datasource.cache_delimiter(delimiter)
            return user.update_datasource(datasource)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def mark_datasource_as_shared(u, datasource_id, shared_with_workspace_id):
        with User.transaction(u.id) as user:
            user.mark_datasource_as_shared(datasource_id, shared_with_workspace_id)
        return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def unmark_datasource_as_shared(u, datasource_id, shared_with_workspace_id):
        with User.transaction(u.id) as user:
            user.unmark_datasource_as_shared(datasource_id, shared_with_workspace_id)
        return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_shared_datasource(
        u: User,
        original_datasource_id: str,
        workspace_id: str,
        workspace_name: str,
        ds_database: str,
        ds_name: str,
        ds_description: str,
        distributed_mode: Optional[str] = None,
    ) -> Datasource:
        with User.transaction(u.id) as user:
            new_ds = user.add_shared_datasource(
                original_datasource_id,
                workspace_id,
                workspace_name,
                ds_database,
                ds_name,
                ds_description,
                distributed_mode,
            )
        return new_ds

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_branch_shared_datasource(
        u,
        ds_id,
        original_workspace_id,
        original_workspace_name,
        original_ds_database,
        original_ds_name,
        original_ds_description,
    ):
        with User.transaction(u.id) as user:
            new_ds = user.add_branch_shared_datasource(
                ds_id,
                original_workspace_id,
                original_workspace_name,
                original_ds_database,
                original_ds_name,
                original_ds_description,
            )
        return new_ds

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _alter_datasource_name(
        u: User,
        ds_name_or_id: str,
        new_name: str,
        edited_by: Optional[str],
        cascade: bool = True,
        dependencies: Optional[List[str]] = None,
    ) -> Tuple[User, Datasource, Datasource]:
        with User.transaction(u.id) as user:
            old_datasource = user.get_datasource(ds_name_or_id)
            assert isinstance(old_datasource, Datasource)
            datasource = user.alter_datasource_name(
                ds_name_or_id, new_name, edited_by=edited_by, cascade=cascade, dependencies=dependencies
            )
        return user, old_datasource, datasource

    @staticmethod
    async def alter_datasource_name(
        u: User,
        ds_name_or_id: str,
        new_name: str,
        edited_by: Optional[str],
        cascade: bool = True,
        dependencies: Optional[List[str]] = None,
    ) -> Datasource:
        """
        >>> import asyncio
        >>> u = UserAccount.register('alter_datasource_name@example.com', 'pass')
        >>> w = User.register('alter_datasource_name', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_datasource_sync(w, 'test')
        >>> ds = asyncio.run(Users.alter_datasource_name(w, 'test', 'test2', ''))
        >>> ds.name
        'test2'
        >>> t = Users.get_datasource(w, 'test2')
        >>> t != None
        True
        >>> asyncio.run(Users.alter_datasource_name(w, 'test2', '0_invalid_table', ''))
        Traceback (most recent call last):
        ...
        ValueError: Invalid Data Source name "0_invalid_table". Name must start with a letter and contain only letters, numbers, and underscores. Hint: use t_0_invalid_table_.
        >>> asyncio.run(Users.delete(w))
        True
        """
        user, old_datasource, datasource = await Users._alter_datasource_name(
            u, ds_name_or_id, new_name, edited_by, cascade=cascade, dependencies=dependencies
        )
        await sync_to_async(PGService(user).alter_datasource_name)(old_datasource.name, new_name)
        if dependencies:
            for pipe_name in dependencies:
                pipe = u.get_pipe(pipe_name)
                if pipe and pipe.is_published():
                    await PGService(u).on_endpoint_changed(pipe)
        return datasource

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_datasource_json_deserialization(u, ds_name_or_id, new_json_deserialization):
        with User.transaction(u.id) as user:
            for x in user.datasources:
                if x["name"] == ds_name_or_id or x["id"] == ds_name_or_id:
                    if x["json_deserialization"] and not new_json_deserialization:
                        raise Exception("Missing parameter 'jsonpaths'.")
                    x["json_deserialization"] = new_json_deserialization
                    x["updated_at"] = datetime.now()
                    return user.get_datasource(ds_name_or_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_datasource_engine(workspace: User, ds_name_or_id: str, new_engine: Dict[str, str]) -> Datasource | None:
        updated_datasource: Datasource | None = None
        with User.transaction(workspace.id) as w:
            for datasource in w.datasources:
                if datasource["name"] == ds_name_or_id or datasource["id"] == ds_name_or_id:
                    datasource["engine"] = new_engine
                    datasource["updated_at"] = datetime.now()
                    updated_datasource = w.get_datasource(ds_name_or_id)

        return updated_datasource

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_cdk_gcp_service_account(u, cdk_gcp_service_account: Optional[dict]) -> "User":
        with User.transaction(u.id) as user:
            user.cdk_gcp_service_account = cdk_gcp_service_account
        return user

    # We want to delete the Service Account only in certain cases to avoid branches deleting workspace SAs
    # that they shouldn't. A workspace SA should only be deleted if we're trying to delete it from the main workspace or
    # if it's a branch and has it's own SA, diffrent from the main one.
    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def delete_workspace_service_account(u: User) -> None:
        from tinybird.ingest.external_datasources.admin import delete_workspace_service_account

        if not u.cdk_gcp_service_account:
            # No service account to be deleted
            return

        service_account_to_delete = None

        if u.is_main_workspace or (u.origin and not u.has_same_service_account(User.get_by_id(u.origin))):
            service_account_to_delete = u

        if not service_account_to_delete:
            return

        with User.transaction(u.id) as user:
            user.cdk_gcp_service_account = None
        await delete_workspace_service_account(service_account_to_delete)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_kafka_server_group(u, kafka_server_group: Optional[str]):
        with User.transaction(u.id) as user:
            user.kafka_server_group = kafka_server_group
        return user

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_datasource_ignore_paths(u, ds_name_or_id, ignore_paths):
        with User.transaction(u.id) as user:
            for x in user.datasources:
                if x["name"] == ds_name_or_id or x["id"] == ds_name_or_id:
                    x["ignore_paths"] = ignore_paths
                    return user.get_datasource(ds_name_or_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def alter_datasource_ttl(u, ds_name_or_id, new_ttl):
        with User.transaction(u.id) as user:
            for x in user.datasources:
                if x["name"] == ds_name_or_id or x["id"] == ds_name_or_id:
                    x["engine"]["ttl"] = new_ttl
                    x["updated_at"] = datetime.now()
                    return user.get_datasource(ds_name_or_id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def alter_datasource_description(u, ds_name_or_id, description):
        ds = None
        with User.transaction(u.id) as user:
            ds = user.get_datasource(ds_name_or_id)
            if not ds:
                return
            ds.description = description
            ds.updated_at = datetime.now()
            user.update_datasource(ds)

        for shared_with_ws_id in ds.shared_with:
            await Users._alter_shared_datasource_description(ds.id, shared_with_ws_id, description)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _alter_shared_datasource_description(origin_ds_id, shared_ws_id, description):
        with User.transaction(shared_ws_id) as dest_ws:
            shared_ds = dest_ws.get_datasource(origin_ds_id, include_read_only=True)
            if not shared_ds:
                return
            assert isinstance(shared_ds, SharedDatasource)
            shared_ds.update_shared_description(description)
            dest_ws.update_datasource(shared_ds)

    @classmethod
    async def alter_shared_datasource_name(
        cls,
        destination_workspace_id: str,
        origin_datasource_id: str,
        origin_workspace_id: str,
        origin_workspace_name: str,
        origin_datasource_name: str,
        user_email_making_the_request: Optional[str],
        dependencies: Optional[List[str]] = None,
    ) -> None:
        old_name, altered_datasource = await Users._alter_shared_data_source_name(
            destination_workspace_id,
            origin_datasource_id,
            origin_workspace_name,
            origin_datasource_name,
            dependencies=dependencies,
        )
        new_name = altered_datasource.name

        destination_workspace = User.get_by_id(destination_workspace_id)
        await sync_to_async(PGService(destination_workspace).alter_datasource_name)(old_name, new_name)
        if dependencies:
            for pipe in dependencies:
                _pipe = destination_workspace.get_pipe(pipe)
                if _pipe and _pipe.is_published():
                    await PGService(destination_workspace).on_endpoint_changed(_pipe)

        await cls._send_notification_on_shared_data_source_rename(
            destination_workspace, user_email_making_the_request, origin_workspace_id, old_name, new_name
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def discard_datasource_errors(u, ds_name_or_id):
        ds = None
        with User.transaction(u.id) as user:
            ds = user.get_datasource(ds_name_or_id)
            if not ds:
                return
            ds.errors_discarded_at = datetime.now()
            ds.updated_at = datetime.now()
            user.update_datasource(ds)

    @classmethod
    async def _send_notification_on_shared_data_source_rename(
        cls,
        destination_workspace: "User",
        user_email_making_the_request: Optional[str],
        origin_workspace_id: str,
        old_name: str,
        new_name: str,
    ):
        user_emails = destination_workspace.get_user_emails_that_have_access_to_this_workspace()

        origin_workspace = User.get_by_id(origin_workspace_id)
        origin_workspace_users = origin_workspace.get_workspace_users()
        admin_emails = [user["email"] for user in origin_workspace_users if user["role"] == Relationships.ADMIN]

        send_to_emails = list(
            filter(lambda x: x != user_email_making_the_request and x not in admin_emails, user_emails)
        )

        if len(send_to_emails) != 0:
            notification_result = await cls._mailgun_service.send_notification_on_shared_data_source_renamed(
                send_to_emails, old_name, new_name, admin_emails, destination_workspace.id, destination_workspace.name
            )
            if notification_result.status_code != 200:
                logging.error(
                    f"Notification for Data Source has been renamed was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _alter_shared_data_source_name(
        destination_workspace_id: str,
        origin_datasource_id: str,
        origin_workspace_name: str,
        origin_datasource_name: str,
        dependencies: Optional[List[str]] = None,
    ) -> Tuple[str, SharedDatasource]:
        with User.transaction(destination_workspace_id) as destination_workspace:
            return destination_workspace.alter_shared_data_source_name(
                origin_datasource_id, origin_workspace_name, origin_datasource_name, dependencies=dependencies
            )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def alter_pipe(
        u, pipe_name_or_id, name=None, description=None, parent=None, edited_by: Optional[str] = None
    ) -> Optional[Pipe]:
        """
        >>> u = UserAccount.register('test_alter_pipe_name@example.com', 'pass')
        >>> w = User.register('test_alter_pipe_name', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_pipe_sync(w, 'test', 'select * from table')
        >>> asyncio.run(Users.alter_pipe(w, 'test', 'test2')).name
        'test2'
        >>> t = Users.get_pipe(w, 'test2')
        >>> t != None
        True
        >>> t.description == None
        True
        >>> asyncio.run(Users.alter_pipe(w, 'test2', description='my desc')).description
        'my desc'
        >>> Users.get_by_id(w.id).get_pipe('test2').parent
        >>> asyncio.run(Users.alter_pipe(w, 'test2', parent='new_parent_id')).parent
        'new_parent_id'
        >>> asyncio.run(Users.alter_pipe(w, 'test2', '0_invalid_pipe'))
        Traceback (most recent call last):
        ...
        ValueError: Invalid Pipe name "0_invalid_pipe". Name must start with a letter and contain only letters, numbers, and underscores. Hint: use t_0_invalid_pipe_.
        >>> asyncio.run(Users.alter_pipe(w, 'test2', 'from'))
        Traceback (most recent call last):
        ...
        ValueError: from is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use from_.
        >>> asyncio.run(Users.delete(w))
        True
        """
        with User.transaction(u.id) as user:
            return user.alter_pipe(pipe_name_or_id, name, description, parent, edited_by=edited_by)

    @staticmethod
    def drop_datasource(workspace: "User", ds_name: str) -> Optional[Datasource]:
        """
        >>> u = UserAccount.register('test_drop_ds@example.com', 'pass')
        >>> w = User.register('test_drop_ds', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> tokens_count = len(Users.get_tokens(w))
        >>> ds = Users.add_datasource_sync(w, 'ds_to_drop')
        >>> tokens_count == len(Users.get_tokens(w))
        True
        >>> ds = Users.drop_datasource(w, ds.id)
        >>> ds is not None
        True
        >>> tokens_count == len(Users.get_tokens(w))
        True
        >>> ds = Users.add_datasource_sync(w, 'ds_to_drop')
        >>> t = Users.add_token(w, 'extra_token', None)
        >>> _ = Users.add_scope_to_token(w, t, scopes.DATASOURCES_READ, ds.id)
        >>> user_tokens = Users.get_tokens(w)
        >>> new_tokens = 1  # the extra token
        >>> tokens_count + new_tokens == len(user_tokens)
        True
        >>> t in [t.token for t in user_tokens]
        True
        >>> _ = Users.drop_datasource(w, ds.id)
        >>> new_tokens = 1  # we keep the extra token
        >>> user_tokens = Users.get_tokens(w)
        >>> tokens_count + new_tokens == len(user_tokens)
        True
        >>> t in [t.token for t in user_tokens]
        True
        >>> asyncio.run(Users.delete(w))
        True
        """
        with User.transaction(workspace.id) as user:
            return user.drop_datasource(ds_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def drop_datasource_sync(workspace: "User", ds_name: str) -> Optional[Datasource]:
        return Users.drop_datasource(workspace, ds_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_datasource_async(workspace: "User", ds_name: str) -> Optional[Datasource]:
        return Users.drop_datasource(workspace, ds_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def drop_pipe_async(u, pipe_name):
        return Users.drop_pipe(u, pipe_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def copy_pipeline(u, original_pipe_name: str, pipe_to_swap_name: str) -> Pipe:
        with User.transaction(u.id) as user:
            return user.copy_pipeline(original_pipe_name, pipe_to_swap_name)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_pipe_async(u: User, pipe: Pipe) -> bool:
        with User.transaction(u.id) as user:
            return user.update_pipe(pipe)

    @staticmethod
    def drop_pipe(u, pipe_name):
        """
        >>> u = UserAccount.register('test_drop_pipe@example.com', 'pass')
        >>> w = User.register('test_drop_pipe', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> tokens_count = len(Users.get_tokens(w))
        >>> pipe = Users.add_pipe_sync(w, 'pipe_to_drop', 'select * from table')
        >>> t = Users.add_token(w, 'new_pipe_token', scopes.PIPES_READ, pipe.id)
        >>> user_tokens = Users.get_tokens(w)
        >>> Users.drop_pipe(w, pipe.id)
        True
        >>> user_tokens = Users.get_tokens(w)
        >>> tokens_count + 1 == len(user_tokens)  # do not delete the token
        True
        >>> t in [t.token for t in user_tokens]
        True
        >>> Users.drop_token(w, t)
        True
        >>> tokens_count == len(Users.get_tokens(w))  # we are back to initial state
        True
        >>> pipe = Users.add_pipe_sync(w, 'pipe_to_drop', 'select * from table')
        >>> t = Users.add_token(w, 'extra_token', None)
        >>> _ = Users.add_scope_to_token(w, t, scopes.PIPES_READ, pipe.id)
        >>> user_tokens = Users.get_tokens(w)
        >>> new_tokens = 1  # we keep the default token
        >>> tokens_count + new_tokens == len(user_tokens)
        True
        >>> t in [t.token for t in user_tokens]
        True
        >>> _ = Users.drop_pipe(w, pipe.id)
        >>> new_tokens = 1  # we keep the default
        >>> user_tokens = Users.get_tokens(w)
        >>> tokens_count + new_tokens == len(user_tokens)
        True
        >>> t in [t.token for t in user_tokens]
        True
        >>> asyncio.run(Users.delete(w))
        True
        """

        with User.transaction(u.id) as user:
            return user.drop_pipe(pipe_name)

    @staticmethod
    def replace_tables(
        u,
        query,
        readable_resources=None,
        use_service_datasources_replacements=True,
        pipe=None,
        filters=None,
        use_pipe_nodes=False,
        staging_tables=False,
        extra_replacements=None,
        variables=None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        allow_use_internal_tables: Optional[bool] = True,
        release_replacements: Optional[bool] = False,
        function_allow_list: Optional[FrozenSet[str]] = None,
    ):
        user = User.get_by_id(u.id)

        return user.replace_tables(
            query,
            readable_resources=readable_resources,
            use_service_datasources_replacements=use_service_datasources_replacements,
            pipe=pipe,
            use_pipe_nodes=use_pipe_nodes,
            filters=filters,
            staging_tables=staging_tables,
            extra_replacements=extra_replacements,
            variables=variables,
            template_execution_results=template_execution_results,
            allow_use_internal_tables=allow_use_internal_tables,
            release_replacements=release_replacements,
        )

    @staticmethod
    def get_service_datasources_replacements(
        workspace: "User", include_org_service_datasources: bool
    ) -> Dict[Tuple[str, str], Tuple[str, str]]:
        from tinybird.organization.organization import Organization

        public_workspace = public.get_public_user()

        def is_internal_release() -> bool:
            return workspace.is_release and any([r for r in public_workspace.get_releases() if r.id == workspace.id])

        is_internal: bool = (workspace["id"] == public_workspace["id"]) or is_internal_release()

        datasources: List[Datasource] = workspace.get_datasources()
        public_database: str = public_workspace.database

        # Precalculate this common particle instead of calculating it on each iteration
        where_clause_extra_readonly_datasources: str = ""
        read_only_ds_ids: List[str] = [ds.id for ds in datasources if ds.is_read_only]
        if len(read_only_ds_ids) > 0:
            extra_datasources_surrounded_by_quotes = [f"'{ds_id}'" for ds_id in read_only_ds_ids]
            extra_datasources_sql_in_content = ",".join(extra_datasources_surrounded_by_quotes)
            where_clause_extra_readonly_datasources = f" OR datasource_id IN ({extra_datasources_sql_in_content})"

        org: Optional[Organization] = (
            Organization.get_by_id(workspace.organization_id)
            if include_org_service_datasources and workspace.organization_id
            else None
        )
        if include_org_service_datasources and workspace.is_branch_or_release_from_branch and not org:
            main_workspace = workspace.get_main_workspace()
            org = Organization.get_by_id(main_workspace.organization_id) if main_workspace.organization_id else None
            if org:
                workspace.organization_id = main_workspace.organization_id
                org.workspace_ids.add(workspace.id)
                org.databases.add(workspace.database)

        def get_sql_clauses(replacement: Replacement) -> Optional[Tuple[str, str, str]]:
            """Defer SQL clause generation until really needed."""

            columns: str
            where_clause: str
            group_by: str

            columns = (
                replacement.featured_columns.columns
                if replacement.featured_columns
                and FeatureFlagsWorkspaceService.feature_for_id(
                    replacement.featured_columns.feature_flag, "", workspace.feature_flags
                )
                else replacement.columns
            )

            if replacement.filter_by_organization or replacement.filter_by_workspace or replacement.filter_by_database:
                if replacement.filter_by_organization:
                    if not workspace.organization_id or not include_org_service_datasources or not org:
                        return None
                    if replacement.organization_id_column:
                        where_clause = f"where {replacement.organization_id_column} in ('{workspace.organization_id}')"
                    elif replacement.filter_by_workspace:
                        if not org.workspace_ids:
                            return None
                        filter_ids = "', '".join(org.workspace_ids)
                        where_clause = f"where {replacement.workspace_id_column} in ('{filter_ids}')"
                    else:
                        assert replacement.filter_by_database
                        if not org.databases:
                            return None
                        filter_ids = "', '".join(org.databases)
                        where_clause = f"where database in ('{filter_ids}')"
                else:
                    where_clause = (
                        f"where {replacement.workspace_id_column} = '{workspace.id}'"
                        if replacement.filter_by_workspace
                        else f"where database = '{workspace.database}'"
                    )

                if replacement.include_read_only_datasources and where_clause_extra_readonly_datasources:
                    where_clause += where_clause_extra_readonly_datasources

                if replacement.filter_by_billable:
                    where_clause += " AND billable = 1"
            else:
                where_clause = ""

            group_by = f"group by {replacement.group_by}" if replacement.group_by else ""

            return columns, where_clause, group_by

        datasources_shared_from_internal_workspace: List[str] = [
            ds.original_ds_name
            for ds in datasources
            if isinstance(ds, SharedDatasource) and ds.original_workspace_id == public_workspace.id
        ]

        remote: str = VALID_REMOTE
        cluster: str = public_workspace["clusters"][0] if public_workspace["clusters"] else "tinybird"
        replacements: Dict[Tuple[str, str], Tuple[str, str]] = {}

        # TODO: We should simplify this code to make it more readable. It's really hard to understand how the whole replacement works
        for repl in REPLACEMENTS:
            if repl.namespace == "organization" and not org:
                continue

            is_shared_from_internal: bool = repl.resource in datasources_shared_from_internal_workspace

            resources: List[str]
            if repl.is_pipe:
                pipe = public_workspace.get_pipe(repl.resource)
                if not pipe:
                    continue
                resources = pipe.pipeline.get_materialized_tables()
            else:
                datasource = public_workspace.get_datasource(
                    repl.resource, include_used_by=False, include_read_only=True
                )
                if not datasource:
                    continue
                resources = [datasource.id]

            final_particle = "FINAL" if repl.add_final else ""

            for res in resources:
                key: Tuple[str, str]
                if repl.expose_internal_resource:
                    replacements[(repl.namespace, repl.name)] = (public_database, res)
                    key = (public_database, res)
                else:
                    key = (repl.namespace, repl.name)

                # Within internal it does not make sense to do further processing
                if is_internal:
                    continue

                multi_cluster: bool = workspace.cluster != cluster
                table = f"cluster({cluster}, {public_database}.{res})" if multi_cluster else f"{public_database}.{res}"

                final_query: str

                if is_shared_from_internal:
                    if repl.add_final:
                        continue
                    final_query = f"(select * from {table})"
                else:
                    sql_clauses = get_sql_clauses(repl)
                    if not sql_clauses:
                        continue

                    columns, where_clause, group_by = sql_clauses
                    final_query = f"(select {columns} from {table} {final_particle} {where_clause} {group_by})"

                replacements[key] = (remote, final_query)
        return replacements

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_cluster(u: "User", cluster: CHCluster):
        with User.transaction(u.id) as user:
            user.clusters = [cluster.name]
            user.database_server = cluster.server_url
            u = user
        return await Users.create_database(u)

    @staticmethod
    async def create_database(workspace: "User"):
        cluster_sql = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
        try:
            await Users.query_user_db(
                workspace,
                f"CREATE DATABASE IF NOT EXISTS {workspace['database']} {cluster_sql}",
                read_only=False,
                include_database=False,
            )
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error while creating database for the workspace {workspace.name}")

    @staticmethod
    async def sync_resources_cluster(u):
        for ds in u.get_datasources():
            if ds.is_read_only:
                continue
            ds.cluster = u.cluster
            u.update_datasource(ds)

        for pipe in u.get_pipes():
            for node in pipe.pipeline.nodes:
                if node.materialized:
                    node.cluster = u.cluster
                    u.update_node(pipe.id, node)

    @staticmethod
    async def query_user_db(
        workspace: "User",
        query: str,
        read_only: bool = True,
        include_database: bool = True,
    ):
        query_id = str(uuid.uuid4())
        query = query + " FORMAT JSON"
        params: Dict[str, Any] = workspace.ddl_parameters(skip_replica_down=True)

        client = HTTPClient(workspace.database_server, database=workspace.database if include_database else None)
        try:
            headers, body = await client.query(
                query,
                read_only=read_only,
                query_id=query_id,
                **params,
            )
        except ValueError as e:
            raise e
        if body:
            # for some queries clickhouse returns TSV even if you ask for JSON
            # this is why this check is here
            # sometimes the header is 'application/json; charset=UTF-8'
            if headers["content-type"].startswith("application/json"):
                return json.loads(body)
            else:
                return body

    @classmethod
    async def stop_sharing_a_datasource(
        cls,
        user_account: "UserAccount",
        origin_workspace: "User",
        destination_workspace: "User",
        datasource_id: str,
        send_notification: bool = True,
        force: bool = False,
        check_used: bool = True,
    ) -> None:
        if not force and check_used:
            cls.check_used_by_pipes(destination_workspace, datasource_id, include_workspace_name=True)

        ds_in_dest = destination_workspace.get_datasource(datasource_id, include_read_only=True)
        if ds_in_dest:
            assert isinstance(ds_in_dest, SharedDatasource)

            if ds_in_dest.distributed_mode:
                from tinybird.table import drop_table  # Avoid circular import.

                await drop_table(destination_workspace, ds_in_dest.id)

        data_source_at_destination_workspace = await Users.drop_datasource_async(destination_workspace, datasource_id)
        await Users.unmark_datasource_as_shared(origin_workspace, datasource_id, destination_workspace.id)

        if data_source_at_destination_workspace is None:
            logging.exception(
                f"Data Source '{datasource_id}' from '{origin_workspace.id}/{origin_workspace.name}' "
                f"was expected to be found in '{destination_workspace.id}/{destination_workspace.name}' "
                f"so it can be removed but was not found."
            )
            raise Exception("Operation could not be completed. Please contact Tinybird support.")

        if send_notification:
            await cls._send_notification_on_shared_data_source_removed(
                user_account, destination_workspace, origin_workspace, data_source_at_destination_workspace.name
            )

    @classmethod
    def get_used_by_materialized_nodes(
        cls,
        workspace: "User",
        ds_id: str,
        pipes: Optional[List[Pipe]] = None,
        include_shared_with: bool = True,
        only_shared_with: bool = False,
        include_workspace_name: bool = False,
    ) -> Tuple[List[str], List[str], List[str], List[str], List[str], List[str]]:
        ds = workspace.get_datasource(ds_id, include_used_by=True, include_read_only=True)
        if ds is None:
            return [], [], [], [], [], []

        mat_deps: Any = set()
        direct_deps: Any = set()

        # check shared
        if include_shared_with:
            for workspace_id in ds.shared_with:
                _workspace = User.get_by_id(workspace_id)
                m, d = cls._get_used_by_materialized_nodes(_workspace, ds, include_workspace_name=include_shared_with)
                mat_deps.update(m)
                direct_deps.update(d)

        if not only_shared_with:
            # check current
            m, d = cls._get_used_by_materialized_nodes(
                workspace, ds, pipes=pipes, include_workspace_name=include_workspace_name
            )
            mat_deps.update(m)
            direct_deps.update(d)

        # result
        l_direct_dependencies = list(direct_deps)
        mat_pipe_nodes = [*zip(*mat_deps, strict=True)]
        pipe_nodes = [*zip(*l_direct_dependencies, strict=True)]

        # TODO: Refactor this to easily understand the return values
        mat_pipes, mat_node_names, target_ds, mat_node_ids, dep_pipes, dep_nodes = [], [], [], [], [], []  # type: ignore
        if mat_pipe_nodes and pipe_nodes:
            mat_pipes, mat_node_names, target_ds, mat_node_ids = mat_pipe_nodes  # type: ignore
            dep_pipes, dep_nodes = pipe_nodes[:2]  # type: ignore
            return mat_pipes, mat_node_names, target_ds, mat_node_ids, dep_pipes, dep_nodes
        return [], [], [], [], [], []

    @classmethod
    def get_used_upstream_by_materialized_nodes(
        cls,
        workspace: "User",
        ds_id: str,
        pipes: Optional[List[Pipe]] = None,
        include_shared_with: bool = True,
        only_shared_with: bool = False,
        include_workspace_name: bool = False,
    ) -> Tuple[List[str], List[str], List[str]]:
        ds = workspace.get_datasource(ds_id, include_used_by=True, include_read_only=True)
        if ds is None:
            return [], [], []

        upstream_mat_deps: Any = set()

        # get upstream materialized dependencies of workspaces where it is shared
        if include_shared_with:
            for workspace_id in ds.shared_with:
                _workspace = User.get_by_id(workspace_id)
                m = cls._get_used_upstream_by_materialized_nodes(
                    _workspace, ds, include_workspace_name=include_shared_with
                )
                upstream_mat_deps.update(m)

        # get upstream materialized dependencies of current workspace
        if not only_shared_with:
            m = cls._get_used_upstream_by_materialized_nodes(
                workspace, ds, pipes=pipes, include_workspace_name=include_workspace_name
            )
            upstream_mat_deps.update(m)

        # TODO: Refactor this to easily understand the return values
        upstream_mat_pipe_nodes = [*zip(*upstream_mat_deps, strict=True)]
        if upstream_mat_pipe_nodes:
            upstream_mat_pipes_names, upstream_mat_nodes_names, _, upstream_mat_node_ids = upstream_mat_pipe_nodes
            return upstream_mat_pipes_names, upstream_mat_nodes_names, upstream_mat_node_ids  # type: ignore
        return [], [], []

    @classmethod
    def get_used_downstream_by_materialized_nodes(
        cls,
        workspace: "User",
        ds_id: str,
        pipes: Optional[List[Pipe]] = None,
        include_shared_with: bool = True,
        only_shared_with: bool = False,
        include_workspace_name: bool = False,
    ) -> Tuple[List[str], List[str], List[str]]:
        mat_pipes, mat_node_names, _, mat_node_ids, _, _ = cls.get_used_by_materialized_nodes(
            workspace,
            ds_id,
            pipes=pipes,
            include_shared_with=include_shared_with,
            only_shared_with=only_shared_with,
            include_workspace_name=include_workspace_name,
        )
        (
            upstream_mat_pipes_names,
            upstream_mat_nodes_names,
            upstream_mat_node_ids,
        ) = cls.get_used_upstream_by_materialized_nodes(
            workspace,
            ds_id,
            pipes=pipes,
            include_shared_with=include_shared_with,
            only_shared_with=only_shared_with,
            include_workspace_name=include_workspace_name,
        )
        downstream_mat_pipes = list(set(mat_pipes).symmetric_difference(set(upstream_mat_pipes_names)))
        downstream_mat_nodes_names = list(set(mat_node_names).symmetric_difference(set(upstream_mat_nodes_names)))
        downstream_mat_nodes_ids = list(set(mat_node_ids).symmetric_difference(set(upstream_mat_node_ids)))
        return downstream_mat_pipes, downstream_mat_nodes_names, downstream_mat_nodes_ids

    @classmethod
    def _get_used_by_materialized_nodes(
        cls, workspace: "User", ds: Datasource, pipes: Optional[List[Pipe]] = None, include_workspace_name: bool = False
    ):
        pipes = pipes or workspace.get_pipes()
        _pipes_index = {pipe.name: pipe for pipe in pipes}
        _nodes_index = {}
        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                all_node_deps = node.dependencies + [node.id for node in pipe.pipeline.get_dependent_nodes(node.id)]
                if ds.id == node.materialized:
                    all_node_deps = [*all_node_deps, ds.name]
                _nodes_index[node.id] = {"dependencies": all_node_deps, "pipe_name": pipe.name, "name": node.name}

        deps = defaultdict(set)
        ds_map: Any = {}
        for p in pipes:
            for node in p.pipeline.nodes:
                if node.materialized == ds.id:
                    deps[ds.name].add(p.name)
                    deps[f"{workspace.name}.{ds.name}"].add(p.name)
                for t in node.dependencies:
                    deps[t].add(p.name)
                    ds_map[t.split(".")[-1]] = t
                for dep_node in p.pipeline.get_dependent_nodes(node.id):
                    deps[dep_node.id].add(p.name)

        def recurse_dependent_materialized_nodes(deps, key, result, visited):
            _key = ds_map.get(key, key)
            for dep in deps[_key]:
                if dep in visited:
                    continue
                visited.append(dep)
                if dep in _pipes_index:
                    pp = _pipes_index[dep]
                    for node in pp.pipeline.nodes:
                        if node.materialized:
                            result.add((pp.name, node.name, node.materialized, node.id))
                recurse_dependent_materialized_nodes(deps, dep, result, visited)

        # this is to get materialized nodes that will break if the data source is renamed / deleted
        dependent_materialized_nodes: Any = set()
        recurse_dependent_materialized_nodes(deps, ds.name, dependent_materialized_nodes, [])

        direct_dependencies: Any = set()

        def recurse_direct_dependencies(res, datasource, nodes, visited):
            if res in visited:
                return
            visited.append(res)
            if hasattr(res, "pipeline"):
                pipe = res
                for n in pipe.pipeline.nodes:
                    n = {"dependencies": n.dependencies, "pipe_name": pipe.name, "name": n.name}
                    recurse_direct_dependencies(n, datasource, nodes, visited)
                return

            if "dependencies" not in res:
                return

            node = res
            _ds_name = ds_map.get(datasource.name, datasource.name)
            if _ds_name in node["dependencies"]:
                nodes.add((node["pipe_name"], node["name"]))

            for d in node["dependencies"]:
                if d in _nodes_index:
                    recurse_direct_dependencies(_nodes_index[d], datasource, nodes, visited)
                if d in _pipes_index:
                    recurse_direct_dependencies(_pipes_index[d], datasource, nodes, visited)

        # this is to report the exact pipe and node names where the data source is being used
        for _, _, _, node_id in dependent_materialized_nodes:
            recurse_direct_dependencies(_nodes_index[node_id], ds, direct_dependencies, [])

        return (
            {
                (f"{workspace.name}.{x[0]}", f"{workspace.name}.{x[1]}", x[2], x[3]) if include_workspace_name else x
                for x in dependent_materialized_nodes
            },
            {(f"{workspace.name}.{x[0]}", x[1]) if include_workspace_name else x for x in direct_dependencies},
        )

    @classmethod
    def _get_used_upstream_by_materialized_nodes(
        cls, workspace: "User", ds: Datasource, pipes: Optional[List[Pipe]] = None, include_workspace_name: bool = False
    ):
        pipes = pipes or workspace.get_pipes()
        _nodes_index = {}
        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                all_node_deps = node.dependencies + [node.id for node in pipe.pipeline.get_dependent_nodes(node.id)]
                if ds.id == node.materialized:
                    all_node_deps = [*all_node_deps, ds.name]
                _nodes_index[node.id] = {"dependencies": all_node_deps, "pipe_name": pipe.name, "name": node.name}

        upstream_materialized_nodes: Any = set()
        for p in pipes:
            for node in p.pipeline.nodes:
                if node.materialized == ds.id:
                    upstream_materialized_nodes.add((p.name, node.name, node.materialized, node.id))

        return {
            (f"{workspace.name}.{x[0]}", f"{workspace.name}.{x[1]}", x[2]) if include_workspace_name else x
            for x in upstream_materialized_nodes
        }

    @classmethod
    def get_used_by_copy(cls, workspace: "User", ds_id: str) -> List[Dict[str, Any]]:
        return workspace.get_source_copy_pipes(ds_id)

    @classmethod
    def check_used_by_pipes(
        cls,
        workspace: "User",
        ds_id: str,
        pipes: Optional[List[Pipe]] = None,
        include_workspace_name: bool = False,
        include_shared_with: bool = True,
        only_shared_with: bool = False,
        force: bool = False,
        is_api: bool = False,
        is_cli: bool = False,
    ):
        dependencies = Users.get_datasource_dependencies(workspace, ds_id)
        (
            upstream_mat_pipes_names,
            upstream_mat_nodes_names,
            upstream_mat_nodes_ids,
        ) = cls.get_used_upstream_by_materialized_nodes(
            workspace,
            ds_id,
            pipes=pipes,
            include_shared_with=include_shared_with,
            only_shared_with=only_shared_with,
            include_workspace_name=include_workspace_name,
        )
        (
            downstream_mat_pipes_names,
            downstream_mat_nodes_names,
            downstream_mat_nodes_ids,
        ) = cls.get_used_downstream_by_materialized_nodes(
            workspace,
            ds_id,
            pipes=pipes,
            include_shared_with=include_shared_with,
            only_shared_with=only_shared_with,
            include_workspace_name=include_workspace_name,
        )
        mat_nodes_ids = [*upstream_mat_nodes_ids, *downstream_mat_nodes_ids]
        if not force and mat_nodes_ids:
            raise DependentMaterializedNodeException(
                upstream_mat_pipes_names,
                upstream_mat_nodes_names,
                downstream_mat_pipes_names,
                downstream_mat_nodes_names,
                dependencies,
                workspace.name,
                include_workspace_name,
                is_api,
                is_cli,
            )
        elif force and downstream_mat_nodes_ids:
            raise DependentMaterializedNodeException(
                [],
                [],
                downstream_mat_pipes_names,
                downstream_mat_nodes_names,
                dependencies,
                workspace.name,
                include_workspace_name,
                is_api,
                is_cli,
            )

        pipe_deps = dependencies.get("pipes")
        assert isinstance(pipe_deps, list)

        copy_dependencies = [pipe for pipe in pipe_deps if pipe.get("type") == "copy"]
        if not force and copy_dependencies:
            raise DependentCopyPipeException(
                dependencies=dependencies,
                workspace_name=workspace.name,
                include_workspace_name=include_shared_with,
                is_cli=is_cli,
            )
        return dependencies

    @classmethod
    async def get_dependent_nodes_by_materialized_node(cls, workspace: "User"):
        materialized_nodes: Any = defaultdict(set)
        for pp in workspace.get_pipes():
            for nn in pp.pipeline.nodes:
                if nn.materialized:
                    materialized_nodes[pp.id].add(nn.id)

        def get_dependent_nodes(ws, pipe_id, node_id):
            pipe = ws.get_pipe(pipe_id)
            target_node = pipe.pipeline.get_node(node_id)
            if not target_node:
                pipe = ws.get_pipe(node_id)
                if not pipe:
                    return []
                target_node = pipe.endpoint

            def get_node_dependencies(pipe, node):
                try:
                    deps = []
                    for node in node.dependencies:  # noqa: B020
                        _node = pipe.pipeline.get_node(node)
                        if not _node:
                            _pipe = ws.get_pipe(node)
                            if _pipe:
                                deps.append((_pipe.id, _pipe.endpoint))
                        else:
                            deps.append((pipe.id, _node.id))
                    return deps
                except Exception:
                    return []

            dependent_nodes = {target_node.id: target_node}

            seen_dependencies = set()
            dependencies = get_node_dependencies(pipe, target_node)
            while dependencies:
                pipe_id, node_id = dependencies.pop()
                seen_dependencies.add((pipe_id, node_id))
                node = ws.get_node(node_id)
                if node:
                    dependent_nodes[node.id] = node
                    for pipe_id, node_id in get_node_dependencies(ws.get_pipe(pipe_id), node):  # noqa: B020
                        if (pipe_id, node_id) not in seen_dependencies:
                            dependencies.append((pipe_id, node_id))

            return list(dependent_nodes.values())

        mv_deps = defaultdict(set)
        for pipe_id, mvs in materialized_nodes.items():
            for mv in mvs:
                deps = get_dependent_nodes(workspace, pipe_id, mv)
                deps = [dep.id for dep in deps]
                mv_deps[mv].update(deps)

        return mv_deps

    @classmethod
    async def check_dependent_nodes_by_materialized_node(cls, workspace: "User", node_id: str):
        mv_deps = await Users.get_dependent_nodes_by_materialized_node(workspace)
        mv_names = []
        node = workspace.get_node(node_id)
        if not node:
            return

        for mv, deps in mv_deps.items():
            if node.id in deps:
                _node = workspace.get_node(mv)
                if _node:
                    _pipe = workspace.get_pipe_by_node(_node.id)
                    name = f"{_pipe.name}.{_node.name}" if _pipe else _node.name
                    mv_names.append(name)

        if mv_names:
            names = ",".join(mv_names)
            raise DependentMaterializedNodeOnUpdateException(
                f"Cannot modify the node {node.name} since it's used in Materialized Nodes: {names}. You can duplicate the Pipe or unlink the related Materialized Nodes."
            )

    @classmethod
    async def _send_notification_on_shared_data_source_removed(
        cls, user_account: "UserAccount", destination_workspace: "User", origin_workspace: "User", ds_name: str
    ):
        user_emails = destination_workspace.get_user_emails_that_have_access_to_this_workspace()

        if user_account:
            send_to_emails = list(filter(lambda x: x != user_account.email, user_emails))
        else:
            send_to_emails = user_emails

        origin_workspace_users = origin_workspace.get_workspace_users()
        owner_emails = [user["email"] for user in origin_workspace_users if user["role"] == Relationships.ADMIN]

        if len(send_to_emails) != 0:
            notification_result = await cls._mailgun_service.send_notification_on_shared_data_source_unshared(
                send_to_emails, ds_name, owner_emails, destination_workspace.id, destination_workspace.name
            )

            if notification_result.status_code != 200:
                logging.error(
                    f"Notification for Data Source has been unshared was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )

    @staticmethod
    async def unshare_all_data_sources_in_this_workspace(
        workspace_to_delete: User, user_account: UserAccount, keep_shared_ds_if_both_workspaces_belong_the_user=False
    ):
        def both_workspaces_belong_to_the_user(user: "UserAccount", origin_ws: "User", destination_ws: "User") -> bool:
            return user.owns_this_workspace(origin_ws) and user.owns_this_workspace(destination_ws)

        for datasource in workspace_to_delete.get_datasources():
            if isinstance(datasource, SharedDatasource) and not isinstance(datasource, BranchSharedDatasource):
                origin_workspace = User.get_by_id(datasource.original_workspace_id)
                if keep_shared_ds_if_both_workspaces_belong_the_user and both_workspaces_belong_to_the_user(
                    user_account, origin_workspace, workspace_to_delete
                ):
                    continue

                await Users.stop_sharing_a_datasource(
                    user_account,
                    origin_workspace,
                    workspace_to_delete,
                    datasource.id,
                    send_notification=False,
                    force=True,
                )
            else:
                for destination_workspace_id in datasource.shared_with:
                    destination_workspace = User.get_by_id(destination_workspace_id)
                    if keep_shared_ds_if_both_workspaces_belong_the_user and both_workspaces_belong_to_the_user(
                        user_account, workspace_to_delete, destination_workspace
                    ):
                        continue

                    await Users.stop_sharing_a_datasource(
                        user_account, workspace_to_delete, destination_workspace, datasource.id, force=True
                    )

    @classmethod
    async def _send_notification_on_build_plan_limits(
        cls,
        workspace: "User",
        max_api_requests_per_day: int,
        max_gb_storage_used: int,
        processed_price: float,
        storage_price: float,
        exceeded: bool,
        quantity_api_requests_per_day: Optional[int] = None,
        quantity_gb_storage_used: Optional[float] = None,
        quantity_gb_processed: Optional[int] = None,
    ):
        send_to_emails = workspace.get_user_emails_that_have_access_to_this_workspace()

        if len(send_to_emails) != 0:
            notification_result = await cls._mailgun_service.send_notification_on_build_plan_limits(
                send_to_emails,
                workspace.id,
                workspace.name,
                quantity_api_requests_per_day,
                max_api_requests_per_day,
                quantity_gb_storage_used,
                max_gb_storage_used,
                processed_price,
                storage_price,
                exceeded=exceeded,
                quantity_gb_processed=quantity_gb_processed,
            )

            if notification_result.status_code != 200:
                logging.error(
                    f"Build plan limits email for {workspace.id} was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )
            else:
                logging.info(f"Build plan limits email exceeded:{exceeded} for {workspace.id} sent)")

    @classmethod
    def _is_build_plan_limit_notification_required(cls, workspace: "User", exceeded: bool, requests: Optional[int]):
        today = date.today()
        required = False
        build_plan_limits_notifications = None
        if workspace.plan == BillingPlans.DEV:
            notification_key = "plan_exceeded" if exceeded else "plan_reaching"
            build_plan_limits_notifications = workspace.billing_details.get("notifications")
            if build_plan_limits_notifications is None:
                build_plan_limits_notifications = {notification_key: today}
                required = True
            else:
                prev_notification = build_plan_limits_notifications.get(notification_key)
                if prev_notification:
                    is_today = prev_notification == today
                    is_current_month = prev_notification.month == today.month and prev_notification.year == today.year
                if (
                    prev_notification is None
                    or (requests and not is_today)
                    or (requests is None and not is_current_month)
                ):
                    build_plan_limits_notifications.update({notification_key: today})
                    required = True
        return required, build_plan_limits_notifications

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def notify_build_plan_limits(
        cls,
        workspace_id: str,
        max_requests: int,
        max_storage: int,
        processed_price: float,
        storage_price: float,
        exceeded: bool,
        requests: Optional[int] = None,
        storage: Optional[float] = None,
        processed: Optional[int] = None,
    ):
        # check additionaly before transaction to save open transactions
        workspace = User.get_by_id(workspace_id)
        required, build_plan_limits_notifications = cls._is_build_plan_limit_notification_required(
            workspace, exceeded, requests
        )
        if not required:
            return
        with User.transaction(workspace_id) as workspace:
            required, build_plan_limits_notifications = cls._is_build_plan_limit_notification_required(
                workspace, exceeded, requests
            )
            if required:
                workspace.billing_details["notifications"] = build_plan_limits_notifications

        if required:
            await cls._send_notification_on_build_plan_limits(
                workspace,
                max_requests,
                max_storage,
                processed_price,
                storage_price,
                exceeded,
                requests,
                storage,
                processed,
            )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_rate_limit_config(user_id, name, count_per_period, period, max_burst=0, quantity=1):
        with User.transaction(user_id) as workspace:
            workspace.set_rate_limit_config(name, count_per_period, period, max_burst, quantity)
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_feature_flag(workspace_id: str, feature_flag_key: str, feature_flag_value: bool):
        with User.transaction(workspace_id) as workspace:
            workspace.feature_flags[feature_flag_key] = feature_flag_value
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_attribute(workspace_id: str, attribute_key: str, attribute_value: Any) -> User:
        with User.transaction(workspace_id) as workspace:
            workspace[attribute_key] = attribute_value
            return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _copy_workspace_to_releases_to_rollback(rollback_info: RollbackInfo) -> None:
        for r in rollback_info.release_ids:
            with User.transaction(r) as md:
                md.pipes = rollback_info.pipes
                md.datasources = rollback_info.datasources
                md.tokens = rollback_info.tokens

    @staticmethod
    async def add_release(
        workspace: "User",
        commit: str,
        semver: str,
        status: ReleaseStatus,
        metadata: Optional["User"] = None,
        force: bool = False,
    ) -> Release:
        if not validate_semver(semver):
            raise ReleaseStatusException(
                f"Cannot create Release in {workspace.name}, the version '{semver}' is not right, use a valid semver. Example: 1.0.0"
            )
        rollback_info: Optional[Users.RollbackInfo] = None

        workspace = User.get_by_id(workspace.id)
        validate_semver_greater_than_workspace_releases(workspace, semver)
        release = Release(id="fake", commit=commit, semver=semver, status=status)
        max_number_of_total_releases = (
            Limit.release_max_number_of_total_releases_in_branches
            if workspace.is_branch
            else workspace.get_limits(prefix="release").get(
                "max_number_of_total_releases", Limit.release_max_number_of_total_releases
            )
        )
        if len(workspace.releases) >= max_number_of_total_releases:
            oldest_release = Release.sort_by_date(workspace.get_releases())[-1]
            raise MaxNumberOfReleasesReachedException(
                f"Error: Maximum number of releases reached ({max_number_of_total_releases}). Delete your oldest Release ({oldest_release.semver}) and retry."
            )

        if not force:
            release, metadata, rollback_info = await workspace.apply_release_status_state_machine(
                status, release, metadata
            )

            if release.is_deploying and semver:
                assert metadata is not None
                release.id = metadata.id
        else:
            if not metadata:
                metadata = workspace.clone(semver)
            release.id = metadata.id

        await Users.add_release_to_workspace(workspace=workspace, release=release)

        if rollback_info:
            await Users._copy_workspace_to_releases_to_rollback(rollback_info)

        return release

    @staticmethod
    async def update_release(
        workspace: "User",
        release: Release,
        metadata: Optional["User"] = None,
        status: Optional[ReleaseStatus] = None,
        semver: Optional[str] = None,
        commit: Optional[str] = None,
        force: Optional[bool] = False,
        update_created_at: Optional[bool] = False,
    ) -> "User":
        original_release = release
        original_semver = release.semver
        rollback_info: Optional[Users.RollbackInfo] = None
        idx = None
        updated = True

        workspace = Users.get_by_id(workspace.id)
        idx = next((idx for idx, x in enumerate(workspace.releases) if x.get("semver") == release.semver), None)
        if idx is not None:
            if metadata and metadata.id != workspace.id:
                # FIXME: delete previous metadata from CH
                release.id = metadata.id
            if status:
                wmv = release.metadata
                if not wmv:
                    raise ReleaseStatusException(f"Cannot find metadata of Release {original_release.semver}")
                if not force:
                    release, _, rollback_info = await workspace.apply_release_status_state_machine(
                        status, release, metadata=wmv
                    )
            if semver:
                release.semver = semver
            if commit:
                release.commit = commit
            if update_created_at:
                release.created_at = datetime.now()

            # in case of rollback, we need to update the idx corresponding to the rolled back release
            workspace = User.get_by_id(workspace.id)
            semver_to_match = release.semver if status == ReleaseStatus.rollback else original_semver
            idx = next((idx for idx, x in enumerate(workspace.releases) if x.get("semver") == semver_to_match), None)
            if idx is None:
                raise ReleaseStatusException(f"Cannot find Release {release.semver} in Workspace {workspace.name}")

            workspace.releases[idx] = release.to_dict()

            # changing status so there's no two releases in "live" status
            # deletion is done in a separate transaction
            if status == ReleaseStatus.rollback:
                original_release.status = ReleaseStatus.deleting
                idx = next(
                    (idx for idx, x in enumerate(workspace.releases) if x.get("semver") == original_release.semver),
                    None,
                )
                if idx is None:
                    logging.exception(
                        f"Deleting release => Cannot find Release {release.semver} in Workspace {workspace.name}"
                    )
                else:
                    workspace.releases[idx] = original_release.to_dict()

            workspace = await Users.update_releases(workspace.id, workspace.releases)
            updated = True

        if status in [ReleaseStatus.rollback, ReleaseStatus.failed] and updated:
            idx = next(
                (idx for idx, x in enumerate(workspace.releases) if x.get("semver") == original_release.semver), None
            )
            if idx is not None:
                # here we drop resources from CH not used in any other release
                # FIXME check shared data sources
                workspace = await Users.delete_release(workspace, original_release, force=True)
            else:
                raise ReleaseStatusException(
                    f"Cannot find Release {original_release.semver} in Workspace {workspace.name}"
                )

            if original_release.id != workspace.id:
                User._delete(original_release.id)

        if rollback_info:
            await Users._copy_workspace_to_releases_to_rollback(rollback_info)

        return workspace

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_release_to_workspace(workspace: User, release: Release):
        with User.transaction(workspace.id) as workspace:
            if workspace.releases is None:
                workspace.releases = [release.to_dict()]
            else:
                workspace.releases.append(release.to_dict())
            workspace.flush()
            return workspace

    @staticmethod
    async def delete_release(workspace: "User", release: Release, force: bool = False, dry_run: bool = False) -> "User":
        await workspace.delete_release(release=release, force=force, dry_run=dry_run)
        return Users.get_by_id(workspace.id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_releases(workspace_id: str, releases: List[Dict[str, Any]]) -> "User":
        with User.transaction(workspace_id) as w:
            w.releases = releases
            w.flush()
            return w

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def delete_release_metadata(workspace: "User", release: Release) -> bool:
        if release.id != workspace.id:
            with User.transaction(release.id) as release_metadata:
                await release_metadata.delete()
            return True
        return False

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_promote_release(
        workspace_id: str, release: Release, metadata: "User"
    ) -> Tuple[Release, Users.RollbackInfo]:
        with User.transaction(workspace_id) as workspace:
            return await workspace.on_promote_release(release=release, metadata=metadata)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_preview_release(workspace_id: str, release: Release) -> Release:
        with User.transaction(workspace_id) as workspace:
            return workspace.on_preview_release(release=release)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_rollback_release(workspace_id: str, release: Release) -> Release:
        with User.transaction(workspace_id) as workspace:
            return workspace.on_rollback_release(release=release)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_deploying_release(
        workspace_id: str, release: Release, metadata: Optional["User"]
    ) -> Tuple[Release, User]:
        with User.transaction(workspace_id) as workspace:
            return workspace.on_deploying_release(release=release, metadata=metadata)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_failed_release(workspace_id: str, release: Release) -> Release:
        with User.transaction(workspace_id) as workspace:
            return workspace.on_failed_release(release=release)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def on_deleting_release(workspace_id: str, release: Release) -> Release:
        with User.transaction(workspace_id) as workspace:
            return workspace.on_deleting_release(release=release)


class public:
    """
    tinybird has a public account that contains:
    - public tables
    - internal tables that track internal application activity
    """

    INTERNAL_USER_EMAIL: str = os.environ.get("INTERNAL_USER_EMAIL", "r@localhost")
    INTERNAL_USER_WORKSPACE_NAME: str = os.environ.get("INTERNAL_USER_WORKSPACE_NAME", "Internal")
    INTERNAL_YEPCODE_WORKSPACE_NAME: str = os.environ.get("INTERNAL_YEPCODE_WORKSPACE_NAME", "yepcode_integration")
    INTERNAL_USER_DATABASE: str = os.environ.get("INTERNAL_USER_DATABASE", "public")

    INTERNAL_USER_ID: Optional[str] = None
    INTERNAL_WORKSPACE_ID: Optional[str] = None

    _public_datasets: List[str] = []

    _metrics_cluster: Optional[CHCluster] = None

    @staticmethod
    def set_public_user(public_email: str, database: Optional[str] = None) -> None:
        public.INTERNAL_USER_EMAIL = public_email
        public.INTERNAL_USER_WORKSPACE_NAME = public_email.split("@")[0]
        public.INTERNAL_YEPCODE_WORKSPACE_NAME = "yepcode_integration_" + public_email.split("@")[0]
        public.INTERNAL_USER_ID = None
        public.INTERNAL_WORKSPACE_ID = None
        if database:
            public.INTERNAL_USER_DATABASE = database

    @staticmethod
    def get_public_user() -> "User":
        if not public.INTERNAL_USER_ID:
            user = UserAccount.get_by_email(public.INTERNAL_USER_EMAIL)
            public.INTERNAL_USER_ID = user.id

        if public.INTERNAL_WORKSPACE_ID is not None:
            return User.get_by_id(public.INTERNAL_WORKSPACE_ID)
        else:
            workspace = User.get_by_name(public.INTERNAL_USER_WORKSPACE_NAME)
            public.INTERNAL_WORKSPACE_ID = workspace.id
            return workspace

    @staticmethod
    def register_public_user(cluster: Optional[CHCluster] = None) -> "User":
        try:
            user_account = UserAccount.register(public.INTERNAL_USER_EMAIL, str(uuid.uuid4()))
            user_account.confirmed_account = True
            user_account.save()
        except Exception:
            pass

        user_account = UserAccount.get_by_email(public.INTERNAL_USER_EMAIL)

        try:
            workspace = User.register(name=public.INTERNAL_USER_WORKSPACE_NAME, admin=user_account.id, cluster=cluster)

            workspace.database = public.INTERNAL_USER_DATABASE
            workspace.plan = BillingPlans.CUSTOM
            workspace.feature_flags.update({FeatureFlagWorkspaces.VERSIONS_GA.value: False})
            workspace.save()
        except Exception as e:
            logging.exception(e)

        workspace = User.get_by_name(public.INTERNAL_USER_WORKSPACE_NAME)

        return workspace

    @staticmethod
    def get_public_email() -> str:
        return public.INTERNAL_USER_EMAIL

    @staticmethod
    def get_public_database() -> str:
        return public.INTERNAL_USER_DATABASE

    @staticmethod
    def add_public_dataset(ds: str) -> None:
        public._public_datasets.append(ds)

    @staticmethod
    def public_datasets() -> List[str]:
        return public._public_datasets

    @staticmethod
    def set_metrics_cluster(name: str, server_url: str) -> None:
        public._metrics_cluster = CHCluster(name, server_url)

    @staticmethod
    def metrics_cluster() -> Optional[CHCluster]:
        return public._metrics_cluster

    @staticmethod
    def get_yepcode_database() -> str:
        yepcode_workspace = User.get_by_name(public.INTERNAL_YEPCODE_WORKSPACE_NAME)
        return yepcode_workspace.database

    @staticmethod
    async def query_internal(query: str) -> dict[str, Any]:
        internal_workspace = public.get_public_user()
        return await Users.query_user_db(workspace=internal_workspace, query=query)


class DatabaseDescriptor:
    def __get__(self, instance, owner):
        if not instance._database:
            return None
        return instance._database.split("__")[0]

    def __set__(self, instance, value):
        instance._database = value


class ChildKind(Enum):
    BRANCH = "branch"
    RELEASE = "release"


class User(RedisModel):
    __namespace__ = "users"
    __props__ = [
        "name",
        "_normalized_name_index",
        "password",
        "database",
        "database_server",
        "clusters",
        "pipes",
        "datasources",
        "tokens",
        "secrets",
        "tags",
        "explorations_ids",
        "confirmed_account",
        "deleted",
        "deleted_date",
        "max_execution_time",
        "enabled_pg",
        "pg_server",
        "pg_foreign_server",
        "pg_foreign_server_port",
        "limits",
        "plan",
        "billing_details",
        "stripe",
        "feature_flags",
        "hfi_frequency",
        "hfi_frequency_gatherer",
        "hfi_database_server",
        "hfi_concurrency_limit",
        "hfi_concurrency_timeout",
        "hfi_max_request_mb",
        "storage_policies",
        "origin",
        "cdk_gcp_service_account",
        "organization_id",
        "kafka_server_group",
        "releases",
        "env_database",
        "external_clusters",
        "profiles",
        "remote",
        "use_gatherer",
        "allow_gatherer_fallback",
        "gatherer_allow_s3_backup_on_user_errors",
        "gatherer_flush_interval",
        "gatherer_deduplication",
        "gatherer_wait_false_traffic",
        "gatherer_wait_true_traffic",
        "child_kind",
    ]

    __fast_scan__ = True

    __indexes__ = ["_normalized_name_index", "database"]

    secret: str = ""
    secrets_key: bytes = b""
    CH_HOST: str = os.environ.get("CLICKHOUSE_CLUSTER_HOST", "ci_ch")
    CH_HTTP_PORT: str = os.environ.get("CLICKHOUSE_CLUSTER_HTTP_PORT", "6081")
    default_database_server: str = f"{CH_HOST}:{CH_HTTP_PORT}"
    internal_database_server: str = f"{CH_HOST}:{CH_HTTP_PORT}"
    default_cluster: str = "tinybird"
    default_postgres_server: str = "10.156.0.9"
    default_postgres_foreign_server: str = "10.156.0.3"
    default_postgres_foreign_server_port: str = "8123"
    default_plan: str = BillingPlans.DEV

    replace_executor = None

    # TODO: Remove this once we changed all the code to expect Optional[User]
    @classmethod
    def get_by_id(cls, _id: str, in_transaction: bool = False) -> User:
        return super().get_by_id(_id, in_transaction)  # type: ignore

    def __repr__(self) -> str:
        return f"User(id='{self.id}')"

    @classmethod
    def config(
        cls,
        redis_client,
        secret,
        replace_executor=None,
        secrets_key=None,
    ):
        super().config(redis_client)
        cls.secret = secret
        try:
            if not secrets_key:
                logging.warning("Master key not found")
            else:
                cls.secrets_key = Base64Encoder.decode(secrets_key.encode())
        except Exception as e:
            logging.exception(f"Master key not set: {str(e)}")
        cls.replace_executor = replace_executor

    # TODO add @override once Python is updated to 3.12
    @staticmethod
    def _get_index_value(the_class: Any, index: str) -> Optional[str]:
        # releases cannot be indexed by database. They share the same database value as the main and the database index
        # must point to the main.
        if index == "database" and the_class.is_release:
            return None
        return super()._get_index_value(the_class, index)

    @staticmethod
    def clone_limits(
        limits_prefixes: List[str], origin: User, default_branches: Optional[bool] = False
    ) -> Dict[str, Tuple[str, str]]:
        limits: Dict[str, Tuple[str, str]] = dict()
        for prefix in limits_prefixes:
            _limits = origin.get_limits(prefix)
            _branch_limits = origin.get_limits(f"branch{prefix}")
            for key, value in _limits.items():
                limits[key] = (
                    (prefix, _branch_limits.get(f"branch{key}", value)) if default_branches else (prefix, value)
                )
        return limits

    @staticmethod
    def register(
        name: str,
        admin: Optional[str] = None,
        cluster: Optional[CHCluster] = None,
        normalize_name_and_try_different_on_collision: bool = False,
        origin: Optional[User] = None,
        plan: Optional[str] = None,
    ) -> "User":
        uid, database_name = User.generate_uid_and_database_name_and_try_different_on_collision()
        remote = {}
        cdk_gcp_service_account = User.cdk_gcp_service_account if hasattr(User, "cdk_gcp_service_account") else None

        if not admin:
            raise Exception("Workspace must have an owner")

        user_owner = UserAccount.get_by_id(admin)
        if not user_owner:
            raise UserAccountDoesNotExist("User account does not exist")

        if not name:
            raise Exception("Workspace must have a name")

        limits = {}
        plan = plan or User.default_plan
        if origin:
            branch_name = BranchName(name, origin.name)
            User.assert_workspace_name_is_not_in_use(branch_name)

            normalized_name = name
            normalized_name_index = str(branch_name)
            remote = copy.deepcopy(origin.remote)
            remote["branch"] = name
            remote["last_commit_sha"] = ""

            cdk_gcp_service_account = copy.deepcopy(origin.cdk_gcp_service_account)
            limits = User.clone_limits(["copy", "workspace"], origin, default_branches=True)
            plan = (
                BillingPlans.BRANCH_ENTERPRISE
                if origin.plan in (BillingPlans.ENTERPRISE, BillingPlans.CUSTOM)
                else BillingPlans.DEV
            )
        else:
            if normalize_name_and_try_different_on_collision:
                name = str(User.normalize_name_and_try_different_on_collision(name))
            else:
                workspace_name = WorkspaceName(name)
                User.assert_workspace_name_is_not_in_use(workspace_name)

            normalized_name = normalized_name_index = str(name)

        if not cluster:
            cluster = CHCluster(name=User.default_cluster, server_url=User.default_database_server)

        workspace_data: Dict[str, Any] = {
            "id": uid,
            "name": normalized_name,
            "_normalized_name_index": normalized_name_index,
            "password": "",
            "database": database_name,
            "database_server": cluster.server_url,
            "clusters": [cluster.name] if cluster.name is not None else None,
            "pipes": [],
            "datasources": [],
            "tokens": [],
            "secrets": [],
            "confirmed_account": False,
            "deleted": False,
            "enabled_pg": False,
            "pg_server": User.default_postgres_server,
            "pg_foreign_server": User.default_postgres_foreign_server,
            "pg_foreign_server_port": User.default_postgres_foreign_server_port,
            "limits": limits,
            "stripe": {},
            "feature_flags": {},
            "origin": origin.id if origin else None,
            "cdk_gcp_service_account": cdk_gcp_service_account,
            "releases": [],
            "env_database": None,
            "external_clusters": {},
            "profiles": {},
            "remote": remote,
            "child_kind": ChildKind.BRANCH.value if origin else None,
            "use_gatherer": (
                FeatureFlagsWorkspaceService.feature_for_id(
                    FeatureFlagWorkspaces.GATHERER_ON_BRANCHES, "", origin.feature_flags
                )
                if origin
                else GathererDefaults.USE_GATHERER
            ),
            "allow_gatherer_fallback": GathererDefaults.ALLOW_GATHERER_FALLBACK,
            "gatherer_allow_s3_backup_on_user_errors": (
                False if origin else GathererDefaults.ALLOW_S3_BACKUP_ON_USER_ERRORS
            ),
            "plan": plan,
        }

        workspace = User(**workspace_data)

        workspace.add_token("admin token", scopes.ADMIN)
        workspace.add_token(f"admin {user_owner.email}", scopes.ADMIN_USER, user_owner.id)
        workspace.add_token("create datasource token", scopes.DATASOURCES_CREATE)

        workspace.save()

        UserWorkspaceRelationship.create_relationship(
            user_id=user_owner.id, workspace_id=workspace.id, relationship=Relationships.ADMIN
        )

        UserWorkspaceNotifications.create_notifications(
            user_id=user_owner.id, workspace_id=workspace.id, notifications=[Notifications.INGESTION_ERRORS]
        )

        if not workspace.origin:
            assigned_org = User._assign_workspace_to_organization(workspace, user_owner)
            if assigned_org:
                logging.info(
                    f"Workspace {workspace.name} ({workspace.id}) assigned to organization {assigned_org.name} ({assigned_org.id})"
                )

        return User.get_by_id(workspace.id)

    @staticmethod
    def _assign_workspace_to_organization(workspace: User, owner: "UserAccount") -> Any:
        from tinybird.organization.organization import Organization
        from tinybird.organization.organization_service import OrganizationService

        for org in Organization.get_all():
            if org.contains_email(owner.email):
                return OrganizationService.add_workspace_to_organization(org, workspace.id)
        return None

    def __init__(self, **user_dict: Any) -> None:
        # Ignore this inconsistency for now
        self.id: str = None  # type: ignore
        self.name: str = None  # type: ignore

        self._normalized_name_index: Optional[str] = None
        self.password: Optional[str] = None
        self._database: str = user_dict.get("database", None)
        self.database_server: str = User.default_database_server
        self.clusters: List[str] = []
        self.pipes: List[Dict[str, Any]] = []
        self.datasources: List[Dict[str, Any]] = []
        self.explorations_ids: List[str] = []
        self.tokens: List[AccessToken] = []
        self.secrets: List[Dict[str, Any]] = []
        self.tags: List[Dict[str, Any]] = []
        self.confirmed_account: bool = False
        self.deleted: bool = False
        self.deleted_date: Optional[datetime] = None
        self.enabled_pg: bool = False
        self.pg_server: str = User.default_postgres_server
        self.pg_foreign_server: str = User.default_postgres_foreign_server
        self.pg_foreign_server_port: str = User.default_postgres_foreign_server_port
        self.limits: Dict[str, Any] = {}
        self.plan: str = User.default_plan
        self.billing_details: Dict[str, Any] = {"prices_overrides": {}, "packages": []}
        self.stripe: Dict[str, Any] = {}
        self.feature_flags: Dict[str, bool] = {}
        self.hfi_frequency: Optional[float] = None
        self.hfi_frequency_gatherer: Optional[float] = None
        self.hfi_database_server: str = ""
        self.hfi_concurrency_limit: Optional[int] = None
        self.hfi_concurrency_timeout: Optional[float] = None
        self.hfi_max_request_mb: Optional[int] = None
        self.storage_policies: Dict[str, int] = {}
        self.origin: Optional[str] = user_dict.get("origin", None)
        self.cdk_gcp_service_account: Optional[Dict[str, Any]] = None
        self.organization_id: Optional[str] = None
        self.kafka_server_group: Optional[str] = None
        self.releases: List[Dict[str, Any]] = []
        self.env_database: str = user_dict.get("env_database", None)
        self.external_clusters: Dict[str, Any] = {}
        self.profiles: Dict[str, str] = {}
        self.remote: Dict[str, Any] = user_dict.get("remote", {})
        self.use_gatherer: Optional[bool] = GathererDefaults.USE_GATHERER
        self.allow_gatherer_fallback: Optional[bool] = GathererDefaults.ALLOW_GATHERER_FALLBACK
        self.gatherer_allow_s3_backup_on_user_errors: Optional[bool] = GathererDefaults.ALLOW_S3_BACKUP_ON_USER_ERRORS
        self.gatherer_flush_interval: Optional[int] = None
        self.gatherer_deduplication: Optional[bool] = None
        self.gatherer_wait_false_traffic: Optional[int] = None
        self.gatherer_wait_true_traffic: Optional[int] = None
        self.child_kind: Optional[str] = None

        super().__init__(**user_dict)

        self.flush()

    database: str = DatabaseDescriptor()  # type: ignore

    def __getattribute__(self, name):
        if name == "database":
            return DatabaseDescriptor().__get__(self, User)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == "database":
            if not value:
                return
            DatabaseDescriptor().__set__(self, value)
        else:
            super().__setattr__(name, value)

    def clone(self, semver: str, database: Optional[str] = None) -> User:
        database = self.database if not database else database
        uid, _ = User.generate_uid_and_database_name_and_try_different_on_collision()
        origin = self.id
        normalized_semver = f'{semver.replace(".", "_").replace("-", "_")}'
        name: str = f'{self.name}__{normalized_semver}__{origin.replace("-", "_")}'
        workspace_name = WorkspaceName(name)
        try:
            User.assert_workspace_name_is_not_in_use(workspace_name)
        except NameAlreadyTaken:
            validate_semver_greater_than_workspace_releases(self, semver)
            raise
        normalized_name = str(workspace_name)

        user_data: Dict[str, Any] = {
            "id": uid,
            "name": name,
            "_normalized_name_index": normalized_name,
            "password": "",
            "database": f"{database}__{normalized_semver}",
            "database_server": self.database_server,
            "clusters": self.clusters,
            "pipes": self.pipes,
            "datasources": self.datasources,
            "explorations_ids": self.explorations_ids,
            "tokens": self.tokens,
            "secrets": self.secrets,
            "confirmed_account": self.confirmed_account,
            "deleted": self.deleted,
            "enabled_pg": False,
            "pg_server": self.pg_server,
            "pg_foreign_server": self.pg_foreign_server,
            "pg_foreign_server_port": self.pg_foreign_server_port,
            "limits": {},
            "stripe": {},
            "plan": self.plan,
            "billing_details": {"prices_overrides": {}, "packages": []},
            "feature_flags": {},
            "origin": origin,
            "cdk_gcp_service_account": self.cdk_gcp_service_account,
            "releases": [],
            "env_database": None,
            "external_clusters": self.external_clusters,
            "profiles": self.profiles,
            "hfi_frequency": self.hfi_frequency,
            "hfi_frequency_gatherer": self.hfi_frequency_gatherer,
            "hfi_database_server": None,
            "hfi_concurrency_limit": self.hfi_concurrency_limit,
            "hfi_concurrency_timeout": self.hfi_concurrency_timeout,
            "hfi_max_request_mb": self.hfi_max_request_mb,
            "storage_policies": self.storage_policies,
            "organization_id": self.organization_id,
            "kafka_server_group": None,
            "remote": self.remote,
            "use_gatherer": self.use_gatherer,
            "allow_gatherer_fallback": self.allow_gatherer_fallback,
            "gatherer_allow_s3_backup_on_user_errors": self.gatherer_allow_s3_backup_on_user_errors,
            "gatherer_flush_interval": self.gatherer_flush_interval,
            "gatherer_deduplication": self.gatherer_deduplication,
            "gatherer_wait_false_traffic": self.gatherer_wait_false_traffic,
            "gatherer_wait_true_traffic": self.gatherer_wait_true_traffic,
            "child_kind": ChildKind.RELEASE.value,
        }

        user = User(**user_data)
        user.save()
        user.flush()
        return User.get_by_id(user.id)

    def flush(self) -> None:
        self._pipes = list(map(Pipe.from_dict, self.pipes))
        self._releases = list(map(Release.from_dict, self.releases))
        self._secrets = list(map(Secret.from_dict, self.secrets))

    def __getitem__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            raise AttributeError(f"'User' does not contain the '{item}' attribute")

    def __setitem__(self, item, value):
        try:
            object.__getattribute__(self, item)
        except AttributeError as e:
            # Explicit raising to be clear about behaviour
            raise e
        object.__setattr__(self, item, value)

    def __contains__(self, item):
        try:
            object.__getattribute__(self, item)
            return True
        except AttributeError:
            return False

    def __eq__(self, other):
        """
        >>> u0 = User(id='abcd')
        >>> u0 == None
        False
        >>> User(id='abcd') == User(id='abcd')
        True
        >>> User(id='abcd') == User(id='1234')
        False
        >>> class F:
        ...    id = u0.id
        >>> u0 == F()
        False
        """
        return other is not None and type(self) == type(other) and self.id == other.id  # noqa: E721

    @staticmethod
    def get_by_name(name: str) -> "User":
        user = User.get_by_index("_normalized_name_index", name)
        if not user:
            raise UserDoesNotExist("workspace does not exist")
        return user

    @staticmethod
    def get_by_database(database: str) -> "User":
        """Return the workspace or branch associated to the database, or the origin workspace in case of a release"""

        user: Optional["User"] = User.get_by_index("database", database)
        if not user:
            raise UserDoesNotExist("workspace does not exist")

        # TODO: the logic to get the main in case the workspace returned is a release should not be needed anymore after
        #  the changes in https://gitlab.com/tinybird/analytics/-/merge_requests/13474. Added a warning to track that
        #  the index has been updated.
        if user.is_release and user.origin:
            logging.warning(
                f"Inconsistency issue: Release still has the database index pointing to it. release id: '{user.id}', database: '{user.database}', origin: {user.origin}."
            )
            user = user.get_by_id(user.origin)
            if not user:
                raise UserDoesNotExist("workspace does not exist")

        return user

    @classmethod
    def _filter_workspaces(
        cls: Type[T], workspaces: List[T], include_branches: bool, include_releases: bool
    ) -> List[T]:
        result: List[T] = []
        for w in workspaces:
            if not include_releases and w.is_release:
                continue
            if not include_branches and w.is_branch:
                continue
            result.append(w)
        return result

    @classmethod
    def get_all(cls: Type[T], include_branches: bool, include_releases: bool, *args: Any, **kwargs: Any) -> List[T]:
        """
        Get all models from redis.
        You can pass a keyword argument `count` to limit the number of models returned.
        """
        items = super().get_all(*args, **kwargs)
        return cls._filter_workspaces(items, include_branches=include_branches, include_releases=include_releases)

    @classmethod
    async def get_all_paginated(
        cls: Type[T],
        skip_count: int,
        page_size: int,
        include_branches: bool,
        include_releases: bool,
        *args: Any,
        **kwargs: Any,
    ) -> List[T]:
        """
        Get all models from redis paginated.
        - You can pass a keyword argument `batch_count` to limit the number of keys fetched from Redis in the same take.
        """
        page_items = await super().get_all_paginated(*args, skip_count=skip_count, page_size=page_size, **kwargs)
        return cls._filter_workspaces(page_items, include_branches=include_branches, include_releases=include_releases)

    @staticmethod
    def get_soft_deleted_workspaces_for_hard_deletion() -> List[User]:
        """
        Get all workspaces that were soft deleted more than 30 days ago.
        """
        all_workspaces = User.get_all(include_branches=True, include_releases=False)
        safety_time = datetime.utcnow() - timedelta(days=30)

        ws_to_remove: List[User] = []
        for ws in all_workspaces:
            if ws.deleted and ws.deleted_date and ws.deleted_date < safety_time:
                ws_to_remove.append(ws)

        return ws_to_remove

    def database_host_ip_port(self) -> str:
        """
        returns ip:port for the user database
        >>> u0 = User(id='test')
        >>> u0['database_server'] = '127.0.0.1'
        >>> u0.database_host_ip_port()
        '127.0.0.1:9000'
        >>> u0['database_server'] = '127.0.0.1:9001'
        >>> u0.database_host_ip_port()
        '127.0.0.1:9001'
        >>> u0['database_server'] = 'http://127.0.0.1'
        >>> u0.database_host_ip_port()
        '127.0.0.1:9000'
        """
        # database_server can have an ip or a full url
        h = urlparse(self["database_server"])
        if "http" in h.scheme:
            host = h.netloc
        else:
            host = self["database_server"]

        # remote function needs the port in the url if you have several servers running on the same machine
        # this does not usually happen in production setups but it could in development envs
        if ":" not in host:
            host = host + ":9000"
        return host

    def database_host_ip(self) -> str:
        """
        returns ip for the user database
        >>> u0 = User(id='test')
        >>> u0['database_server'] = '127.0.0.1'
        >>> u0.database_host_ip()
        '127.0.0.1'
        >>> u0['database_server'] = '127.0.0.1:9001'
        >>> u0.database_host_ip()
        '127.0.0.1'
        >>> u0['database_server'] = 'http://127.0.0.1'
        >>> u0.database_host_ip()
        '127.0.0.1'
        """
        host_ip = self.database_host_ip_port()
        return host_ip.split(":")[0]

    @property
    def cluster(self) -> Optional[str]:
        if self.clusters:
            return self.clusters[0]
        return None

    @property
    def storage_policy(self) -> Optional[str]:
        """
        >>> u0 = User(id='test_storage_policy')
        >>> u0.storage_policy == None
        True
        >>> u0.storage_policies = {'s3': 0}
        >>> u0.storage_policy == None
        True
        >>> u0.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = True
        >>> u0.storage_policy == 's3'
        True
        """
        if self.storage_policies and FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY, "", self.feature_flags
        ):
            return list(self.storage_policies.keys())[0]
        return None

    def is_valid_cluster(self, cluster: Optional[str]) -> bool:
        if not cluster:
            return True
        return cluster in self.clusters

    def get_resource(self, name_or_id: str, pipe: Optional[Pipe] = None) -> Optional[Union[Datasource, Pipe, PipeNode]]:
        if not name_or_id:
            return None

        datasource = self.get_datasource(name_or_id, include_read_only=True)
        if datasource:
            return datasource

        name_or_id = Resource.normalize(name_or_id)
        pipes = [pipe] if pipe else self.get_pipes()
        for pipe in pipes:
            if pipe.name == name_or_id or pipe.id == name_or_id:
                return pipe
            for node in pipe.pipeline.nodes:
                if node.name == name_or_id or node.id == name_or_id:
                    return node
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "max_seats": self.max_seats_limit,
            "kafka_max_topics": self.kafka_max_topics,
            "members": self.members,
            "active": self.is_active,
            "plan": self.plan,
            "created_at": self.created_at.date().isoformat(),
            "clusters": self.clusters,
            "database": self.database,
            "database_server": self.database_server,
            "pg_server": self.pg_server,
            "pg_foreign_server": self.pg_foreign_server,
            "pg_foreign_server_port": self.pg_foreign_server_port,
            "deleted": self.deleted,
            "is_read_only": self.is_read_only,
            "remote": self.remote,
        }

    def to_json(
        self,
        with_token: bool = False,
        with_feature_flags: bool = False,
        with_bi_enabled: bool = False,
        with_stripe: bool = False,
    ) -> Dict[str, Any]:
        workspace_info = {
            "id": self.id,
            "name": self.name,
            "max_seats": self.max_seats_limit,
            "kafka_max_topics": self.kafka_max_topics,
            "members": self.members,
            "active": self.is_active,
            "plan": self.plan,
            "created_at": self.created_at.date().isoformat(),
            "clusters": self.clusters,
            "deleted": self.deleted,
            "is_read_only": self.is_read_only,
            "is_branch": self.is_branch,
            "is_branch_outdated": self.is_branch_outdated,
            "main": self.origin,
            "rate_limits": self.rate_limits,
            "release": self.current_release.to_json() if self.current_release else None,
        }

        if with_token:
            workspace_info["token"] = self.get_token_for_scope(scopes.ADMIN)

        if with_feature_flags:
            feature_flags = self.feature_flags

            if self.is_branch and self.origin:
                main_workspace = self.get_by_id(self.origin)
                feature_flags = main_workspace.feature_flags

            workspace_info["feature_flags"] = FeatureFlagsWorkspaceService.get_all_feature_values(feature_flags)

        if with_bi_enabled:
            workspace_info["bi_enabled"] = self.enabled_pg

        if with_stripe:
            workspace_info["stripe"] = {"client_secret": self.stripe.get("client_secret"), "api_key": None}

        if self.remote.get("provider") or self.remote.get("status") in [
            GitHubSettingsStatus.UNLINKED.value,
            GitHubSettingsStatus.CLI.value,
        ]:
            # Don't include auth details
            remote = dict(self.remote)
            if "access_token" in remote:
                del remote["access_token"]
            workspace_info["remote"] = remote

        return workspace_info

    def get_workspace_info(self, with_token: bool = False, with_members_and_owner: bool = True) -> Dict[str, Any]:
        workspace_info = {
            "id": self.id,
            "name": self.name,
            "max_seats": self.max_seats_limit,
            "kafka_max_topics": self.kafka_max_topics,
            "active": self.is_active,
            "plan": self.plan,
            "role": Relationships.ADMIN,  # Keep backwards compatibility with previous CLI versions
            "created_at": self.created_at.date().isoformat(),
            "is_branch": self.is_branch,
            "release": self.current_release.to_json() if self.current_release else None,
            "main": self.origin,
            "rate_limits": self.rate_limits,
            "is_read_only": self.is_read_only,
        }

        from tinybird.organization.organization import Organization

        organization = Organization.get_by_id(self.organization_id) if self.organization_id else None
        if organization:
            workspace_info["organization"] = {
                "id": organization.id,
                "name": organization.name,
                "plan": {
                    "billing": organization.plan_details["billing"],
                    "commitment": organization.plan_details["commitment"],
                },
            }

        if with_members_and_owner:
            members = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
            owner = None
            workspace_members = []

            for member in members:
                try:
                    user_account = UserAccounts.get_by_id(member.user_id)
                except UserAccountDoesNotExist:
                    logging.warning(
                        f"Inconsistency: UserAccount {member.user_id} not found for workspace {self.name} ({self.id})"
                    )
                    continue
                user_workspace_notifications = UserWorkspaceNotifications.get_by_user_and_workspace(
                    member.user_id, self.id
                )
                workspace_members.append(
                    {
                        "email": user_account.email,
                        "id": user_account.id,
                        "max_owned_workspaces": user_account.max_owned_limit,
                        "max_workspaces": user_account.max_workspaces_limit,
                        "created_at": user_account.created_at.date().isoformat(),
                        "role": member.relationship,
                        "notifications": (
                            user_workspace_notifications.notifications if user_workspace_notifications else []
                        ),
                    }
                )
                if member.relationship == Relationships.ADMIN:
                    owner = member.user_id

            workspace_info["owner"] = owner
            workspace_info["members"] = workspace_members

        if with_token:
            workspace_info["token"] = self.get_token_for_scope(scopes.ADMIN)
        return workspace_info

    def get_workspace_users(self) -> List[Dict[str, Any]]:
        users: List[Dict[str, Any]] = []

        workspace_users = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
        for workspace_user in workspace_users:
            try:
                user_account = UserAccounts.get_by_id(workspace_user.user_id)
            except UserAccountDoesNotExist:
                logging.warning(
                    f"Inconsistency: The user account {workspace_user.user_id} does not exist, but the user workspace relationship exists for workspace {self.name} ({self.id})"
                )
                continue
            user_workspace_notifications = UserWorkspaceNotifications.get_by_user_and_workspace(
                workspace_user.user_id, self.id
            )
            user_info = user_account.get_user_info()
            user_info["role"] = workspace_user.relationship
            user_info["notifications"] = (
                user_workspace_notifications.notifications if user_workspace_notifications else []
            )
            users.append(user_info)

        return users

    # This is a simplified version of get_workspace_users() that returns only the email and id of the users that belong to the workspace
    async def get_simple_members(self) -> List[UserAccount]:
        user_relationships = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
        members: List[UserAccount] = []
        for relationship in user_relationships:
            user = await UserAccount.get_by_id_async(relationship.user_id)
            if user:
                members.append(user)
        return members

    # TODO: Convert this property in a method where users can specify which information need. Make notifications information optional
    @property
    def members(self) -> List[Dict[str, Any]]:
        return self.get_workspace_users()

    def get_user_emails_that_have_access_to_this_workspace(self) -> List[str]:
        # TODO add tests
        users: List[str] = []

        workspace_users = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
        for workspace_user in workspace_users:
            user = UserAccounts.get_by_id(workspace_user.user_id)
            if not user:
                logging.warning(
                    f"Inconsistency: UserAccount {workspace_user.user_id} not found for workspace {self.name} ({self.id})"
                )
                continue
            users.append(user.email)

        return users

    def get_user_accounts(self) -> List[Dict[str, Any]]:
        # TODO add tests
        user_workspaces = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
        users: List[Dict[str, Any]] = []

        for user_workspace in user_workspaces:
            user_account = UserAccount.get_by_id(user_workspace.user_id)
            if not user_account:
                logging.warning(
                    f"Inconsistency: UserAccount {user_workspace.user_id} not found for workspace {self.name} ({self.id})"
                )
                continue

            user_workspace_notifications = UserWorkspaceNotifications.get_by_user_and_workspace(
                user_workspace.user_id, self.id
            )

            users.append(
                {
                    "email": user_account.email,
                    "id": user_account.id,
                    "max_owned_workspaces": user_account.max_owned_limit,
                    "max_workspaces": user_account.max_workspaces_limit,
                    "created_at": user_account.created_at.date().isoformat(),
                    "role": user_workspace.relationship,
                    "notifications": user_workspace_notifications.notifications if user_workspace_notifications else [],
                    "integrations": user_account.integrations or [],
                }
            )

        return users

    @property
    def user_accounts(self):
        return self.get_user_accounts()

    @property
    def user_accounts_emails(self):
        return self.get_user_emails_that_have_access_to_this_workspace()

    def _get_datasources_from_branch(self) -> List[Datasource]:
        datasources: List[Datasource] = []
        for ds in self.datasources:
            if ds.get("shared_from", False):
                datasources.append(BranchSharedDatasource.from_dict(ds))
            elif ds.get("origin_connector_id"):
                datasources.append(KafkaBranchDatasource.from_dict(ds))
            else:
                datasources.append(BranchDatasource.from_dict(ds))
        return datasources

    def get_datasources(self) -> List[Datasource]:
        if self.is_branch or self.is_release_in_branch:
            return self._get_datasources_from_branch()
        else:
            return list(
                map(
                    lambda ds: (
                        SharedDatasource.from_dict(ds) if ds.get("shared_from", False) else Datasource.from_dict(ds)
                    ),
                    self.datasources,
                )
            )

    def add_datasource(
        self,
        ds_name: str,
        stats=None,
        cluster: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        prefix: str = "t",
        fixed_name: bool = False,
        json_deserialization: Optional[List[Dict[str, Any]]] = None,
        description="",
        fixed_id: Optional[str] = None,
        origin_database: Optional[str] = None,
        origin_connector_id: Optional[str] = None,
        service_name=None,
        service_conf=None,
    ) -> Datasource:
        datasource = self.get_datasource(ds_name)
        existing_resource = self.get_resource(ds_name)
        if existing_resource and datasource != existing_resource:
            raise ResourceAlreadyExists(
                f'There is already a {existing_resource.resource_name} with name "{ds_name}". Data Source names must be globally unique'
            )

        existing_datasources = len(self.get_datasources())
        # unfortunately we might arrive here from a release but not as ReleaseWorkspace
        if self.is_release:
            metadata_for_limits = self.get_main_workspace()
        else:
            metadata_for_limits = self
        max_datasources = metadata_for_limits.get_limits(prefix="workspace").get(
            "max_datasources", Limit.max_datasources
        )
        if existing_datasources >= max_datasources:
            raise DatasourceLimitReached(
                f"The maximum number of datasources for this workspace is {int(max_datasources)}."
            )

        if not self.is_valid_cluster(cluster):
            raise ValueError(f"Invalid cluster '{cluster}'")

        if not datasource:
            id = ds_name if fixed_name else fixed_id if fixed_id else Resource.guid(prefix)
            new_datasource = {
                "id": id,
                "name": ds_name,
                "replicated": bool(cluster),
                "cluster": cluster,
                "tags": tags or {},
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "json_deserialization": json_deserialization or [],
                "description": description,
                "ignore_paths": [],
                "service": service_name,
                "service_conf": service_conf,
            }
            if origin_database:
                new_datasource.update({"origin_database": origin_database})
            if origin_connector_id:
                new_datasource.update({"origin_connector_id": origin_connector_id})
            self.datasources.append(new_datasource)
            self.flush()
            if origin_database:
                if origin_connector_id:
                    return KafkaBranchDatasource.from_dict(new_datasource)
                else:
                    return BranchDatasource.from_dict(new_datasource)
            else:
                return Datasource.from_dict(new_datasource)
        return datasource

    def mark_datasource_as_shared(self, datasource_id: str, shared_with_workspace_id: str) -> None:
        existing_datasource = self.get_datasource(datasource_id, include_read_only=True)
        if not existing_datasource:
            raise DataSourceNotFound(datasource_id)

        if existing_datasource.is_read_only:
            raise DataSourceIsReadOnly()

        if shared_with_workspace_id in existing_datasource.shared_with:
            raise DatasourceAlreadySharedWithWorkspace(
                workspace_id=shared_with_workspace_id, datasource_name=datasource_id
            )

        existing_datasource.shared_with.append(shared_with_workspace_id)

        self.update_datasource(existing_datasource)

    def unmark_datasource_as_shared(self, datasource_id: str, shared_with_workspace_id: str):
        """
        >>> u = User(pipes=[], datasources=[{'id': 'ds_a', 'name': 'ds_name', 'statistics': None, 'shared_with': ['w_a','w_b','w_c',]}])
        >>> u.unmark_datasource_as_shared('ds_a', 'w_b')
        >>> u.get_datasource('ds_a').shared_with
        ['w_a', 'w_c']
        >>> u.unmark_datasource_as_shared('ds_a', 'w_b')
        Traceback (most recent call last):
        ...
        tinybird.user.DatasourceIsNotSharedWithThatWorkspace
        """
        existing_datasource = self.get_datasource(datasource_id)
        if not existing_datasource:
            raise DataSourceNotFound(datasource_id)

        if shared_with_workspace_id not in existing_datasource.shared_with:
            raise DatasourceIsNotSharedWithThatWorkspace()

        existing_datasource.shared_with = list(
            filter(lambda w_id: w_id != shared_with_workspace_id, existing_datasource.shared_with)
        )

        self.update_datasource(existing_datasource)

    def add_shared_datasource(
        self,
        original_datasource_id: str,
        workspace_id: str,
        workspace_name: str,
        ds_database: str,
        ds_name: str,
        ds_description: str,
        distributed_mode: Optional[str] = None,
    ) -> Datasource:
        ds = SharedDatasource(
            original_datasource_id, workspace_id, workspace_name, ds_database, ds_name, ds_description, distributed_mode
        )

        existing_datasource = self.get_datasource(ds.name, include_read_only=True)
        if existing_datasource:
            raise ValueError(f"The '{existing_datasource.name}' is already shared in this workspace")

        self.datasources.append(ds.to_dict(include_internal_data=True))
        return ds

    def add_branch_shared_datasource(
        self,
        ds_id: str,
        original_workspace_id: str,
        original_workspace_name: str,
        original_ds_database: str,
        original_ds_name: str,
        original_ds_description: str,
    ) -> BranchSharedDatasource:
        ds = BranchSharedDatasource(
            ds_id,
            original_workspace_id,
            original_workspace_name,
            original_ds_database,
            original_ds_name,
            original_ds_description,
        )
        self.datasources.append(ds.to_dict(include_internal_data=True))
        return ds

    def update_datasource(self, ds: Datasource, update_last_commit_status: bool = True):
        idx = next((idx for idx, x in enumerate(self.datasources) if x["id"] == ds.id or x["name"] == ds.name), None)
        if idx is not None:
            ds.touch()
            self.datasources[idx] = ds.to_dict(
                include_internal_data=True, update_last_commit_status=update_last_commit_status
            )
            self.flush()
            return True
        return False

    def update_pipes_datasource_name(
        self, old_name: str, new_name: str, dependencies: Optional[List[str]], edited_by: Optional[str]
    ) -> None:
        if not dependencies:
            return

        updated_at = datetime.now()
        for idx, pipe in enumerate(self.get_pipes()):
            if pipe.name in dependencies or f"{self.name}.{pipe.name}" in dependencies:
                for node in pipe.pipeline.nodes:
                    sql = node._sql
                    sql = re.sub("([\t \\n']+|^)" + old_name + "([\t \\n'\\)]+|$)", "\\1" + new_name + "\\2", sql)
                    node.sql = sql
                    node.updated_at = updated_at
                    pipe.updated_at = updated_at
                    if edited_by:
                        pipe.edited_by = edited_by
                self.pipes[idx] = pipe.to_dict()

    def get_dependencies(
        self, recursive: bool = False, pipe: Optional[Pipe] = None, datasource_name: Optional[str] = None
    ) -> Dict[str, List[str]]:
        datasources = [ds.to_json() for ds in self.get_datasources()]
        ds_ids = {ds["id"]: ds["name"] for ds in datasources}
        pipes = [pipe.to_json() for pipe in self.get_pipes()]
        node_names = {
            node.name: {**node.to_json(), **{"pipe": pipe.name}}
            for pipe in self.get_pipes()
            for node in pipe.pipeline.nodes
        }

        ds: Dict[str, Set[str]] = defaultdict(set)
        if pipe:
            pipes = [x for x in pipes if pipe == x["name"]]
        if datasource_name:
            datasources = [x for x in datasources if datasource_name == x["name"]]

        def direct_dependencies(ds: Dict[str, Set[str]], ws: User):
            pipes = [pipe.to_json() for pipe in ws.get_pipes()]
            if pipe:
                pipes = [x for x in pipes if pipe == x["name"]]
            for p in pipes:
                for node in p["nodes"]:
                    for t in node["dependencies"] + [ds_ids.get(node["materialized"], None)]:
                        if t is None:
                            continue
                        # direct dependency
                        ds[t].add(p["name"])

                        # fill possible dependency in another workspace
                        parts = t.split(".")
                        p_name = f"{ws.name}.{p['name']}" if len(parts) > 1 else p["name"]
                        ds[parts[-1]].add(p_name)

                        # pipes dependencies
                        node = node_names.get(parts[-1], None)
                        if node is None:
                            ds[p["name"]].add(t)
                        if node and node["pipe"] != p["name"]:
                            ds[node["pipe"]].add(p["name"])
            return ds

        direct_dependencies(ds, self)
        for x in datasources:
            if "shared_with" in x:
                for ws_id in x["shared_with"]:
                    ws = User.get_by_id(ws_id)
                    direct_dependencies(ds, ws)

        response = {}
        resources = []
        if datasource_name:
            resources += datasources
        if pipe:
            resources += pipes
        if not datasource_name and not pipe:
            resources = datasources + pipes

        for x in resources:
            response[x["name"]] = [p for p in ds[x["name"]]]

        if recursive:
            deps = set()
            for x in response:
                visited = []
                deps.update(response[x])
                while deps:
                    dep = deps.pop()
                    if dep not in visited and dep != x:
                        visited.append(dep)
                        elems = response.get(dep, None)
                        if elems is None:
                            continue
                        deps.update(elems)
                        response[x].append(dep)
                response[x] = list(set(response[x]))
        return response

    def get_dependent_pipes_for_pipes(self, pipes: Optional[List] = None) -> List[Pipe]:
        if not pipes:
            return []

        new_dependent_pipes = []
        for pipe in pipes:
            try:
                dependencies = pipe.get_dependencies()
                for dependency in dependencies:
                    dependent_pipe = self.get_pipe(dependency)
                    if dependent_pipe and dependent_pipe not in pipes and dependent_pipe not in new_dependent_pipes:
                        new_dependent_pipes.append(dependent_pipe)
            except Exception as e:
                logging.warning(f"Error while checking dependencies on workspace: {e}")
                pass
        pipes.extend(new_dependent_pipes)
        return pipes

    def get_used_pipes_in_query(self, q: str, pipe: Optional[Pipe] = None) -> List[Pipe]:
        try:
            used_resources = sql_get_used_tables(
                q, raising=False, default_database=self.database, table_functions=False
            )
            if not used_resources:
                return []
            resources = used_resources[0]
            pipes = []

            if pipe:
                pipes.append(pipe)

            for resource_name in resources:
                pipe = self.get_pipe(resource_name)
                if pipe not in pipes and pipe:
                    pipes.append(pipe)

            pipes = self.get_dependent_pipes_for_pipes(pipes=pipes)
            return pipes
        except Exception as e:
            logging.warning(f"Error while checking used pipes on workspace: {e}")
            return []

    def alter_datasource_name(
        self,
        ds_name_or_id: str,
        new_name: str,
        edited_by: Optional[str],
        cascade: bool = True,
        dependencies: Optional[List[str]] = None,
    ) -> Datasource:
        try:
            if not Resource.validate_name(new_name):
                raise ValueError(f'Invalid Data Source name "{new_name}". {Resource.name_help(new_name)}')
        except ForbiddenWordException as e:
            raise ValueError(f"{str(e)}")

        datasource = self.get_datasource(ds_name_or_id)
        existing_resource = self.get_resource(new_name)
        if existing_resource and datasource != existing_resource:
            if isinstance(existing_resource, PipeNode):
                pipe_by_node = self.get_pipe_by_node(existing_resource.id)
                if pipe_by_node:
                    raise ResourceAlreadyExists(
                        f'There is already a {existing_resource.resource_name} with name "{new_name}" in Pipe "{pipe_by_node.name}". Data Source names must be globally unique'
                    )
            raise ResourceAlreadyExists(
                f'There is already a {existing_resource.resource_name} with name "{new_name}". Data Source names must be globally unique'
            )

        updated_at = datetime.now()
        if cascade:
            self.update_pipes_datasource_name(
                ds_name_or_id,
                new_name,
                dependencies=dependencies,
                edited_by=f"{edited_by} (from Data Source '{new_name}' update)",
            )

        def search_ds() -> Optional[Dict[str, Any]]:
            return next((x for x in self.datasources if x["name"] == ds_name_or_id or x["id"] == ds_name_or_id), None)

        ds = search_ds()
        if not ds:
            # Let's try extracting the guid
            guid = Resource.extract_guid(ds_name_or_id)
            if guid:
                ds_name_or_id = guid
                ds = search_ds()

        assert isinstance(ds, dict)
        ds["name"] = new_name
        ds["updated_at"] = updated_at
        self.flush()

        result = self.get_datasource(new_name)
        assert isinstance(result, Datasource)
        return result

    def alter_shared_data_source_name(
        self,
        origin_datasource_id: str,
        origin_workspace_name: str,
        origin_datasource_name: str,
        dependencies: Optional[List[str]] = None,
    ) -> Tuple[str, SharedDatasource]:
        ds = self.get_datasource(origin_datasource_id, include_read_only=True)
        if ds is None:
            raise DataSourceNotFound(origin_datasource_name)
        old_name = ds.name

        if not isinstance(ds, SharedDatasource):
            raise DataSourceIsNotASharedOne()

        ds.update_shared_name(origin_workspace_name, origin_datasource_name)

        self.update_pipes_datasource_name(
            old_name,
            f"{origin_workspace_name}.{origin_datasource_name}",
            dependencies=dependencies,
            edited_by=f"Workspace '{origin_workspace_name}' (from Data Source '{origin_workspace_name}.{origin_datasource_name}' update)",
        )
        self.update_datasource(ds)
        return old_name, cast(SharedDatasource, self.get_datasource(ds.name, include_read_only=True))

    def drop_datasource(self, ds_name_or_id) -> Optional[Datasource]:
        data_source_to_remove = self.get_datasource(ds_name_or_id, include_read_only=True)
        if data_source_to_remove:
            idx: int = next((idx for idx, x in enumerate(self.datasources) if x["id"] == data_source_to_remove.id), -1)
            if idx != -1:
                del self.datasources[idx]
            self.flush()
            # Drop scopes from tokens
            for x in self.tokens:
                x.remove_scope_with_resource(data_source_to_remove.id)
            return data_source_to_remove
        return None

    def get_datasource(
        self, ds_name_or_id: Optional[str], include_used_by: bool = False, include_read_only: bool = False
    ) -> Optional[Datasource]:
        ds = Resource.by_name_or_id(self.get_datasources(), ds_name_or_id)
        if ds and not include_read_only and ds.is_read_only:
            return None

        if ds and include_used_by:
            ds.used_by = self.get_datasource_used_by(ds)

        return ds

    def get_datasource_used_by(self, ds: Datasource, pipes: Optional[List[Pipe]] = None) -> List[Pipe]:
        # look for dependencies
        used_by: List[Pipe] = []
        pipes = pipes if isinstance(pipes, list) else self.get_pipes()
        for p in pipes:
            try:
                if ds.name in p.get_dependencies():
                    used_by.append(p)
                elif p.copy_node:
                    node = p.pipeline.get_node(p.copy_node)
                    if node and node.tags.get(PipeNodeTags.COPY_TARGET_DATASOURCE) == ds.id:
                        used_by.append(p)
            except ValueError:
                # error parsing SQL
                pass
        return used_by

    def get_pipes(self) -> List[Pipe]:
        return self._pipes

    def get_releases(self) -> List[Release]:
        return self._releases

    def get_secrets(self) -> List[Secret]:
        secrets = self._secrets
        if self.is_branch_or_release_from_branch:
            secrets = self.get_main_workspace()._secrets
        return secrets

    def get_tags(self) -> List[ResourceTag]:
        tags = self.tags
        if self.is_branch_or_release_from_branch:
            tags = self.get_main_workspace().tags
        return list(map(ResourceTag.from_dict, tags))

    def get_tags_by_resource(self, resource_id: str, resource_name: str) -> List[ResourceTag]:
        return [
            tag
            for tag in self.get_tags()
            if any(resource["name"] == resource_name or resource["id"] == resource_id for resource in tag.resources)
        ]

    def get_tag_names_by_resource(self, resource_id: str, resource_name: str) -> List[str]:
        try:
            return [tag.name for tag in self.get_tags_by_resource(resource_id, resource_name)]
        except Exception:
            logging.warning(f"Error while getting tags from resource with ID {resource_id} and name {resource_name}")
            return []

    def get_explorations(self, semver: Optional[str]) -> Tuple[Exploration, ...]:
        def get(id: str) -> Exploration:
            result = Explorations.get_by_id(id)
            result.workspace_id = self.id  # Old explorations didn't track parent workspace
            return result

        versions_to_check = []
        if self.is_release:
            versions_to_check = [semver]
        else:
            versions_to_check = [None, self.release_semver()]

        explorations_by_workspace = map(get, self.explorations_ids)
        return tuple([expl for expl in explorations_by_workspace if expl.semver in versions_to_check])

    def get_pipe(self, pipe_name_or_id: str) -> Optional[Pipe]:
        return Resource.by_name_or_id(self.get_pipes(), pipe_name_or_id)

    def get_pipe_by_node(self, node_name_or_uid: str) -> Optional[Pipe]:
        if not node_name_or_uid:
            return None

        guid = Resource.extract_guid(node_name_or_uid)
        if guid:
            node_name_or_uid = guid

        pipes = self.get_pipes()
        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                if node.name == node_name_or_uid or node.id == node_name_or_uid:
                    return pipe
        return None

    def append_node_to_pipe(self, pipe_id: str, node: PipeNode, edited_by: Optional[str]) -> None:
        pipe = self.get_pipe(pipe_id)
        if pipe is None:
            raise PipeNotFound()
        pipe.append_node(node, edited_by=edited_by)
        self.update_pipe(pipe)

    def get_node(self, node_name_or_uid) -> Optional[PipeNode]:
        if not node_name_or_uid:
            return None

        guid = Resource.extract_guid(node_name_or_uid)
        if guid:
            node_name_or_uid = guid

        pipes = self.get_pipes()
        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                if node.name == node_name_or_uid or node.id == node_name_or_uid:
                    return node
        return None

    def update_node(self, pipe_id: str, node: PipeNode, edited_by: Optional[str] = None) -> bool:
        pipe = self.get_pipe(pipe_id)
        if pipe is None:
            raise PipeNotFound()

        for index, pipe_node in enumerate(pipe.pipeline.nodes):
            if pipe_node.id == node.id:
                pipe.pipeline.nodes[index] = node

        if edited_by:
            pipe.edited_by = edited_by

        pipe.updated_at = datetime.now()

        return self.update_pipe(pipe)

    def get_node_by_materialized(
        self, mv_uid: str, pipe_id: Optional[str] = None, i_know_what_im_doing: Optional[bool] = False
    ) -> Optional[PipeNode]:
        if not mv_uid:
            return None

        if pipe_id is None and not i_know_what_im_doing:
            raise ValueError(
                "If there's more than one node materializing to the same mv_uid, which is supported, this method might return wrong results if pipe_id is not passed. If you know what you are doing use `i_know_what_im_doing=True` to suppress this error."
            )

        guid = Resource.extract_guid(mv_uid)
        if guid:
            mv_uid = guid

        pipes = []
        if pipe_id:
            pipe = self.get_pipe(pipe_id)
            if not pipe:
                raise PipeNotFound()
            pipes = [pipe]
        else:
            pipes = self.get_pipes()

        for pipe in pipes:
            for node in pipe.pipeline.nodes:
                if node.materialized == mv_uid:
                    return node
        return None

    def add_pipe(
        self,
        name: str,
        sql: Optional[str] = None,
        nodes: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        fixed_id: Optional[str] = None,
        edited_by: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> Pipe:
        existing_resource = self.get_resource(name)
        if existing_resource:
            raise ResourceAlreadyExists(
                f'There is already a {existing_resource.resource_name} with name "{name}". Pipe names must be globally unique'
            )

        if isinstance(nodes, list):
            pass
        elif sql:
            nodes = [{"sql": sql}]
        else:
            raise ValueError("Either sql or nodes parameters must be set for adding a new Pipe")

        for i, node_item in enumerate(nodes):
            node_item["name"] = node_item.get("name", f"{name}_{i}")

        pipe = Pipe(name, nodes, description=description, guid=fixed_id, edited_by=edited_by, workspace_id=self.id)

        for i, node in enumerate(pipe.pipeline.nodes):
            existing_resource = self.get_resource(node.name)
            if existing_resource and not isinstance(existing_resource, PipeNode):
                raise ValueError(
                    f'Error with node at position {i}, there is already a {existing_resource.resource} with name "{node.name}". Pipe names must be globally unique'
                )

        self.pipes.append(pipe.to_dict())
        self.flush()

        return pipe

    def update_pipe(self, pipe: Pipe, update_last_commit_status: bool = True) -> bool:
        idx = next((idx for idx, x in enumerate(self.pipes) if x["id"] == pipe.id or x["name"] == pipe.name), None)
        if idx is None:
            return False

        self.pipes[idx] = pipe.to_dict(update_last_commit_status=update_last_commit_status)

        self.flush()
        return True

    def alter_pipe(
        self,
        pipe_name_or_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent=None,
        edited_by: Optional[str] = None,
    ) -> Optional[Pipe]:
        if name is not None:
            try:
                if not Resource.validate_name(name):
                    raise ValueError(f'Invalid Pipe name "{name}". {Resource.name_help(name)}')
            except ForbiddenWordException as e:
                raise ValueError(f"{str(e)}")

            pipe = self.get_pipe(pipe_name_or_id)
            existing_resource = self.get_resource(name)
            if existing_resource and pipe != existing_resource:
                if isinstance(existing_resource, PipeNode):
                    pipe_by_node = self.get_pipe_by_node(existing_resource.id)
                    if pipe_by_node:
                        if pipe_by_node.id == pipe_name_or_id or pipe_by_node.name == pipe_name_or_id:
                            raise ResourceAlreadyExists(
                                f'There is already a {existing_resource.resource_name} in this Pipe with name "{name}". Pipe names must be globally unique'
                            )
                        else:
                            raise ResourceAlreadyExists(
                                f'There is already a {existing_resource.resource_name} in Pipe "{pipe_by_node.name}" with name "{name}". Pipe names must be globally unique'
                            )

                raise ResourceAlreadyExists(
                    f'There is already a {existing_resource.resource_name} with name "{name}". Pipe names must be globally unique'
                )

        def search_pipe() -> Optional[Dict[str, Any]]:
            return next((x for x in self.pipes if x["name"] == pipe_name_or_id or x["id"] == pipe_name_or_id), None)

        pp = search_pipe()
        if not pp:
            guid = Resource.extract_guid(pipe_name_or_id)
            if guid:
                pipe_name_or_id = guid
                pp = search_pipe()

        assert isinstance(pp, dict)

        new_name = pipe_name_or_id
        if name is not None:
            new_name = name
            pp["name"] = name
        if description is not None:
            pp["description"] = description
        if parent is not None:
            pp["parent"] = parent
        pp["updated_at"] = datetime.now()
        if edited_by is not None:
            pp["edited_by"] = edited_by
        self.flush()
        return self.get_pipe(new_name)

    def copy_pipeline(self, original_pipe_name: str, pipe_to_swap_name: str) -> Pipe:
        pipe_to_swap = self.get_pipe(pipe_to_swap_name)
        original_pipe = self.get_pipe(original_pipe_name)
        if not original_pipe or not pipe_to_swap:
            raise PipeNotFound()

        original_pipe.copy_from_pipe(pipe_to_swap)
        self.update_pipe(original_pipe)
        self.update_pipe(pipe_to_swap)
        return original_pipe

    def drop_pipe(self, pipe_name: str) -> bool:
        t = self.get_pipe(pipe_name)
        if not t:
            return False

        idx = next((idx for idx, x in enumerate(self.pipes) if x["id"] == t.id), None)
        if idx is None:
            return True

        del self.pipes[idx]
        self.flush()
        # Drop scope from tokens
        for x in self.tokens:
            x.remove_scope_with_resource(t.id)
        return True

    def set_node_of_pipe_as_endpoint(
        self, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type == PipeTypes.COPY:
            raise PipeIsCopy(f"Pipe {pipe_name_or_id} cannot be an endpoint because it is already set as copy.")

        IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS, "", self.feature_flags
        )

        if IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE:
            if pipe.pipe_type == PipeTypes.MATERIALIZED:
                raise PipeIsMaterialized(
                    f"Pipe {pipe_name_or_id} cannot be an endpoint because it already has a materialized view."
                )
            if pipe.pipe_type != PipeTypes.DEFAULT:
                raise PipeIsNotDefault(
                    f"Pipe {pipe_name_or_id} cannot be an endpoint because it is already set as {pipe.pipe_type}"
                )

        if node_id is None or node_id == "":
            pipe.endpoint = None

        else:
            node = pipe.pipeline.get_node(node_id)
            if node is None:
                raise NodeNotFound()
            pipe.endpoint = node_id
            if node.node_type != PipeNodeTypes.ENDPOINT:
                pipe.update_node(node.id, node_type=PipeNodeTypes.ENDPOINT)
        if edited_by:
            pipe.edited_by = edited_by
        self.update_pipe(pipe)

    def set_node_of_pipe_as_datasink(
        self,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type == PipeTypes.DATA_SINK:
            raise PipeIsDataSink(
                f"Pipe {pipe_name_or_id} cannot be set to sink because it already is set as sink, kindly update the pipe instead"
            )

        if pipe.pipe_type != PipeTypes.DEFAULT:
            raise PipeIsNotDefault(
                f"Pipe {pipe_name_or_id} cannot be set to sink because it already is set as {pipe.pipe_type}"
            )

        node = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        pipe.sink_node = node.id

        if node.node_type != PipeNodeTypes.DATA_SINK:
            pipe.update_node(node.id, node_type=PipeNodeTypes.DATA_SINK)
        if edited_by:
            pipe.edited_by = edited_by
        # todo add tags
        self.update_pipe(pipe)

    def set_node_of_pipe_as_stream(
        self,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type == PipeTypes.STREAM:
            raise PipeIsStream(
                f"Pipe {pipe_name_or_id} cannot be set to stream because it already is set as stream, kindly update the pipe instead"
            )

        if pipe.pipe_type != PipeTypes.DEFAULT:
            raise PipeIsNotDefault(
                f"Pipe {pipe_name_or_id} cannot be set to stream because it already is set as {pipe.pipe_type}"
            )

        node = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        pipe.stream_node = node.id

        if node.node_type != PipeNodeTypes.STREAM:
            pipe.update_node(node.id, node_type=PipeNodeTypes.STREAM)
        if edited_by:
            pipe.edited_by = edited_by
        self.update_pipe(pipe)

    def set_node_of_pipe_as_copy(
        self,
        pipe_name_or_id: str,
        node_name_or_id: str,
        target_datasource_id: str,
        target_workspace_id: str,
        mode: Optional[str],
        edited_by: Optional[str],
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type == PipeTypes.COPY:
            raise PipeIsCopy(
                f"Pipe {pipe_name_or_id} cannot be set to copy because it already is set as copy, kindly update the pipe instead"
            )

        if pipe.pipe_type != PipeTypes.DEFAULT:
            raise PipeIsNotDefault(
                f"Pipe {pipe_name_or_id} cannot be set to copy because it already is set as {pipe.pipe_type}"
            )

        node = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        pipe.copy_node = node.id
        if node.node_type != PipeNodeTypes.COPY:
            pipe.update_node(
                node.id, node_type=PipeNodeTypes.COPY, mode=mode if mode and mode != node.mode else node.mode
            )

        pipe.set_node_tag(
            node_name_or_id, PipeNodeTags.COPY_TARGET_DATASOURCE, value=target_datasource_id, edited_by=edited_by
        )
        pipe.set_node_tag(
            node_name_or_id, PipeNodeTags.COPY_TARGET_WORKSPACE, value=target_workspace_id, edited_by=edited_by
        )
        self.update_pipe(pipe)

    def update_copy_pipe_target(
        self,
        pipe_name_or_id: str,
        target_datasource_id: str,
        target_workspace_id: str,
        edited_by: Optional[str],
        mode: Optional[str] = None,
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type != PipeTypes.COPY:
            raise PipeIsNotCopy(f"Pipe {pipe_name_or_id} cannot be updated as copy because it is not set as copy")

        node = pipe.pipeline.get_node(pipe.copy_node)
        if node is None:
            raise NodeNotFound()

        if mode:
            pipe.set_node_mode(node.id, mode=mode, edited_by=edited_by)

        pipe.set_node_tag(node.id, PipeNodeTags.COPY_TARGET_DATASOURCE, value=target_datasource_id, edited_by=edited_by)
        pipe.set_node_tag(node.id, PipeNodeTags.COPY_TARGET_WORKSPACE, value=target_workspace_id, edited_by=edited_by)

        self.update_pipe(pipe)

    def drop_copy_of_pipe_node(
        self, pipe_name_or_id: str, node_name_or_id: Optional[str], edited_by: Optional[str]
    ) -> None:
        pipe: Optional[Pipe] = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type != PipeTypes.COPY:
            raise CopyNodeNotFound()

        node: Optional[PipeNode] = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        if pipe.copy_node != node.id:
            raise CopyNodeNotFound()

        if node.node_type == PipeNodeTypes.COPY:
            pipe.update_node(node.id, node_type=PipeNodeTypes.STANDARD)

        pipe.copy_node = None
        pipe.set_node_mode(node.id, mode=None, edited_by=edited_by)
        pipe.drop_node_tag(node.id, PipeNodeTags.COPY_TARGET_DATASOURCE, edited_by)
        pipe.drop_node_tag(node.id, PipeNodeTags.COPY_TARGET_WORKSPACE, edited_by)

        self.update_pipe(pipe)

    async def drop_sink_of_pipe_node(
        self, pipe_name_or_id: str, node_name_or_id: Optional[str], edited_by: Optional[str]
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type != PipeTypes.DATA_SINK:
            raise SinkNodeNotFound()

        node = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        if pipe.sink_node != node.id:
            raise SinkNodeNotFound()

        if node.node_type == PipeNodeTypes.DATA_SINK:
            pipe.update_node(node.id, node_type=PipeNodeTypes.STANDARD, edited_by=edited_by)

        pipe.sink_node = None
        pipe.set_node_mode(node.id, mode=None, edited_by=edited_by)

        self.update_pipe(pipe)

        # Remove associated scheduled sink
        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, self.id)
            await data_sink.delete()
        except Exception as e:
            logging.warning(f"Sink Pipe does not have linked Data Sink: {pipe.id}, error: {e}")

    async def drop_stream_of_pipe_node(
        self, pipe_name_or_id: str, node_name_or_id: Optional[str], edited_by: Optional[str]
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type != PipeTypes.STREAM:
            raise StreamNodeNotFound()

        node = pipe.pipeline.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()

        if pipe.stream_node != node.id:
            raise StreamNodeNotFound()

        if node.node_type == PipeNodeTypes.STREAM:
            pipe.update_node(node.id, node_type=PipeNodeTypes.STANDARD, edited_by=edited_by)

        pipe.stream_node = None
        pipe.set_node_mode(node.id, mode=None, edited_by=edited_by)

        self.update_pipe(pipe)

        # Remove associated sink
        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, self.id)
            await data_sink.delete()
        except Exception as e:
            logging.warning(f"Stream Pipe does not have linked Data Sink: {pipe.id}, error: {e}")

    def drop_endpoint_of_pipe_node(
        self, pipe_name_or_id: str, node_id: Optional[str], edited_by: Optional[str]
    ) -> None:
        pipe = self.get_pipe(pipe_name_or_id)

        if not pipe:
            raise PipeNotFound()

        if pipe.pipe_type != PipeTypes.ENDPOINT:
            raise EndpointNotFound()

        node = pipe.pipeline.get_node(node_id)
        if node is None:
            raise NodeNotFound()

        endpoint_node = pipe.pipeline.get_node(pipe.endpoint)
        if not endpoint_node or endpoint_node.id != node.id:
            raise EndpointNotFound()

        pipe.endpoint = None
        if node.node_type == PipeNodeTypes.ENDPOINT:
            pipe.update_node(node.id, node_type=PipeNodeTypes.STANDARD)

        if edited_by:
            pipe.edited_by = edited_by
        self.update_pipe(pipe)

    def set_dependent_datasource_tag(
        self, source_datasource_id: str, target_datasource_id: str, workspace_id: str, engine: str
    ) -> None:
        source_datasource = self.get_datasource(source_datasource_id)
        if not source_datasource:
            raise DataSourceNotFound(source_datasource_id)

        dependent_datasources = source_datasource.tags.get("dependent_datasources", {})
        dependent_datasources.update({target_datasource_id: {"engine": engine, "workspace": workspace_id}})
        source_datasource.tags.update({"dependent_datasources": dependent_datasources})
        self.update_datasource(source_datasource)

    def update_dependent_datasource_tag(self, source_datasource_id: str, target_datasource_id: str) -> None:
        """
        Deletes a dependent datasource tag successfully

        >>> u = UserAccount.register('update_dependent_datasource_tag@example.com', 'pass')
        >>> w = User.register('update_dependent_datasource_tag', admin=u.id)
        >>> source_ds = Users.add_datasource_sync(w, 'source_ds')
        >>> dependent_ds = Users.add_datasource_sync(w, 'dependent_ds')
        >>> dependent_dependent = Users.add_datasource_sync(w, 'dependent_dependent')
        >>> Users.set_dependent_datasource_tag(w, source_ds.id, dependent_ds.id, w.id, 'MergeTree')
        >>> w = Users.get_by_name('update_dependent_datasource_tag')
        >>> source_ds = w.get_datasource('source_ds')
        >>> dependent = source_ds.tags.get('dependent_datasources').get(dependent_ds.id)
        >>> dependent.get('engine')
        'MergeTree'
        >>> Users.update_dependent_datasource_tag(w, source_ds.id, 'non_existing_id')
        >>> w = Users.get_by_name('update_dependent_datasource_tag')
        >>> source_ds = w.get_datasource('source_ds')
        >>> dependent = source_ds.tags.get('dependent_datasources').get(dependent_ds.id)
        >>> dependent.get('engine')
        'MergeTree'
        >>> Users.update_dependent_datasource_tag(w, source_ds.id, dependent_ds.id)
        >>> w = Users.get_by_name('update_dependent_datasource_tag')
        >>> source_ds = w.get_datasource('source_ds')
        >>> source_ds.tags
        {'dependent_datasources': {}}
        """

        source_datasource = self.get_datasource(source_datasource_id)
        if not source_datasource:
            raise DataSourceNotFound(source_datasource_id)

        dependent_datasources = source_datasource.tags.get("dependent_datasources", {})
        if target_datasource_id in dependent_datasources:
            del dependent_datasources[target_datasource_id]
            source_datasource.tags.update({"dependent_datasources": dependent_datasources})

        self.update_datasource(source_datasource)

    def set_source_copy_pipes_tag(self, target_datasource_id: str, source_pipe_id: str) -> User:
        target_datasource = self.get_datasource(target_datasource_id)
        if not target_datasource:
            raise DataSourceNotFound(target_datasource_id)

        source_copy_pipes = target_datasource.tags.get("source_copy_pipes", {})
        source_copy_pipes.update({source_pipe_id: {"workspace": self.id}})
        target_datasource.tags.update({"source_copy_pipes": source_copy_pipes})
        self.update_datasource(target_datasource)
        return self

    def get_source_copy_pipes(self, target_datasource_id: str) -> List[Dict[str, Any]]:
        target_datasource = self.get_datasource(target_datasource_id)
        assert isinstance(target_datasource, Datasource)
        source_copy_pipes = target_datasource.tags.get("source_copy_pipes", {})
        pipes = [
            {"id": pipe_id, "workspace": pipe_info.get("workspace")} for pipe_id, pipe_info in source_copy_pipes.items()
        ]
        return pipes

    def remove_source_copy_pipes_tag(self, target_datasource_id: str, source_pipe_id: str) -> User:
        target_datasource = self.get_datasource(target_datasource_id)
        if not target_datasource:
            raise DataSourceNotFound(target_datasource_id)

        source_copy_pipes = target_datasource.tags.get("source_copy_pipes", {})
        if source_pipe_id in source_copy_pipes:
            del source_copy_pipes[source_pipe_id]
            target_datasource.tags.update({"source_copy_pipes": source_copy_pipes})

        self.update_datasource(target_datasource)
        return self

    def drop_node_from_pipe(self, pipe_name_or_id: str, node_name_or_id: str, edited_by: Optional[str]) -> PipeNode:
        pipe = self.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound()

        node = pipe.pipeline.get_node(node_name_or_id)
        if not node:
            raise NodeNotFound()

        pipe.drop_node(node_name_or_id, edited_by)
        self.update_pipe(pipe)
        return node

    def get_tokens(self) -> List[AccessToken]:
        return self.tokens

    def get_token_for_exploration(self, exploration_id: str) -> Optional[AccessToken]:
        return next(
            (
                t
                for t in self.get_tokens()
                if t.origin.origin_code == Origins.TIMESERIES and t.origin.resource_id == exploration_id
            ),
            None,
        )

    def get_safe_user_tokens(self, user_id: str) -> List[AccessToken]:
        """
        Get all workspace tokens that the user can access, obfuscating those tokens which
        the user should not view directly (ADMIN_USER). For guest and viewer users, ADMIN and
        ADMIN_USER tokens of other users are not included. VIEWER users get all tokens obfuscated
        except their ADMIN_USER one.

        >>> admin = UserAccount.register('test_get_safe_user_tokens@example.com', 'pass')
        >>> guest = UserAccount.register('guest_user@example.com', 'pass')
        >>> w = User.register('test_get_safe_user_tokens', admin=admin.id)
        >>> w = asyncio.run(Users.add_users_to_workspace_async(w.id, ['guest_user@example.com'], role='guest'))
        >>> w.tokens
        [token: admin token, token: admin test_get_safe_user_tokens@example.com, token: create datasource token, token: admin guest_user@example.com]
        >>> w.get_safe_user_tokens(admin.id)
        [token: admin token, token: admin test_get_safe_user_tokens@example.com, token: create datasource token, token: admin guest_user@example.com]
        >>> w.get_safe_user_tokens('user_id_without_admin_rights')
        []
        >>> w.get_safe_user_tokens(guest.id)
        [token: create datasource token, token: admin guest_user@example.com]
        >>> [t for t in w.get_safe_user_tokens(guest.id) if not t.is_obfuscated()]
        [token: create datasource token, token: admin guest_user@example.com]
        >>> viewer = UserAccount.register('viewer_user@example.com', 'pass')
        >>> w = asyncio.run(Users.add_users_to_workspace_async(w.id, ['viewer_user@example.com'], role='viewer'))
        >>> w.tokens
        [token: admin token, token: admin test_get_safe_user_tokens@example.com, token: create datasource token, token: admin guest_user@example.com, token: viewer viewer_user@example.com]
        >>> w.get_safe_user_tokens(viewer.id)
        [token: create datasource token, token: viewer viewer_user@example.com]
        """

        if not UserWorkspaceRelationship.user_has_access(user_id, self.id):
            if not self.origin:
                return []
            else:
                if not UserWorkspaceRelationship.user_has_access(user_id, self.origin):
                    return []

        user_is_workspace_viewer = UserWorkspaceRelationship.user_is_viewer(user_id, self.id) or (
            self.origin and UserWorkspaceRelationship.user_is_viewer(user_id, self.origin)
        )

        user_is_workspace_admin = UserWorkspaceRelationship.user_is_admin(user_id, self.id) or (
            self.origin and UserWorkspaceRelationship.user_is_admin(user_id, self.origin)
        )

        safe_tokens = []

        for t in self.tokens:
            # 1) The user is a workspace *guest* or *viewer* --> we won't even list other ADMIN tokens
            #    (workspace and user)
            if not user_is_workspace_admin:
                if (
                    t.has_scope(scopes.ADMIN)
                    or t.has_scope(scopes.TOKENS)
                    or (t.has_scope(scopes.ADMIN_USER) and user_id not in t.get_resources_for_scope(scopes.ADMIN_USER))
                ):
                    continue
                # Obfuscate all tokens for viewers, except their ADMIN_USER one
                if user_is_workspace_viewer and not t.has_scope(scopes.ADMIN_USER):
                    t = copy.deepcopy(t)
                    t.obfuscate()

                safe_tokens.append(t)

            # 2) The user is a workspace *admin* --> he can view all tokens (except other users' ADMIN_USER)
            else:
                if t.has_scope(scopes.ADMIN_USER) and user_id not in t.get_resources_for_scope(scopes.ADMIN_USER):
                    t = copy.deepcopy(t)
                    t.obfuscate()
                safe_tokens.append(t)

        return safe_tokens

    def get_safe_tokens_for_token_admin(self, token: AccessToken) -> List[AccessToken]:
        """
        Get all workspace tokens that a token admin (ADMIN, TOKEN) can access
        """

        safe_tokens = []

        can_view_admin = not token.has_scope(scopes.TOKENS)

        for t in self.tokens:
            if t.has_scope(scopes.ADMIN_USER) or (not can_view_admin and t.has_scope(scopes.ADMIN)):
                t = copy.deepcopy(t)
                t.obfuscate()
            safe_tokens.append(t)

        return safe_tokens

    def get_token(self, name: str) -> Optional[AccessToken]:
        return next((x for x in self.tokens if x.name == name), None)

    def get_secret(self, name: str) -> Optional[Secret]:
        return next((x for x in self.get_secrets() if x.name == name), None)

    def get_secrets_for_template(self) -> List[str]:
        return [f"{secret_template_key(secret.name)}" for secret in self.get_secrets()]

    def get_secrets_ch_params_by(self, keys: Set[str]) -> Dict[str, str]:
        if not keys:
            return {}

        return {
            f"{CH_PARAM_PREFIX}{secret.name}": secret_decrypt(User.secrets_key, secret.value)
            for secret in self.get_secrets()
            if secret.name in keys
        }

    def get_tag(self, name_or_id: str) -> Optional[ResourceTag]:
        return next((x for x in self.get_tags() if x.name == name_or_id or x.id == name_or_id), None)

    def get_token_access_info(
        self, token_name_or_id: str, tokens: Optional[List[AccessToken]] = None
    ) -> Optional[AccessToken]:
        tokens = tokens or self.tokens
        for t in tokens:
            if t.token == token_name_or_id or t.name == token_name_or_id or t.id == token_name_or_id:
                return t
        return None

    def get_token_for_scope(self, scope: str, resource_id: Optional[str] = None) -> Optional[str]:
        for t in self.tokens:
            if t.has_scope(scope):
                if resource_id and resource_id not in t.get_resources_for_scope(scope):
                    continue
                return t.token
        return None

    def get_access_token_for_scope(self, scope: str, resource_id: Optional[str] = None) -> Optional[AccessToken]:
        for t in self.tokens:
            if t.has_scope(scope):
                if resource_id and resource_id not in t.get_resources_for_scope(scope):
                    continue
                return t
        return None

    def get_tokens_for_resource(self, resource: str, scope: str) -> List[str]:
        return [t.token for t in self.tokens if resource in t.get_resources_for_scope(scope)]

    def get_access_tokens_for_resource(self, resource: str, scope) -> List[AccessToken]:
        return [t for t in self.tokens if resource in t.get_resources_for_scope(scope)]

    def get_token_for_origin(self, origin_code: str, resource_id: str) -> Optional[str]:
        for t in self.tokens:
            if t.origin.origin_code == origin_code and t.origin.resource_id == resource_id:
                return t.token
        return None

    def get_unique_token_for_resource(self, resource, scope):
        """
        >>> u = UserAccount.register('test_unique_token_resource@example.com', 'pass')
        >>> w = User.register('test_unique_token_resource', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> pipe_1 = Users.add_pipe_sync(w, 'test_pipe_1', 'select 1')
        >>> t1 = Users.add_token(w, 'test_token_1', scopes.PIPES_READ, pipe_1.id)
        >>> w = User.get_by_id(w.id)
        >>> token = w.get_unique_token_for_resource(pipe_1.id, scopes.PIPES_READ)
        >>> t1 == token
        True
        >>> pipe_2 = Users.add_pipe_sync(w, 'test_pipe_2', 'select 1')
        >>> _ = Users.add_scope_to_token(w, t1, scopes.PIPES_READ, pipe_2.id)
        >>> w = User.get_by_id(w.id)
        >>> token = w.get_unique_token_for_resource(pipe_1, scopes.PIPES_READ)
        >>> not token
        True
        """

        for t in self.tokens:
            resources = t.get_resources_for_scope(scope)
            if resources and len(resources) == 1 and resource in resources:
                return t.token

        return None

    def get_workspace_access_token(self, user_id):
        workspace_token = self.get_unique_token_for_resource(user_id, scopes.ADMIN_USER)

        if not workspace_token:
            with User.transaction(self.id) as workspace:
                workspace_token = workspace.create_workspace_access_token(user_id)

        return workspace_token

    def create_workspace_access_token(self, user_id):
        token = self.get_unique_token_for_resource(user_id, scopes.ADMIN_USER)

        if token:
            return token

        user = UserAccounts.get_by_id(user_id)
        token_name = f"admin {user.email}"

        if self.get_token(token_name):
            token_name = self.next_valid_token_name(token_name)

        self.add_token(token_name, scopes.ADMIN_USER, user_id)
        return self.get_unique_token_for_resource(user_id, scopes.ADMIN_USER)

    def add_data_source_connector_token(self, datasource, connector_name):
        """
        >>> from tinybird.user import Users, UserAccount
        >>> from tinybird.tokens import scopes
        >>> u = UserAccount.register('test_unique_token_add_dl@example.com', 'pass')
        >>> w = User.register('test_unique_token_add_dl', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> ds1 = Users.add_datasource_sync(w, 'ds1')
        >>> w = User.get_by_id(w.id)
        >>> token = w.add_data_source_connector_token(ds1, "wadus")
        >>> w.add_data_source_connector_token(ds1, "wadus") == token
        True
        >>> ds2 = Users.add_datasource_sync(w, 'ds2')
        >>> unique_token = Users.add_token(w, 'wadus_ds2', scopes.DATASOURCES_CREATE, ds2.id)
        >>> w = User.get_by_id(w.id)
        >>> token = w.add_data_source_connector_token(ds2, "wadus")
        >>> token == unique_token
        True
        >>> ds = Users.drop_datasource(w, 'ds2')
        >>> ds is not None
        True
        >>> ds2 = Users.add_datasource_sync(w, 'ds2')
        >>> w = User.get_by_id(w.id)
        >>> token = w.add_data_source_connector_token(ds2, "wadus")
        >>> token_info = Users.get_token_access_info(w, token)
        >>> token_info.name
        'wadus_ds2 1'
        """

        token = self.get_unique_token_for_resource(datasource.id, scopes.DATASOURCES_CREATE)

        if token:
            return token

        token_name = get_token_name(connector_name, datasource.name)

        if self.get_token(token_name):
            token_name = self.next_valid_token_name(token_name)

        return self.add_token(token_name, scopes.DATASOURCES_CREATE, datasource.id)

    def get_resource_id(self, resource_name_or_uid: str) -> Optional[str]:
        resource = self.get_resource(resource_name_or_uid)
        if resource:
            return resource.id

        # Check if it's a service DS
        return next(
            (f"{r.namespace}.{r.name}" for r in REPLACEMENTS if resource_name_or_uid == f"{r.namespace}.{r.name}"), None
        )

    def get_resource_id_for_scope(self, scope: str, resource_name_or_uid: str):
        pipe = self.get_pipe(resource_name_or_uid)
        if pipe:
            return pipe.id

        ds = self.get_datasource(resource_name_or_uid, include_read_only=True)
        if not ds:
            # Check if is a service DS
            service_ds = next(
                (f"{r.namespace}.{r.name}" for r in REPLACEMENTS if resource_name_or_uid == f"{r.namespace}.{r.name}"),
                None,
            )
            if not service_ds:
                raise CreateTokenError("datasource or pipe %s does not exist" % resource_name_or_uid)

            # Service DS are read-only
            if scope != scopes.DATASOURCES_READ:
                raise CreateTokenError(
                    f'Data source "{resource_name_or_uid}" is a Service Data Source. As it\'s read-only, it only supports READ scope tokens.'
                )

            return service_ds

        if isinstance(ds, SharedDatasource) and scope != scopes.DATASOURCES_READ:
            raise CreateTokenError(
                f'Data source "{resource_name_or_uid}" is a Shared Data Source. As it\'s read-only, it only supports READ scope tokens.'
            )

        return ds.id

    def add_secret(self, name: str, value: str, edited_by: Optional[str]) -> Secret:
        if self.get_secret(name):
            raise CreateSecretError(f'Secret with name "{name}" already exists')

        existing_secrets = len(self.secrets)
        if existing_secrets >= MAX_SECRETS:
            raise CreateSecretError(f"The maximum number of secrets for this workspace is {MAX_SECRETS}.")

        secret = Secret(User.secrets_key, name, value, edited_by=edited_by)
        self.secrets.append(secret.to_dict())
        self.flush()
        return secret

    def add_tag(self, name: str, resources: List[Dict[str, str]]) -> ResourceTag:
        if self.get_tag(name):
            raise CreateTagError(f'Tag with name "{name}" already exists')

        tag = ResourceTag(name, resources)
        self.tags.append(tag.to_dict())
        return tag

    def add_token(
        self,
        name: str,
        scope: Optional[str],
        resource=None,
        origin: Optional[TokenOrigin] = None,
        description: Optional[str] = None,
        host: Optional[str] = None,
    ) -> str:
        if self.get_token(name):
            raise CreateTokenError(f'Token with name "{name}" already exists')

        existing_tokens = len(self.tokens)
        max_tokens = self.get_limits(prefix="workspace").get("max_tokens", Limit.max_tokens)
        if existing_tokens >= max_tokens:
            raise CreateTokenError(f"The maximum number of tokens for this workspace is {int(max_tokens)}.")

        if scope and not scopes.is_valid(scope):
            raise WrongScope(scope)
        ac = AccessToken(self.id, name, User.secret, description=description, origin=origin, host=host)
        if scope:
            ac.add_scope(scope, resource)
        self.tokens.append(ac)
        return ac.token

    def add_scopes_to_token(self, token, scope_details: List[Tuple[str, Optional[str], Optional[str]]]) -> str:
        ac = self.get_token_access_info(token)
        if not ac:
            raise TokenNotFound("token not found")
        for scope_detail in scope_details:
            scope = scope_detail[0]
            resource = scope_detail[1]
            filters = scope_detail[2]
            ac.add_scope(scope, resource, filters)
        return ac.token

    def check_connector_token(self, token: str):
        t = self.get_token_access_info(token)

        if not t:
            return

        token_datasources = t.get_resources_for_scope(scopes.DATASOURCES_CREATE)
        for token_datasource in token_datasources:
            datasource = self.get_datasource(token_datasource)
            if datasource and datasource.datasource_type in DATASOURCE_CONNECTOR_TYPES:
                raise TokenUsedInConnector(
                    f"Forbidden: token {t.name} is being used in {datasource.datasource_type} Data Source '{datasource.name}'"
                )

        linker_tokens = DataConnector.get_all_linker_tokens_by_owner(self.id)
        if t.token in linker_tokens:
            raise TokenUsedInConnector(
                f"Forbidden: token {t.name} is being used in one or more connected Data Sources."
            )

    def drop_token(self, token: str) -> bool:
        self.check_connector_token(token=token)
        for i, t in enumerate(self.tokens):
            if t.token == token or t.id == token or t.name == token:
                del self.tokens[i]
                return True
        return False

    def drop_secret(self, name: str) -> bool:
        for i, t in enumerate(self.secrets):
            if t["name"] == name:
                del self.secrets[i]
                self.flush()
                return True
        return False

    def drop_tag(self, tag: str) -> bool:
        for i, t in enumerate(self.tags):
            if t["name"] == tag or t["id"] == tag:
                del self.tags[i]
                self.flush()
                return True
        return False

    def update_secret(self, name: str, value: str, edited_by: Optional[str]) -> Secret:
        secret = None
        idx = next((idx for idx, x in enumerate(self.secrets) if x["name"] == name), None)
        if idx is not None:
            old_secret = self.secrets[idx]
            secret = Secret(
                User.secrets_key,
                name,
                value,
                created_at=old_secret["created_at"],
                updated_at=datetime.now(),
                edited_by=edited_by,
            )
            self.secrets[idx] = secret.to_dict()
            self.flush()
            return secret
        else:
            raise SecretNotFound("Secret not found")

    def update_tag(
        self, id_or_name: str, name: Optional[str], resources: Optional[List[Dict[str, str]]]
    ) -> ResourceTag:
        tag = None
        idx = next((idx for idx, x in enumerate(self.tags) if x["name"] == id_or_name or x["id"] == id_or_name), None)
        if idx is not None:
            old_tag = self.tags[idx]
            name = name if name is not None else old_tag["name"]
            resources = resources if resources is not None else old_tag["resources"]
            tag = ResourceTag(name, resources, created_at=old_tag["created_at"], updated_at=datetime.now())
            self.tags[idx] = tag.to_dict()
            return tag
        else:
            raise TagNotFound(f"Tag {id_or_name} not found")

    def remove_resource_from_tags(self, resource_id: str, resource_name: str) -> bool:
        for t in self.tags:
            found = next(
                (
                    resource
                    for resource in t["resources"]
                    if resource["name"] == resource_name or resource["id"] == resource_id
                ),
                None,
            )
            if found:
                self.update_tag(
                    t["id"],
                    t["name"],
                    [
                        resource
                        for resource in t["resources"]
                        if resource["name"] != resource_name and resource["id"] != resource_id
                    ],
                )
                return True
        return False

    def next_valid_token_name(self, token_name=""):
        """
        >>> u = UserAccount.register('next_valid_token_name@example.com', 'pass')
        >>> w = User.register('next_valid_token_name', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> t = Users.add_token(w, 'test', None)
        >>> t = Users.add_token(w, 'test 0', None)
        >>> t = Users.add_token(w, 'test 2', None)
        >>> t = Users.add_token(w, 'test 1', None)
        >>> w = User.get_by_id(w.id)
        >>> w.next_valid_token_name('test')
        'test 3'
        >>> w.next_valid_token_name('rambo')
        'rambo 0'
        """

        names = set([x.name for x in self.tokens if x.name.startswith(token_name)])
        pattern = re.compile(rf"{token_name}.*?(\d+)$")
        next_i = sum(token_name in token.name for token in self.tokens)

        for name in sorted(names, reverse=True):
            m = re.match(pattern, name)
            if m and m.groups():
                next_i = int(m.group(1)) + 1
                # we need to still check because sorting tokens does not guarantee they are sorted by
                # the sequential order
                if f"{token_name} {next_i}" not in names:
                    break
        return f"{token_name} {next_i}"

    async def replace_tables_async(self, *args, **kwargs) -> Tuple[str, List[Any]]:
        template_execution_results: TemplateExecutionResults = kwargs.get(
            "template_execution_results", TemplateExecutionResults()
        )

        ff = kwargs.get("finalize_aggregations", None)
        if ff is not None:
            del kwargs["finalize_aggregations"]

        replace_fn = partial(self.try_get_query_and_template_results, *args, **kwargs)
        q, _template_execution_results, used_tables = await IOLoop.current().run_in_executor(
            User.replace_executor, replace_fn
        )

        qq = await ch_finalize_aggregations(self.database_server, self.database, q) if ff else q
        template_execution_results.update_all(_template_execution_results)

        return qq, used_tables

    def replace_tables(self, *args, **kwargs) -> str:
        query, _, _ = self.get_query_and_template_results(*args, **kwargs)
        return query

    def try_get_query_and_template_results(self, *args, **kwargs) -> Tuple[str, Optional[Dict[str, Any]], List[Any]]:
        try:
            split_to_array_escape = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.SPLIT_TO_ARRAY_ESCAPE, "", self.feature_flags
            )
            ff_split_to_array_escape.set(split_to_array_escape)

            preprocess_parameters_circuit_breaker = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.PREPROCESS_PARAMETERS_CIRCUIT_BREAKER, "", self.feature_flags
            )
            ff_preprocess_parameters_circuit_breaker.set(preprocess_parameters_circuit_breaker)

            return self.get_query_and_template_results(*args, **kwargs)
        except CircularDependencyError as e:
            raise ValueError(str(e))

    def tables_to_tuples(self, tables: List[Union[str, Tuple[str, str]]]) -> Set[Tuple[str, str]]:
        """Turns a list of table_name or (database, table_name) into a set of (database, table_name)

        When the database name is not specified, and only the table name is provided, the Workspace's database is used
        """
        tuples = set()
        for t in tables:
            if isinstance(t, tuple):
                tuples.add(t)
            else:
                tuples.add((self.database, t))
        return tuples

    def check_service_datasources_permissons(
        self,
        allow_direct_access_to_service_datasources_replacements: bool,
        allow_use_internal_tables: bool,
        allow_using_org_service_datasources: bool,
        used_tables: list,
        readable_resources_set: Set[str],
        service_datasources_replacements: Dict[Tuple[str, str], Tuple[str, str]],
    ) -> None:
        if (
            not allow_direct_access_to_service_datasources_replacements
            or not allow_use_internal_tables
            or not allow_using_org_service_datasources
        ):
            for used_table in used_tables:
                db_and_table_tup = (used_table[0], used_table[1])
                table_name = f"{used_table[0]}.{used_table[1]}"
                using_org_service_datasources = (
                    used_table[0] == "organization" and table_name not in readable_resources_set
                )
                using_service_datasources = (
                    db_and_table_tup in service_datasources_replacements and table_name not in readable_resources_set
                )
                if using_service_datasources and not allow_direct_access_to_service_datasources_replacements:
                    raise QueryNotAllowedForToken(
                        f"Services Data Sources like '{table_name}' can't be directly accessed without an ADMIN token. If you need to access it with a non ADMIN token you can read it from a Pipe and create a token with just read access to that Pipe"
                    )
                if using_service_datasources and not allow_use_internal_tables:
                    raise ServicesDataSourcesError(f'This query uses Service Data Sources: "{table_name}"')
                if using_org_service_datasources and not allow_using_org_service_datasources:
                    error_message = f'This query uses Organization-level Service Data Sources: "{table_name}". Only Organization admins can access them with their admin tokens from within Workspaces added to the Organization.'
                    raise QueryNotAllowedForToken(error_message)

    def get_query_and_template_results(
        self,
        query: str,
        readable_resources: Optional[List[str]] = None,
        use_service_datasources_replacements: bool = True,
        pipe: Optional[Pipe] = None,
        use_pipe_nodes: bool = False,
        filters: Optional[Dict[str, str]] = None,
        staging_tables: bool = False,
        extra_replacements: Optional[Dict[Tuple[str, str], Tuple[str, str]]] = None,
        variables: Optional[Dict[str, str]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        check_functions: bool = False,
        allow_direct_access_to_service_datasources_replacements: bool = True,
        allow_using_org_service_datasources: bool = False,
        allow_use_internal_tables: bool = True,
        check_endpoint: bool = True,
        playground: Optional[Playground] = None,
        release_replacements: bool = False,
        output_one_line: bool = False,
        function_allow_list: Optional[FrozenSet[str]] = None,
        secrets: Optional[List[str]] = None,
    ) -> Tuple[str, Optional[TemplateExecutionResults], List[Any]]:
        origin_workspace = None
        main_workspace = None

        logging.debug(f"Original query: {query}")
        try:
            origin_workspace = Users.get_by_id(self.origin) if self.origin else None
        except UserDoesNotExist:
            pass
        try:
            if self.is_release:
                main_workspace = self.get_main_workspace()
        except UserDoesNotExist:
            pass

        try:
            all_used_tables = sql_get_used_tables(
                query, raising=True, default_database=self.database, function_allow_list=function_allow_list
            )
        except (InvalidFunction, InvalidResource) as e:
            raise QueryNotAllowed(e.msg) from e
        used_tables: list = []
        disabled_table_functions: list = []
        if function_allow_list is None:
            _enabled_table_functions = ENABLED_TABLE_FUNCTIONS
        else:
            _enabled_table_functions = ENABLED_TABLE_FUNCTIONS.union(function_allow_list)
        for table in all_used_tables:
            database_or_namespace, table_name, table_func = table
            if table_func and table_func not in _enabled_table_functions:
                disabled_table_functions.append(table_func)
            if database_or_namespace or table_name:
                used_tables.append(table)

        if disabled_table_functions:
            logging.info(f"user {self.id} trying to access table functions {disabled_table_functions}")
            msg = f"The query uses disabled table functions: '{','.join(disabled_table_functions)}'"
            raise QueryNotAllowed(msg)

        service_datasources_replacements = Users.get_service_datasources_replacements(
            main_workspace if main_workspace else self,
            include_org_service_datasources=allow_using_org_service_datasources,
        )
        readable_resources_set: Set[str] = set() if readable_resources is None else set(readable_resources)
        self.check_service_datasources_permissons(
            allow_direct_access_to_service_datasources_replacements,
            allow_use_internal_tables,
            allow_using_org_service_datasources,
            used_tables,
            readable_resources_set,
            service_datasources_replacements,
        )

        names: list[str] = [
            name if database == self.database else f"{database}.{name}" for database, name, _ in used_tables
        ]
        user_pipes = self.get_pipes()
        user_datasources = self.get_datasources()
        pipes_used = Resource.by_names_or_ids(user_pipes, names)
        if readable_resources is not None:
            datasources_used = Resource.by_names_or_ids(user_datasources, names)
            for _pipe in pipes_used:
                if _pipe.id not in readable_resources_set:
                    raise QueryNotAllowedForToken(
                        f"Not enough permissions for pipe '{_pipe.name}', token needs PIPES:READ:{_pipe.name} scope to access this pipe. The command to do this is: curl -X PUT https://api.tinybird.co/v0/tokens/token?scope=PIPES:READ:{_pipe.name}"
                    )
            for ds in datasources_used:
                if ds.id not in readable_resources_set:
                    raise QueryNotAllowedForToken(
                        f"Not enough permissions for datasource '{ds.name}', token needs DATASOURCES:READ:{ds.name} scope to access this datasource. The command to do this is: curl -X PUT https://api.tinybird.co/v0/tokens/token?scope=DATASOURCES:READ:{ds.name}"
                    )

        if check_endpoint:
            for _pipe in pipes_used:
                is_materialized = len(_pipe.pipeline.nodes) and _pipe.pipeline.nodes[-1].materialized
                if not _pipe.endpoint and not is_materialized and _pipe != pipe:
                    raise PipeWithoutEndpoint(f"The pipe '{_pipe.name}' does not have an endpoint yet")

        replacements: Dict[str, str] = {}
        pipes_replacements: Dict[str, str] = {}
        if pipe:
            pipes_replacements["_"] = pipe.id
            if use_pipe_nodes:
                pipes_replacements.update(
                    pipe.pipeline.get_replacements(variables, template_execution_results, secrets=secrets)
                )
        if playground:
            pipes_replacements["_"] = playground.id
            if use_pipe_nodes:
                pipes_replacements.update(
                    playground.pipeline.get_replacements(variables, template_execution_results, secrets=secrets)
                )
        for p in user_pipes:
            pipes_replacements.update(p.get_replacements(variables, template_execution_results, secrets=secrets))
        replacements.update(pipes_replacements)
        ds_replacements: Dict[str, str] = {}
        for ds in user_datasources:
            ds_replacements.update(
                ds.get_replacements(
                    staging_table=staging_tables,
                    workspace=self,
                    origin_workspace=origin_workspace,
                    main_workspace=main_workspace,
                    release_replacements=release_replacements,
                )
            )
        replacements.update(ds_replacements)

        if use_service_datasources_replacements:
            replacements.update(service_datasources_replacements)

        # Filters are where clauses tied to a specific token.
        if filters:
            filters_with_replace_format = {}
            for filter in filters:
                filters_with_replace_format[_separate_as_tuple_if_contains_database_and_table(filter)] = filters[filter]
            filters = filters_with_replace_format

            def expand_filter(replacement_key: Any, filter: str) -> str:
                """Expands a filter string using `replacements[replacement_key]` as the table name"""
                # repl contains the table used to expand the filter
                repl = replacements[replacement_key]
                table = repl if isinstance(repl, str) else f"{repl[0]}.{repl[1]}"
                return f"(select * from {table} where {filter})"

            # Let's iterate over all replacements searching por
            # matching filters to be added

            # Work with a copy of the keys.
            # The dict might change size during this process and we don't want to raise a stupid exception
            replacement_keys = tuple(replacements.keys())
            for key in replacement_keys:
                # We use the replacement as a key to find a filter
                repl = replacements[key]

                # Direct match?
                filter = filters.get(repl, "")
                if filter:
                    replacements[key] = expand_filter(key, filter)
                elif not isinstance(repl, str):
                    # Do we have a match only by table name?
                    # (this happens with shared datasources which don't
                    # include the database name)
                    try:
                        filter_key = repl[1]
                    except Exception:
                        continue
                    filter = filters.get(filter_key, "")
                    if filter:
                        # We need to add a fully qualified reference to the table in replacements
                        # using the same matching tuple (db,table) as the key.
                        table_tuple = repl
                        replacements[table_tuple] = expand_filter(key, filter)

        if extra_replacements:
            replacements.update(extra_replacements)
        replacements.update({("system", t): ("system", t) for t in ENABLED_SYSTEM_TABLES})

        valid_tables: Set[Tuple[str, str]] = set(service_datasources_replacements.keys())
        valid_tables |= self.tables_to_tuples(list(ds_replacements.keys()))
        valid_tables |= self.tables_to_tuples(list(ds_replacements.values()))
        valid_tables |= self.tables_to_tuples(list(pipes_replacements.keys()))
        if extra_replacements:
            valid_tables |= self.tables_to_tuples(list(extra_replacements.keys()))

        valid_tables |= {*[("system", table) for table in ENABLED_SYSTEM_TABLES]}

        for database, table_name, _ in used_tables:
            if (database or self.database, table_name) not in valid_tables:
                logging.info(f"user {self.id} trying to access {database}.{table_name}")
                database_resource = "" if database == self.database else f"{database}."
                logging.info(
                    "Resource not found in get_query_and_template_results: %s",
                    {
                        "query": query,
                        "used_tables": used_tables,
                        "valid_tables": valid_tables,
                    },
                )
                raise QueryNotAllowed(f"Resource '{database_resource}{table_name}' not found")

        try:
            q = replace_tables(
                query,
                replacements,
                default_database=self.database,
                check_functions=check_functions,
                valid_tables=valid_tables,
                output_one_line=output_one_line,
                function_allow_list=function_allow_list,
            )
        except (InvalidFunction, InvalidResource) as e:
            raise QueryNotAllowed(e.msg) from e

        # After we have the full query, we can get the tables used
        used_tables = sql_get_used_tables(
            q,
            raising=False,
            default_database=self.database,
            table_functions=False,
            function_allow_list=function_allow_list,
        )

        logging.debug(f"Final query: {q}")

        return q, template_execution_results, used_tables

    def remove_users_from_workspace(self, user_emails: List[str], allow_removing_admins: bool = False) -> List[str]:
        """
        >>> from tinybird.user import Users, UserAccount
        >>> u = UserAccount.register('test_workspace_remove_users@example.com', 'pass')
        >>> w = User.register('test_workspace_remove_users', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> u1 = UserAccount.register('test_user1_rm@example.com', 'pass')
        >>> u1 = UserAccount.get_by_id(u1.id)
        >>> u2 = UserAccount.register('test_user2_rm@example.com', 'pass')
        >>> u2 = UserAccount.get_by_id(u2.id)
        >>> _ = asyncio.run(Users.add_users_to_workspace_async(w.id, ['test_user1_rm@example.com', 'test_user2_rm@example.com']))
        >>> _ = w.remove_users_from_workspace(['test_user1_rm@example.com', 'test_user2_rm@example.com', 'test_workspace_remove_users@example.com'])
        Traceback (most recent call last):
        ...
        tinybird.user.WorkspaceException: Workspace's owner can not be removed from workspace
        >>> _ = w.remove_users_from_workspace(['test_user1_rm@example.com', 'test_user2_rm@example.com'])
        >>> asyncio.run(u1.get_workspaces())
        []
        >>> asyncio.run(u2.get_workspaces())
        []
        >>> w.user_accounts_emails
        ['test_workspace_remove_users@example.com']
        """

        user_emails = list(set(user_emails))
        user_ids = []

        # 1. Get user accounts from emails
        for user_email in user_emails:
            try:
                user = UserAccounts.get_by_email(user_email)
            except UserAccountDoesNotExist:
                pass
            else:
                if user.has_access_to(self.id):
                    user_ids.append(user.id)

        # 2. Remove workspace user tokens
        for user_id in user_ids:
            token = self.get_unique_token_for_resource(user_id, scopes.ADMIN_USER)

            if token:
                try:
                    self.drop_token(token)
                except TokenUsedInConnector as e:
                    logging.exception(
                        f"Could not delete admin token for user {user_id} in workspace {self.name} ({self.id}). {e}"
                    )

        # 3. Remove user workspace relationships
        user_workspaces = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)

        for user_workspace in user_workspaces:
            if user_workspace.user_id in user_ids:
                if user_workspace.relationship == Relationships.ADMIN and not allow_removing_admins:
                    raise WorkspaceException("Workspace's owner can not be removed from workspace")
                UserWorkspaceRelationship._delete(user_workspace.id)

        return user_ids

    def lives_in_the_same_ch_cluster_as(self, another_workspace: "User"):
        return self.cluster == another_workspace.cluster

    def change_pg_password(self, password):
        PGService(self).change_password(password)
        return True

    def find_pipe_in_releases_metadata_by_pipe_node_id(
        self, pipe_node_id: str
    ) -> Tuple[Union[User, ReleaseWorkspace, None], Optional[Pipe]]:
        metadata_workspace: Union[User, ReleaseWorkspace] = self
        pipe = metadata_workspace.get_pipe_by_node(pipe_node_id)
        if pipe:
            return metadata_workspace, pipe

        # If we are processing a branch release, check only the branch, not the main workspace
        if metadata_workspace.is_release and metadata_workspace.origin:
            metadata_workspace = User.get_by_id(metadata_workspace.origin)
            if not metadata_workspace:
                return None, None

        pipe = metadata_workspace.get_pipe_by_node(pipe_node_id)
        if pipe:
            return metadata_workspace, pipe

        # As last option, check the releases of the workspace/branch
        for release in metadata_workspace.get_releases():
            metadata = release.metadata
            assert metadata is not None
            metadata_workspace = metadata
            pipe = metadata_workspace.get_pipe_by_node(pipe_node_id)
            if pipe:
                return metadata_workspace, pipe

        return metadata_workspace, None

    def find_datasource_in_releases_metadata_by_datasource_id(
        self, datasource_id: str
    ) -> Tuple[Union[User, ReleaseWorkspace], Optional[Datasource]]:
        metadata_workspace: Union[User, ReleaseWorkspace] = self
        datasource = metadata_workspace.get_datasource(datasource_id)
        if datasource:
            return metadata_workspace, datasource

        # If we are processing a branch release, do not go the main workspace
        if metadata_workspace.is_branch_or_release_from_branch and metadata_workspace.origin:
            metadata_workspace = User.get_by_id(metadata_workspace.origin)
            if not metadata_workspace:
                return metadata_workspace, None
        else:
            metadata_workspace = metadata_workspace.get_main_workspace()

        metadata_workspace = self.get_main_workspace()
        datasource = metadata_workspace.get_datasource(datasource_id)
        if datasource:
            return metadata_workspace, datasource

        for release in metadata_workspace.get_releases():
            metadata = release.metadata
            assert metadata is not None
            metadata_workspace = metadata
            datasource = metadata_workspace.get_datasource(datasource_id)
            if datasource:
                return metadata_workspace, datasource
        return metadata_workspace, None

    async def delete_release(
        self, release: Release, force: bool = False, dry_run: bool = False
    ) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
        # in order to delete a release in one of these status it needs to be updated first to "deleting"
        if release.is_live:
            raise LiveReleaseProtectedException("Cannot delete a Release in live status")
        try:
            rs = await release.get_resources_to_delete(self.get_releases())
        except Exception as e:
            raise ReleaseStatusException(str(e))

        wmv = release.metadata

        notes: Dict[str, Set[str]] = defaultdict(lambda: set())
        pipes_removed: Dict[str, str] = {}
        ds_removed: Dict[str, str] = {}
        _notes: Dict[str, str] = {}

        async def add_note_if_ds_is_shared(ds_to_check: Datasource) -> None:
            if len(ds_to_check.shared_with) == 0:
                return

            dependent_views = await ch_table_dependent_views_async(self.database_server, self.database, ds_to_check.id)

            if len(dependent_views) == 0:
                return

            relation_of_workspaces_and_pipes: Dict[str, Set[str]] = defaultdict(lambda: set())
            for dependant_view in dependent_views:
                relation_of_workspaces_and_pipes[dependant_view.database].add(dependant_view.table)

            list_of_text_for_ws_and_pipes = []
            for workspace_database in relation_of_workspaces_and_pipes:
                workspace = User.get_by_database(workspace_database)
                workspace_metadata = None
                pipe_names = []
                for pipe_node_id in relation_of_workspaces_and_pipes[workspace_database]:
                    workspace_metadata, pipe = workspace.find_pipe_in_releases_metadata_by_pipe_node_id(pipe_node_id)
                    if not pipe:
                        continue
                    pipe_names.append(f"'{pipe.name}'")

                if workspace_metadata is not None and len(pipe_names) > 0:
                    list_of_text_for_ws_and_pipes.append(
                        f"In Workspace '{workspace_metadata.name}' the pipes: " + ", ".join(pipe_names)
                    )
            final_text_of_ws_and_pipes = ". ".join(list_of_text_for_ws_and_pipes)

            notes[ds_to_check.id].add(
                f"This Data Source is being used in other Workspaces and these Pipes need to be "
                f"updated to use the live version of '{ds_to_check.name}'. {final_text_of_ws_and_pipes}. "
                f"In case of doubt please contact us at support@tinybird.co"
            )

        async def add_note_if_ds_is_still_receiving_data(
            ds_to_check: Optional[Datasource], result: Optional[Dict[str, List[Any]]]
        ) -> None:
            if not ds_to_check or not result:
                return

            for data in result.get("data", []):
                if data["datasource_id"] == ds_to_check.id:
                    if data.get("total", 0) == 0:
                        return
                    else:
                        notes[ds_to_check.id].add(
                            f"This Data Source had {data.get('total')} operation(s) in the last 12h, stop operations before Release deletion"
                        )
                        break

        async def add_note_if_pipe_is_still_requested(
            pipe_to_check: Optional[Pipe], result: Optional[Dict[str, List[Any]]]
        ) -> None:
            if not pipe_to_check or not result:
                return

            for data in result.get("data", []):
                if data["pipe_id"] == pipe_to_check.id:
                    if data.get("total", 0) == 0:
                        return
                    else:
                        notes[pipe_to_check.id].add(
                            f"This Pipe had {data.get('total')} request(s) in the last 20 minutes, stop requests before Release deletion"
                        )
                        break

        def build_notes(notes: Dict[str, Set[str]]) -> Dict[str, str]:
            return {
                ds_id: f"🚨 Warning 🚨: {'. '.join(individual_notes)}." for (ds_id, individual_notes) in notes.items()
            }

        if wmv and self.database:
            # fallback if metadata is legacy
            if "_database" not in wmv.__dict__ and "database" in wmv.__dict__:
                database = wmv.__dict__.pop("database")
                wmv.__dict__["_database"] = database

            async def dry_run_check():
                ds_dict = {}
                for datasource_name in rs[0]:
                    if (resource := wmv.get_resource(datasource_name)) is not None:
                        assert isinstance(resource, Datasource)
                        ds_removed[datasource_name] = resource.id
                        ds_dict[resource.id] = resource
                result = await get_by_pipe_endpoint(
                    api_host.get(None),
                    "requests_by_datasource",
                    **{"workspace_id": self.id, "datasources": ",".join(ds_removed.values())},
                )
                for _, resource in ds_dict.items():
                    await add_note_if_ds_is_shared(resource)
                    await add_note_if_ds_is_still_receiving_data(resource, result)

                pipes_dict = {}
                for pipe_name in rs[1]:
                    if (resource := wmv.get_resource(pipe_name)) is not None:
                        assert isinstance(resource, Pipe)
                        pipes_dict[resource.id] = resource
                        pipes_removed[pipe_name] = resource.id

                result_p = await get_by_pipe_endpoint(
                    api_host.get(None),
                    "requests_by_pipe",
                    **{"workspace_id": self.id, "pipes": ",".join(pipes_removed.values()), "release": release.semver},
                )
                for _, resource in pipes_dict.items():
                    await add_note_if_pipe_is_still_requested(resource, result_p)

                _notes = build_notes(notes)
                _notes_keys = _notes.keys()
                for p_name, _p in copy.deepcopy(pipes_removed).items():
                    if _p not in _notes_keys and pipes_dict[_p].endpoint:
                        del pipes_removed[p_name]

                return (
                    ds_removed,
                    pipes_removed,
                    _notes,
                )

            if dry_run:
                return await dry_run_check()

            for ds in rs[0]:
                datasource: Optional["Datasource"] = wmv.get_datasource(ds)
                if datasource:
                    for workspace_id in datasource.shared_with:
                        Users.check_used_by_pipes(
                            User.get_by_id(workspace_id), datasource.id, include_workspace_name=True
                        )

            from tinybird.table import drop_table  # Avoid circular import.

            _, _, _notes = await dry_run_check()
            if not (force or self.is_branch or self.is_release_in_branch) and len(_notes.items()):
                raise Exception(
                    f"Cannot delete resources from Release {release.semver}. Use `force=true` or `--force` to avoid this validation. Details: {build_notes(notes)}"
                )

            last_release = len(self.get_releases()) == 1 and self.get_releases()[0].id == release.id
            datasources = rs[0]
            pipes = rs[1]
            for pipe in pipes:
                p: Optional[Pipe] = wmv.get_pipe(pipe)
                if p is None:
                    continue
                pipes_removed[pipe] = p.id
                for node in p.pipeline.nodes:
                    if node.materialized:
                        if not last_release and self.get_resource(node.id):
                            errors = [Exception(f"{p.name}:{node.id} is used in live release")]
                        else:
                            errors = await drop_table(wmv, node.id)
                        for err in errors:
                            logging.warning(
                                f"Could not drop materialized view on drop Release {release.semver} from Workspace {self.name} - Database: {self.database} - is_branch: {self.is_branch} - origin: {self.origin}: {str(err)}\n{''.join(traceback.format_exception(err))}"
                            )

            dss: Dict[str, Datasource] = {}
            for datasource_name in datasources:
                datasource = wmv.get_datasource(datasource_name)
                if datasource:
                    dss[datasource.name] = datasource

            for ds, datasource in dss.items():
                if not last_release and self.get_resource(datasource.id):
                    errors = [Exception(f"{datasource.name}:{datasource.id} is used in live release")]
                else:
                    ds_removed[ds] = datasource.id
                    errors = await drop_table(wmv, datasource.id)
                for err in errors:
                    logging.warning(
                        f"Could not drop table on drop Release {release.semver} from Workspace {self.name}: {str(err)}\n{''.join(traceback.format_exception(err))}"
                    )
            await Users.delete_release_metadata(self, release)
        else:
            logging.error(f"Could not find metadata for Release {release.semver}")

        releases = [r for r in self.releases if r["id"] != release.id]
        await Users.update_releases(workspace_id=self.id, releases=releases)
        return ds_removed, pipes_removed, _notes

    async def delete(self) -> None:
        # If the workspace is already deleted, let's add a log to understand why we are deleting it again
        # https://gitlab.com/tinybird/analytics/-/issues/13060#note_2003350517
        if self.deleted:
            logging.error(f"Workspace {self.id} is already deleted")

        self.set_name(User.normalize_name_and_try_different_on_collision(f"{self.name}_deleted"))
        self.deleted = True
        self.deleted_date = datetime.utcnow()
        self.confirmed_account = False

    async def _hard_delete(self, database: Optional[str] = None) -> None:
        """
        This method will only delete the workspace from the database and Redis.
        You should use `UserAccount.delete_workspace` to delete safetly the workspace and all associated resources
        """

        if not self.deleted:
            await Users.delete(self)
            user_workspaces = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
            for uw in user_workspaces:
                UserWorkspaceRelationship._delete(uw.id)
        try:
            if self.origin:
                origin = User.get_by_id(self.origin)
                if origin and self.origin and database == origin.database:
                    raise Exception("Cannot delete a release")

            params: Dict[str, Any] = self.ddl_parameters(skip_replica_down=True)

            await ch_drop_database(
                self.database_server,
                self.database if not database else database,
                self.cluster,
                **params,
            )
            User._delete(self.id)
        except Exception as e:
            logging.exception(f"Could not hard delete workspace {self.id}: {str(e)}")
            raise e

    def pg_metadata(self, role):
        if role == "admin":
            return {
                "user": "postgres",
                "host": self.pg_server,
                "port": "5432",
                "database": "postgres",
                "connect_timeout": Limit.pg_connect_timeout,
                "options": f'-c statement_timeout={os.environ.get("PG_STATEMENT_TIMEOUT", Limit.pg_statement_timeout)}',
            }
        else:
            return {
                "user": "postgres",
                "host": self.pg_server,
                "port": "5432",
                "database": self.database,
                "connect_timeout": Limit.pg_connect_timeout,
                "options": f'-c statement_timeout={os.environ.get("PG_STATEMENT_TIMEOUT", Limit.pg_statement_timeout)}',
            }

    def has_limit(self, name):
        return name in self.limits

    def delete_limit_config(self, name):
        if name in self.limits:
            del self.limits[name]

    def rate_limit_config(self, rl_config: RateLimitConfig):
        key = f"{self.id}:{rl_config.key}"
        user_config = self.limits.get(rl_config.key, None)
        if user_config and user_config[0] == "rl":
            # override plan rate limit not allowed
            return RateLimitConfig(key, *user_config[1:])
        return RateLimitConfig(
            key,
            rl_config.count_per_period,
            rl_config.period,
            rl_config.max_burst,
            rl_config.quantity,
            rl_config.msg_error,
            rl_config.documentation,
        )

    def set_rate_limit_config(self, name, count_per_period, period, max_burst=0, quantity=1):
        self.limits[name] = ("rl", count_per_period, period, max_burst, quantity)

    def get_rate_limit_all_configs(self):
        return {
            name: RateLimitConfig(f"{self.id}:{name}", *config[1:])
            for name, config in self.limits.items()
            if config[0] == "rl"
        }

    def set_user_limit(self, name, value, prefix):
        self.limits[name] = (prefix, value)

    def set_endpoint_limit(self, name, value, endpoint, limit):
        self.limits[name] = (endpoint, limit, value)

    def get_limits(self, prefix):
        return {name: config[1] for name, config in self.limits.items() if config[0] == prefix}

    def get_endpoint_limit(self, endpoint: str, limit: EndpointLimit):
        limits_key = EndpointLimits.get_limit_key(endpoint, limit)
        config = self.limits.get(limits_key, None)
        if config:
            return config[2]
        return None

    def get_join_algorithm(self):
        ff_activated = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.JOIN_ALGORITHM_AUTO, "", self.feature_flags
        )
        return CH_SETTINGS_JOIN_ALGORITHM_AUTO if ff_activated else CH_SETTINGS_JOIN_ALGORITHM_HASH

    @property
    def is_branch_or_release_from_branch(self) -> bool:
        if self.origin:
            origin = User.get_by_id(self.origin)
            if origin:
                return self.is_branch or origin.is_branch
        return False

    @property
    def is_main_workspace(self) -> bool:
        return not self.is_branch_or_release_from_branch and not self.is_release

    def has_same_service_account(self, main_workspace: User) -> bool:
        if not main_workspace.cdk_gcp_service_account or not self.cdk_gcp_service_account:
            return False

        return main_workspace.cdk_gcp_service_account.get("client_email") == self.cdk_gcp_service_account.get(
            "client_email"
        )

    def get_max_execution_time(self, is_admin: bool = False) -> int:
        ch_limits = self.get_limits(prefix="ch")
        # the execution time should be set by the token but until that's implemented
        # we are taking the user max_execution_time and allow the admin token to use the user setting
        # ideally this should be max_execution_time = min(token_max_execution_time, user_max_execution_time)
        max_execution_time = ch_limits.get("max_execution_time", Limit.ch_max_execution_time)
        if is_admin:
            max_execution_time = ch_limits.get("admin_max_execution_time", max_execution_time)
        return int(max_execution_time)

    def ddl_parameters(self, skip_replica_down=False) -> Dict[str, Any]:
        max_execution_time = self.get_limits(prefix="ch").get("ddl_max_execution_time", Limit.ch_ddl_max_execution_time)

        # Allow DDL null status using skip_replica_down, by default for just for branches and releases from branches.
        if not self.cluster or (not skip_replica_down and not self.is_branch_or_release_from_branch):
            return {
                "max_execution_time": max_execution_time,
            }

        return self.ddl_null_status_parameters(max_execution_time, max_execution_time - 2)

    def ddl_null_status_parameters(self, max_execution_time: int, ddl_task_timeout: int) -> Dict[str, Any]:
        return {
            "max_execution_time": max_execution_time,
            "distributed_ddl_task_timeout": ddl_task_timeout,
            "distributed_ddl_output_mode": DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
        }

    @property
    def is_active(self):
        return not self.deleted

    @property
    def is_branch(self) -> bool:
        if self.child_kind:
            return self.child_kind == ChildKind.BRANCH.value
        if not self.origin:
            return False
        # Fallback
        if self.is_release:
            return False
        ws: Optional["User"] = User.get_by_id(self.origin)
        if ws:
            for release in ws.get_releases():
                if release.id == self.id:
                    return False
        return True

    @property
    def is_release(self) -> bool:
        if self.child_kind:
            return self.child_kind == ChildKind.RELEASE.value
        if not self.origin:
            return False
        # Fallback
        ws: Optional["User"] = User.get_by_id(self.origin)
        if ws:
            for release in ws.get_releases():
                if release.id == self.id and not release.is_live:
                    return True
        # We have some legacy release that do not have the value child_kind set
        # Also we have some releases that are no longer connected to the origin workspaces, but should still be considered as release
        if self.origin.replace("-", "_") in self.name:
            return True
        return False

    @property
    def is_release_in_branch(self) -> bool:
        if self.is_release and self.origin:
            origin: Optional["User"] = User.get_by_id(self.origin)
            if origin:
                return origin.is_branch
        return False

    def get_release_metadata(self, semver: str) -> User:
        if semver == "snapshot":
            workspace = self.get_snapshot()
            if not workspace:
                raise ValueError(f"Could not find Release: {semver}")
            return workspace
        else:
            version_ws = None
            for release in self.get_releases():
                if release.semver == semver:
                    version_ws = release.metadata
                    break
            if not version_ws:
                raise ValueError(f"Could not find Release: {semver}")
            return version_ws

    def get_snapshot(self) -> Optional[User]:
        if not self.current_release:
            origin = User.get_by_id(self.origin) if self.origin else None
            if not origin:
                return None
            return origin.get_snapshot()
        if not len(self.get_releases()):
            return None
        if self.is_branch:
            release = self.get_releases()[0]
        else:
            release = self.current_release
        if not release:
            return None
        snapshot_ws = release.metadata
        if not snapshot_ws:
            return None
        snapshot_ws.flush()
        return snapshot_ws

    @property
    def parent_workspace_or_branch_id(self) -> str:
        return self.origin if self.is_release and self.origin else self.id

    def find_parent_workspace_or_branch(self) -> User:
        """
        If you are on a release, this will return you the general workspace. In other cases, it will return the same workspace
        """
        if self.is_release and self.origin:
            return User.get_by_id(self.origin)
        return self

    def get_main_workspace(self) -> User:
        """
        This will return the production workspace of a branch or release.
        In case you are on release of a branch and you want to get the general workspace. Please use `get_parent_workspace` method
        """
        if self.origin:
            parent: "User" = User.get_by_id(self.origin)
            if not parent:
                # This indicates an orphan release or branch
                logging.warning(
                    f"Could not find parent workspace for workspace {self.id} {self.name} with origin {self.origin}"
                )

            if parent.origin:
                return User.get_by_id(parent.origin)
            return parent
        return self

    @property
    def is_branch_outdated(self) -> bool:
        try:
            if self.is_branch:
                main_workspace = self.get_main_workspace()
                live_release = main_workspace.current_release if main_workspace else None
                return self.get_release_by_commit(live_release.commit) is None if live_release else False
            return False
        except Exception as exc:
            logging.exception(exc)
            return False

    @property
    def workspaces_limits(self):
        return {
            name: config[1]
            for name, config in self.limits.items()
            if not isinstance(config, int) and config[0] == "workspaces"
        }

    def set_max_workspaces_limit(self, max_workspaces):
        self.limits["max_workspaces"] = ("workspaces", max_workspaces)

    @property
    def max_seats_limit(self):
        return self.workspaces_limits.get("max_seats", Limit.max_seats)

    def set_max_seats_limit(self, max_seats):
        workspace_users_count = len(self.user_accounts)

        if workspace_users_count > max_seats:
            raise Exception(
                f"The number of max seats can't be lower than the number of users in the workspace ({workspace_users_count})"
            )
        else:
            self.limits["max_seats"] = ("workspaces", max_seats)

    def set_name(self, new_name: WorkspaceName):
        new_name_as_string = str(new_name)
        if self._normalized_name_index == new_name_as_string:
            return

        self.assert_workspace_name_is_not_in_use(new_name)

        if self._normalized_name_index:
            self._clean_index("_normalized_name_index")

        self._normalized_name_index = new_name_as_string
        self.name = new_name_as_string

    def set_is_read_only(self, is_read_only: bool):
        self.feature_flags[FeatureFlagWorkspaces.PROD_READ_ONLY.value] = is_read_only

    @property
    def kafka_max_topics(self):
        max_topics = self.limits.get("max_topics", ("kafka", Limit.max_seats))
        return max_topics[1]

    @classmethod
    def normalize_name_and_try_different_on_collision(cls, new_possible_name: str) -> WorkspaceName:
        tries = 0
        max_tries = 4
        name_available = False
        while not name_available or tries < max_tries:
            if tries == 0:
                normalized_name = WorkspaceName.create_from_not_normalized_name(
                    new_possible_name, random_string_at_the_end=False
                )
            else:
                random_number_at_the_end = cls._get_string_with_random_numbers(tries * 2)
                normalized_name = WorkspaceName.create_from_not_normalized_name(
                    new_possible_name, custom_random_string=random_number_at_the_end
                )

            try:
                User.assert_workspace_name_is_not_in_use(normalized_name)
                return normalized_name
            except NameAlreadyTaken:
                tries += 1

        raise ValueError("Name could not be set from an not normalized mail, too many tries to find a not used name")

    @classmethod
    def generate_uid_and_database_name_and_try_different_on_collision(cls) -> Tuple[str, str]:
        tries = 0
        max_tries = 4
        while tries < max_tries:
            uid = str(uuid.uuid4())
            database_name = "d_" + hashlib.sha224(uid.encode()).hexdigest()[:6]
            try:
                User.get_by_database(database_name)
            except UserDoesNotExist:
                return uid, database_name
            tries += 1
        raise DatabaseNameCollisionError("Database name could not be set in workspace creation")

    @staticmethod
    def _get_string_with_random_numbers(size: int) -> str:
        return "".join([str(int(random.random() * 10)) for _ in range(size)])

    def name_is_normalized_and_unique(self) -> bool:
        return self._normalized_name_index is not None

    @staticmethod
    def assert_workspace_name_is_not_in_use(possible_workspace_name: WorkspaceName):
        u = None
        try:
            u = User.get_by_name(str(possible_workspace_name))
        except UserDoesNotExist:
            pass
        if u:
            raise NameAlreadyTaken(name_taken=str(possible_workspace_name))

    def set_stripe_settings(
        self,
        stripe_customer_id=None,
        stripe_email=None,
        stripe_subscription_id=None,
        stripe_client_secret=None,
        stripe_setup_intent=None,
    ):
        self.stripe.update(
            {
                "customer_id": stripe_customer_id or self.stripe.get("customer_id", None),
                "email": stripe_email or self.stripe.get("email", None),
                "subscription_id": stripe_subscription_id or self.stripe.get("subscription_id", None),
                "client_secret": stripe_client_secret or self.stripe.get("client_secret", None),
                "setup_intent_id": stripe_setup_intent or self.stripe.get("setup_intent_id", None),
            }
        )

    def add_profile(self, profile_name: str, profile_value: str):
        """
        >>> from tinybird.user import Users, UserAccount
        >>> email = 'add_profile@example.com'
        >>> u = UserAccount.register(email, 'pass')
        >>> workspace_name = 'add_profile'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w.add_profile('populates', 'value')
        >>> w.profiles.get('populates') == 'value'
        True
        >>> w.add_profile('populates', 'value')
        Traceback (most recent call last):
        ...
        Exception: Profile "populates" is already defined
        """

        if self.profiles.get(profile_name):
            raise Exception(f'Profile "{profile_name}" is already defined')
        self.profiles[profile_name] = profile_value

    def update_profile(self, profile_name: str, profile_value: str):
        """
        >>> from tinybird.user import Users, UserAccount
        >>> email = 'update_profile@example.com'
        >>> u = UserAccount.register(email, 'pass')
        >>> workspace_name = 'update_profile'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w.update_profile('populates', 'value')
        Traceback (most recent call last):
        ...
        Exception: Profile "populates" is not defined
        >>> w.add_profile('populates', 'value')
        >>> w.update_profile('populates', 'value2')
        >>> w.profiles.get('populates') == 'value2'
        True
        """

        if not self.profiles.get(profile_name):
            raise Exception(f'Profile "{profile_name}" is not defined')
        self.profiles.update({profile_name: profile_value})

    def delete_profile(self, profile_name: str):
        """
        >>> from tinybird.user import Users, UserAccount
        >>> email = 'delete_profile@example.com'
        >>> u = UserAccount.register(email, 'pass')
        >>> workspace_name = 'delete_profile'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w.delete_profile('populates')
        Traceback (most recent call last):
        ...
        Exception: Profile "populates" is not defined
        >>> w.add_profile('populates', 'value')
        >>> w.delete_profile('populates')
        >>> w.profiles.get('populates') is None
        True
        """

        if not self.profiles.get(profile_name):
            raise Exception(f'Profile "{profile_name}" is not defined')
        del self.profiles[profile_name]

    def update_last_commit(self, last_commit: str, resources: List[GitHubResource]) -> User:
        self.remote.update({"last_commit_sha": last_commit})

        for resource in resources:
            if resource.resource_type == "datasource":
                datasource = self.get_datasource(resource.resource_id)
                if not datasource:
                    continue
                datasource.last_commit.update({"content_sha": resource.sha, "status": "ok", "path": resource.path})
                self.update_datasource(datasource, update_last_commit_status=False)

            if resource.resource_type == "pipe":
                pipe = self.get_pipe(resource.resource_id)
                if not pipe:
                    continue
                pipe.last_commit.update({"content_sha": resource.sha, "status": "ok", "path": resource.path})
                self.update_pipe(pipe, update_last_commit_status=False)
        return self

    async def update_remote(self, remote: GitHubSettings) -> User:
        name: Optional[str] = ""
        if not remote.name and remote.remote:
            parsed_remote = urlparse(remote.remote)
            name = parsed_remote.path.split("/")[-1].replace(".git", "")
        else:
            name = remote.name

        if not self.origin:
            try:
                if self.current_release:
                    release_workspace = Users.get_by_id(self.current_release.id)
                    await Users.update_remote(release_workspace, remote=remote)
            except Exception as e:
                logging.exception(f"Error on update_remote for the live release (workspace: {self.id}): {e}")

        self.remote = {
            "provider": remote.provider if remote.provider else self.remote.get("provider", ""),
            "owner": remote.owner if remote.owner else self.remote.get("owner", ""),
            "owner_type": remote.owner_type if remote.owner_type else self.remote.get("owner_type", ""),
            "remote": remote.remote if remote.remote else self.remote.get("remote", ""),
            "name": name if name else self.remote.get("name", ""),
            "access_token": remote.access_token if remote.access_token else self.remote.get("access_token", ""),
            "branch": remote.branch if remote.branch else self.remote.get("branch", ""),
            "project_path": (
                remote.project_path if remote.project_path is not None else self.remote.get("project_path", "")
            ),
            "last_commit_sha": self.remote.get("last_commit_sha", ""),
            "status": remote.status if remote.status else self.remote.get("status", GitHubSettingsStatus.LINKED.value),
        }

        return self

    async def get_branches(self) -> List[Dict[str, Any]]:
        user_workspaces = UserWorkspaceRelationship.get_by_workspace(self.id, self.max_seats_limit)
        owners = [uw for uw in user_workspaces if uw.relationship == Relationships.ADMIN]
        branches = []
        owner_branches = {}

        if not len(owners):
            return []

        for owner in owners:
            owner_user = UserAccount.get_by_id(owner.user_id)
            if not owner_user:
                logging.exception(f"User {owner.user_id} not found")
                continue
            owner_workspaces = await owner_user.get_workspaces(
                with_token=True, with_environments=True, only_environments=True, filter_by_workspace=self.id
            )
            for workspace in owner_workspaces:
                owner_branches[workspace.get("id")] = workspace

        branches = [branch for branch in owner_branches.values()]
        return branches

    async def delete_remote(self, force: Optional[bool] = False) -> User:
        branches = []

        if not self.origin:
            try:
                branches = await self.get_branches()
            except Exception as e:
                logging.exception(f"Error on delete_remote when getting workspace branches (workspace: {self.id}): {e}")

            if (len(self.releases) > 1 or len(branches)) and not force:
                raise DeleteRemoteException("Remote can't be deleted")

            try:
                if self.current_release:
                    release_workspace = Users.get_by_id(self.current_release.id)
                    await Users.delete_remote(release_workspace, force=force)
            except Exception as e:
                logging.exception(f"Error on delete_remote for the live release (workspace: {self.id}): {e}")

        self.remote = asdict(GitHubSettings(status=GitHubSettingsStatus.CLI.value))
        return self

    def remove_stripe_subscription(self):
        self.stripe.update(
            {
                "email": None,
                "subscription_id": None,
                "client_secret": None,
                "setup_intent_id": None,
            }
        )

    def _get_workspace_color(self) -> str:
        """
        >>> from tinybird.user import Users, UserAccount
        >>> email = 'test_workspace_color@example.com'
        >>> u = UserAccount.register(email, 'pass')
        >>> workspace_name = 'new_workspace'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> w.color
        '#f94144'
        >>> workspace_name = 'test_workspace_color'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> w.color
        '#43aa8b'
        >>> workspace_name = 'test_work'
        >>> w = User.register(workspace_name, admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> w.color
        '#f9c74f'
        """
        random_number = 0
        for char in self.name:
            random_number += ord(char)
        return WORKSPACE_COLORS[random_number % len(WORKSPACE_COLORS)]

    @property
    def color(self):
        return self._get_workspace_color()

    def get_release_by(self, attr: str, value: str) -> Optional[Release]:
        for r in self.releases:
            if r.get(attr, None) == value:
                return Release.from_dict(r)
        return None

    def get_release_by_commit(self, commit: str) -> Optional[Release]:
        return self.get_release_by("commit", commit)

    def get_release_by_semver(self, semver: str) -> Optional[Release]:
        if semver == "live" or "snapshot" in semver:
            return self.current_release
        if semver.startswith("v"):
            semver = semver[1:].replace("_", ".")
        release = self.get_release_by("semver", semver)

        # live is 0.0.0 or 0.0.0-x and you are pushing to 0.0.0-y
        if not release and "-" in semver:
            _semver = semver.split("-")[0]
            releases = [r for r in self.get_releases() if _semver == semver.split("-")[0]]
            if len(releases):
                # there's only one post release, but just in case we support more get the most recent
                release = Release.sort_by_date(releases)[0]
        return release

    def get_release_by_id(self, id: str) -> Optional[Release]:
        return self.get_release_by("id", id)

    async def tables_metadata(self) -> Tuple[List[Dict[str, str]], Dict[str, Dict[str, TableDetails]]]:
        db_tables = get_datasources_internal_ids(self.get_datasources(), default_database=self.database)
        if not db_tables:
            return [], {}
        schemas = await ch_databases_tables_schema_async(
            self.database_server,
            condition=f"(database, table) IN {tuple(db_tables)}",
            include_default_columns=True,
            timeout=2,
        )
        details = await ch_many_tables_details_async(self.database_server, datasources=db_tables, timeout=2)
        return schemas, details

    def validate_preview_release_limit(self) -> None:
        preview_releases = [r for r in self.get_releases() if r.status == ReleaseStatus.preview]

        max_number_of_preview_releases = self.get_limits(prefix="release").get(
            "max_number_of_preview_releases", Limit.release_max_number_of_preview_releases
        )

        if len(preview_releases) >= max_number_of_preview_releases:
            preview_releases_semvers = ", ".join([f"'{preview.semver}'" for preview in preview_releases])
            raise MaxNumberOfReleasesReachedException(
                f"Error: Maximum number of releases in preview status reached ({max_number_of_preview_releases}). Delete or promote one of the existing releases in Preview state ({preview_releases_semvers}) and retry."
            )

    def on_preview_release(self, release: Release) -> Release:
        if release.status != ReleaseStatus.deploying:
            raise ReleaseStatusException(f"Release {release.semver} was not in deploying status, can't preview it.")
        self.validate_preview_release_limit()
        release.status = ReleaseStatus.preview
        return release

    def get_rollback_release_candidate(self, release: Release) -> Release:
        if release.status != ReleaseStatus.live:
            raise ReleaseStatusException(f"Release {release.semver} is not in live status, can't rollback it.")
        if len(self.releases) == 1:
            raise ReleaseStatusException(f"Release {release.semver} doesn't have any Release to roll back.")
        idx = next((idx for idx, x in enumerate(self.get_releases()) if x.semver == release.semver), None)
        if idx is None or idx == 0:
            raise ReleaseStatusException(f"Release {release.semver} doesn't have any Release to roll back.")
        rollback_release = None
        i = idx
        while i > 0:
            i -= 1
            rollback_release = self.releases[i]
            if rollback_release["status"] == ReleaseStatus.rollback.value:
                break
        if not rollback_release:
            raise ReleaseStatusException(f"Release {release.semver} doesn't have any Release to roll back.")
        return Release.from_dict(rollback_release)

    def on_rollback_release(self, release: Release) -> Release:
        if release.is_post:
            raise ReleaseStatusException(
                f"Release {release.semver} cant be rolled back. Post Releases do not support this feature."
            )

        rollback_release = self.get_rollback_release_candidate(release)

        # Important to get the metadata before changing the status to "live"
        # Once the status is "live" the main workspace metadata is returned instead of the release to rollback.
        metadata = rollback_release.metadata
        rollback_release.status = ReleaseStatus.live
        if not metadata:
            raise ReleaseStatusException(f"Release {release.semver} doesn't have any metadata to roll back.")

        update_shared_datasources(self.datasources, metadata)
        rollback_release = self.update_release_tokens(rollback_release, metadata)

        self.pipes = metadata.pipes
        self.datasources = metadata.datasources
        self.tokens = metadata.tokens
        # FIXME sync connectors, etc.
        return rollback_release

    async def on_promote_release(self, release: Release, metadata: "User") -> Tuple[Release, Users.RollbackInfo]:
        if release.status != ReleaseStatus.preview:
            raise ReleaseStatusException(f"Release {release.semver} is not in preview status, can't promote it.")

        max_number_of_rollback_releases = self.get_limits(prefix="release").get(
            "max_number_of_rollback_releases", Limit.release_max_number_of_rollback_releases
        )

        number_of_existing_rollback_releases = len(
            [r for r in self.get_releases() if r.status == ReleaseStatus.rollback]
        )

        if not self.is_branch and number_of_existing_rollback_releases >= max_number_of_rollback_releases:
            oldest_release = Release.sort_by_date(self.get_releases())[-1]
            raise MaxNumberOfReleasesReachedException(
                f"Error: Maximum number of releases in Rollback status reached ({number_of_existing_rollback_releases}). Delete your oldest Release ({oldest_release.semver}) and retry."
            )

        live_releases = [r for r in self.releases if r["status"] == ReleaseStatus.live.value]
        if any(live_releases):
            for r in live_releases:  # Rollback everything in the workspace
                r["status"] = ReleaseStatus.rollback.value

        rollback_info = Users.RollbackInfo(
            release_ids=[r["id"] for r in live_releases if r["id"] != self.id],
            pipes=self.pipes,
            datasources=self.datasources,
            tokens=self.tokens,
        )

        release.status = ReleaseStatus.live

        # FIXME this needs to be done in a separate transaction
        update_shared_datasources(self.datasources, metadata)
        release = self.update_release_tokens(release, metadata)

        self.pipes = metadata.pipes
        self.datasources = metadata.datasources
        self.tokens = metadata.tokens
        return release, rollback_info

    def on_deploying_release(self, release: Release, metadata: Optional["User"]) -> Tuple[Release, User]:
        deploying_releases = [r for r in self.get_releases() if r.status == ReleaseStatus.deploying]
        if any(deploying_releases):
            release.status = ReleaseStatus.failed
            raise ReleaseStatusException(
                f"There's already a deploying Release (version: {deploying_releases[0].semver}), please wait for it to finish and retry."
            )
        self.validate_preview_release_limit()
        release.status = ReleaseStatus.deploying

        if not metadata:
            metadata = self.clone(release.semver)

        return release, metadata

    def on_failed_release(self, release: Release) -> Release:
        failed_releases = [r for r in self.get_releases() if r.status == ReleaseStatus.failed]
        if any(failed_releases):
            raise ReleaseStatusException(
                f"There's already a failed Release (version: {failed_releases[0].semver}), please remove it or retry it to continue."
            )
        release.status = ReleaseStatus.failed
        return release

    def on_deleting_release(self, release: Release) -> Release:
        release.status = ReleaseStatus.deleting
        return release

    def update_release_tokens(self, release: Release, metadata: "User") -> Release:
        if release.id != metadata.id:
            logging.exception(
                "This Workspace requires a migration to avoid using WorkspaceMetadataVersion. See https://gitlab.com/tinybird/analytics/-/merge_requests/8718"
            )
        # FIXME: We need to revisit this logic below, we might be leaving orphaned metadata versions
        for token in metadata.tokens:
            old_token = self.get_token(token.name)
            if not old_token:
                token.user_id = self.id
                token.resource_id = self.id
                token.refresh(User.secret, self.id)
            else:
                token.user_id = old_token.user_id
                token.resource_id = old_token.resource_id
                token.token = old_token.token
                if old_token.origin.resource_id and old_token.origin.resource_id == token.origin.resource_id:
                    if ds := self.get_datasource(token.origin.resource_id):
                        if new_ds := metadata.get_datasource(ds.name):
                            token.origin.resource_id = new_ds.id
                    elif (pipe := self.get_pipe(token.origin.resource_id)) and (
                        new_pipe := metadata.get_pipe(pipe.name)
                    ):
                        token.origin.resource_id = new_pipe.id
        return release

    async def apply_release_status_state_machine(
        self, status: ReleaseStatus, release: Release, metadata: Optional["User"]
    ) -> Tuple[Release, Optional["User"], Optional[Users.RollbackInfo]]:
        rollback_info: Optional[Users.RollbackInfo] = None
        if status == ReleaseStatus.live:
            if not metadata:
                raise ReleaseStatusException(f"Metadata is required to change Release status to {status}.")
            release, rollback_info = await Users.on_promote_release(self.id, release, metadata)
        elif status == ReleaseStatus.preview:
            release = await Users.on_preview_release(self.id, release)
        elif status == ReleaseStatus.rollback:
            release = await Users.on_rollback_release(self.id, release)
        elif status == ReleaseStatus.deploying:
            release, metadata = await Users.on_deploying_release(self.id, release, metadata)
        elif status == ReleaseStatus.failed:
            release = await Users.on_failed_release(self.id, release)
        elif status == ReleaseStatus.deleting:
            release = await Users.on_deleting_release(self.id, release)
        else:
            raise ReleaseStatusException(f"Invalid Release status: {status}")

        return release, metadata, rollback_info

    @property
    def current_release(self) -> Optional[Release]:
        for r in self.get_releases():
            if r.is_live:
                return r
        return None

    @property
    def rate_limits(self) -> Dict[str, Dict[str, int]]:
        """
        >>> u0 = User(id='test_rate_limits')
        >>> u0.rate_limits['api_datasources_create_append_replace']
        {'count_per_period': 5, 'max_burst': 3, 'period': 60}
        >>> u0.set_rate_limit_config('api_datasources_create_append_replace', 10, 5, 100)
        >>> u0.rate_limits['api_datasources_create_append_replace']
        {'count_per_period': 10, 'max_burst': 100, 'period': 5}
        """
        rate_limits = {}
        for k, rl_config in Limit.__dict__.items():
            if not isinstance(rl_config, RateLimitConfig):
                continue
            rl_config = self.rate_limit_config(rl_config)

            rate_limits[k] = {
                "count_per_period": rl_config.count_per_period,
                "max_burst": rl_config.max_burst,
                "period": rl_config.period,
            }
        return rate_limits

    @property
    def is_read_only(self) -> bool:
        return FeatureFlagsWorkspaceService.feature_for_id(FeatureFlagWorkspaces.PROD_READ_ONLY, "", self.feature_flags)

    @property
    def main_id(self) -> "str":
        return self.origin if self.origin and self.is_release else self.id

    def allowed_table_functions(self) -> FrozenSet[str]:
        allowed_functions = self.get_limits(prefix="workspace").get("allowed_table_functions", "postgresql").split(",")
        # make sure postgresql is always there because is GA
        allowed_functions.append("postgresql")
        return frozenset(allowed_functions)

    def release_semver(self) -> str:
        try:
            if self.origin and self.is_release:
                current_release = User.get_by_id(self.origin).get_release_by_id(self.id)
            else:
                current_release = self.current_release
            return current_release.semver if current_release else ""
        except Exception as exc:
            # Defensive code in case we fail getting release semver
            logging.exception(f"Error getting release semver for {self.id}: {exc}")
            return ""

    def release_oldest_rollback(self) -> Optional[Release]:
        rollback_releases = [r for r in self.get_releases() if r.is_rollback]
        max_rollback = self.get_limits(prefix="release").get(
            "max_number_of_rollback_releases", Limit.release_max_number_of_rollback_releases
        )
        if len(rollback_releases) < max_rollback or len(rollback_releases) == 0:
            return None
        return Release.sort_by_date(rollback_releases, reverse=False)[0]


def migration_pipe_endpoints(u):
    """
    >>> from tinybird.user import Users, UserAccount
    >>> email = 'test_endpoint_migration@example.com'
    >>> name = 'test_endpoint_migration'
    >>> u = UserAccount.register(email, 'pass')
    >>> w = User.register(name, admin=u.id)
    >>> w = User.get_by_id(w.id)
    >>> _ = Users.add_pipe_sync(w, 'test', 'select * from table')
    >>> w = User.get_by_id(w.id)
    >>> pipe = w['pipes'][0]
    >>> del pipe['endpoint']
    >>> pipe['published_version'] = 'foo'
    >>> pipe['published_date'] = 'bar'
    >>> 'endpoint' in pipe
    False
    >>> w = Users.get_by_id(w.id)
    >>> w = migration_pipe_endpoints(w)
    >>> pipe = w['pipes'][0]
    >>> 'published_date' in pipe
    False
    >>> 'published_version' in pipe
    False
    >>> pipe['endpoint'] is None
    True
    """
    delete_keys = ["published_version", "published_date"]
    for pipe in u["pipes"]:
        for k in delete_keys:
            if k in pipe:
                del pipe[k]
        if "endpoint" not in pipe:
            pipe["endpoint"] = None
    return u


def add_parent(u):
    """adds a parent pipe. When a pipe is copied it tracks where it comes from"""
    for pipe in u["pipes"]:
        pipe["parent"] = None
    return u


def add_clusters(u):
    u["clusters"] = u.get("clusters", [])
    return u


def add_replicated_version_and_project(u):
    for ds in u["datasources"]:
        ds["replicated"] = False
        ds["version"] = 0
        ds["project"] = ""
    return u


def add_version_and_project_to_pipes(u):
    for ds in u["pipes"]:
        ds["version"] = 0
        ds["project"] = ""
    return u


def add_tags_to_pipes(u):
    for pipe in u["pipes"]:
        pipe["tags"] = pipe.get("tags", {})
    return u


def add_sessionrewind_field(u):
    u["enabled_sessionrewind"] = False
    return u


def add_user_details(u):
    u["name"] = u.get("name", "")
    u["avatar_url"] = u.get("avatar_url", "")
    return u


def deduplicate_token_names(u):
    """
    >>> u = UserAccount.register('deduplicate_token_names@example.com', 'pass')
    >>> w = User.register('deduplicate_token_names', admin=u.id)
    >>> w = User.get_by_id(w.id)
    >>> ac = AccessToken('id_u', 'unique', '')
    >>> w.tokens.append(ac)
    >>> ac = AccessToken('id', 'test', '')
    >>> w.tokens.append(ac)
    >>> ac = AccessToken('id2', 'test', '')
    >>> w.tokens.append(ac)
    >>> ac = AccessToken('id3', 'test', '')
    >>> w.tokens.append(ac)
    >>> [t.name for t in w.tokens]
    ['admin token', 'admin deduplicate_token_names@example.com', 'create datasource token', 'unique', 'test', 'test', 'test']
    >>> u_migrated = deduplicate_token_names(w._to_storage())
    >>> [t.name for t in u_migrated['tokens']]
    ['admin token', 'admin deduplicate_token_names@example.com', 'create datasource token', 'unique', 'test 2', 'test 3', 'test']
    """

    c = _get_tokens_counter(u)
    count = 1

    while len(u["tokens"]) > len(c.items()):
        # get repeated ones and reemplace the token name
        for x in [k for k, v in c.items() if v > 1]:
            tk = next((token for token in u["tokens"] if token.name == x), None)
            if tk:
                tk.name = f"{tk.name} {count + 1}"

        count += 1
        c = _get_tokens_counter(u)

    return u


def _get_tokens_counter(u):
    c: Counter = Counter()

    for x in u["tokens"]:
        c[x.name] += 1

    return c


def add_cache_datasource_headers(u):
    for ds in u["datasources"]:
        ds["headers"] = ds.get("headers", {})
    return u


def add_max_execution_time(u):
    u["max_execution_time"] = 10  # this is the max execution time set when this migration was created
    return u


def add_pg_field(u):
    u["enabled_pg"] = False
    return u


def add_pg_metadata(u):
    u["pg_server"] = User.default_postgres_server
    u["pg_foreign_server"] = User.default_postgres_foreign_server
    u["pg_foreign_server_port"] = User.default_postgres_foreign_server_port
    return u


def add_limits_field(u):
    u["limits"] = u.get("limits", {}) or {}
    return u


def move_max_execution_to_limits(u):
    """
    >>> move_max_execution_to_limits({'max_execution_time': 10})
    {'limits': {}}
    >>> move_max_execution_to_limits({'limits': {}})
    {'limits': {}}
    >>> move_max_execution_to_limits({'limits': {}, 'max_execution_time': 5})
    {'limits': {'admin_max_execution_time': ('ch', 5)}}
    >>> move_max_execution_to_limits({'limits': {'x': 'y'}, 'max_execution_time': 5})
    {'limits': {'x': 'y', 'admin_max_execution_time': ('ch', 5)}}
    >>> move_max_execution_to_limits({'limits': None, 'max_execution_time': 5})
    {'limits': {'admin_max_execution_time': ('ch', 5)}}
    >>> move_max_execution_to_limits({'max_execution_time': 5})
    {'limits': {'admin_max_execution_time': ('ch', 5)}}
    >>> move_max_execution_to_limits({'max_execution_time': 5})
    {'limits': {'admin_max_execution_time': ('ch', 5)}}
    >>> move_max_execution_to_limits({})
    {'limits': {}}
    """
    u["limits"] = u.get("limits", {}) or {}
    current_admin_max_execution_time = u.get("max_execution_time", 10)
    if current_admin_max_execution_time != 10:
        u["limits"]["admin_max_execution_time"] = ("ch", current_admin_max_execution_time)
    if "max_execution_time" in u:
        del u["max_execution_time"]
    return u


def add_workspaces_metadata(u):
    u["workspaces"] = u.get("workspaces", []) or []
    u["access_users"] = u.get("access_users", []) or []

    return u


def add_workspaces_ownership(u):
    workspace_limits = u.get("workspace_limits", {}) or {}
    u["limits"]["max_owned"] = ("workspaces", workspace_limits.get("max_owned", Limit.max_owned))
    u["owned_workspaces"] = u.get("owned_workspaces", []) or []
    user_id = u.get("id")
    u["owner"] = u.get("owner", user_id) or user_id

    return u


def reset_max_owned_limits(u):
    if u["limits"] and "max_owned" in u["limits"] and u["limits"]["max_owned"][1] == Limit.max_owned:
        del u["limits"]["max_owned"]

    return u


def add_enabled_workspaces_and_plan_fields(u):
    u["enabled_workspaces"] = u.get("enabled_workspaces", False) or False
    u["plan"] = u.get("plan", BillingPlans.DEV) or BillingPlans.DEV

    return u


def rename_shared_data_sources_attributes(u):
    """
    >>> rename_shared_data_sources_attributes({'datasources': []})
    {'datasources': []}
    >>> rename_shared_data_sources_attributes({'datasources': [{}, {'external':{}}, {'shared_with_workspaces':{}}]})
    {'datasources': [{}, {'shared_from': {}}, {'shared_with': {}}]}
    """

    def rename_key_if_exists(thedict, origin_key, destination_key):
        if origin_key in thedict:
            thedict[destination_key] = thedict.pop(origin_key)

    for ds in u["datasources"]:
        rename_key_if_exists(ds, "external", "shared_from")
        rename_key_if_exists(ds, "shared_with_workspaces", "shared_with")
    return u


def json_path_to_jsonpath(u):
    for ds in u["datasources"]:
        for column in ds.get("json_deserialization", []):
            if column.get("json_path", None):
                column["jsonpath"] = column["json_path"]
    return u


def personal_plan_to_dev_plan(u):
    if u["plan"] == "personal":
        u["plan"] = BillingPlans.DEV
    return u


def add_stripe_settings(u):
    u["stripe"] = u.get("stripe", {})
    return u


def del_json_path(u):
    for ds in u["datasources"]:
        for column in ds.get("json_deserialization", []):
            if column.get("json_path", None):
                del column["json_path"]
    return u


def add_feature_flags(u):
    u["feature_flags"] = u.get("feature_flags", {})

    return u


def fast_scan(u):
    return u


def add_notifications(u):
    max_seats = u["limits"].get("max_seats", ("workspaces", Limit.max_seats))[1]
    workspace_users = UserWorkspaceRelationship.get_by_workspace(u["id"], max_seats)
    for workspace_user in workspace_users:
        if workspace_user.relationship == Relationships.ADMIN:
            user_workspace_notifications = UserWorkspaceNotifications.get_by_user_and_workspace(
                workspace_user.user_id, u["id"]
            )
            if not user_workspace_notifications:
                UserWorkspaceNotificationsHandler.change_notifications(
                    workspace_user.user_id, u["id"], [Notifications.INGESTION_ERRORS]
                )

    return u


def database_index(u):
    return u


def drop_active_version_id(u):
    if "active_version_id" in u:
        del u["active_version_id"]
    return u


def add_external_clusters(u):
    u["external_clusters"] = u.get("external_clusters", {})
    return u


def add_profiles(u):
    u["profiles"] = u.get("profiles", {})
    return u


def add_deleted_date_for_already_removed(u):
    if u["deleted"] and u.get("deleted_date", None) is None:
        u["deleted_date"] = u["updated_at"]
    return u


def migrate_secrets(u):
    u["secrets"] = u.get("secrets", [])
    needs_migration = any([secret for secret in u["secrets"] if isinstance(secret, Secret)])
    if needs_migration:
        secrets_as_dict = []
        for secret in u["secrets"]:
            if isinstance(secret, Secret):
                secrets_as_dict.append(secret.to_dict())
        u["secrets"] = secrets_as_dict
    return u


def migrate_tags(u):
    tags = u.get("tags", [])
    if len(tags) == 0:
        tags = Tag.get_all_by_owner(u["id"])
        tags_as_dict = []
        for legacy_tag in tags:
            tag = ResourceTag(legacy_tag.name, legacy_tag.resources, legacy_tag.created_at, legacy_tag.updated_at)
            tags_as_dict.append(tag.to_dict())
        u["tags"] = tags_as_dict
    return u


User.__migrations__ = {
    1: migration_pipe_endpoints,
    2: add_parent,
    3: add_clusters,
    4: add_replicated_version_and_project,
    5: add_version_and_project_to_pipes,
    6: add_tags_to_pipes,
    7: add_sessionrewind_field,
    8: add_user_details,
    9: deduplicate_token_names,
    10: add_max_execution_time,
    11: add_cache_datasource_headers,
    12: add_pg_field,
    13: add_pg_metadata,
    14: add_limits_field,
    15: move_max_execution_to_limits,
    16: add_workspaces_metadata,
    17: add_workspaces_ownership,
    18: reset_max_owned_limits,
    19: add_enabled_workspaces_and_plan_fields,
    20: rename_shared_data_sources_attributes,
    21: json_path_to_jsonpath,
    22: personal_plan_to_dev_plan,
    23: del_json_path,
    24: add_stripe_settings,
    25: add_feature_flags,
    26: fast_scan,
    27: add_notifications,
    28: database_index,
    29: drop_active_version_id,
    30: add_external_clusters,
    31: add_profiles,
    32: add_deleted_date_for_already_removed,
    33: migrate_secrets,
    34: migrate_tags,
}


class ReleaseWorkspace(User):
    def __init__(self, workspace: User):
        self.workspace = workspace
        self.main = User.get_by_id(self.workspace.origin) if self.workspace.origin else self.workspace

        if not self.main:
            logging.exception(f"Cannot create ReleaseWorkspace {self.workspace}")
            raise ReleaseStatusException("Cannot create ReleaseWorkspace")

        self._init_attributes()

    def _init_attributes(self):
        # Only initialize the attributes that are unique to self.workspace
        self.id = self.workspace.id
        self.name = self.workspace.name
        self._normalized_name_index = self.workspace._normalized_name_index
        self.database = self.workspace.database
        self.pipes = self.workspace.pipes
        self.datasources = self.workspace.datasources
        self.tokens = self.workspace.tokens
        self.origin = self.workspace.origin
        self.releases = []

    def __getattr__(self, item):
        # Delegate attribute access to self.main for specific attributes
        return self._get_delegated_attribute(item)

    def __getitem__(self, item):
        # Support dictionary-style attribute access
        return self._get_delegated_attribute(item)

    def _get_delegated_attribute(self, item):
        # FIXME: we might need to update this list periodically
        main_attributes = [
            "password",
            "database_server",
            "clusters",
            "confirmed_account",
            "deleted",
            "explorations_ids",
            "max_execution_time",
            "enabled_pg",
            "pg_server",
            "pg_foreign_server",
            "pg_foreign_server_port",
            "limits",
            "stripe",
            "plan",
            "billing_details",
            "feature_flags",
            "hfi_frequency",
            "hfi_frequency_gatherer",
            "hfi_database_server",
            "hfi_concurrency_limit",
            "hfi_concurrency_timeout",
            "hfi_max_request_mb",
            "storage_policies",
            "cdk_gcp_service_account",
            "organization_id",
            "kafka_server_group",
            "env_database",
            "external_clusters",
            "profiles",
            "remote",
            "use_gatherer",
            "allow_gatherer_fallback",
            "gatherer_allow_s3_backup_on_user_errors",
            "gatherer_flush_interval",
            "gatherer_deduplication",
        ]
        if item in main_attributes:
            return getattr(self.main, item)

        # Fallback to workspace attributes
        return getattr(self.workspace, item, None)


class UserAccounts:
    """
    >>> u0 = UserAccount.register('test@example.com', 'pass')
    >>> u1 = UserAccounts.login('test@example.com', 'pass')
    >>> u0['password'] == u1['password']
    True
    >>> UserAccounts.login('test2@example.com', 'pass')
    Traceback (most recent call last):
    ...
    tinybird.user.UserAccountDoesNotExist: User account (test2@example.com) does not exist
    >>> UserAccount.register('test@example.com', 'pass')
    Traceback (most recent call last):
    ...
    tinybird.user.UserAccountAlreadyExists: User account already registered
    >>> u = UserAccounts.get_by_email('test@example.com')
    >>> u.email
    'test@example.com'
    """

    @staticmethod
    def delete(u: UserAccount) -> bool:
        with UserAccount.transaction(u.id) as user_account:
            user_account.delete()
        return True

    @staticmethod
    def login(mail, password) -> Optional[UserAccount]:
        u = UserAccounts.get_by_email(mail)
        if pbkdf2_sha256.verify(password, u["password"]):
            return u
        return None

    @staticmethod
    def get_by_email(mail: str) -> UserAccount:
        return UserAccount.get_by_email(mail)

    @staticmethod
    def get_by_id(uid: str) -> UserAccount:
        user_account = UserAccount.get_by_id(uid)
        if not user_account:
            raise UserAccountDoesNotExist("User account does not exist")
        return user_account

    @staticmethod
    def get_token_for_scope(u, scope) -> Optional[str]:
        user_account = UserAccount.get_by_id(u.id)
        if not user_account:
            logging.exception(f"User {u.id} not found")
            return None
        return user_account.get_token_for_scope(scope)

    @staticmethod
    def confirmed_account(u: "UserAccount") -> bool:
        return u.confirmed_account or FeatureFlagsService.feature_for_email(
            FeatureFlag.CONFIRM_ACCOUNT_AUTOMATICALLY, u.email, u.feature_flags
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def confirm_account(user_account_id: "str") -> UserAccount:
        with UserAccount.transaction(user_account_id) as user_account:
            user_account.confirmed_account = True
        return user_account

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _disable_confirmed_account(user_id):
        with UserAccount.transaction(user_id) as userAccount:
            userAccount.confirmed_account = False

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def change_password(user_account, password) -> bool:
        with UserAccount.transaction(user_account.id) as user_account:
            user_account.password = pbkdf2_sha256.using(**ENCRYPT_SETTINGS).encrypt(password)
        return True

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_enable_sessionrewind_value(user_id, value):
        with UserAccount.transaction(user_id) as user_account:
            user_account.enabled_sessionrewind = value
            user_account.enabled_fullstory = value

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_organization_id(user: UserAccount, organization_id: Optional[str]) -> None:
        if organization_id and user.organization_id and user.organization_id != organization_id:
            raise UserAccountAlreadyBelongsToOrganization(user.id, user.organization_id)

        with UserAccount.transaction(user.id) as u:
            u.organization_id = organization_id

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def refresh_token(user: UserAccount, token_name_or_id: str) -> AccessToken:
        with UserAccount.transaction(user.id) as u:
            tk = u.get_token_access_info(token_name_or_id)
            if not tk:
                raise TokenNotFound("Auth token not found")

            tk.refresh(UserAccount.secret, u.id)
            return tk

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_integration(user: UserAccount, _type: str, _id: str) -> UserAccount:
        with UserAccount.transaction(user.id) as u:
            integrations: List[IntegrationInfo] = u.integrations or []
            integrations.append(IntegrationInfo(_type, _id))
            u.integrations = integrations
            return u

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_integration(user: UserAccount, integration_id: str) -> UserAccount:
        if not user.integrations:
            return user

        with UserAccount.transaction(user.id) as u:
            assert u.integrations
            u.integrations = [d for d in u.integrations if d.integration_id != integration_id]
            return u

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_integrations_by_type(user: UserAccount, integration_type: str) -> UserAccount:
        if not user.integrations:
            return user

        with UserAccount.transaction(user.id) as u:
            assert u.integrations
            u.integrations = [d for d in u.integrations if d.integration_type != integration_type]
            return u

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def reset_integrations(user: UserAccount) -> UserAccount:
        """FIXME: Delete this method after dev phase"""

        if not user.integrations:
            return user

        with UserAccount.transaction(user.id) as u:
            u.integrations = []
            return u


class UserAccount(RedisModel):
    __namespace__ = "user_accounts"
    __props__ = [
        "email",
        "password",
        "enabled_fullstory",
        "enabled_sessionrewind",
        "deleted",
        "confirmed_account",
        "limits",
        "feature_flags",
        "tokens",
        "plan",
        "region_selected",
        "viewed_campaigns",
        "organization_id",
        "integrations",
    ]

    __indexes__ = ["email"]

    secret = ""
    confirmed_account: bool = True
    default_feature_flags: Dict[str, Any] = {}

    def __repr__(self) -> str:
        return f"UserAccount(email='{self.email}')"

    @classmethod
    def config(cls, redis_client, secret, confirmed_account=True, default_feature_flags=None):
        if default_feature_flags is None:
            default_feature_flags = {}

        super().config(redis_client)
        cls.secret = secret
        cls.confirmed_account = confirmed_account
        cls.default_feature_flags.update(default_feature_flags)

    @staticmethod
    def register(
        mail: str, password: Optional[str] = None, overwritten_redis_client: Optional[TBRedisClientSync] = None
    ) -> "UserAccount":
        user_account = None
        uid = str(uuid.uuid4())
        password = password or str(uuid.uuid4)
        user_email = mail.lower()

        try:
            if overwritten_redis_client:
                user_account = UserAccount.get_by_index_from_redis(overwritten_redis_client, "email", user_email)
            else:
                user_account = UserAccount.get_by_email(user_email)
        except Exception:
            pass
        if user_account:
            raise UserAccountAlreadyExists("User account already registered")

        user_data: Dict[str, Any] = {
            "id": uid,
            "email": user_email,
            "password": pbkdf2_sha256.using(**ENCRYPT_SETTINGS).hash(password),
            "enabled_fullstory": False,
            "enabled_sessionrewind": False,
            "deleted": False,
            "confirmed_account": UserAccount.confirmed_account,
            "region_selected": False,
            "limits": {},
            "feature_flags": UserAccount.default_feature_flags,
            "plan": BillingPlans.DEV,
            "tokens": [],
            "viewed_campaigns": set(),
        }

        user_account = UserAccount(**user_data)

        user_account.add_token("auth_token", scopes.AUTH)

        if overwritten_redis_client:
            UserAccount.save_to_redis(user_account, overwritten_redis_client)
            account = UserAccount.get_by_id_from_redis(overwritten_redis_client, user_account.id)
            if not account:
                raise Exception(f"Unexpected error: User {user_account.id} not found")
            assert isinstance(account, UserAccount)
            return account

        user_account.save()
        user_account_id = user_account.id
        user_account = UserAccount.get_by_id(user_account_id)
        if not user_account:
            raise Exception(f"Unexpected error: User {user_account_id} not found")
        return user_account

    def __init__(self, **user_dict: Any):
        self.id: str = None  # type: ignore
        self.email: str = user_dict["email"]
        self.password: Optional[str] = None
        self.enabled_fullstory: bool = False
        self.enabled_sessionrewind: bool = False
        self.deleted: bool = False
        self.confirmed_account: bool = False
        self.limits: Dict[str, Tuple[str, Any]] = {}
        self.feature_flags: Dict[str, Any] = {}
        self.tokens: List[AccessToken] = []
        self.region_selected: bool = False
        self.plan = BillingPlans.DEV
        self.viewed_campaigns: Set[str] = set()

        # This is the organization that the user is admin of. If the user is just a member of an organization, this will be
        # None.
        self.organization_id: Optional[str] = None
        self.integrations: Optional[List[IntegrationInfo]] = None

        super().__init__(**user_dict)

    def __getitem__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            raise AttributeError(f"'User' does not contain the '{item}' attribute")

    def __setitem__(self, item, value):
        try:
            object.__getattribute__(self, item)
        except AttributeError as e:
            # Explicit raising to be clear about behaviour
            raise e
        object.__setattr__(self, item, value)

    def __contains__(self, item):
        try:
            object.__getattribute__(self, item)
            return True
        except AttributeError:
            return False

    def __eq__(self, other):
        """
        >>> u0 = UserAccount(id='abcd', email='a@a.com')
        >>> u0 == None
        False
        >>> UserAccount(id='abcd', email='a@a.com') == UserAccount(id='abcd', email='a@a.com')
        True
        >>> UserAccount(id='abcd', email='a@a.com') == UserAccount(id='1234', email='b@b.com')
        False
        >>> class F:
        ...    id = u0.id
        >>> u0 == F()
        False
        """
        return other is not None and type(self) == type(other) and self.id == other.id  # noqa: E721

    def __hash__(self) -> int:
        return hash(self.id)

    @staticmethod
    def get_by_email(email: str) -> "UserAccount":
        user = UserAccount.get_by_index("email", email.lower())
        if not user:
            raise UserAccountDoesNotExist(f"User account ({email}) does not exist")
        return user

    def get_user_info(
        self,
        with_feature_flags: bool = False,
        with_integrations: bool = True,
        with_organization: bool = True,
        with_tracking: bool = False,
    ) -> Dict[str, Any]:
        user_info = {
            "email": self.email,
            "id": self.id,
            "active": self.is_active,
            "region_selected": self.region_selected,
            "enabled_sessionrewind": self.enabled_sessionrewind or self.enabled_fullstory,
            "max_owned_workspaces": self.max_owned_limit,
            "max_workspaces": self.max_workspaces_limit,
            "created_at": self.created_at.date().isoformat(),
        }
        if with_feature_flags:
            user_info["feature_flags"] = FeatureFlagsService.get_all_feature_values(self.email, self.feature_flags)

        if with_integrations:
            try:
                integrations = [
                    {"type": integration.integration_type, "id": integration.integration_id}
                    for integration in self.get_integrations()
                ]
            except Exception:
                integrations = []
            user_info["integrations"] = integrations

        if with_organization:
            user_info["organization_id"] = self.organization_id

        if with_tracking:
            tracker_token = None
            u = public.get_public_user()
            if u:
                ui_product_events_ds = u.get_datasource("ui_product_events")
                if ui_product_events_ds:
                    tokens = u.get_tokens_for_resource(ui_product_events_ds.id, scopes.DATASOURCES_APPEND)
                    tracker_token = tokens[0] if len(tokens) else None
            user_info["tracker_token"] = tracker_token

        return user_info

    def owns_this_workspace(self, workspace: User) -> bool:
        return UserWorkspaceRelationship.user_is_admin(self.id, workspace.id)

    async def get_workspaces(
        self,
        with_token: bool = False,
        with_environments: bool = True,
        only_environments: bool = False,
        filter_by_workspace: Optional[str] = None,
        additional_attrs: Optional[List[str]] = None,
        with_members_and_owner: bool = True,
    ) -> List[Dict[str, Any]]:
        # TODO add tests
        relationships_and_workspaces = await self.get_relationships_and_workspaces(
            with_environments, only_environments, filter_by_workspace
        )
        workspaces = []

        for relationship, workspace in relationships_and_workspaces:
            workspace_info = workspace.get_workspace_info(
                with_token=with_token, with_members_and_owner=with_members_and_owner
            )

            if additional_attrs:
                for attr in additional_attrs:
                    workspace_info[attr] = getattr(workspace, attr, None)

            # "token" is already filled in get_workspace_info. But the call is slightly different. I need to check if I
            # can remove it from here
            if with_token:
                tokens = workspace.get_tokens_for_resource(self.id, scopes.ADMIN_USER)
                if tokens:
                    workspace_info["token"] = tokens[0]

            if workspace.remote.get("provider"):
                # Don't include auth details
                remote = dict(workspace.remote)
                if "access_token" in remote:
                    del remote["access_token"]
                workspace_info["remote"] = remote

            workspace_info["role"] = relationship.relationship
            workspaces.append(workspace_info)

        return workspaces

    async def get_relationships_and_workspaces(
        self, with_environments: bool = True, only_environments: bool = False, filter_by_workspace: Optional[str] = None
    ) -> List[Tuple[UserWorkspaceRelationship, User]]:
        user_workspaces_relationships = UserWorkspaceRelationship.get_by_user(self.id)
        relationships_and_workspaces: List[Tuple[UserWorkspaceRelationship, User]] = []

        for relationship in user_workspaces_relationships:
            workspace = await User.get_by_id_async(relationship.workspace_id)
            if workspace is None:
                logging.warning(
                    f"Inconsistency: User {self.id}/{self.email} has a relationship with a deleted "
                    f"workspace {relationship.workspace_id}"
                )
                continue
            if workspace.is_release:
                continue
            if not with_environments and workspace.is_branch:
                continue
            if only_environments and not workspace.is_branch:
                continue
            if only_environments and filter_by_workspace and workspace.origin != filter_by_workspace:
                continue
            relationships_and_workspaces.append((relationship, workspace))

        return relationships_and_workspaces

    @property
    def number_of_workspaces(self) -> int:
        return len(UserWorkspaceRelationship.get_by_user(self.id))

    @property
    def is_member_of_any_workspaces(self) -> bool:
        # TODO: surely this can be optimised by doing an exist call in Redis, instead of actually fetching all
        # relationships to compute the length.
        return self.number_of_workspaces > 0

    @property
    def owned_workspaces(self) -> List[UserWorkspaceRelationship]:
        return UserWorkspaceRelationship.get_user_workspaces_by_relationship(self.id, Relationships.ADMIN)

    def has_access_to(self, workspace_id: str) -> bool:
        return UserWorkspaceRelationship.user_has_access(self.id, workspace_id)

    @staticmethod
    async def delete_workspace(
        user: Optional["UserAccount"],
        workspace: User,
        hard_delete: bool = False,
        job_executor: Optional[Any] = None,
        request_id: Optional[str] = None,
        track_log: Optional[bool] = True,
        tracer: Optional[ClickhouseTracer] = None,
    ) -> None:
        def log_deletion_error(text: str) -> None:
            logging.exception(f"[Workspace deletion] Workspace {workspace.name} ({workspace.id}): {text}")

        def log_deletion_warning(text: str) -> None:
            logging.warning(f"[Workspace deletion] Workspace {workspace.name} ({workspace.id}): {text}")

        delete_mode = "hard" if hard_delete else "soft"
        logging.info(f"[Delete Workspace {workspace.id}] ({delete_mode}) delete_workspace")

        async def validate_hard_delete() -> None:
            if not workspace.is_branch:
                if (
                    workspace.database in [public.INTERNAL_USER_DATABASE, "default"]
                    or workspace.name == public.INTERNAL_YEPCODE_WORKSPACE_NAME
                ):
                    msg = "Cannot delete an Internal Workspace"
                    logging.exception(msg)
                    raise WorkspaceException(msg)
            else:
                if workspace.database in [
                    public.INTERNAL_USER_DATABASE,
                    "default",
                ]:
                    raise WorkspaceException("Cannot delete an Internal Workspace")

        def delete_user_relations() -> None:
            logging.info(f"[Delete Workspace {workspace.id}] delete_user_relations")
            users_in_workspace = UserWorkspaceRelationship.get_by_workspace(workspace.id)
            for uw in users_in_workspace:
                try:
                    UserWorkspaceRelationship._delete(uw.id)
                except Exception as ex:
                    log_deletion_error(f"Error deleting user-workspace relation {uw.id}: {str(ex)}")

        async def delete_branches() -> None:
            logging.info(f"[Delete Workspace {workspace.id}] delete_branches")
            if user and not workspace.origin:
                if not UserWorkspaceRelationship.user_is_admin(user_id=user.id, workspace_id=workspace.id):
                    return

                branches = await workspace.get_branches()
                for branch in branches:
                    # confirm we are deleting branch that belongs to workspace
                    if branch.get("is_branch") and branch.get("main") == workspace.id:
                        await UserAccount.delete_workspace(
                            user, User.get_by_id(branch["id"]), hard_delete=True, track_log=track_log, tracer=tracer
                        )
                    else:
                        log_deletion_error(f"Branch {branch['id']} found but metadata is corrupted")

        async def unshare_datasources() -> None:
            logging.info(f"[Delete Workspace {workspace.id}] unshare_datasources")
            if not user:
                return
            try:
                await Users.unshare_all_data_sources_in_this_workspace(workspace, user)
            except Exception as ex:
                log_deletion_error(f"Error unsharing datasources: {str(ex)}")

        async def delete_releases(workspace: User, hard_delete: bool) -> None:
            logging.info(f"[Delete Workspace {workspace.id}] delete_releases")
            try:
                origin = User.get_by_id(workspace.origin) if workspace.origin else None
                releases = workspace.get_releases()
                for release in releases:
                    logging.info('"Deleting release {} for workspace {}'.format(release.id, workspace.id))
                    if not workspace.is_branch or (
                        origin and release.id not in [release.id for release in origin.get_releases()]
                    ):
                        if workspace.is_branch:
                            release.status = ReleaseStatus.deleting
                        try:
                            if not hard_delete or (hard_delete and release.metadata is not None):
                                # This fails if release.metadata is missing, safe to skip it for hard_delete cases
                                # We need to refresh the workspace to get the information fresh of the releases currently in the workspace
                                # `delete_release` will compare the current release with the other releases and if the release is already removed will not find the metadata in Redis
                                workspace = await Users.delete_release(workspace, release, dry_run=False, force=True)
                        except LiveReleaseProtectedException:
                            # If hard_delete=True, we should delete the release even if it's the Live Release
                            # Otherwise, we can mark the release as soft deleted
                            if hard_delete:
                                User._delete(release.id)
                            else:
                                await Users.delete_release_metadata(workspace, release)
                        else:
                            if release.id != workspace.id:
                                User._delete(release.id)
                        logging.info('"Deleted release {} for workspace {}'.format(release.id, workspace.id))
                    else:
                        log_deletion_error(f"Release {release.id} found but metadata is corrupted")

                # fallback for old workspaces / branches not using releases, we should remove this eventually
            except Exception as ex:
                log_deletion_error(f"Error deleting Releases: {str(ex)}")

        async def delete_pipes(hard_delete: bool) -> None:
            # HACK Crappy way to quickly fix a circular dependency
            from tinybird.views.api_pipes import PipeUtils

            logging.info(f"[Delete Workspace {workspace.id}] delete_pipes")

            for pipe in workspace._pipes:
                for snap_id, _ in Snapshot.get_items_for("parent_pipe_id", pipe.id):
                    try:
                        Snapshot._delete(snap_id)
                    except Exception as ex:
                        log_deletion_error(f"Error deleting snapshot {snap_id} from pipe {pipe.id}: {str(ex)}")

                try:
                    await PipeUtils.delete_pipe(workspace, pipe, job_executor, edited_by=None, hard_delete=hard_delete)
                except Exception as ex:
                    log_deletion_error(f"Error dropping pipe {pipe.id}: {str(ex)}")

        async def delete_datasources(hard_delete: bool, track_log: Optional[bool] = True) -> None:
            from tinybird.datasource_service import DatasourceService

            logging.info(f"[Delete Workspace {workspace.id}] delete_datasources")

            req_id = request_id or uuid.uuid4().hex

            for ds in workspace.get_datasources():
                if isinstance(ds, SharedDatasource):
                    continue

                try:
                    await DatasourceService.drop_datasource(
                        workspace=workspace,
                        ds=ds,
                        force=hard_delete,
                        branch_mode="None",
                        request_id=req_id,
                        job_executor=job_executor,
                        user_account=user,
                        edited_by=None,
                        hard_delete=hard_delete,
                        track_log=track_log,
                    )
                except Exception as ex:
                    if not hard_delete:
                        log_deletion_error(f"Error dropping datasource {ds.name} ({ds.id}): {str(ex)}")

        async def delete_cdk_service_account() -> None:
            try:
                await Users.delete_workspace_service_account(workspace)
            except Exception as ex:
                log_deletion_error(f"Error deleting CDK service account: {str(ex)}")

        async def delete_timeseries() -> None:
            # HACK Crappy way to quickly fix a circular dependency
            from tinybird.explorations_service import ExplorationsService

            logging.info(f"[Delete Workspace {workspace.id}] delete_timeseries")

            for expl_id in workspace.explorations_ids:
                expl = Exploration.get_by_id(expl_id)
                if not expl:
                    break
                try:
                    _ = await ExplorationsService.remove_and_save_workspace(expl)
                except Exception as ex:
                    log_deletion_error(f"Error deleting time series {expl.id}: {str(ex)}")

        async def leave_organization() -> None:
            # HACK Crappy way to quickly fix a circular dependency
            from tinybird.organization.organization_service import OrganizationService

            logging.info(f"[Delete Workspace {workspace.id}] leave_organization")

            if not workspace.organization_id:
                return
            try:
                await OrganizationService.remove_workspace_from_organization(workspace.organization_id, workspace.id)
            except Exception as ex:
                log_deletion_error(f"Error leaving organization {workspace.organization_id}: {str(ex)}")

        async def delete_playgrounds() -> None:
            logging.info(f"[Delete Workspace {workspace.id}] delete_playgrounds")
            try:
                playgrounds = Playground.get_all_by_owner(workspace.id)
                for playground in playgrounds:
                    await Playgrounds.delete_playground(playground)
            except Exception as ex:
                log_deletion_error(f"Error Removing playgrounds: {str(ex)}")

        async def cancel_subscription() -> None:
            # HACK Crappy way to quickly fix a circular dependency
            from tinybird.plans import PlansService

            logging.info(f"[Delete Workspace {workspace.id}] cancel subscription Stripe")

            try:
                await PlansService.cancel_subscription(workspace)

                # Let's mark as a DEV workspace to avoid any issues with the new pricing while being soft deleted
                await Users.change_workspace_plan(workspace, BillingPlans.DEV)
            except Exception as ex:
                log_deletion_error(f"Error cancelling subscription {workspace.plan}: {str(ex)}")

        async def delete_connectors() -> None:
            # HACK Crappy way to quickly fix a circular dependency
            from tinybird.ingest.cdk_utils import CDKUtils, is_cdk_service_datasource

            logging.info(f"[Delete Workspace {workspace.id}] delete_connectors")

            try:
                data_connectors = DataConnector.get_all_by_owner(workspace.id, limit=100)
                for data_connector in data_connectors:
                    try:
                        await data_connector.hard_delete()
                    except Exception as e:
                        log_deletion_error(f"Error deleting Data Connector {data_connector.id}: {str(e)}")
            except Exception as e:
                log_deletion_error(f"Error deleting Data Connectors: {str(e)}")

            for ds in workspace.get_datasources():
                try:
                    if is_cdk_service_datasource(ds.service):
                        await CDKUtils.delete_dag(workspace.id, ds.id)
                except Exception as e:
                    log_deletion_error(f"Error deleting DAG: {str(e)}")

        async def delete_workspace_or_env() -> None:
            logging.info(f"[Delete Workspace {workspace.id}] delete_workspace_or_env")
            try:
                if not hard_delete:
                    await Users.delete(workspace)
                else:
                    if await ch_database_exists(workspace.database_server, workspace.database):
                        await workspace._hard_delete(database=workspace.database)
                    else:
                        log_deletion_warning("Database not found")
                        User._delete(workspace.id)
            except Exception as ex:
                log_deletion_error(f"Error deleting workspace: {str(ex)}")
                raise ex

        deletion_tasks: List[asyncio.Task] = []

        def enqueue_task(task: Coroutine[Any, Any, None]) -> None:
            """Enqueues a task for parallel execution, taking care
            of logging any unhandled exception.
            """

            async def inner_task() -> None:
                try:
                    await asyncio.wait_for(task, timeout=None)
                except Exception as ex:
                    log_deletion_error(f"Unhandled error: {str(ex)}")

            deletion_tasks.append(asyncio.create_task(inner_task()))

        if hard_delete:
            await validate_hard_delete()

        if not workspace.is_branch:
            await unshare_datasources()
            # Refresh workspace to get the latest changes
            workspace = User.get_by_id(workspace.id)

        # Do as much as possible async
        enqueue_task(delete_playgrounds())
        enqueue_task(cancel_subscription())
        enqueue_task(delete_connectors())
        enqueue_task(delete_timeseries())
        enqueue_task(delete_pipes(hard_delete))
        enqueue_task(delete_releases(workspace, hard_delete))
        enqueue_task(leave_organization())
        enqueue_task(delete_branches())
        enqueue_task(delete_cdk_service_account())
        await asyncio.wait(deletion_tasks, return_when=asyncio.ALL_COMPLETED)

        await delete_datasources(hard_delete, track_log)
        delete_user_relations()

        # Finally, delete the workspace
        await delete_workspace_or_env()

        if tracer:
            from tinybird.workspace_service import WorkspaceService

            WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceDeleted", user)

    def get_token_for_scope(self, scope) -> Optional[str]:
        for t in self.tokens:
            if t.has_scope(scope):
                return t.token
        return None

    def delete(self) -> None:
        self.deleted = True

    def has_limit(self, name):
        return name in self.limits

    def delete_limit_config(self, name):
        if name in self.limits:
            del self.limits[name]

    def set_user_limit(self, name, value, prefix):
        self.limits[name] = (prefix, value)

    def get_limits(self, prefix):
        return {name: config[1] for name, config in self.limits.items() if config[0] == prefix}

    @property
    def is_active(self):
        return (not self.deleted) or self.is_tinybird

    @property
    def max_workspaces_limit(self):
        max_workspaces = self.limits.get("max_workspaces", ("workspaces", Limit.max_seats))
        return max_workspaces[1]

    def set_max_workspaces_limit(self, max_workspaces):
        self.limits["max_workspaces"] = ("workspaces", max_workspaces)

    @property
    def max_owned_limit(self) -> int:
        max_owned = self.limits.get("max_owned", ("workspaces", Limit.max_owned))
        return int(max_owned[1])

    def set_max_owned_workspaces(self, max_owned):
        self.limits["max_owned"] = ("workspaces", max_owned)

    def get_token_access_info(self, token_name_or_id: str) -> Optional[AccessToken]:
        for t in self.tokens:
            if t.token == token_name_or_id or t.name == token_name_or_id:
                return t
        return None

    def add_token(
        self, name: str, scope: str, resource=None, origin: Optional[TokenOrigin] = None, host: Optional[str] = None
    ) -> str:
        if self.get_token(name):
            raise ValueError(f'Token with name "{name}" already exists')
        if scope and not scopes.is_valid(scope):
            raise WrongScope(scope)
        ac = AccessToken(self.id, name, UserAccount.secret, origin=origin, host=host)
        if scope:
            ac.add_scope(scope, resource)
        self.tokens.append(ac)
        return ac.token

    def get_token(self, name: str):
        return next((x for x in self.tokens if x.name == name), None)

    def _get_cluster_used_in_oldest_workspace(self) -> Optional[CHCluster]:
        internal_cluster = public.get_public_user().cluster

        def is_internal(workspace_id: str) -> bool:
            w = User.get_by_id(workspace_id)
            return w is not None and w.cluster == internal_cluster and not w.is_branch

        try:
            user_workspaces_relations = UserWorkspaceRelationship.get_by_user(self.id)

            # Skip internal! (#7161)
            user_workspaces_relations = [r for r in user_workspaces_relations if not is_internal(r.workspace_id)]

        except UserWorkspaceRelationshipDoesNotExist:
            user_workspaces_relations = []

        if user_workspaces_relations:
            first_workspace_relation = min(user_workspaces_relations, key=lambda relation: relation.created_at)
            workspace = User.get_by_id(first_workspace_relation.workspace_id)
            return CHCluster(name=workspace.cluster or User.default_cluster, server_url=workspace.database_server)
        return None

    async def get_org_clusters(self) -> Optional[list[CHCluster]]:
        if "@" not in self.email:
            return None

        # Avoid circular import error
        from tinybird.organization.organization import Organizations

        org = await Organizations.get_by_email(self.email)

        if org is None:
            return None

        return [dedicated_cluster.cluster for dedicated_cluster in org.get_dedicated_clusters()]

    async def get_cluster(self) -> Optional[CHCluster]:
        """Gets the default cluster for the user based on:
        1. For accounts with dedicated infra -> their designated cluster
        2. If the user has previous workspaces -> the same cluster
        3. Finally, the default cluster
        """
        org_clusters = await self.get_org_clusters()
        if org_clusters is not None:
            for cluster in org_clusters:
                if await ch_server_is_reachable_and_has_cluster(
                    cluster.server_url, cluster.name
                ) or await ch_server_is_reachable_and_has_cluster(User.default_database_server, cluster.name):
                    return cluster

        cluster_from_oldest_workspace: Optional[CHCluster] = self._get_cluster_used_in_oldest_workspace()
        if cluster_from_oldest_workspace:
            is_reachable = await ch_server_is_reachable_and_has_cluster(
                cluster_from_oldest_workspace.server_url, cluster_from_oldest_workspace.name
            )
            if is_reachable:
                return cluster_from_oldest_workspace

        return CHCluster(name=User.default_cluster, server_url=User.default_database_server)

    async def has_organization_cluster(self) -> bool:
        clusters = await self.get_org_clusters()
        return clusters is not None

    @property
    def is_tinybird(self):
        return self.email.find("@") != -1 and self.email.split("@")[1] == DEFAULT_DOMAIN

    def get_integrations(self) -> List[IntegrationInfo]:
        return self.integrations or []

    def get_integration_info(self, integration_id: str) -> Optional[IntegrationInfo]:
        if not self.integrations:
            return None
        try:
            items = (info for info in self.integrations if info.integration_id == integration_id)
            return next(items, None)
        except Exception as ex:
            logging.exception(ex)
            return None

    def get_integration_info_by_type(self, _type: str) -> List[IntegrationInfo]:
        if not self.integrations:
            return []

        try:
            return [info for info in self.integrations if info.integration_type == _type]
        except Exception as ex:
            logging.exception(ex)
            return []


def add_region_selected(u):
    u["region_selected"] = u.get("region_selected", True)
    return u


UserAccount.__migrations__ = {1: add_region_selected}


def update_shared_datasources(datasources: List[Dict[str, Any]], metadata: "User") -> None:
    for ds in datasources:
        if ds.get("shared_with"):
            for workspace_id in ds["shared_with"]:
                workspace = User.get_by_id(workspace_id)
                if workspace:
                    shared_ds = workspace.get_datasource(ds["id"], include_read_only=True)
                    if shared_ds:
                        new_ds = metadata.get_datasource(ds["name"])
                        if new_ds:
                            shared_ds.id = new_ds.id
                            new_ds.shared_with.append(workspace.id)
                            new_ds.shared_with = list(set(new_ds.shared_with))
                            Users.update_datasource(workspace, shared_ds)
                            metadata.update_datasource(new_ds)
