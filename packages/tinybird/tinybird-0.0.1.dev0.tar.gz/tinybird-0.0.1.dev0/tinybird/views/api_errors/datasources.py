from . import parse_error, request_error


class ClientErrorBadRequest:
    num_columns_not_supported = request_error(400, "The maximum number of columns allowed is {parameters}.")
    external_datasource_no_query = request_error(400, "Data Source creation requires a 'query' parameter")
    external_datasource_required = request_error(
        400, "Data Source creation requires an 'external_data_source' parameter with two dots (.)"
    )
    external_datasource_or_query_required = request_error(
        400,
        "Data Source creation requires an 'external_data_source' parameter with two dots (.) or a 'query' parameter",
    )
    service_is_unknown = request_error(400, "Unknown service {service_name}")
    external_datasource_invalid_cron = request_error(400, "'cron' parameter is not a valid cron expression")
    service_invalid_mode = request_error(400, "Service 'mode' parameter must be one of 'replace', 'append'")
    alter_no_parameters = request_error(400, "Alter operation requires additional parameters: {parameters}.")
    missing_parameter = request_error(400, 'The parameter "{parameter}" is required in this endpoint')
    invalid_parameter = request_error(
        400, 'The parameter "{parameter}" value "{value}" is invalid. Valid values are: {valid}'
    )
    invalid_arguments = request_error(
        400, 'Invalid arguments: "{invalid_args}". Valid arguments are: "{valid_argument_names}"'
    )
    invalid_mode = request_error(400, 'Invalid mode "{mode}", valid modes are {valid_modes}')
    invalid_url = request_error(400, "Invalid url")
    invalid_data_source_name = request_error(400, 'Invalid Data Source name "{name}". {name_help}')
    forbidden_data_source_name = request_error(400, 'Forbidden Data Source name "{name}". {name_help}')
    invalid_pipe_name = request_error(
        400, 'A Pipe with the "{name}" name exists, Pipe and Data Source names are unique'
    )
    invalid_schema_datasource_name = request_error(400, "Data Source name must be set when creating with schema")
    invalid_schema_mode = request_error(400, "Schema creation is only compatible with mode=create")
    invalid_engine_schema = request_error(400, "The engine parameter requires the schema parameter")
    invalid_data_source_replace_name = request_error(
        400, "Data source name must be set with mode=replace (name=my_datasource)"
    )
    mandatory_delete_condition = request_error(400, "The delete_condition='delete_statement' is mandatory")
    invalid_data_source_delete_name = request_error(400, "Data source name must be provided (name=my_datasource)")
    nonexisting_data_source_replace_name = request_error(
        400, 'Data Source "{name}" does not exist, can not replace a non existing Data Source'
    )
    nonexisting_data_source_delete_name = request_error(
        400, 'Data Source "{name}" does not exist, can not delete a non existing Data Source'
    )
    invalid_data_source_create_name = request_error(400, 'Data Source "{name}" already exists, use mode=append')
    nonexisting_data_source_append_name = request_error(400, "Data Source name must be set with mode=append")
    invalid_ch_table_exists = request_error(400, 'Data Source "{name}" already exists')
    invalid_ch_unknown_storage = request_error(400, 'Invalid engine "{engine}"')
    not_supported_url = request_error(400, "Url is not supported, only http, and https schemes are")
    invalid_body_or_payload = request_error(
        400, "Url or body payload should be sent. Are you doing a POST without data?"
    )
    invalid_url_fetch_error = request_error(400, "Trying to fetch {url} returns {error_code}: {error_message}")
    url_fetch_error = request_error(400, "Trying to fetch {url} failed with {error_message}")
    invalid_body_empty = request_error(400, "Body is empty, you should either set url or send csv sample in the body")
    invalid_encoding = request_error(400, "Couldn't guess the file encoding, transform it to utf8")
    failed_truncate = request_error(400, "Failed to truncate: {error}")
    invalid_value_for_argument = request_error(
        400, "Invalid value for argument '{argument}': {value}. Valid values: {valid}."
    )
    invalid_argument_for_non_kafka = request_error(
        400, "Argument '{argument}' can only be used with Kafka Data Sources."
    )
    alter_no_operations = request_error(
        400, "There were no operations to perform, new schema, ttl and indexes are the same as the existing ones"
    )
    alter_not_supported = request_error(400, "Could not perform alter operation, reason: {reason}")
    alter_engine_not_supported = request_error(
        400,
        "The data source engine ({engine}) is not supported. Schema modifications are only supported for the Null engine and the engines from the MergeTree family.",
    )
    max_alter_operations = request_error(
        400,
        "The maximum number of operations to modify columns definition is 1 while {number_operations} are generated from the definition. Please execute one operation at a time and refer to our docs to see the list of allowed operations => https://www.tinybird.co/docs/api-reference/datasource-api#post--v0-datasources-(.+)-alter.",
    )
    engine_not_supported_for_delete = request_error(
        400,
        "The data source engine ({engine}) is not supported. Deletion of data is supported for engines from the family MergeTree",
    )
    dialect_invalid_length = request_error(400, "The dialect {component} must be a 1-character string")
    dialect_invalid_delimiter_tab_suggestion = request_error(
        400,
        "The dialect delimiter must be a 1-character string. If you are trying to set a TAB delimiter, review your backslash-escaped characters. In bash-like environments, you can get ANSI C escape sequences using something like $'\t', for instance `curl -d dialect_delimiter=$'\t' ...`.",
    )
    invalid_option = request_error(400, "{option} is not a valid option")
    no_data = request_error(400, "No data was provided")
    no_data_url = request_error(400, "No data was provided. Make sure the file ({url}) is not empty")
    job_not_in_cancellable_status = request_error(400, "Job is not in cancellable status")
    job_already_being_canceled = request_error(400, "Job is already being cancelled")
    invalid_connector = request_error(400, "Connector {connector} does not exist")
    missing_connector = request_error(
        400,
        "A connector is required for the {service_name} service. Please provide the connector ID in the 'connector' parameter.",
    )
    incompatible_connector_engine = request_error(
        400,
        "When adding a data source for {service}, the data source engine is created automatically and can not be set manually",
    )
    missing_jsonpaths = request_error(
        400,
        "When adding a data source for {service}, setting the schema requires to set the respective jsonpath for each column",
    )
    missing_schema = request_error(
        400, "When adding a data source for {service}, setting jsonpaths requires to set the schema parameter"
    )
    invalid_settings = request_error(
        400, "Invalid settings for {service} connector, valid settings are: {valid_settings}"
    )
    required_setting = request_error(400, "Required setting '{setting}' is missing")
    invalid_setting = request_error(400, "Invalid value for setting '{setting}', valid values are: {valid_values}")
    max_topics_limit = request_error(
        400, "Max kafka connected topics ({max_topics}) reached. Contact support@tinybird.co."
    )
    can_not_delete_data_source_as_it_is_a_shared_ds_in_a_destination_ws = request_error(
        400,
        'Data Source "{name}" is a Shared Data Source so it can\'t be directly deleted. To stop having it in this Workspace you have to unshare it from the origin Workspace.',
    )
    can_not_import_data_in_data_source_as_it_is_read_only = request_error(
        400,
        "Data Source \"{name}\" is read-only so it can't be modified. If it's a shared Data Source, the operations available in this endpoint should be done from the origin Workspace.",
    )
    origin_workspace_does_not_have_a_normalized_and_unique_name = request_error(
        400,
        'Can\'t share a Data Source because the origin Workspace "{name}" '
        "doesn't have a normalized name or it's not unique. Please rename it with a name"
        " that have letters, numbers and underscores.",
    )
    a_shared_data_source_can_not_be_reshared = request_error(
        400,
        "Data Source \"{datasource_id}\" can't be shared. If it's an external Data Source you have to share the original datasource.",
    )
    data_source_already_shared_with_workspace = request_error(
        400, 'The datasource "{datasource_name}" is already shared with the workspace "{workspace_id}"'
    )
    a_normal_data_source_can_not_be_unshared = request_error(
        400,
        'Data Source "{datasource_id}" is not a Shared Datasource. If you want to delete it, please use the normal Data Source\'s delete operation.',
    )
    data_source_is_not_shared_with_that_workspace = request_error(
        400,
        'This Data Source is not being shared between the Workspaces "{origin_workspace_name}" and "{destination_workspace_name}".',
    )
    ndjson_multipart_name = request_error(
        400,
        "NDJSON/Parquet multipart requests require name field set to 'ndjson'/'parquet'. Example: curl -F \"ndjson=@events.ndjson\" ...",
    )
    wrong_multipart_name = request_error(
        400,
        "Multipart requests require name field to be set to 'file', 'csv' or 'ndjson' and a non-empty file. Example: curl -F \"ndjson=@events.ndjson\" ...",
    )
    can_not_share_data_sources_between_workspaces_in_different_clusters = request_error(
        400,
        "The sharing Data Sources functionality doesn't support sharing a Data Source between Workspaces living in different clusters.",
    )
    can_not_share_data_sources_between_branches = request_error(
        400, "The sharing Data Sources functionality doesn't support sharing a Data Source between Branches."
    )
    cannot_copy_data_between_workspaces_in_different_clusters = request_error(
        400, "This functionality doesn't support exporting data between Workspaces living in different clusters."
    )
    unsupported_file_to_analyze = request_error(
        400, "Cannot analyze {format} file. Please check your file is valid or contact us at support@tinybird.co"
    )
    unsupported_file_to_analyze_db_error = request_error(
        400,
        "Cannot analyze {format} file. Please check your file is valid or contact us at support@tinybird.co. Error: {error}",
    )
    failed_delete_condition = request_error(400, "Failed to apply delete_condition='{delete_condition}': {error}")
    max_active_delete_jobs = request_error(
        429, "You have reached the maximum number of delete jobs ({workspace_max_jobs})"
    )
    invalid_append_data_source_dependent_join = request_error(
        400,
        "Operation not allowed, use 'mode=replace' instead. The 'append' operation is not allowed on the data source '{datasource_name}' because it has a dependent Join Materialized View. When using 'mode=replace', non-existent rows will be added. Dependencies: {datasources}",
    )
    invalid_append_data_source_join = request_error(
        400,
        "Operation not allowed, use 'mode=replace' instead. The 'append' operation is not allowed on the data source '{datasource_name}' because it is a Join Data Source. When using 'mode=replace', non-existent rows will be added.",
    )
    topic_repeated_in_workspace = request_error(
        400,
        "A Kafka topic can be used once per workspace. The topic: {topic} is already used in the workspace: {workspace}. Contact support@tinybird.co.",
    )
    topic_repeated_in_branch = request_error(
        400,
        "A Kafka topic can be used once per branch. The topic: {topic} is already used in the branch: {branch}. Contact support@tinybird.co.",
    )
    missing_body_param = request_error(400, "Body parameter {param} is missing.")
    invalid_scheduler_state = request_error(
        400, "Invalid schduler state '{state}'. Must be one of ('running', 'paused')."
    )
    cannot_pause_with_ongoing_run = request_error(
        400,
        "Cannot pause Data Source '{datasource_name}' because there is a running execution. Try again once the execution is finished. ",
    )
    invalid_json_body = request_error(400, "Invalid JSON body")
    invalid_sql_query = request_error(400, "Invalid extraction SQL query: {message}")
    exchange_disabled = request_error(
        404,
        "This command depends on the Exchange feature currently for internal usage.",
    )
    jsonpaths_and_default_values_not_supported = request_error(
        400,
        "DEFAULT value is not allowed when jsonpath is set. Contact support@tinybird.co.",
    )
    cannot_share_datasource_with_parent_workspace = request_error(
        400,
        "Cannot share a data source with its parent workspace.",
    )


