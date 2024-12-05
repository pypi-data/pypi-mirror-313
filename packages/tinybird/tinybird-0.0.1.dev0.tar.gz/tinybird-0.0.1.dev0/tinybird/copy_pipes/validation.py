import logging
from typing import Dict, Optional

from chtoolset import query as chquery
from croniter import CroniterBadCronError, croniter

from tinybird.ch import CHTable, ch_get_columns_from_query
from tinybird.datasource import get_trigger_datasource
from tinybird.materialized import AnalyzeException
from tinybird.matview_checks import SQLValidationException
from tinybird.pipe import CopyModes, Pipe, PipeNode, PipeTypes
from tinybird.plan_limits.copy import CopyLimits
from tinybird.sql_template import SQLTemplateCustomError, SQLTemplateException, TemplateExecutionResults
from tinybird.user import User as Workspace
from tinybird.views.api_errors.pipes import CopyError
from tinybird.views.base import ApiHTTPError


async def get_copy_datasource_definition(workspace: Workspace, pipe: Pipe, node: PipeNode, target_datasource: str):
    try:
        template_execution_results = TemplateExecutionResults()
        secrets = workspace.get_secrets_for_template()
        sql = node.render_sql(secrets=secrets, template_execution_results=template_execution_results)
        replaced_sql, _ = await workspace.replace_tables_async(
            sql,
            pipe=pipe,
            use_pipe_nodes=True,
            template_execution_results=template_execution_results,
            allow_use_internal_tables=False,
            function_allow_list=workspace.allowed_table_functions(),
            secrets=secrets,
        )
        columns = await ch_get_columns_from_query(
            workspace.database_server,
            workspace.database,
            replaced_sql,
            ch_params=workspace.get_secrets_ch_params_by(template_execution_results.ch_params),
        )

        table_definition = CHTable(columns)
        datasource_name = target_datasource or f"copy_{pipe.name}"
        left_table = None

        try:
            left_table = chquery.get_left_table(replaced_sql, default_database=workspace.database)
        except Exception:
            pass

        response = {
            "analysis": {
                "pipe": {
                    "id": pipe.id,
                    "name": pipe.name,
                },
                "node": node.to_json(dependencies=False, attrs=["id", "name"]),
                "sql": node.sql.strip(),
                "trigger_datasource": get_trigger_datasource(workspace, left_table),
                "datasource": {
                    "name": datasource_name,
                    "schema": table_definition.table_structure(),
                    "engine": table_definition.get_engine_settings({"engine": "MergeTree", "type": "MergeTree"}),
                    "columns": table_definition.columns,
                },
            }
        }

        return response
    except Exception as e:
        if isinstance(e, ValueError):
            raise AnalyzeException(str(e)) from e
        raise e


def validate_copy_pipe_or_raise(
    workspace: Workspace,
    pipe: Pipe | None,
    schedule_cron: str | None,
    is_overriding_pipe: bool = False,
    mode: Optional[str] = None,
):
    max_pipes = CopyLimits.max_copy_pipes.get_limit_for(workspace)

    if (not pipe or pipe.pipe_type != PipeTypes.COPY) and (
        not is_overriding_pipe and CopyLimits.max_copy_pipes.has_reached_limit_in(max_pipes, {"workspace": workspace})
    ):
        raise ApiHTTPError.from_request_error(
            CopyError.max_copy_pipes_exceeded(max_pipes=max_pipes),
            documentation="/api-reference/pipe-api.html#quotas-and-limits",
        )

    if mode and not CopyModes.is_valid(mode):
        valid_modes = ", ".join(CopyModes.valid_modes)
        raise ApiHTTPError.from_request_error(CopyError.invalid_mode(mode=mode, valid_modes={valid_modes}))

    if schedule_cron and not croniter.is_valid(schedule_cron):
        raise ApiHTTPError.from_request_error(CopyError.invalid_cron(schedule_cron=schedule_cron))

    if schedule_cron:
        suggested_cron = validate_gcs_cron_expression(schedule_cron)
        if suggested_cron:
            raise ApiHTTPError.from_request_error(
                CopyError.invalid_cron_without_range(schedule_cron=schedule_cron, suggested_cron=suggested_cron)
            )

    min_period = CopyLimits.min_period_between_copy_jobs.get_limit_for(workspace)
    if schedule_cron and CopyLimits.min_period_between_copy_jobs.has_reached_limit_in(
        min_period, {"schedule_cron": schedule_cron}
    ):
        copy_error_params = CopyLimits.min_period_between_copy_jobs.get_error_message_params(min_period)
        raise ApiHTTPError.from_request_error(
            CopyError.min_period_between_copy_jobs_exceeded(**copy_error_params),
            documentation="/api-reference/pipe-api.html#quotas-and-limits",
        )


