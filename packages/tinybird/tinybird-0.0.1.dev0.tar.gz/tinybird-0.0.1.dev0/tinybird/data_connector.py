import asyncio  # noqa: F401. Flake said it's imported but unused, but it's used in the doctests
import logging
import string
import uuid
from collections import ChainMap
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

from pydantic import BaseModel, ValidationError

from tinybird.ch import url_from_host
from tinybird.ch_utils.engine import engine_full_from_dict
from tinybird.connector_settings import (
    DATA_CONNECTOR_SETTINGS,
    DataConnectors,
    DataConnectorSetting,
    DataConnectorType,
    DataLinkerSettings,
    DataSensitiveSettings,
    DataSinkSettings,
    DynamoDBConnectorSetting,
    S3IAMConnectorSetting,
)
from tinybird.constants import KAFKA_BOOTSTRAP_SERVER_TO_SERVER_GROUP
from tinybird.data_connectors.credentials import IAMRoleAWSCredentials
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.gatherer_common import get_gatherer_config_from_workspace
from tinybird.gc_scheduler.constants import GCloudScheduleException
from tinybird.gc_scheduler.scheduler_jobs import GCloudSchedulerJobs
from tinybird.model import RedisModel, retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.providers.auth import get_auth_provider
from tinybird.providers.aws.dynamodb import (
    DYNAMODB_MANDATORY_COLUMNS,
    DYNAMODB_MANDATORY_COLUMNS_JSONPATHS,
    DynamoDBTableKeySchema,
)
from tinybird.providers.aws.exceptions import AuthenticationFailed, Forbidden, UnexpectedBotoClientError
from tinybird.validation_utils import handle_pydantic_errors

if TYPE_CHECKING:
    from tinybird.datasource import Datasource
    from tinybird.pipe import Pipe
    from tinybird.user import User, Users

DEFAULT_SERVER_GROUP = "tbakafka"


class DataConnectorService(BaseModel):
    service: DataConnectors
    name: str

    @classmethod
    def validate(cls, *args, **kwargs) -> "DataConnectorService":
        try:
            return cls(*args, **kwargs)
        except ValidationError as e:
            raise InvalidSettingsException(handle_pydantic_errors(e)) from None


class DataConnectorChannels:
    TBAKAFKA_CONNECTOR = "tbakafka_connector_channel"
    TBAKAFKA_LINKER = "tbakafka_linker_channel"


class DataSinkSettingsCommon:
    branch = ["branch", "origin"]


class InvalidSettingsException(Exception):
    pass


class DuplicatedConnectorNameException(Exception):
    pass


class WrongConnectorOriginException(Exception):
    pass


class DataSourceNotConnected(Exception):
    # This exception should not be exposed to the end user
    pass


class ResourceNotConnected(Exception):
    pass


class DataConnectorNotFound(Exception):
    pass


class InvalidHost(Exception):
    pass


class DataLinkerValidSettings:
    kafka = [
        "tb_max_wait_seconds",
        "tb_max_wait_records",
        "tb_max_wait_bytes",
        "tb_max_partition_lag",
        *DataLinkerSettings.kafka,
    ]


MEGABYTE = 1024**2


class DataConnectorSchema:
    SCHEMAS = {
        "kafka": """
            value String,
            topic LowCardinality(String),
            partition Int16,
            offset Int64,
            timestamp DateTime,
            key String""",
        "kafka_with_prefix": """
            __value String,
            __topic LowCardinality(String),
            __partition Int16,
            __offset Int64,
            __timestamp DateTime,
            __key String""",
        "dynamodb": ", ".join(DYNAMODB_MANDATORY_COLUMNS),
        "default": "value String",
    }

    @staticmethod
    def get_schema(service, kafka_metadata_prefix=False, kafka_store_headers=False):
        if kafka_metadata_prefix:
            service += "_with_prefix"
        if service in DataConnectorSchema.SCHEMAS:
            schema = DataConnectorSchema.SCHEMAS[service]
            if kafka_store_headers:
                schema += ", __headers Map(String, String)"
            return schema
        return DataConnectorSchema.SCHEMAS["default"]

    @staticmethod
    def get_jsonpaths(service: str):
        if service == DataConnectors.AMAZON_DYNAMODB:
            return ", ".join(DYNAMODB_MANDATORY_COLUMNS_JSONPATHS)
        return ""