class ClientErrorForbidden:
    invalid_data_source_token_create = request_error(
        403, "Token does not have DATASOURCES:CREATE scope, create mode requires the DATASOURCES:CREATE scope"
    )
    invalid_data_source_token_replace = request_error(
        403,
        "Token does not have DATASOURCES:CREATE scope, replace mode requires the DATASOURCES:CREATE scope because is a destructive action",
    )
    invalid_data_source_token_append_create = request_error(
        403, "You must provide a Data Source name when appending (and you don't have CREATE scope)"
    )
    invalid_data_source_token_append = request_error(
        403, 'Token does not have DATASOURCES:APPEND scope for Data Source "{name}"'
    )
    invalid_data_source_permission_drop = request_error(
        403, 'User does not have permissions to drop Data Source "{name}", set DROP scope'
    )
    token_doesnt_have_access_to_this_resource = request_error(
        403, "The token you have provided doesn't have access to this resource"
    )

    invalid_permissions_to_share_a_datasource = request_error(
        403,
        "The user that owns this token needs to have access to both workspaces to share a Data Source between them.",
    )
    invalid_permissions_to_share_a_datasource_as_guest = request_error(
        403, "The user that owns this token needs to be admin of this workspace to share a Data Source."
    )
    invalid_permissions_to_unshare_a_datasource_as_guest = request_error(
        403, "The user that owns this token needs to be admin of the origin workspace to unshare a Data Source."
    )
    invalid_permissions_to_stop_sharing_a_datasource = request_error(
        403,
        "The user that owns this token needs to have access to both workspaces to remove a Data Source between them.",
    )
    invalid_permissions_to_copy_data = request_error(
        403, "The user that owns this token needs to have writing permissions to the Target Data Source"
    )


