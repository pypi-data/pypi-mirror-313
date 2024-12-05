import asyncio
import datetime as dt
import logging
import re
from datetime import datetime
from functools import partial
from typing import Callable, Dict, List, Optional
from urllib.parse import urlparse

import chevron
import google.auth
import google.cloud.storage as gcs
import sqlparse
from croniter import croniter
from google.api_core.exceptions import NotFound
from google.auth._default_async import default_async as _default_credentials_async
from google.oauth2 import _service_account_async, service_account

from tinybird.data_connector import DataConnectors
from tinybird.ingest.bigquery_dag import bigquery_dag_template
from tinybird.ingest.snowflake_dag import snowflake_dag_template
from tinybird.limits import Limit
from tinybird.plan_limits.cdk import CDKLimits
from tinybird.user import User as Workspace

CDK_IMAGE_REGISTRY: str = "europe-west3-docker.pkg.dev/tinybird-cdk-production/eu-west3-cdk/cdk"
MINIMUM_CRON_INTERVAL_SECONDS = 5 * 60
AUTH_SCOPES_GCS_RW = ["https://www.googleapis.com/auth/devstorage.read_write"]


class QueryParsingFailed(Exception):
    pass


class MoreThanOneStatement(QueryParsingFailed):
    def __init__(self):
        super().__init__("Query contains more than one SELECT statement. A single SELECT is supported")


class NotASelectStatement(QueryParsingFailed):
    def __init__(self):
        super().__init__("Not a SELECT statement")


class ContainsJoin(QueryParsingFailed):
    def __init__(self):
        super().__init__("Joins are not supported")


class InvalidRole(Exception):
    def __init__(self, role):
        self.message = f'Invalid role "{role}". Only alphanumeric and underscore characters allowed'
        super().__init__(self.message)


def default_credentials(scopes: List[str]):
    creds, _ = google.auth.default(scopes)
    return creds


def default_credentials_async(scopes: List[str]):
    creds, _ = _default_credentials_async(scopes)
    return creds


def as_jinja_template(string: str) -> str:
    return "{{ " + string + " }}"


def extract_field_names_from_statement(statement, service=None) -> List[str]:
    try:
        field_names = []
        for token in statement.tokens:
            _type = type(token)
            if _type == sqlparse.sql.IdentifierList:
                for identifier in token.get_identifiers():
                    if isinstance(identifier, sqlparse.sql.Identifier):
                        field_names.append(identifier.get_name())
                    else:
                        # The identifier could not be a sqlparse.sql.Identifier
                        # if it's for example a reserved keyword. In this case
                        # we get the value and let the external DB manage it.
                        field_names.append(identifier.value)
            elif _type == sqlparse.sql.Identifier:
                field_names.append(token.get_name())
            elif token.ttype == sqlparse.tokens.Name.Builtin:
                allowed_field_names_for_sf = ["date", "timestamp"]
                if token.normalized in allowed_field_names_for_sf and service == DataConnectors.SNOWFLAKE:
                    # Snowflake won't allow backticked fields. We need an exception
                    # for the Snowflake service and some field names (the most common
                    # ones among the built-ins).
                    # We may need to add other exceptions in the future.
                    field_names.append(token.normalized)
                else:
                    raise QueryParsingFailed(
                        f"Invalid query field {token.normalized}. It must be quoted using backticks (`{token.normalized}`)"
                    )
            elif token.normalized == "FROM":
                break

        if len(field_names) == 0:
            raise QueryParsingFailed("Unable to parse query")
        else:
            return [name.rpartition(".")[2] if "." in name else name for name in field_names]
    except AttributeError as err:
        raise QueryParsingFailed("Unable to parse query") from err