def normalize_path(path: str):
    norm_path = (
        path.replace("$.", "")
        .replace(".", "_")
        .replace("-", "_")
        .replace("[:]", "_")
        .replace("['", "")
        .replace("']", "")
        .replace("$", "DOLLAR_SIGN_")
    )
    norm_path = norm_path[:-1] if norm_path.endswith("_") else norm_path
    sql_friendly_characters = string.ascii_letters + string.digits + "_"
    norm_path = norm_path.translate({ord(c): c if c in sql_friendly_characters else "_" for c in norm_path})
    return norm_path


class DataConnectorEngine:
    @staticmethod
    def get_dynamodb_engine(schema, ddb_key_schemas: dict[str, DynamoDBTableKeySchema], engine_args=None) -> str:
        if engine_args is None:
            engine_args = {}

        def get_default_sorting_key():
            default_sorting_key = normalize_path(ddb_key_schemas.get("HASH").attribute_name)
            range_schema = ddb_key_schemas.get("RANGE", None)
            if range_schema:
                default_sorting_key += ", " + normalize_path(range_schema.attribute_name)
            return default_sorting_key

        def get_default_partition_key():
            return "toYYYYMM(toDateTime64(_timestamp, 3))"

        def check_if_sorting_key_definition_includes_ddb_keys(sorting_key: str):
            ddb_keys = ddb_key_schemas.values()
            sorting_columns = [key.strip() for key in sorting_key.split(",")]

            for ddb_key in ddb_keys:
                if normalize_path(ddb_key.attribute_name) not in sorting_columns:
                    raise InvalidSettingsException(ddb_key.attribute_name)

        opts = {
            "sorting_key": engine_args.get("sorting_key", get_default_sorting_key()),
            "partition_key": engine_args.get("partition_key", get_default_partition_key()),
        }

        check_if_sorting_key_definition_includes_ddb_keys(opts["sorting_key"])

        for k in engine_args:
            if k != "type" and k not in opts:
                opts[k] = engine_args[k]

        engine_full = engine_full_from_dict("ReplacingMergeTree", opts, schema=schema)
        return engine_full

    @staticmethod
    def get_kafka_engine(persistent, ttl, kafka_metadata_prefix, engine_args=None, schema=None):
        if engine_args is None:
            engine_args = {}

        def get_default_sorting_key():
            return "__timestamp" if kafka_metadata_prefix else "timestamp"

        def get_default_partition_key():
            return "toYYYYMM(__timestamp)" if kafka_metadata_prefix else "toYYYYMM(timestamp)"

        if not persistent:
            return engine_full_from_dict("null", {}, schema)

        opts = {
            "sorting_key": engine_args.get("sorting_key", get_default_sorting_key()),
            "partition_key": engine_args.get("partition_key", get_default_partition_key()),
            "ttl": ttl,
        }

        # adding missing engine properties, that don't need default values
        for k in engine_args:
            if k != "type" and k not in opts:
                opts[k] = engine_args[k]

        engine_full = engine_full_from_dict(engine_args.get("type", "MergeTree"), opts, schema=schema)
        return engine_full


class KafkaSettings:
    MAX_WAIT_SECONDS = 6
    MAX_WAIT_RECORDS = 1_000_000_000
    MAX_WAIT_BYTES = 1024 * MEGABYTE
    MAX_PARTITION_LAG = 50_000
    BOOTSTRAP_SERVERS = "localhost:9092"
    PREVIEW_MAX_RECORDS = 10
    PREVIEW_POLL_TIMEOUT_MS = 5000
    AUTO_OFFSET_RESET = "latest"
    TARGET_PARTITIONS = "auto"
    MESSAGE_SIZE_LIMIT_BYTES = 10 * MEGABYTE


VALID_AUTO_OFFSET_RESET = {"latest", "earliest", "error"}