class ClientErrorNotFound:
    nonexisting_data_source = request_error(404, 'Data Source "{name}" does not exist')
    job_not_found = request_error(404, 'Job with id "{id}" not found')


class ClientNotAllowed:
    datasource_not_scheduleable = request_error(405, 'Data Source "{ds}" doesn\'t have an associated schedule')


class ClientErrorConflict:
    conflict_materialized_node = request_error(
        409, "{break_ingestion_message}{affected_materializations_message}{dependent_pipes_message}"
    )
    conflict_override_materialized_node = request_error(
        409,
        "Cannot override Materialized View, there are other dependent Materialized nodes that depend on the Data Source and consistency on the data flow cannot be ensured. If you want to perform that operation you can work with versions => https://docs.tinybird.co/cli.html#working-with-versions. {affected_materializations_message}{dependent_pipes_message}",
    )
    conflict_override_shared_materialized_node = request_error(
        409,
        "Cannot override Materialized View because it's shared with other Workspaces. If you want to perform that operation you can work with versions => https://docs.tinybird.co/cli.html#working-with-versions. Affected workspace => {workspaces_names}",
    )
    conflict_copy_pipes = request_error(409, "{break_copy_message}{dependent_pipes_message}")


class ClientErrorLengthRequired:
    length_required = request_error(411, "Add a valid Content-Length header containing the length of the message-body")


