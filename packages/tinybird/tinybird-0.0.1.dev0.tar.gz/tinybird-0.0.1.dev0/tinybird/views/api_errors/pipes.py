import re
from typing import Dict, List, Optional

from tinybird.data_sinks.config import SUPPORTED_EXPORT_FORMATS_MAPPING
from tinybird.views.api_errors import parse_api_cli_error, parse_error, request_error
from tinybird.views.template_utils import get_node_from_syntax_error, parse_syntax_error


class ForbiddenError(Exception):
    pass


class SQLPipeError:
    error_missing_group_by = parse_error("GROUP BY is missing, sorting keys are: {sorting_keys}.")

    error_columns_match = parse_error("The pipe has columns {extra_columns} not found in the destination Data Source.")

    error_column_types_match = parse_api_cli_error(
        api_message="Incompatible column types {table_columns} (Data Source) != {pipe_columns} (pipe): {error_messages}",
        cli_message="\n\nIncompatible column types:\n {message_error_column_type}",
        ui_message="Incompatible column types {table_columns} (Data Source) != {pipe_columns} (pipe): {error_messages}",
    )

    error_keys_match = parse_error(
        "Columns used in GROUP BY do not match the columns from the ENGINE_SORTING_KEY in the destination Data Source. Please, make sure columns present in the ENGINE_SORTING_KEY ({sorting_keys}) are the same than the ones used in the GROUP BY ({group_by_columns})"
    )

    error_engine_match = parse_error(
        "The engine settings are already configured for '{datasource_name}' Data Source, and are not compatible with the engine settings used to materialize ('{setting_key} \"{value}\"' and '{setting_key} \"{setting_value}\"' don't match). Either you remove the settings to materialize or choose a different Data Source and try again."
    )

    error_engine_partition_key = parse_error(
        "The engine partition key would result in creating too many parts under current ingestion. Please, review your partition key"
    )

    error_sql_template = parse_error("{error_message} (in node '{node_name}' from pipe '{pipe_name}')")

    @staticmethod
    def override_datasource_msg(is_cli: bool = False, is_from_ui: bool = False):
        override_datasource_msg = "If you want to try to force override the Materialized View, please send `override_datasource=true` as a node parameter in the request"
        if is_cli:
            override_datasource_msg = "If you want to try to force override the Materialized View, please use the `--override-datasource` flag"
        elif is_from_ui:
            override_datasource_msg = ""
        return override_datasource_msg

    @staticmethod
    def missing_columns_error(error: str, node_sql: str) -> str:
        regex = re.search(r"Missing columns:.*?:", error)
        if not regex:
            return ""
        missing_cols_text = regex.group()
        final_error_message = f"{''.join([missing_cols_text, f' {node_sql}'])}"
        return final_error_message


class AppendNodeError:
    materialized_nodes_dont_support_templates = request_error(
        400,
        "Materialized nodes don't support templates. Please remove any `{{% ... %}}` template code or the `%` mark from this pipe node.",
    )
    datasource_parameter_mandatory = request_error(400, "The 'datasource' parameter is mandatory.")
    datasource_create_scope_required_to_create_datasource = request_error(
        403,
        "Forbidden. Provided token doesn't have permissions to create the datasource required in the materialized node, it also needs ``ADMIN`` or ``DATASOURCES:CREATE`` scope.",
    )
    datasource_drop_scope_required_to_override_datasource = request_error(
        403,
        "Forbidden. Provided token doesn't have permissions to override the datasource required in the materialized node, it also needs ``ADMIN`` or ``DATASOURCES:CREATE`` and ``DATASOURCES:DROP`` scopes.",
    )


class CopyNodeError:
    target_datasource_parameter_mandatory = request_error(400, "The 'target_datasource' parameter is mandatory.")


INVALID_CRON_MESSAGE = (
    '"schedule_cron" is invalid. "{schedule_cron}" is not a valid crontab expression. '
    "Use a valid crontab expression or contact us at support@tinybird.co"
)

INVALID_CRON_WITHOUT_RANGE_MESSAGE = (
    '"{schedule_cron}" will not work as expected. Please use "{suggested_cron}". '
    "Cron expression must have a range when a step is provided."
)

MIN_PERIOD_BETWEEN_SINK_JOBS_EXCEEDED = (
    "The specified cron expression schedules sink jobs exceeding the allowable rate limit. "
    "According to the imposed limit, only one sink job per pipe may be scheduled every {cron_schedule_limit} seconds. "
    'To adhere to this limit, the recommended cron expression is "{cron_recommendation}".'
)


