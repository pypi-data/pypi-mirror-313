import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Tuple

import orjson
from tornado.web import url

from tinybird.datasource import Datasource
from tinybird.integrations.s3 import get_data_connector, get_files_in_bucket, sign_s3_url
from tinybird.providers.aws.s3 import parse_s3_url
from tinybird.views.base import ApiHTTPError

from ..ch import HTTPClient, ch_get_replicas_with_problems_per_cluster_host, ch_get_tables_metadata_sync
from ..user import User as Workspace
from ..user import public
from ..user_tables import get_all_tables
from .base import BaseHandler


class APIHealthHandler(BaseHandler):
    async def get(self) -> None:
        self.set_header("content-type", "application/json")
        self.write({"status": "ok"})


class APIHealthOrphanHandler(BaseHandler):
    def get_int_argument(self, name: str, default: int) -> int:
        try:
            return int(self.get_argument(name, str(default)))
        except Exception:
            return default

    async def get(self) -> None:
        date_format = "%Y-%m-%d %H:%M:%S"
        secret = self.get_argument("secret", None)
        only_materialized = self.get_argument("only_materialized", "false") == "true"
        # list of infixes we use when we generate temp tables, we use this list to discard tables or matviews including the infix so we have a better vision of what's actually orphan
        # _filtered,_generator,_replaced_,_mirror_,tmp_populate,_quarantine
        avoid_temp_tables = self.get_argument("avoid_temp_tables", None)
        if avoid_temp_tables:
            avoid_temp_tables = avoid_temp_tables.split(",")
        avoid_database_names = self.get_argument("avoid_database_names", "system,default")
        avoid_database_servers = self.get_argument("avoid_database_servers", None)
        database_names = self.get_argument("database_names", None)
        days = self.get_int_argument("days", 2)

        def to_s(x: object) -> str:
            return str(x).strip()

        avoid_database_names = tuple(map(to_s, avoid_database_names.split(",")))
        database_names = tuple(map(to_s, database_names.split(","))) if database_names else None
        avoid_database_servers = list(map(to_s, avoid_database_servers.split(","))) if avoid_database_servers else None

        if secret != "speed_wins":
            self.set_status(404)
            self.render("404.html")
            return

        def get_metadata_information() -> Tuple[set, Dict[Any, Any]]:
            _, users_tables, ch_servers = get_all_tables(
                only_materialized=only_materialized, avoid_database_servers=avoid_database_servers
            )
            ch_tables = ch_get_tables_metadata_sync(
                database_servers=ch_servers,
                avoid_database_names=avoid_database_names,
                database_names=database_names,
                only_materialized=only_materialized,
            )
            return (users_tables, ch_tables)

        (users_tables, ch_tables) = await asyncio.get_event_loop().run_in_executor(
            None, lambda: get_metadata_information()
        )

        orphan_tables = []
        for t, (_engine, size, mtime, _database_server, _count, _cluster) in ch_tables.items():
            if t not in users_tables:
                mdatetime = datetime.strptime(mtime, date_format)
                if (datetime.now() - mdatetime).days >= days:
                    if not avoid_temp_tables:
                        orphan_tables.append({f"{t[0]}.{t[1]}": f"{size}"})
                    else:
                        if not any([temp for temp in avoid_temp_tables if temp in t[1]]):
                            orphan_tables.append({f"{t[0]}.{t[1]}": f"{size}"})

        self.set_header("content-type", "application/json")
        if orphan_tables:
            if only_materialized:
                self.set_status(420, "error: found orphan materialized views")
                self.write_json(
                    {
                        "status": "error",
                        "orphan_matviews": orphan_tables,
                        "message": "orphan materialized views are materialized views in ClickHouse with no corresponding materialized node in Redis. This can have very bad consequences, since we might be duplicating data in the target Data Source, to mitigate the issue we should delete the Materialized View and to fix it find the reason why it was not deleted in the first place.",
                    }
                )
            else:
                self.set_status(420, "error: found orphan tables")
                self.write_json(
                    {
                        "status": "error",
                        "orphan_tables": orphan_tables,
                        "message": "orphan tables are tables in ClickHouse with no corresponding Data Source in Redis. Ideally we should not have orphan tables since they indicate a bug in some of our APIs. If tables are bigger than 50GB it is safe to just remove them by now.",
                    }
                )
        else:
            self.write_json({"status": "ok"})


class APIHealthReplicasHandler(BaseHandler):
    def get_int_argument(self, name: str, default: int) -> int:
        try:
            return int(self.get_argument(name, str(default)))
        except Exception:
            return default

    async def get(self) -> None:
        secret = self.get_argument("secret", None)
        report_public = bool(self.get_argument("public", False))

        if secret != "speed_wins":
            self.set_status(404)
            self.render("404.html")
            return

        kwchecks = dict(
            future_parts=self.get_int_argument("future_parts", 20),
            parts_to_check=self.get_int_argument("parts_to_check", 10),
            queue_size=self.get_int_argument("queue_size", 100),
            inserts_in_queue=self.get_int_argument("inserts_in_queue", 50),
            merges_in_queue=self.get_int_argument("merges_in_queue", 50),
            absolute_delay=self.get_int_argument("absolute_delay", 30),
        )

        u = public.get_public_user()
        replicas_problems = await ch_get_replicas_with_problems_per_cluster_host(
            database_server=u["database_server"], **kwchecks
        )

        errors = defaultdict(list)
        for cluster_host, rows in replicas_problems.items():
            if not len(rows):
                continue
            for row in rows:
                if report_public or row["database"] != "public":
                    errors[cluster_host].append(row)

        self.set_header("content-type", "application/json")
        self.set_span_tag({"errors": errors})
        if errors:
            self.set_status(420, "error: wrong replicas status")
            self.write_json({"status": "error", "errors": errors})
        else:
            self.write_json({"status": "ok"})