async def validate_copy_pipe(schedule_cron: str, workspace: Workspace, node: PipeNode, mode: str):
    errors = []
    try:
        if mode and not CopyModes.is_valid(mode):
            valid_modes = ", ".join(CopyModes.valid_modes)
            errors.append(
                {
                    "mode_invalid": True,
                    "message": (f"mode is invalid. Valid modes are: {valid_modes}"),
                }
            )

        if schedule_cron and schedule_cron != "@on-demand" and not croniter.is_valid(schedule_cron):
            errors.append(
                {
                    "schedule_cron_invalid": True,
                    "message": (
                        f"'schedule_cron' is invalid. '{schedule_cron}' is not a valid crontab expression. Use a valid"
                        " crontab expression or contact us at support@tinybird.co"
                    ),
                }
            )

        if schedule_cron and schedule_cron != "@on-demand" and croniter.is_valid(schedule_cron):
            suggested_cron = validate_gcs_cron_expression(schedule_cron)
            if suggested_cron and not errors:
                errors.append(
                    {
                        "schedule_cron_invalid_range": True,
                        "message": (
                            f'"{schedule_cron}" will not work as expected. Please use "{suggested_cron}". Cron'
                            " expression must have a range when a step is provided."
                        ),
                    }
                )

        min_period = CopyLimits.min_period_between_copy_jobs.get_limit_for(workspace)
        if (
            schedule_cron
            and schedule_cron != "@on-demand"
            and CopyLimits.min_period_between_copy_jobs.has_reached_limit_in(
                min_period, {"schedule_cron": schedule_cron}
            )
        ):
            copy_error_params = CopyLimits.min_period_between_copy_jobs.get_error_message_params(min_period)
            errors.append(
                {
                    "copy_min_period_jobs_exceeded": True,
                    "message": (
                        "The specified cron expression schedules copy jobs exceeding the allowable rate limit."
                        " According to the imposed limit, only one copy job per pipe may be scheduled every"
                        f' {copy_error_params["cron_schedule_limit"]} seconds. To adhere to this limit, the recommended'
                        f' cron expression is "{copy_error_params["cron_recommendation"]}".'
                    ),
                    "documentation": "/api-reference/pipe-api.html#quotas-and-limits",
                }
            )

        max_pipes = CopyLimits.max_copy_pipes.get_limit_for(workspace)
        if CopyLimits.max_copy_pipes.has_reached_limit_in(max_pipes, {"workspace": workspace}):
            errors.append(
                {
                    "copy_max_pipes_exceeded": True,
                    "message": f"You have reached the maximum number of copy pipes ({max_pipes}).",
                    "documentation": "/api-reference/pipe-api.html#quotas-and-limits",
                }
            )
        node.render_sql()
    except CroniterBadCronError:
        # not adding it to errors since it is added when croniter is_valid returns falsy
        logging.error("schedule is invalid")
    except SQLTemplateCustomError as e:
        errors.append(
            {
                "sql_error": True,
                "message": str(e),
            }
        )
    except (ValueError, SyntaxError, SQLTemplateException) as e:
        errors.append(
            {
                "sql_error": True,
                "message": str(e),
                "documentation": getattr(e, "documentation", "/query/query-parameters.html"),
            }
        )
    except SQLValidationException as e:
        errors.append(
            {
                "sql_error": True,
                "message": str(e),
                "documentation": getattr(e, "documentation", "/query/query-parameters.html"),
            }
        )

    return {"errors": errors}