def get_field_names_from_query(query: str, service: Optional[str] = None) -> List[str]:
    """
    >>> get_field_names_from_query('select `a` from table')
    ['a']
    >>> get_field_names_from_query('select `a`, `b` from table')
    ['a', 'b']
    >>> get_field_names_from_query('select a, b from table')
    ['a', 'b']
    >>> get_field_names_from_query('select a, `b` from table')
    ['a', 'b']
    >>> get_field_names_from_query('select `a` as `b` from table')
    ['b']
    >>> get_field_names_from_query('select `a` as `b`, `c` from table')
    ['b', 'c']
    >>> get_field_names_from_query('SELECT product_id, user_id, event, extra_data FROM orders')
    ['product_id', 'user_id', 'event', 'extra_data']
    >>> get_field_names_from_query('SELECT date, product_id, user_id, event, extra_data FROM orders')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.QueryParsingFailed: Invalid query field date. It must be quoted using backticks (`date`)
    >>> get_field_names_from_query('SELECT product_id, user_id, date, event, extra_data FROM orders')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.QueryParsingFailed: Invalid query field date. It must be quoted using backticks (`date`)
    >>> get_field_names_from_query('SELECT product_id, user_id, timestamp, event, extra_data FROM orders')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.QueryParsingFailed: Invalid query field timestamp. It must be quoted using backticks (`timestamp`)
    >>> get_field_names_from_query('SELECT product_id, user_id, date, event, extra_data FROM orders', 'snowflake')
    ['product_id', 'user_id', 'date', 'event', 'extra_data']
    >>> get_field_names_from_query('SELECT product_id, user_id, timestamp, event, extra_data FROM orders', 'snowflake')
    ['product_id', 'user_id', 'timestamp', 'event', 'extra_data']
    >>> get_field_names_from_query('SELECT `date`, product_id, user_id, event, extra_data FROM orders')
    ['date', 'product_id', 'user_id', 'event', 'extra_data']
    >>> get_field_names_from_query('SELECT INT_COLUMN FROM TINYBIRD.SAMPLES.TEST')
    ['INT_COLUMN']
    >>> get_field_names_from_query('SELECT A FROM TINYBIRD.SAMPLES.TEST')
    ['A']
    >>> get_field_names_from_query('SELECT A, language, C FROM TINYBIRD.SAMPLES.TEST')
    ['A', 'language', 'C']
    >>> get_field_names_from_query('''SELECT A, replace(myfield2, '\\'', '\\'\\'') as replacefield, C FROM TINYBIRD.SAMPLES.TEST''')
    ['A', 'replacefield', 'C']
    """
    try:
        statements = sqlparse.parse(query)
        if len(statements) > 1:
            raise MoreThanOneStatement()
        if statements[0].get_type() != "SELECT":
            raise NotASelectStatement()
        for token in statements[0]:
            if token.ttype is sqlparse.tokens.Keyword and "JOIN" in token.value.upper():
                raise ContainsJoin()
        return extract_field_names_from_statement(statements[0], service)
    except AttributeError as err:
        raise QueryParsingFailed("Unable to parse query") from err


def get_gcs_bucket_uri(workspace_id: str) -> str:
    return f"gcs://{CDKUtils.gcs_export_bucket}/{workspace_id}"


def get_cdk_image(workspace: Workspace) -> str:
    cdk_version = normalize_version(workspace.get_limits(prefix="cdk").get("cdk_version", Limit.cdk_version))
    return f"{CDK_IMAGE_REGISTRY}:{cdk_version}"


def get_env_for_snowflake(env: Dict[str, Optional[str]]) -> Dict[str, str]:
    env = env.copy()
    for key in (
        "SF_ACCOUNT",
        "SF_USER",
        "SF_PWD",
        "SF_ROLE",
        "SF_WAREHOUSE",
        "SF_DATABASE",
        "SF_SCHEMA",
        "SF_STAGE",
        "SF_INTEGRATION",
    ):
        if env.get(key) is None:
            env[key] = ""
    return env  # type: ignore


