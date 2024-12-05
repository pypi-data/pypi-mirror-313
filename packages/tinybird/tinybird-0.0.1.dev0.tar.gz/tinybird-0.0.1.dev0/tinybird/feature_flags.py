from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, cast

"""
Usage:
- Add the new feature flag to the FeatureFlag Enum class
- Add the details (default, value, a quick description, if it would be different for tinybird.co accounts...)
"""


class FeatureFlagBase(Enum):
    pass


class FeatureFlag(FeatureFlagBase):
    FULL_ACCESS_ACCOUNT = "full_access_account"
    CONFIRM_ACCOUNT_AUTOMATICALLY = "confirm_account_automatically"
    MV1 = "mv1"
    MERGE = "finalize_aggregations"
    GCS_CONNECTOR = "gcs_connector"
    ALL_NEW_WORKSPACES_WITH_VERSIONS = "all_new_workspaces_with_versions"
    NEW_BILLNG_PAGE = "new_billing_page"
    NEW_ORGANIZATION_USAGE_PAGE = "new_organization_usage_page"
    SHARED_INFRA_FLOW = "shared_infra_flow"
    FIX_SQL_ERROR = "fix_sql_error"


class FeatureFlagWorkspaces(FeatureFlagBase):
    FORBIDDEN_APPEND_TO_JOIN = "forbidden_append_to_join"
    DISABLE_TEMPLATE_SECURITY_VALIDATION = "disable_template_security_validation"
    JOIN_ALGORITHM_AUTO = "join_algorithm_auto"
    PIPE_NODE_RESTRICTIONS = "pipe_node_restrictions"
    PIPE_ENDPOINT_RESTRICTIONS = "pipe_endpoint_restrictions"
    ENABLE_STORAGE_POLICY = "enable_storage_policy"
    PARTIAL_REPLACES_WITH_NULL_TABLES = "partial_replaces_with_null_tables"
    LEGACY_KAFKA_METADATA = "legacy_kafka_metadata"
    SHARE_DATASOURCES_BETWEEN_CLUSTERS = "shared_datasources_between_clusters"
    FORCE_NONATOMIC_COPY = "force_nonatomic_copy"
    PROD_READ_ONLY = "prod_read_only"
    DATA_SINKS_FILES_OBSERVABILITY = "data_sinks_advanced_observability"
    LOG_MORE_HTTP_INSIGHTS = "log_more_http_insights"
    USE_POPULATES_REVAMP = "use_populates_revamp"
    USE_POPULATES_OLD = "use_populates_old"
    EXCHANGE_API = "exchange_api"
    VERSIONS_GA = "versions_ga"
    PARQUET_THROUGH_CLICKHOUSE = "parquet_through_clickhouse"
    PREPROCESS_PARAMETERS_CIRCUIT_BREAKER = "preprocess_parameters_circuit_breaker"
    SPLIT_TO_ARRAY_ESCAPE = "split_to_array_escape"
    DECODE_AVRO_AS_DICT = "decode_avro_as_dict"
    PARQUET_THROUGH_CLICKHOUSE_QUARANTINE = "parquet_through_clickhouse_quarantine"
    STREAMING_QUERIES = "streaming_queries"
    GATHERER_ON_BRANCHES = "gatherer_on_branches"
    VALIDATE_KAFKA_HOST = "validate_kafka_host"
    CH_META_EDITOR = "ch_meta_editor"
    DISTRIBUTED_ENDPOINT_CONCURRENCY = "distributed_endpoint_concurrency"
    KAFKA_SINKS = "kafka_sinks"
    PARQUET_THROUGH_CLICKHOUSE_USE_METADATA = "parquet_through_clickhouse_use_metadata"
    DELETE_JOB_ALLOW_NONDETERMINISTIC_MUTATIONS = "delete_job_allow_nondeterministic_mutations"
    POOL_REPLICA_FOR_POPULATES = "pool_replica_for_populates"
    INHERITED_TEMPLATING_VARIABLES = "inherited_templating_variables"
    ENABLE_CUSTOM_PREVIEW_FOR_S3_CONNECTOR = "enable_custom_preview_for_s3_connector"
    ORG_RATE_LIMIT = "org_rate_limit"


@dataclass()
class FeatureDetails:
    description: str
    default_value: bool
    private: bool = True  # Private features will not be sent to the Front.
    override_for_configured_domain: Optional[bool] = None

    def to_json(self) -> Dict[str, Any]:
        return {"description": self.description, "default_value": self.default_value}


class FeatureFlagsBase:
    configured_domain: str = ""
    map_features_and_details: Dict[FeatureFlagBase, FeatureDetails] = {}

    @classmethod
    def to_json(cls) -> List[Dict[str, Any]]:
        return list(
            map(
                lambda feature_flag: {
                    "name": feature_flag[0].value,
                    "description": feature_flag[1].description,
                    "default_value": feature_flag[1].default_value,
                },
                cls.map_features_and_details.items(),
            )
        )


