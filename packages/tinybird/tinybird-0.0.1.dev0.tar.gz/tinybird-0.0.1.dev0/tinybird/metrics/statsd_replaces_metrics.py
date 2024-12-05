from tinybird_shared.metrics.statsd_client import statsd_client


def parse_prefix(message):
    def formatter(**kwargs):
        return f"{message.format(**kwargs)}"

    return formatter


class StatsdReplacesMetrics:
    replaces_origin_success = parse_prefix(
        "tinybird"
        f".{statsd_client.region_app_machine}"
        ".replaces"
        ".{replace_type}"
        ".origin"
        ".{database_server}"
        ".{origin_workspace_id}"
        ".{origin_datasource_id}"
        ".success"
        ".total"
    )

    replaces_origin_error = parse_prefix(
        "tinybird"
        f".{statsd_client.region_app_machine}"
        ".replaces"
        ".{replace_type}"
        ".origin"
        ".{database_server}"
        ".{origin_workspace_id}"
        ".{origin_datasource_id}"
        ".error"
        ".total"
    )

    replaces_dependent_error = parse_prefix(
        "tinybird"
        f".{statsd_client.region_app_machine}"
        ".replaces"
        ".{replace_type}"
        ".dependent"
        ".{database_server}"
        ".{destination_workspace_id}"
        ".{destination_datasource_id}"
        ".error"
        ".total"
    )

    replaces_dependent_success = parse_prefix(
        "tinybird"
        f".{statsd_client.region_app_machine}"
        ".replaces"
        ".{replace_type}"
        ".dependent"
        ".{database_server}"
        ".{destination_workspace_id}"
        ".{destination_datasource_id}"
        ".success"
        ".total"
    )