class CopyError:
    invalid_mode = request_error(400, 'Invalid mode "{mode}", valid modes are {valid_modes}')
    invalid_cron = request_error(400, INVALID_CRON_MESSAGE)
    non_scheduled = request_error(422, "The copy Pipe is not scheduled")
    non_scheduled_cancel = request_error(
        422,
        "The copy Pipe is not scheduled, use the jobs API to cancel a queued copy job (example: v0/jobs/<job_id>/cancel)",
    )
    schedule_not_found = request_error(404, "Schedule Job for pipe '{pipe_name_or_id}' not found")
    no_copy_pipe = request_error(403, "The pipe '{pipe_name}' should be a copy pipe")
    no_target_datasource = request_error(
        404, "Target Datasource '{target_datasource_name_or_id}' for pipe '{pipe_name_or_id}' not found"
    )
    invalid_cron_without_range = request_error(400, INVALID_CRON_WITHOUT_RANGE_MESSAGE)
    min_period_between_copy_jobs_exceeded = request_error(
        403,
        'The specified cron expression schedules copy jobs exceeding the allowable rate limit. According to the imposed limit, only one copy job per pipe may be scheduled every {cron_schedule_limit} seconds. To adhere to this limit, the recommended cron expression is "{cron_recommendation}".',
    )
    max_copy_pipes_exceeded = request_error(403, "You have reached the maximum number of copy pipes ({max_pipes}).")


class PipeDefinitionError:
    more_than_expected_nodes_of_type = request_error(
        403,
        "There is more than one {node_type} node. Pipes can only have one output. Set only one node to be a {node_type} node and try again.",
    )
    more_than_expected_nodes_of_endpoint = request_error(
        403,
        "There is more than one endpoint node. Pipes can only have one output. Set only one node to be an endpoint node and try again.",
    )
    fork_downstream_do_not_support_pipes_with_engine = request_error(
        403,
        "Materialized views with the target datasource definition in the same datafile are not supported in Versions. Please, split the pipe and the target datasource in two different files.",
    )


class DataSinkError:
    missing_parameter = request_error(400, "The '{parameter_name}' parameter is mandatory.")
    invalid_cron = request_error(400, INVALID_CRON_MESSAGE)
    invalid_cron_without_range = request_error(400, INVALID_CRON_WITHOUT_RANGE_MESSAGE)
    missing_parameters_or_invalid_columns_in_file_template = request_error(
        400,
        "'{missing_columns}' column(s) or parameter(s) defined in file_template property are not present in the node query or within request parameters. Valid columns in the query: '{valid_columns}'",
    )
    date_format_used_in_nondate_column = request_error(
        400,
        "'{column}' column in file_template includes a date format ('{date_format}'), but it is a '{column_type}' column. Try again with a Date or DateTime column.",
    )
    invalid_compression = request_error(
        400,
        '"compression" is invalid. "{compression}" is not a valid or supported compression type. Use a valid or supported compression from {valid_compresssions} or contact us at support@tinybird.co',
    )
    invalid_gcs_bucket_path = request_error(
        400,
        '"{path}" is not a valid bucket path for Google Cloud Storage. Try again with this format: gcs://<bucket-path>',
    )
    invalid_s3_bucket_path = request_error(
        400, '"{path}" is not a valid bucket path for Amazon S3. Try again with this format: s3://<bucket-path>'
    )
    error_deleting_sink_node = request_error(
        409, "Could not delete sink node, please retry or contact us at support@tinybird.co"
    )
    sink_not_allowed = request_error(403, "Sinks are not allowed in this workspace")
    unsupported_export_format = request_error(
        400,
        f"Export format not supported: '{{export_format}}'. Must be one of: {', '.join(SUPPORTED_EXPORT_FORMATS_MAPPING)}",
    )
    max_amount_reached = request_error(403, "Maximum number of sink pipes allowed in the workspace reached.")
    min_period_between_sink_jobs_exceeded = request_error(403, MIN_PERIOD_BETWEEN_SINK_JOBS_EXCEEDED)
    no_such_bucket = request_error(404, "Bucket '{bucket}' does not exist")
    forbidden = request_error(403, "{message}")
    authentication_failed = request_error(401, "{message}")


class StreamError:
    missing_parameter = request_error(400, "The '{parameter_name}' parameter is mandatory.")
    error_deleting_stream_node = request_error(
        409, "Could not delete stream node, please retry or contact us at support@tinybird.co"
    )
    stream_not_allowed = request_error(403, "Streaming queries are not allowed in this workspace")


class PipeClientErrorNotFound:
    no_pipe = request_error(404, "Pipe '{pipe_name_or_id}' not found")


class PipeClientErrorForbidden:
    no_drop_scope = request_error(403, "user does not have permissions to drop pipes, set DROP scope")


def process_syntax_error(e, pipes: Optional[List] = None, pipe_def: Optional[Dict] = None):
    error = parse_syntax_error(e)
    if not pipes and not pipe_def:
        return error

    pipe_name, node_name = get_node_from_syntax_error(exception=e, pipes=pipes, pipe_def=pipe_def)
    if pipe_name and node_name:
        error = SQLPipeError.error_sql_template(error_message=error, pipe_name=pipe_name, node_name=node_name)
    return error


class ChartError:
    invalid_pipe_type = request_error(400, "Pipe must be of type 'endpoint' to create a chart")
    not_found = request_error(404, "Chart '{chart_id}' not found")


class ChartPresetError:
    not_found = request_error(404, "Chart preset '{preset_id}' not found")
