from dataclasses import dataclass
from typing import Optional, Tuple

from tinybird.hfi.hfi_defaults import DEFAULT_HTTP_ERROR
from tinybird_shared.clickhouse.errors import CHErrors

HFI_LOGGER_USER_AGENT = "tb-hfi-logger"


def is_materialized_view_error(error_msg: str) -> bool:
    return " to view" in error_msg


def get_mv_error_not_propagated(error: Optional[str] = None, url: Optional[str] = None) -> str:
    return (
        "Your data was received but it was not propagated due to a conflict with Materialized Views."
        + " Please review the Materialized Views linked to the Data Source and either check our docs to recover data or re-ingest again."
        + f" Error: {str(error)}"
        if error
        else "" + f" url={url}"
        if url
        else ""
    )


def get_mv_error_not_propagated_null_engine(error: Optional[str] = None, url: Optional[str] = None) -> str:
    return (
        "Your data has not been ingested to any datasource because it has Null Engine and it was not propagated to any Materialized View due to conflicts in them."
        + " Please review the Materialized Views linked to the Data Source and re-ingest again."
        + f" Error: {str(error)}"
        if error
        else "" + f" url={url}"
        if url
        else ""
    )


@dataclass(frozen=True)
class ErrorMessageAndHttpCode:
    error_message: str
    http_code: int


def get_error_message_and_http_code_for_ch_error_code(
    error_message: str, ch_error_code: int, default_http_error: int = DEFAULT_HTTP_ERROR
) -> Tuple[str, int]:
    ch_error_map = {
        CHErrors.TOO_MANY_SIMULTANEOUS_QUERIES: ErrorMessageAndHttpCode("", 503),
        CHErrors.TOO_MANY_PARTS: ErrorMessageAndHttpCode(error_message, 422),
    }

    ret_value = ch_error_map.get(ch_error_code, ErrorMessageAndHttpCode(error_message, default_http_error))
    return ret_value.error_message, ret_value.http_code