def validate_gcs_cron_expression(schedule_cron: str) -> Optional[str]:
    """
    We are using Google Cloud Scheduler (GCS) to create scheduled jobs, we need to validate the cron
    expression provided, to GCS standards. For example when a cron expression 0 0/1 * * * is provided
    GCS will not parse it correctly, since when steps are provided before the / e.g /1 GCS expects a range
    for it to run on the specified set schedule.

    We need to inform the user to use a valid GCS cron expression. In this case 0 0-23/1 * * *
    So we will validate based on the following valid ranges:
        minute         0-59
        hour           0-23
        day of month   1-31
        month          1-12 (or names, see below)
        day of week    0-7 (0 or 7 is Sunday, or use names)

    >>> validate_gcs_cron_expression('0 16/1 * * *')
    '0 16-23/1 * * *'
    >>> validate_gcs_cron_expression('* 16/1 * * *')
    '* 16-23/1 * * *'
    >>> validate_gcs_cron_expression('*/5 16/1 * * *')
    '*/5 16-23/1 * * *'
    >>> validate_gcs_cron_expression('5/15 * * * *')
    '5-59/15 * * * *'
    >>> print(validate_gcs_cron_expression('0 0-23/1 * * *'))
    None
    >>> validate_gcs_cron_expression('5/15 1/1 * * *')
    '5-59/15 1-23/1 * * *'
    >>> print(validate_gcs_cron_expression('0 * * * *'))
    None
    >>> print(validate_gcs_cron_expression('0 13 * * *'))
    None
    >>> print(validate_gcs_cron_expression('30 4 1,15 * 5'))
    None
    >>> print(validate_gcs_cron_expression('25 30 10 * *'))
    None
    >>> print(validate_gcs_cron_expression('0 22 * * 1-5'))
    None
    >>> print(validate_gcs_cron_expression('23 0-20/2 * * *'))
    None
    >>> print(validate_gcs_cron_expression('5 4 * * sun'))
    None
    >>> validate_gcs_cron_expression('0 0/5 14,18,3-39,52')
    '0 0-23/5 14,18,3-39,52'
    >>> print(validate_gcs_cron_expression('0 0,12 1 */2 *'))
    None
    >>> print(validate_gcs_cron_expression('0 0 12 */7 *'))
    None
    >>> print(validate_gcs_cron_expression('*/15 */6 */10 */4 1-5'))
    None
    >>> print(validate_gcs_cron_expression('*/15 * * * *'))
    None
    >>> print(validate_gcs_cron_expression('0 */1 * * *'))
    None
    """
    time_ranges = ["0-59", "0-23", "1-31", "1-12", "0-7"]
    suggested_cron_expression = ""
    for time, time_range in zip(schedule_cron.split(" "), time_ranges):
        if "/" in time:
            cron_suggestion = validate_cron_time_expression(time, time_range)
            if cron_suggestion.get("step_range"):
                time = f"{cron_suggestion.get('step_range')}/{cron_suggestion.get('step')}"
                suggested_cron_expression = "{} {}".format(suggested_cron_expression, time)
        else:
            suggested_cron_expression = "{} {}".format(suggested_cron_expression, time)
    suggested_cron_expression = suggested_cron_expression.strip()
    if schedule_cron == suggested_cron_expression:
        return None
    return suggested_cron_expression


def validate_cron_time_expression(time: str, time_step_range: str) -> Dict[str, str]:
    cron_suggestion = {"step": "", "step_range": ""}
    step_range, step = time.split("/")
    start_range, end_range = time_step_range.split("-")
    if "-" not in step_range and step_range != "*":
        cron_suggestion.update(
            {
                "step": str(step),
                "step_range": f"{step_range}-{end_range}",
            }
        )
    else:
        cron_suggestion.update(
            {
                "step": str(step),
                "step_range": step_range,
            }
        )
    return cron_suggestion