class DataConnector(RedisModel):
    __namespace__ = "dataconnector"
    __owner__ = "user_id"

    __props__ = ["id", "user_id", "name", "service", "settings"]
    __fast_scan__ = True

    def __init__(self, **config: Union[str, Optional[str], dict]) -> None:
        self.id = None
        self.user_id: Optional[str] = None
        self.name = None
        self.service: str
        self.settings: Dict[str, Any] = {}

        super().__init__(**config)

    def __getstate__(self):
        self.updated_at = datetime.now()
        return self.__dict__.copy()

    @property
    def all_settings(self):
        return {
            setting.replace("tb_", "") if setting.startswith("tb_") else setting: value
            for setting, value in self.settings.items()
        }

    @property
    def service_settings(self):
        return {setting: value for setting, value in self.settings.items() if setting.startswith(f"{self.service}_")}

    @property
    def channel(self):
        return DataConnectorChannels.TBAKAFKA_CONNECTOR

    @property
    def public_settings(self):
        return {
            k.replace(self.service, ""): v
            for k, v in self.settings.items()
            if k not in getattr(DataSensitiveSettings, self.service)
        }

    def to_json(self):
        linkers = self.get_linkers()
        sinks = self.get_sinks()

        return {
            "id": self.id,
            "name": self.name,
            "service": self.service,
            "settings": self.all_settings,
            "linkers": [linker.to_json() for linker in linkers],
            "sinks": [sink.to_json() for sink in sinks],
        }

    def to_dict(self):
        linkers = self.get_linkers()
        sinks = self.get_sinks()

        return {
            "id": self.id,
            "name": self.name,
            "service": self.service,
            "settings": self.settings,
            "updated_at": self.updated_at,
            "linkers": [linker.to_dict() for linker in linkers],
            "sink": [sink.to_dict() for sink in sinks],
        }

    @property
    def validated_settings(self) -> DataConnectorSetting:
        service = cast(DataConnectorType, self.service)  # To make mypy happy
        return DataConnector.validate_service_settings(service, self.settings)

    @staticmethod
    def get_all_by_owner_and_service(owner: str, service: str) -> List["DataConnector"]:
        all_data_connectors = DataConnector.get_all_by_owner(owner)
        return [data_connector for data_connector in all_data_connectors if data_connector.service == service]

    @staticmethod
    def get_by_owner_and_name(owner: str, name: str) -> Union["DataConnector", None]:
        all_data_connectors = DataConnector.get_all_by_owner(owner)
        return next(
            (data_connector for data_connector in all_data_connectors if data_connector.name == name),
            None,
        )

    @staticmethod
    def get_all_linker_tokens_by_owner(owner: str) -> List[str]:
        all_data_connectors = DataConnector.get_all_by_owner(owner)
        tokens: set[str] = set()
        for dc in all_data_connectors:
            linkers = dc.get_linkers()
            for linker in linkers:
                token = linker.settings.get("tb_token")
                if token:
                    tokens.add(token)
        return list(tokens)

    def get_linkers(self):
        return DataLinker.get_all_by_owner(self.id)

    def get_sinks(self) -> List["DataSink"]:
        return DataSink.get_all_by_owner(self.id)

    def update_name(self, name):
        if name:
            self.name = name

    def update_settings(self, settings):
        self.settings.update(settings)

    async def hard_delete(self):
        linkers = self.get_linkers()
        sinks = self.get_sinks()

        for linker in linkers:
            DataLinker._delete(linker.id)
        for sink in sinks:
            await sink.delete()

        DataConnector._delete(self.id)
        await DataConnector.publish(self.id, self.service)

    @classmethod
    async def publish(cls, connector_id, connector_service=None):
        if connector_service in [DataConnectors.KAFKA, DataConnectors.AMAZON_DYNAMODB]:
            receivers = await cls.publish_with_retry(DataConnectorChannels.TBAKAFKA_CONNECTOR, connector_id)
            logging.info(f"Kafka publish to connector channel received by {receivers} agents")

    @staticmethod
    def get_config(id):
        connector = DataConnector.get_by_id(id)
        linkers = DataLinker.get_all_by_owner(connector.id)

        config = {
            f"{linker.id}": {
                "id": linker.id,
                "name": f"{connector.name}_{linker.name}",
                **connector.settings,
                **linker.settings,
            }
            for linker in linkers
        }

        return config

    @staticmethod
    def add_connector(
        workspace: "User", name: str, service: DataConnectors, settings: Optional[dict] = None
    ) -> "DataConnector":
        uid = str(uuid.uuid4())

        if not settings:
            settings = {}

        DataConnectorService.validate(service=service, name=name)
        data_connector_settings = DataConnector.validate_service_settings(service=service, settings=settings)

        if workspace.origin:
            raise WrongConnectorOriginException("Data Connectors can only be created in the main workspace")

        if DataConnector.is_duplicated_name(name, workspace):
            raise DuplicatedConnectorNameException("Duplicated data connector name")

        data_connector = DataConnector(
            id=uid,
            user_id=workspace.id,
            name=name,
            service=service,
            settings=data_connector_settings.model_dump(exclude_none=True),
        )

        data_connector.save()
        return data_connector

    @staticmethod
    def is_duplicated_name(name: str, user: "User") -> bool:
        return DataConnector.get_by_owner_and_name(user.id, name) is not None

    @staticmethod
    def validate_service_settings(service: DataConnectors, settings: Optional[dict] = None) -> DataConnectorSetting:
        from tinybird.views.base import ApiHTTPError

        if not settings:
            settings = {}
        try:
            connector_settings = DATA_CONNECTOR_SETTINGS[service](**settings)
            # validate credentials for s3iam role
            # we have to do it here because providers/auth.py is a wrapper
            # for google/AWS session handlers and we don't want to include them
            # in the CLI :sadpanda:
            if isinstance(connector_settings, S3IAMConnectorSetting) or isinstance(
                connector_settings, DynamoDBConnectorSetting
            ):
                DataConnector.validate_credentials(connector_settings.credentials)

        except ValidationError as e:
            raise InvalidSettingsException(handle_pydantic_errors(e)) from None
        except Forbidden as e:
            raise ApiHTTPError(403, str(e)) from None
        except UnexpectedBotoClientError:
            raise ApiHTTPError(500, "Internal server error") from None
        except AuthenticationFailed as e:
            raise ApiHTTPError(401, str(e)) from None

        return connector_settings

    @staticmethod
    def validate_credentials(credentials: IAMRoleAWSCredentials) -> None:
        aws_session = get_auth_provider().get_aws_session()
        aws_session.assume_role(role_arn=credentials.role_arn, external_id=credentials.external_id)

    @staticmethod
    async def validate_kafka_host(host: str, application_settings: Dict[str, Any]):
        from tinybird.views.utils import validate_kafka_host

        try:
            await validate_kafka_host(host.strip(), application_settings)
        except Exception as err:
            raise InvalidHost(
                f"{err}. Please double-check and try again, if you believe should be valid contact us at support@tinybird.co"
            )

    @staticmethod
    def get_user_data_connectors(user_id: str):
        def _get_linkers(connector_id):
            return [
                {
                    "id": data_linker.id,
                    "data_connector_id": data_linker.data_connector_id,
                    "datasource_id": data_linker.datasource_id,
                    "name": data_linker.name,
                    "settings": data_linker.all_settings,
                }
                for data_linker in DataLinker.get_all_by_owner(connector_id)
            ]

        def _get_sinks(connector_id):
            return [
                {
                    "id": data_sink.id,
                    "data_connector_id": data_sink.data_connector_id,
                    "resource_id": data_sink.resource_id,
                    "name": data_sink.name,
                    "settings": data_sink.public_settings,
                }
                for data_sink in DataSink.get_all_by_owner(connector_id)
            ]

        return [
            {
                "id": data_connector.id,
                "name": data_connector.name,
                "user_id": data_connector.user_id,
                "service": data_connector.service,
                "settings": data_connector.all_settings,
                "linkers": _get_linkers(data_connector.id),
                "sinks": _get_sinks(data_connector.id),
            }
            for data_connector in DataConnector.get_all_by_owner(user_id)
            if data_connector.service
        ]

    @staticmethod
    def get_public_settings_by_datasource(user_id: str):
        def _get_settings(data_connector: DataConnector) -> Dict[Optional[str], Any]:
            return {
                data_linker.datasource_id: {
                    "connector": data_connector.id,
                    "service": data_connector.service,
                    **data_linker.service_settings,
                }
                for data_linker in DataLinker.get_all_by_owner(data_connector.id)
                if data_linker
            }

        return dict(
            ChainMap(
                *list(
                    map(
                        lambda x: _get_settings(x),
                        DataConnector.get_all_by_owner(user_id),
                    )
                )
            )
        )

    @staticmethod
    def get_user_gcscheduler_connectors(workspace_id):
        connectors = [
            data_connector
            for data_connector in DataConnector.get_all_by_owner(workspace_id)
            if data_connector.service == DataConnectors.GCLOUD_SCHEDULER
        ]
        if len(connectors) > 1:
            raise Exception("More than one GC Scheduler connector for workspace")
        return connectors[0] if connectors else None

    @staticmethod
    def get_all_config_by_linker_for_service(service: str, server_group: str, Users: "Users"):
        """
        >>> from tinybird.user import User, UserAccount, Users
        >>> u = UserAccount.register('kafka_test@example.com', 'pass')
        >>> w = User.register('kafka_test', admin=u.id)
        >>>
        >>> ds = Users.add_datasource_sync(w, 'test')
        >>> DataConnector.get_all_config_by_linker_for_service("kafka", "test", None)
        {}
        >>> con = DataConnector.add_connector(w, "test", "kafka", {"kafka_bootstrap_servers": "asdf", "kafka_sasl_plain_username": "asdf", "kafka_sasl_plain_password": "asdf", "kafka_server_group": "test_server_group"})
        >>> linker = asyncio.run(DataLinker.add_linker(con, ds, w, {"server_group": "test_server_group", "tb_clickhouse_host": "wadus"}))
        >>> DataConnector.get_all_config_by_linker_for_service("kafka", "tbakafka", None)
        {}
        >>> DataConnector.get_all_config_by_linker_for_service("kafka", "test_server_group", None).get(linker.id, None).get("tb_clickhouse_host", None)
        'wadus'
        """
        # Dependency injection for the "Users" parameter to avoid circular import
        data_connectors = DataConnector.get_all()
        data_linkers = DataLinker.get_all()
        workspaces_cache: Dict[str, "User"] = {}
        config_by_linker = {}

        for data_connector in data_connectors:
            if data_connector.service != service:
                continue

            def filter_linkers(data_linker: "DataLinker", ws: Optional["User"] = None):
                # For now, we don't want to inform tbkafka about the linkers of the branches
                if ws and ws.is_branch_or_release_from_branch:
                    return False

                if data_linker.data_connector_id != data_connector.id:  # noqa: B023
                    return False

                linker_server_group = data_linker.all_settings.get("server_group", None)
                if not linker_server_group and ws is not None and ws.kafka_server_group:
                    linker_server_group = ws.kafka_server_group

                if not linker_server_group:
                    for override in KAFKA_BOOTSTRAP_SERVER_TO_SERVER_GROUP:
                        kafka_bootstrap_servers = data_connector.settings.get(  # noqa: B023
                            "kafka_bootstrap_servers", []
                        )
                        if kafka_bootstrap_servers and override["bootstrap_server"] in kafka_bootstrap_servers:
                            linker_server_group = override["server_group"]
                if not linker_server_group:
                    linker_server_group = DEFAULT_SERVER_GROUP
                return linker_server_group == server_group

            if not (workspace := workspaces_cache.get(data_connector.user_id, None)):  # type: ignore
                try:
                    workspace = Users.get_by_id(data_connector.user_id)  # type: ignore
                    workspaces_cache[data_connector.user_id] = workspace  # type: ignore
                except Exception:
                    pass

            data_linkers_for_connector = [
                data_linker for data_linker in data_linkers if filter_linkers(data_linker, workspace)
            ]

            linker_config = DataConnector.get_linker_config_for_data_connector(
                data_connector, data_linkers_for_connector, workspace
            )
            for linker in linker_config.values():
                if linker and not linker.get("tb_clickhouse_host", None):
                    linker["tb_clickhouse_host"] = url_from_host(
                        Users.get_by_id(data_connector.user_id).database_server  # type: ignore
                    )
            config_by_linker.update(linker_config)
        return config_by_linker

    @staticmethod
    def get_linker_config_for_data_connector(
        data_connector: "DataConnector", data_linkers: List["DataLinker"], workspace: Optional["User"] = None
    ) -> Dict[str, Dict[str, Any]]:
        gatherer_config = get_gatherer_config_from_workspace(workspace)
        if workspace:
            avro_as_dict = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.DECODE_AVRO_AS_DICT, workspace.id, workspace.feature_flags
            )
        else:
            avro_as_dict = False

        return {
            data_linker.id: {
                "id": data_linker.id,
                "name": f"{data_connector.name}_{data_linker.name}",
                "connector_updated_at": data_connector.updated_at,
                "linker_updated_at": data_linker.updated_at,
                "workspace_id": data_connector.user_id,
                "gatherer_config": gatherer_config,
                **data_connector.settings,
                **data_linker.settings,
                "avro_as_dict": avro_as_dict,
            }
            for data_linker in data_linkers
        }