class FeatureFlagsService(FeatureFlagsBase):
    configured_domain: str = "@tinybird.co"

    map_features_and_details: Dict[FeatureFlagBase, FeatureDetails] = {
        FeatureFlag.FULL_ACCESS_ACCOUNT: FeatureDetails(
            description="Give access to Cheriff and other administration details",
            default_value=False,
            override_for_configured_domain=True,
        ),
        FeatureFlag.CONFIRM_ACCOUNT_AUTOMATICALLY: FeatureDetails(
            description="Accounts with this feature will be automatically confirmed.",
            default_value=False,
            override_for_configured_domain=True,
        ),
        FeatureFlag.MV1: FeatureDetails(
            description="Activate the second iteration of the Materialization initiative",
            default_value=False,
            private=False,
            override_for_configured_domain=False,
        ),
        FeatureFlag.MERGE: FeatureDetails(
            description="Automatically apply finalizeAggregation to Materialized Views",
            default_value=False,
            private=False,
            override_for_configured_domain=False,
        ),
        FeatureFlag.GCS_CONNECTOR: FeatureDetails(
            description="Enable GCS connector",
            default_value=False,
            private=False,
            override_for_configured_domain=False,
        ),
        FeatureFlag.ALL_NEW_WORKSPACES_WITH_VERSIONS: FeatureDetails(
            description="All new Workspaces created by this user will have Versions available",
            default_value=False,
            override_for_configured_domain=True,
        ),
        FeatureFlag.NEW_BILLNG_PAGE: FeatureDetails(
            description="Show the new page for usage-based billing",
            default_value=False,
            override_for_configured_domain=True,
            private=False,
        ),
        FeatureFlag.NEW_ORGANIZATION_USAGE_PAGE: FeatureDetails(
            description="Show the new page for organization usage metrics",
            default_value=False,
            override_for_configured_domain=True,
            private=False,
        ),
        FeatureFlag.SHARED_INFRA_FLOW: FeatureDetails(
            description="Enable the new flow for Shared Infra Billing",
            default_value=False,
            override_for_configured_domain=False,
            private=False,
        ),
        FeatureFlag.FIX_SQL_ERROR: FeatureDetails(
            description="Enable the SQL error fixer",
            default_value=False,
            override_for_configured_domain=True,
            private=False,
        ),
    }

    # Automatic check to detect features added to the Enum without details.
    for feature_to_check in FeatureFlag:
        if feature_to_check not in map_features_and_details:
            raise Exception(f"Feature {feature_to_check} added without a description and a default value")

    @classmethod
    def feature_for_email(
        cls, feature: FeatureFlag, email: str, feature_overrides: Optional[Dict[str, bool]] = None
    ) -> bool:
        feature_details = cls.map_features_and_details[feature]
        if feature_overrides and feature.value in feature_overrides:
            return feature_overrides[feature.value]
        if (
            feature_details.override_for_configured_domain is not None
            and email.find("@") != -1
            and email.split("@")[1] == cls.configured_domain
        ):
            return feature_details.override_for_configured_domain
        return feature_details.default_value

    @classmethod
    def get_all_feature_values(
        cls, email: str, feature_overrides: Optional[Dict[str, bool]] = None, include_private: bool = False
    ) -> Dict[str, bool]:
        compiled_features: Dict[str, bool] = {}
        for feature, ff_details in cls.map_features_and_details.items():
            if not include_private and ff_details.private:
                continue
            compiled_features[feature.value] = cls.feature_for_email(
                cast(FeatureFlag, feature), email, feature_overrides
            )

        return compiled_features