class ClientErrorEntityTooLarge:
    entity_too_large_full_body = request_error(
        413,
        'The message-body is too large. For requests larger than {max_body_size}{units}, you should use a multipart/form-data request. Use curl -F csv=@file.csv "{api_host}/v0/datasources".',
    )
    entity_too_large_stream = request_error(
        413,
        'The message-body is too large. For requests larger than {max_body_size}{units}, you should split your file or upload to an HTTP server and use curl -X POST "{api_host}/v0/datasources?url=URL".',
    )
    entity_too_large_url = request_error(
        413,
        "The file is too large: {file_size} {file_size_unit}, while the limit is {max_import_url} {max_import_url_unit}.",
    )


class ServerErrorInternal:
    failed_delete = request_error(500, 'Failed to delete: "{error}"')
    failed_truncate = request_error(500, 'Failed to truncate: "{error}"')
    failed_exchange = request_error(500, 'Failed to exchange tables: "{error}"')
    import_problem = request_error(
        500, "There was a problem when importing your data. Contact support@tinybird.co. Error: {error}"
    )
    failed_datafile = request_error(
        500, "There was a problem getting your datafile. Contact support@tinybird.co. Error: {error}"
    )
    analyze_csv_problem = request_error(
        500, "There was a problem when guessing your CSV file dialect. Contact support@tinybird.co. Error: {error}"
    )
    failed_delete_condition = request_error(500, 'Failed to delete with condition: "{error}"')


class MatviewDatasourceError:
    error_aggregate_function_engine = parse_error("{engine_full} might not support Aggregate Functions.")


class DynamoDBDatasourceError:
    streams_not_configured = request_error(
        400,
        "'{table_name}' does not have DynamoDB streams configured. Please enable them and set the view type to 'New image'.",
    )
    table_size_exceeds_limit = request_error(
        400,
        "'{table_name}' size ({table_gb:.2f}GB) exceeds the maximum allowed size of {limit_gb:.2f}GB. "
        "Please contact support@tinybird.co if you need to increase the limit.",
    )
    table_write_capacity_exceeds_limit = request_error(
        400,
        "'{table_name}' write capacity units ({table_wcu}WCU) exceeds the maximum allowed size of {limit_wcu}WCU. "
        "Please contact support@tinybird.co if you need to increase the limit.",
    )
    pitr_not_available = request_error(
        400,
        "'{table_name}' does not have point-in-time recovery enabled. Please enable it in the Backups' section within the DynamoDB Table in AWS, and try again.",
    )
    error_while_reading_dynamodb_table = request_error(400, "DynamoDB Table Describe Error: {error_message}")
    error_while_triggering_dynamodb_export = request_error(400, "DynamoDB Table Export Error: {error_message}")
    missing_ddb_property_in_sorting_key = request_error(
        400, "'{property_name}' is missing in the Sorting Key attributes for '{table_name}'"
    )
    error_while_previewing_dynamodb_table = request_error(400, "DynamoDB Table Preview Error: {error_message}")
    dynamodb_sync_already_in_progress = request_error(
        400,
        "Cannot trigger a sync operation in '{datasource_name}' because there is one already in progress. Try again once the execution is finished.",
    )