class DataLinker(RedisModel):
    __namespace__ = "datalinker"
    __owner__ = "data_connector_id"

    __indexes__ = ["datasource_id"]

    __props__ = [
        "id",
        "name",
        "data_connector_id",
        "datasource_id",
        "settings",
        "service",
    ]
    __fast_scan__ = True

    def __init__(self, **config: Union[str, Optional[str], dict]) -> None:
        self.id = None
        self.name = None
        self.data_connector_id = None
        self.datasource_id = None
        self.settings: Dict[str, Any] = {}
        self.service = None

        super().__init__(**config)

    def __getstate__(self):
        self.updated_at = datetime.now()
        return self.__dict__.copy()

    @property
    def all_settings(self):
        migrated_settings = {
            "clickhouse_host": "",
            "clickhouse_table": "",
        }
        current_settings = {
            setting.replace("tb_", "") if setting.startswith("tb_") else setting: value
            for setting, value in self.settings.items()
        }

        default_settings = [
            ("server_group", None),
            ("message_size_limit", None),
        ]
        for setting, default_value in default_settings:
            if setting not in current_settings:
                current_settings[setting] = default_value

        return {**migrated_settings, **current_settings}

    @property
    def public_settings(self):
        return {
            k.replace(self.service, ""): v
            for k, v in self.settings.items()
            if k not in getattr(DataSensitiveSettings, self.service)
        }

    @property
    def channel(self):
        return DataConnectorChannels.TBAKAFKA_LINKER if self.service == DataConnectors.KAFKA else None

    @staticmethod
    def get_by_datasource_id(datasource_id: str) -> "DataLinker":
        data_linker = DataLinker.get_by_index("datasource_id", datasource_id)
        if not data_linker:
            raise DataSourceNotConnected(f"The data source {datasource_id} is not linked to any connector")
        return data_linker

    @property
    def service_settings(self):
        return {setting: value for setting, value in self.settings.items() if setting.startswith(f"{self.service}_")}

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "datasource_id": self.datasource_id,
            "settings": self.all_settings,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "settings": self.settings,
            "updated_at": self.updated_at,
        }

    @staticmethod
    async def add_linker(
        data_connector: DataConnector,
        datasource: "Datasource",
        workspace: "User",
        settings: Optional[dict] = None,
    ) -> "DataLinker":
        uid = str(uuid.uuid4())
        settings = settings or {}

        resource_id = _get_resource_id_from_branch(resource_id=datasource.id, workspace=workspace)
        if workspace and workspace.is_branch_or_release_from_branch:
            settings["branch"] = workspace.origin if workspace.is_release else workspace.id
            settings["origin"] = workspace.get_main_workspace().id

        data_linker = DataLinker(
            id=uid,
            name=f"linker_{resource_id}",
            data_connector_id=data_connector.id,
            datasource_id=resource_id,
            service=data_connector.service,
            settings=settings or {},
        )

        data_linker.save()

        # Prevent to "publish" it if it comes from a branch for now
        if workspace and workspace.is_branch_or_release_from_branch:
            return data_linker

        if data_connector.service in [DataConnectors.KAFKA, DataConnectors.AMAZON_DYNAMODB]:
            await DataLinker.publish(data_linker.id)
        return data_linker

    def update_name(self, name):
        if name:
            self.name = name

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_settings_async(linker: "DataLinker", settings: Any) -> "DataLinker":
        with DataLinker.transaction(linker.id) as linker:
            linker.update_settings(settings)
            return linker

    def update_settings(self, settings):
        new_data_connector_id = settings.pop("data_connector_id", self.data_connector_id)
        if new_data_connector_id != self.data_connector_id:
            self.__old_owner__ = self.data_connector_id
            self.data_connector_id = new_data_connector_id
        self.settings.update((k, v) for k, v in settings.items() if v is not None)

    @classmethod
    async def publish(cls, kafka_linker_id: str):
        data_linker: Optional[DataLinker] = DataLinker.get_by_id(kafka_linker_id)
        if not data_linker:
            # If the linker does not exist, we need to publish to notify the agents that it no longer exists
            receivers = await cls.publish_with_retry(DataConnectorChannels.TBAKAFKA_LINKER, kafka_linker_id)
            logging.info(f"Kafka publish to linker channel received by {receivers} agents")
            return

        branch = data_linker.settings.get("branch")
        if branch:
            logging.info(f"Kafka linker from branch does not publish (branch_id: {branch})")
            return
        receivers = await cls.publish_with_retry(DataConnectorChannels.TBAKAFKA_LINKER, kafka_linker_id)
        logging.info(f"Kafka publish to linker channel received by {receivers} agents")

    @staticmethod
    def get_config(id):
        linker = DataLinker.get_by_id(id)
        connector = DataConnector.get_by_id(linker.data_connector_id)

        config = {
            f"{linker.id}": {
                "id": linker.id,
                "name": f"{connector.name}_{linker.name}",
                **connector.settings,
                **linker.settings,
            }
        }

        return config


