import re
from urllib.parse import urlparse

from tinybird.user import User


def build_error_summary(errors, quarantine_rows, invalid_lines, include_errors=False):
    errors_message = None
    if not errors:
        errors_message = ""
    elif include_errors:
        errors_message = f" {'. '.join(errors)}"
    else:
        errors_message = " Check 'errors' for more information."

    if quarantine_rows or invalid_lines:
        rows = "rows" if quarantine_rows > 1 else "row"
        lines = "lines" if invalid_lines > 1 else "line"
        quarantine = f"{quarantine_rows} {rows} in quarantine" if quarantine_rows else ""
        _and = " and" if quarantine_rows and invalid_lines else ""
        invalid = f" {invalid_lines} invalid {lines}" if invalid_lines else ""
        return f"There was an error with file contents: {quarantine}{_and}{invalid}.{errors_message}"

    return f"There was an error when attempting to import your data.{errors_message}"


def get_errors(blocks):
    errors = set()
    quarantine_rows = 0
    invalid_lines = 0

    for x in blocks:
        if x.get("processing_error"):
            errors.add(x["processing_error"])
        if x.get("process_return"):
            for y in x["process_return"]:
                quarantine_rows += y.get("quarantine", 0)
                invalid_lines += y.get("invalid_lines", 0)
        if x.get("fetch_error"):
            errors.add(f"{x['fetch_error']}")

    return list(errors), quarantine_rows, invalid_lines


def validate_url_error(url: str) -> bool:
    parsed = urlparse(url)

    return parsed.scheme not in ("http", "https")


def replace_table_id_with_datasource_id(ws, error, error_datasource_id=None):
    pipe = None
    ds = None

    try:
        # d_*.t_... or d_*.j_...
        match_iter = re.finditer("(?:d_[a-zA-Z0-9_]*\.)?(?:t_[a-zA-Z0-9_]{32}|j_[a-zA-Z0-9_]{32})", error)

        # Keep only unique finds (comparing the strings) and order them by length so 'd_xxxx.table'
        # appears before 'table'
        matches = list(set([match.group() for match in match_iter]))
        matches.sort(key=len, reverse=True)

        for match_group in matches:
            ws_name = ""
            ds_name = ""
            parts = match_group.split(".")
            if len(parts) == 1:
                database_name = ""
                table = parts[0]
            else:
                database_name = parts[0]
                table = parts[1]

            table_split = table.split("_")
            datasource_id = f"{table_split[0]}_{table_split[1]}"
            ds = ws.get_datasource(ds_name_or_id=datasource_id, include_read_only=True)

            if not ds:
                pipe = ws.get_pipe_by_node(datasource_id)
                node = ws.get_node(datasource_id)

                if node:
                    ds = ws.get_datasource(node.materialized)
                # shared data source
                else:
                    if error_datasource_id:
                        ds = ws.get_datasource(error_datasource_id, include_read_only=True)
                        for id in ds.shared_with:
                            ws = User.get_by_id(id)
                            if not database_name or ws.database == database_name:
                                pipe = ws.get_pipe_by_node(datasource_id)
                                node = ws.get_node(datasource_id)
                                if node:
                                    ds = ws.get_datasource(node.materialized)
                                    break
                                if pipe:
                                    break

                if pipe:
                    extra_info = (
                        f"{ws.name}.{pipe.name} -> node: {node.name} with destination Data Source {ws.name}.{ds.name}"
                    )
                to_view = "while pushing to Materialized View"
                ds_name = ds.name
            else:
                to_view = "while pushing to Data Source"
                shared_from = ds.to_dict().get("shared_from", {})
                if shared_from:
                    ds_name = shared_from.get("original_ds_name", ds.name)
                    ws_name = shared_from.get("original_workspace_name", ws.name)
                    extra_info = f"{ds.name}"
                else:
                    ds_name = ds.name
                    ws_name = ws.name
                    extra_info = f"{ws.name}.{ds.name}"

            if extra_info:
                error = error.replace(match_group, extra_info)

            if database_name and ws_name:
                error = error.replace(database_name, ws_name)

            if ds:
                error = error.replace(f"{ds.id}", f"{ds_name}")
                error = error.replace("in table ", "in Data Source ")
                error = error.replace("from table ", "from Data Source ")

            if to_view:
                error = error.replace("while pushing to view", to_view)
    except Exception:
        pass

    return error
