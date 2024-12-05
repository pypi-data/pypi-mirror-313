import logging
import os
import re
import shutil
import tempfile

import tornado
from streaming_form_data.parser import StreamingFormDataParser
from streaming_form_data.targets import FileTarget
from tornado.web import url

from tinybird.client import TinyB
from tinybird.config import VERSION
from tinybird.datafile import Datafile, folder_push, get_project_filenames, parse_datasource, parse_pipe
from tinybird.token_scope import scopes

from ..limits import Limit
from .base import ApiHTTPError, BaseHandler, authenticated


@tornado.web.stream_request_body
class APIDatafilesHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def data_received(self, chunk):
        self._parser.data_received(chunk)

    async def prepare(self):
        filenames = self.get_argument("filenames", None)
        content_type = self.request.headers.get("content-type", "")
        self.multipart = content_type.startswith("multipart/form-data")

        if not filenames:
            raise ApiHTTPError(
                400,
                log_message="Missing arguments: `filenames` argument not found. Make sure `filenames` argument is provided or contact us at support@tinybird.co",
            )

        if not self.multipart:
            raise ApiHTTPError(
                400,
                log_message="Invalid content: Content-type is not `multipart/form-data`. Make sure Content-Type is correct or contact us at support@tinybird.co",
            )

        self._parser = StreamingFormDataParser(headers=self.request.headers)
        self.folder = tempfile.mkdtemp()

        for name in filenames.split(","):
            self.file_ = FileTarget(os.path.join(self.folder, name))
            self._parser.register(name, self.file_)

    def parse_error(self, e: Exception) -> str:
        error = str(e)
        try:
            error = re.sub(r"\x1b\[\d+m", "", error)
            error = re.sub(r"\*\*", "", error)
        except Exception:
            pass
        return error


class APIDatafilesCheckHandler(APIDatafilesHandler):
    @authenticated
    async def post(self):
        filenames = get_project_filenames(self.folder)
        is_from_ui = self.get_argument("from", None) == "ui"
        try:
            analysis = []
            for filename in filenames:
                doc: Datafile
                if ".pipe" in filename:
                    doc = parse_pipe(filename, hide_folders=is_from_ui)
                else:
                    doc = parse_datasource(filename, hide_folders=is_from_ui)
                name = filename.replace(f"{self.folder}/", "")
                analysis.append({"name": name, "nodes": doc.nodes})
            self.write_json({"analysis": analysis})

        except Exception as e:
            error = self.parse_error(e)
            logging.exception(error)
            raise ApiHTTPError(400, log_message=error)
        finally:
            shutil.rmtree(self.folder, ignore_errors=True)


class APIDatafilesPushHandler(APIDatafilesHandler):
    async def push_datafiles(
        self, tb_host: str, token: str, force: bool, dry_run: bool, hide_folders: bool = False
    ) -> None:
        # Mimic `tb push`
        # Default values extracted from click parameters config in tb_cli::push()
        filenames = None
        check = False
        push_deps = True
        debug = False
        populate = False
        populate_subset = None
        populate_condition = None
        upload_fixtures = False
        wait = False
        ignore_sql_errors = True
        skip_confirmation = True
        only_response_times = False
        workspace_map = None
        workspace_lib_paths = None
        no_versions = False
        run_tests = False
        tests_to_run = 0
        tests_sample_by_params = 1
        tests_failfast = False
        tests_ignore_order = False
        raise_on_exists = True

        tb_client = TinyB(token, tb_host, VERSION)

        await folder_push(
            tb_client,
            filenames=filenames,
            dry_run=dry_run,
            check=check,
            push_deps=push_deps,
            only_changes=False,
            debug=debug,
            force=force,
            folder=self.folder,
            populate=populate,
            populate_subset=populate_subset,
            populate_condition=populate_condition,
            upload_fixtures=upload_fixtures,
            wait=wait,
            ignore_sql_errors=ignore_sql_errors,
            skip_confirmation=skip_confirmation,
            only_response_times=only_response_times,
            workspace_map=workspace_map,
            workspace_lib_paths=workspace_lib_paths,
            no_versions=no_versions,
            run_tests=run_tests,
            tests_to_run=tests_to_run,
            tests_sample_by_params=tests_sample_by_params,
            tests_failfast=tests_failfast,
            tests_ignore_order=tests_ignore_order,
            raise_on_exists=raise_on_exists,
            hide_folders=hide_folders,
        )

    @authenticated
    async def post(self):
        await self.check_rate_limit(Limit.api_datasources_create_schema)
        workspace = self.get_current_workspace()
        region = self.get_current_region()
        tb_host = (
            self.get_region_config(region)["api_host"] if region is not None else self.application.settings.get("host")
        )
        token = workspace.get_token_for_scope(scopes.ADMIN)
        force = self.get_argument("force", "false") == "true"
        dry_run = self.get_argument("dry_run", "false") == "true"
        is_from_ui = self.get_argument("from", None) == "ui"
        try:
            await self.push_datafiles(tb_host, token, force=force, dry_run=dry_run, hide_folders=is_from_ui)
        except Exception as e:
            error = self.parse_error(e)
            logging.exception(error)
            raise ApiHTTPError(400, log_message=error)
        finally:
            shutil.rmtree(self.folder, ignore_errors=True)


def handlers():
    return [url(r"/v0/datafiles/check", APIDatafilesCheckHandler), url(r"/v0/datafiles", APIDatafilesPushHandler)]