class DataSink(RedisModel):
    __namespace__ = "datasink"
    __owner__ = "data_connector_id"

    __indexes__ = ["resource_id"]

    __props__ = [
        "id",
        "name",
        "data_connector_id",
        "resource_id",
        "settings",
        "service",
    ]
    __fast_scan__ = True

    def __init__(self, **config: Union[str, Optional[str], dict]) -> None:
        self.id = None
        self.name = None
        self.data_connector_id: Optional[str] = None
        self.resource_id = None
        self.settings: Dict[str, Any] = {}
        self.service = None

        super().__init__(**config)

    def __getstate__(self):
        self.updated_at = datetime.now()
        return self.__dict__.copy()

    @staticmethod
    def add_sink(
        data_connector: DataConnector,
        resource: Union["Pipe", "DataSink"],
        settings: Optional[dict] = None,
        workspace: Optional["User"] = None,
    ) -> "DataSink":
        uid = str(uuid.uuid4())

        if not settings:
            settings = {}

        if workspace and workspace.is_branch_or_release_from_branch:
            settings["branch"] = workspace.origin if workspace.is_release else workspace.id
            settings["origin"] = workspace.get_main_workspace().id

        valid_sink_settings = _get_valid_sink_settings_for_service(data_connector.service)
        settings = {k: v for k, v in settings.items() if k in valid_sink_settings}

        resource_id = _get_resource_id_from_branch(resource_id=resource.id, workspace=workspace)

        data_sink = DataSink(
            id=uid,
            name=f"sink_{resource_id}",
            data_connector_id=data_connector.id,
            resource_id=resource_id,
            service=data_connector.service,
            settings=settings or {},
        )

        data_sink.save()
        return data_sink

    @staticmethod
    def get_by_resource_id(
        resource_id: str, workspace_id: Optional[str] = None, fallback_main: Optional[bool] = False
    ) -> "DataSink":
        from tinybird.user import User as Workspace

        data_sink: DataSink | None = None
        pipe = None

        if workspace_id:
            try:
                workspace: Workspace = Workspace.get_by_id(workspace_id)
                workspace_resource_id = _get_resource_id_from_branch(resource_id=resource_id, workspace=workspace)
                pipe = workspace.get_pipe(resource_id)
                data_sink = DataSink.get_by_index("resource_id", workspace_resource_id)
                if data_sink:
                    return data_sink

                # If it's a branch and there's no fallback, raise an error
                if not fallback_main and workspace.is_branch_or_release_from_branch:
                    if pipe:
                        raise ResourceNotConnected(f"The pipe {pipe.name} is not connected in this branch")
                    raise ResourceNotConnected(f"The resource {resource_id} is not connected in this branch")

                # Fallback
                # Check main data sink
                data_sink = DataSink.get_by_index("resource_id", resource_id)
            except ResourceNotConnected:
                raise
            except Exception as e:
                logging.exception(f"Unexpected error on get_by_resource_id: {e}")
                raise
        else:
            data_sink = DataSink.get_by_index("resource_id", resource_id)

        if not data_sink:
            if pipe:
                raise ResourceNotConnected(f"The pipe {pipe.name} is not connected")
            raise ResourceNotConnected(f"The pipe {resource_id} is not connected")
        return data_sink

    def to_json(self):
        return {
            "id": self.id,
            "settings": self.public_settings,
            "resource_id": self.resource_id,
        }

    @property
    def public_settings(self):
        return {
            k.replace(self.service, ""): v
            for k, v in self.settings.items()
            if k not in getattr(DataSensitiveSettings, self.service)
        }

    @property
    def service_blob_storage(self):
        return self.service in (
            DataConnectors.AMAZON_S3,
            DataConnectors.AMAZON_S3_IAMROLE,
            DataConnectors.GCLOUD_STORAGE_HMAC,
            DataConnectors.GCLOUD_STORAGE_SA,
            DataConnectors.GCLOUD_STORAGE,
        )

    def update_status(self, status: str):
        self.settings.update({"status": status})

    def update_settings(self, **settings):
        self.settings.update((k, v) for k, v in settings.items() if v is not None)

    async def delete(self, delete_sink: bool = True):
        if self.service == DataConnectors.GCLOUD_SCHEDULER:
            try:
                await GCloudSchedulerJobs.delete_scheduler(self.settings.get("gcscheduler_job_name"))
            except GCloudScheduleException as e:
                if e.status != 404:
                    raise e
                logging.warning(f"Tried to delete a non existing scheduler: {e}")

        # check if the data sink has been used as a resource in another data sink and try to delete it
        workspace_branch_id = self.settings.get("branch")
        try:
            resource_data_sink = DataSink.get_by_resource_id(resource_id=self.id, workspace_id=workspace_branch_id)
            if resource_data_sink:
                await resource_data_sink.delete()
        except ResourceNotConnected:
            pass

        if delete_sink:
            DataSink._delete(self.id)


def _get_valid_sink_settings_for_service(service: str) -> List[str]:
    service_settings = getattr(DataSinkSettings, service, [])
    return service_settings + DataSinkSettingsCommon.branch


def _get_resource_id_from_branch(resource_id: str, workspace: Optional["User"] = None) -> str:
    if not workspace:
        return resource_id
    if workspace.is_branch_or_release_from_branch:
        if workspace.is_release:
            return f"{workspace.origin}_{resource_id}"
        return f"{workspace.id}_{resource_id}"
    return resource_id


def json_path_to_jsonpath(linker):
    json_deserialization = linker["settings"].get("json_deserialization", [])
    for column in json_deserialization:
        if column.get("json_path", None):
            column["jsonpath"] = column["json_path"]
            del column["json_path"]
    return linker


def fast_scan(u):
    return u


DataLinker.__migrations__ = {
    1: json_path_to_jsonpath,
    2: fast_scan,
}


DataConnector.__migrations__ = {
    1: fast_scan,
}