def validate_snowflake_role(role: str) -> None:
    """
    >>> validate_snowflake_role('a_ROLE')
    >>> validate_snowflake_role('a_ROLE with')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.InvalidRole: Invalid role "a_ROLE with". Only alphanumeric and underscore characters allowed
    >>> validate_snowflake_role('a_ROLE;do_something')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.InvalidRole: Invalid role "a_ROLE;do_something". Only alphanumeric and underscore characters allowed
    >>> validate_snowflake_role('a_"ROLE"')
    Traceback (most recent call last):
    ...
    tinybird.ingest.cdk_utils.InvalidRole: Invalid role "a_"ROLE"". Only alphanumeric and underscore characters allowed
    """
    if not re.fullmatch("\w+", role):
        raise InvalidRole(role)


AIRFLOW_ONCE_SCHEDULE_INTERVAL_NAME = "@once"


class CDKUtils:
    gcs_export_bucket = None
    gcs_composer_bucket = None
    api_host = None
    project_id = None
    group_email = None
    cdk_webserver_url: str = ""  # So mypy doesn't force an optional everywhere
    cdk_service_account_key_location: str = "local"

    @classmethod
    def config(
        cls,
        gcs_export_bucket: str,
        gcs_composer_bucket: str,
        api_host: str,
        project_id: str,
        cdk_webserver_url: str,
        cdk_service_account_key_location: str,
        cdk_group_email: str,
    ):
        cls.gcs_export_bucket = gcs_export_bucket
        cls.gcs_composer_bucket = gcs_composer_bucket
        cls.api_host = api_host
        cls.project_id = project_id
        cls.cdk_webserver_url = cdk_webserver_url
        cls.cdk_service_account_key_location = cdk_service_account_key_location
        cls.group_email = cdk_group_email

    @classmethod
    def get_credentials_provider(cls) -> Callable:
        key_filename = cls.cdk_service_account_key_location
        if not key_filename or key_filename == "local":
            return default_credentials
        return partial(service_account.Credentials.from_service_account_file, key_filename)

    @classmethod
    def get_credentials_provider_async(cls) -> Callable:
        key_filename = cls.cdk_service_account_key_location
        if not key_filename or key_filename == "local":
            return default_credentials_async
        return partial(_service_account_async.Credentials.from_service_account_file, key_filename)

    @classmethod
    def get_credentials(cls, scopes: List[str]):
        return cls.get_credentials_provider()(scopes=scopes)

    @classmethod
    def get_project_id(cls) -> str:
        if cls.project_id is None:
            raise AttributeError("project_id")
        return cls.project_id

    @classmethod
    def get_group_email(cls) -> str:
        if cls.group_email is None:
            raise AttributeError("group_email")
        return cls.group_email

    @classmethod
    async def delete_dag(cls, workspace_id: str, datasource_id: str) -> None:
        dag_path = f"dags/{workspace_id}/{datasource_id}_dag.py"
        credentials = cls.get_credentials(AUTH_SCOPES_GCS_RW)
        bucket = gcs.Client(cls.project_id, credentials).bucket(cls.gcs_composer_bucket)

        def sync_delete_dag():
            try:
                bucket.blob(dag_path).delete()
                logging.info(f"DAG deleted in {dag_path}")
            except NotFound as e:
                logging.warning(f"Unable to delete DAG: {e}")

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_delete_dag)
        # await asyncio.to_thread(sync_delete_dag)

    @classmethod
    async def upload_dag(cls, dag: str, workspace_id: str, datasource_id: str) -> None:
        dag_path = f"dags/{workspace_id}/{datasource_id}_dag.py"
        credentials = cls.get_credentials(AUTH_SCOPES_GCS_RW)
        bucket = gcs.Client(cls.project_id, credentials).bucket(cls.gcs_composer_bucket)

        def upload_blob_from_memory():
            bucket.blob(dag_path).upload_from_string(dag)
            logging.info(f"DAG uploaded to {dag_path}")

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, upload_blob_from_memory)
        # await asyncio.to_thread(upload_blob_from_memory)

    @classmethod
    def prepare_dag(
        cls,
        service_name: str,
        workspace: Workspace,
        datasource_id: str,
        tb_token: str,
        connection_parameters: dict,
        ingest_now: bool = False,
    ) -> str:
        hostname = str(urlparse(cls.api_host).netloc)
        # Grab the workspace's parent if it is a branch otherwise there won't be a pool with that name.
        pool_id = workspace.origin if workspace.origin else workspace.id

        cron_expression_str = connection_parameters["CRON"]
        # We don't know what's associated to the 'CRON' key so we need to be defensive and check for nulls
        if cron_expression_str and croniter.is_valid(cron_expression_str):
            cron = croniter(cron_expression_str, start_time=datetime.now(dt.UTC))
            start_dt: dt.datetime = cron.get_prev(dt.datetime) - dt.timedelta(seconds=1)
            start_date = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            start_date = (
                "1987-03-13 17:15:00"  # Set it up to the dawn of time so no wait happens whenever it's triggered
            )

        values = {
            "ENVIRONMENT_TEMPLATE": as_jinja_template("var.value.environment"),
            "SENTRY_CONN_TEMPLATE": as_jinja_template("conn.tb_sentry_dsn.get_uri()"),
            "TB_LOGS_ENDPOINT_TEMPLATE": as_jinja_template(f"conn.get('logs-{hostname}').host"),
            "TB_LOGS_TOKEN_TEMPLATE": as_jinja_template(f"conn.get('logs-{hostname}').password"),
            "TB_LOGS_DATASOURCE_TEMPLATE": as_jinja_template(f"conn.get('logs-{hostname}').extra_dejson.datasource_id"),
            "ID": f"{workspace.id}_{datasource_id}",
            "TB_TOKEN": tb_token,  # TODO: create a good token for this purpose
            "GCS_BUCKET": cls.gcs_export_bucket,
            "START_DATE": start_date,
            "TB_CDK_ENDPOINT": cls.api_host,
            "TB_WORKSPACE_ID": workspace.id,
            "TB_DATASOURCE_ID": datasource_id,
            "ROW_LIMIT": CDKLimits.max_row_limit.get_limit_for(workspace),
            "SERVICE": service_name,
            "POOL_ID": pool_id,
            "CDK_IMAGE": get_cdk_image(workspace),
            **connection_parameters,
        }

        if ingest_now:
            # Set the start_date value to an absurd date very very long time ago :)
            # Since we don't allow catching-up, we should only run this once.
            values["START_DATE"] = "1987-03-13 17:15:00"

        template_based_on_service = {
            "bigquery": bigquery_dag_template,
            DataConnectors.SNOWFLAKE: snowflake_dag_template,
        }

        return chevron.render(template_based_on_service[service_name], values)


def is_cdk_service_datasource(service_name):
    return service_name in [DataConnectors.BIGQUERY, DataConnectors.SNOWFLAKE]


def is_valid_cron_expression(expr: str) -> bool:
    """
    >>> is_valid_cron_expression('*/5 * * * *')
    True
    >>> is_valid_cron_expression('Hola * * * *')
    False
    >>> is_valid_cron_expression('@on-demand')
    True
    >>> is_valid_cron_expression('@once')
    True
    """
    if expr == "@on-demand" or expr == "@once":
        return True
    if not croniter.is_valid(expr):
        return False
    iter = croniter(expr)
    t1 = iter.get_next()
    t2 = iter.get_next()
    delta = t2 - t1
    if delta < MINIMUM_CRON_INTERVAL_SECONDS:
        return False
    return True


def normalize_cron_expression(expr):
    """
    >>> normalize_cron_expression('*/5 * * * *')
    '*/5 * * * *'
    >>> normalize_cron_expression('@on-demand')
    '@once'
    >>> normalize_cron_expression('@once')
    '@once'
    """
    return "@once" if expr == "@on-demand" else expr


def normalize_version(version: str) -> str:
    return version if version.startswith("v") else f"v{version}"