class APIHealthS3Handler(BaseHandler):
    async def get(self) -> None:
        secret = self.get_argument("secret", None)
        workspace_id = self.get_argument("workspace_id", None)
        months = self.get_argument("months", "1")
        datasource_id = self.get_argument("datasource_id", None)

        if secret != "speed_wins":
            self.set_status(404)
            self.render("404.html")
            return

        self.set_header("content-type", "application/json")
        workspace = Workspace.get_by_id(workspace_id)

        all_files = []
        dss = []
        result = []

        if datasource_id:
            datasource = workspace.get_datasource(datasource_id)
            if not datasource:
                raise ApiHTTPError(404, f"datasource {datasource_id} not found")
            datasources = [datasource]
        else:
            datasources = workspace.get_datasources()

        # get files in bucket for each data source
        for ds in datasources:
            if "s3" in ds.datasource_type:
                dss.append(ds)
                try:
                    all_files += await get_files_in_bucket(workspace_id, ds.id)
                except Exception as e:
                    raise ApiHTTPError(500, str(e)) from e

        # get all ds_ops_log entries in last months to compare with files in bucket
        datasources_info = await get_ds_ops_log(dss, workspace.id, months)
        if not datasources_info:
            self.write_json({"not_ingested_files": "cannot detect not ingested files"})
            return

        first_ds_infos = {}
        for element in all_files:
            if element["datasource_id"] not in datasources_info:
                logging.exception(f"no datasource_info for {element['datasource_id']}")
                continue
            ds_info = datasources_info[element["datasource_id"]]
            ds_info_iterator = iter(ds_info.items())

            # TODO: build the URL from the data connector info instead from ds_ops_log
            while element["datasource_id"] not in first_ds_infos:
                try:
                    first_key, first_ds_info = next(ds_info_iterator)
                    if "amazonaws.com" in first_ds_info["file_url"]:
                        first_ds_infos[element["datasource_id"]] = first_ds_info
                        break
                except StopIteration:
                    logging.warning("No match found in ds_info")
                    break

            first_ds_info = first_ds_infos[element["datasource_id"]]
            # when a file in the bucket is not in ds_ops_log, build the URL and sign it
            if element["key"] not in ds_info:
                url = first_ds_info["file_url"].split("amazonaws.com")[0] + "amazonaws.com/" + element["key"]
                try:
                    data_connector, _ = get_data_connector(workspace, element["datasource_id"])
                except ValueError as e:
                    logging.warning(e)
                    continue
                signed_url = await sign_s3_url(data_connector.id, workspace, url)
                if isinstance(signed_url, str):
                    element.update({"signed_url": signed_url})
                    result.append(element)

        self.write_json({"not_ingested_files": result})


async def get_ds_ops_log(datasources: List[Datasource], workspace_id: str, months: str) -> Dict[str, Dict[str, Any]]:
    pu = public.get_public_user()
    ds = pu.get_datasource("datasources_ops_log")
    if not ds:
        return {}

    tables_in_sql = ", ".join([f"'{ds.id}'" for ds in datasources])
    sql = f"""
    SELECT
        Options.Values[1] as file_url,
        decodeURLComponent(path) decoded_path,
        arrayStringConcat(arraySlice(splitByChar('/', arrayStringConcat(arraySlice(splitByChar('?', file_url), 1, 1), '')), 4), '/') AS path,
        datasource_id as id
    FROM {ds.id}
    WHERE
        user_id = '{workspace_id}'
        AND datasource_id IN ({tables_in_sql})
        AND event_type = 'append'
        AND timestamp > now() - interval {months} month
    FORMAT JSON
    """
    client = HTTPClient(pu.database_server, database=pu.database)
    body = None
    try:
        _, body = await client.query(sql, read_only=True, max_execution_time=3)
        rows = orjson.loads(body)["data"]
    except Exception:
        logging.warning(f"Query failed to retrieve ds_ops_log information: SQL={sql} BODY={body!r}")
        rows = []
    result: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if row["id"] not in result:
            result[row["id"]] = {}
        bucket_name = ""
        try:
            bucket_name, _ = parse_s3_url(row["file_url"])
        except Exception:
            pass

        # the bucket name can be as a subdomain or in the path
        extra_decoded_path = row["decoded_path"].split(bucket_name + "/")[-1] if bucket_name else None
        result[row["id"]][row["decoded_path"]] = row
        result[row["id"]][extra_decoded_path] = row  # type: ignore

    return result


def handlers() -> List[url]:
    return [
        url(r"/v0/health", APIHealthHandler),  # TODO deprecated #941
        url(r"/v0/health_replicas", APIHealthReplicasHandler),
        url(r"/v0/health_orphan", APIHealthOrphanHandler),
        url(r"/v0/health_s3", APIHealthS3Handler),
    ]