class FeatureFlagsWorkspaceService(FeatureFlagsBase):
    configured_domain: str = "@tinybird.co"

    map_features_and_details = {
        FeatureFlagWorkspaces.FORBIDDEN_APPEND_TO_JOIN: FeatureDetails(
            description="Do not allow appends to join tables", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.DISABLE_TEMPLATE_SECURITY_VALIDATION: FeatureDetails(
            description="Disable template security validation", default_value=False, private=True
        ),
        FeatureFlagWorkspaces.JOIN_ALGORITHM_AUTO: FeatureDetails(
            description="Uses join_algorithm=auto setting", default_value=False
        ),
        FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS: FeatureDetails(
            description="Forbid creating or modifing a pipe with more than one materialized node.",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS: FeatureDetails(
            description="Forbid materializing a node if an endpoint exists or creating an endpoint if a node is materialized",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY: FeatureDetails(
            description="Enable setting a custom storage policy to a workspace so their data sources make use of it",
            default_value=False,
            private=True,
        ),
        FeatureFlagWorkspaces.PARTIAL_REPLACES_WITH_NULL_TABLES: FeatureDetails(
            description="Execute internal SELECT INTO operations of partial replaces using NULL tables",
            default_value=True,
            private=True,
        ),
        FeatureFlagWorkspaces.LEGACY_KAFKA_METADATA: FeatureDetails(
            description="Do not add underscores to Kafka metadata columns", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.SHARE_DATASOURCES_BETWEEN_CLUSTERS: FeatureDetails(
            description="Allow to share a data source between clusters. The sharing between clusters will be "
            "done with a read-only approach",
            default_value=False,
        ),
        FeatureFlagWorkspaces.FORCE_NONATOMIC_COPY: FeatureDetails(
            description="Force Copy operations to be regular copy append operations instead of atomic",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.PROD_READ_ONLY: FeatureDetails(
            description="Main Branch just read-only", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.DATA_SINKS_FILES_OBSERVABILITY: FeatureDetails(
            description="Enable Files Observability for Data Sinks (Enable only if destination ClickHouse is on 24.1.6 or above)",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.LOG_MORE_HTTP_INSIGHTS: FeatureDetails(
            description="Log in tags from Spans more information about appconnect,...",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.USE_POPULATES_REVAMP: FeatureDetails(
            description="[DEPRECATED], to be removed", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.USE_POPULATES_OLD: FeatureDetails(
            description="If active, runs the old populates", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.EXCHANGE_API: FeatureDetails(
            description="Enable exchange API", default_value=True, private=False
        ),
        FeatureFlagWorkspaces.VERSIONS_GA: FeatureDetails(
            description="DEPRECATED",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE: FeatureDetails(
            description="Enable Parquet ingestion through ClickHouse to process them much faster",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.PREPROCESS_PARAMETERS_CIRCUIT_BREAKER: FeatureDetails(
            description="Enable a circuit breaker to avoid preprocessing parameters in templates",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.SPLIT_TO_ARRAY_ESCAPE: FeatureDetails(
            description="Enable a better string escaping in split_to_array.",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.DECODE_AVRO_AS_DICT: FeatureDetails(
            description="Decode kafka avro as dict instead of convert it to json",
            default_value=False,
        ),
        FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE_QUARANTINE: FeatureDetails(
            description="Enable Parquet ingestion of quarantine through ClickHouse. Disable to speed up just in case you don't expect quarantine or you can ignore",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.STREAMING_QUERIES: FeatureDetails(
            description="Enable the Streaming Queries feature",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.GATHERER_ON_BRANCHES: FeatureDetails(
            description="Enable Gatherer on branches",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.VALIDATE_KAFKA_HOST: FeatureDetails(
            description="Enable validation of kafka host is not in private network and accessible on creation",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.CH_META_EDITOR: FeatureDetails(
            description="Enable the CodeMirror 6 editor with ClickHouse metadata",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY: FeatureDetails(
            description="Enables check_endpoint_concurrency_limit decorator",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.KAFKA_SINKS: FeatureDetails(
            description="Enable Kafka Sinks feature", default_value=False, private=False
        ),
        FeatureFlagWorkspaces.DELETE_JOB_ALLOW_NONDETERMINISTIC_MUTATIONS: FeatureDetails(
            description="Enables flag allow_nondeterministic_mutations in CH in delete jobs",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE_USE_METADATA: FeatureDetails(
            description="Fetch ParquetMetadata stats for the job. This should be useful for presigned S3 urls.",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES: FeatureDetails(
            description="Pool replica for jobs",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.ENABLE_CUSTOM_PREVIEW_FOR_S3_CONNECTOR: FeatureDetails(
            description="Enables the custom preview connector",
            default_value=True,
            private=False,
        ),
        FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES: FeatureDetails(
            description="Enable inherited templating variables",
            default_value=False,
            private=False,
        ),
        FeatureFlagWorkspaces.ORG_RATE_LIMIT: FeatureDetails(
            description="Enable organization rate limit",
            default_value=False,
            private=False,
        ),
    }

    for feature_to_check in FeatureFlagWorkspaces:
        if feature_to_check not in map_features_and_details:
            raise Exception(f"Feature {feature_to_check} added without a description and a default value")

    @classmethod
    def feature_for_id(
        cls, feature: FeatureFlagWorkspaces, id: str, feature_overrides: Optional[Dict[str, bool]] = None
    ) -> bool:
        if feature_overrides and feature.value in feature_overrides:
            return feature_overrides[feature.value]
        else:
            return cls.map_features_and_details[feature].default_value

    @classmethod
    def get_all_feature_values(
        cls, feature_overrides: Optional[Dict[str, bool]] = None, include_private: bool = False
    ) -> Dict[str, bool]:
        features: Dict[str, bool] = {}
        for feature, ff_details in cls.map_features_and_details.items():
            if not include_private and ff_details.private:
                continue
            features[feature.value] = cls.feature_for_id(feature, "", feature_overrides)  # type: ignore

        return features
