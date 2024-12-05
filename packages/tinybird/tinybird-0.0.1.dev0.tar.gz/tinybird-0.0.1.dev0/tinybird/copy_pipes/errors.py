class CopyJobErrorMessages:
    generic = "There was a problem while copying data, kindly contact us at support@tinybird.co"
    timeout = (
        "There was a problem while copying data due to a timeout error ({timeout_seconds}s), "
        "if it's not possible to retry, kindly contact us at support@tinybird.co"
    )
    internal = "There was a internal problem while copying data, kindly retry or contact us at support@tinybird.co"
    timeout_backfill = "There was a problem while copying data due to a timeout error ({timeout_seconds}s). If you are trying to backfill data, try using a smaller time range using parameters."  # TODO: add link to docs https://gitlab.com/tinybird/analytics/-/issues/13404
