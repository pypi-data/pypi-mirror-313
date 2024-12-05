import asyncio
import functools

from tornado.web import url

from tinybird.job import Job, JobAlreadyBeingCancelledException, JobNotInCancellableStatusException, filter_jobs
from tinybird.tokens import scopes
from tinybird.user import User as Workspace
from tinybird.views.api_errors.datasources import ClientErrorBadRequest, ClientErrorForbidden, ClientErrorNotFound
from tinybird.views.api_errors.jobs import JobFilterError
from tinybird.views.base import ApiHTTPError, BaseHandler, authenticated, requires_write_access, with_scope


class APIJobHandler(BaseHandler):
    async def check_valid_token(self, workspace: Workspace, job: Job) -> None:
        valid_token = True

        # We can get job status by using a workspace owned token
        # or an origin's one, if the current workspace is a branch
        valid_workspaces = [workspace.id]
        if workspace.is_branch and workspace.origin:
            valid_workspaces.append(workspace.origin)

        valid_token = job.user_id in valid_workspaces

        # If the Job is from a Release, we need to include access from the Main and Branch Workspaces
        if not valid_token:
            branches = await workspace.get_branches()
            branches_ids = [branch.get("id", "") for branch in branches]
            valid_workspaces.extend(branches_ids)
            job_workspace = Workspace.get_by_id(job.user_id) if job.user_id else None
            if job_workspace and job_workspace.main_id:
                valid_token = job_workspace.main_id in valid_workspaces

        if not valid_token:
            user_account = self.get_user_from_db()
            if not user_account or not user_account.is_tinybird:
                raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

    @authenticated
    @with_scope(scopes.DATASOURCES_CREATE)
    async def get(self, job_id):
        """
        Get the details of a specific Job. You can get the details of a Job by using its ID.

        .. code-block:: bash
            :caption: Get the details of a Job

            curl \\
            -H "Authorization: Bearer <token>" \\
            "https://api.tinybird.co/v0/jobs/:job_id"

        You will get a JSON response with the details of the Job, including the ``kind``, ``status``, ``id``, ``created_at``, ``updated_at``, and the ``datasource`` associated with the Job. This is available for 48h after the Job creation. After that, you can consult the Job details in the Service Data Source jobs_log.

        .. sourcecode:: json
            :caption: Job details

            {
            "kind": "import",
            "id": "d5b869ed-3a74-45f9-af54-57350aae4cef",
            "job_id": "d5b869ed-3a74-45f9-af54-57350aae4cef",
            "status": "done",
            "created_at": "2024-07-22 11:47:58.207606",
            "updated_at": "2024-07-22 11:48:52.971327",
            "started_at": "2024-07-22 11:47:58.351734",
            "is_cancellable": false,
            "mode": "append",
            "datasource": {
                "id": "t_caf95c54174e48f488ea65d181eb5b75",
                "name": "events",
                "cluster": "default",
                "tags": {

                },
                "created_at": "2024-07-22 11:47:51.807384",
                "updated_at": "2024-07-22 11:48:52.726243",
                "replicated": true,
                "version": 0,
                "project": null,
                "headers": {
                "cached_delimiter": ","
                },
                "shared_with": [

                ],
                "engine": {
                "engine": "MergeTree",
                "partition_key": "toYear(date)",
                "sorting_key": "date, user_id, event, extra_data"
                },
                "description": "",
                "used_by": [

                ],
                "last_commit": {
                "content_sha": "",
                "status": "changed",
                "path": ""
                },
                "errors_discarded_at": null,
                "type": "csv"
            },
            "import_id": "d5b869ed-3a74-45f9-af54-57350aae4cef",
            "url": "https://storage.googleapis.com/tinybird-assets/datasets/guides/events_50M_1.csv",
            "statistics": {
                "bytes": 1592720209,
                "row_count": 50000000
            },
            "quarantine_rows": 0,
            "invalid_lines": 0
            }

        """
        workspace = self.get_workspace_from_db()

        job = Job.get_by_id(job_id)
        if not job:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.job_not_found(id=job_id))

        await self.check_valid_token(workspace=workspace, job=job)

        debug = self.get_argument("debug", None)
        job_response = job.to_json(workspace, debug=debug)
        progress_details = await job.progress_details()
        job_response.update(progress_details)

        self.write_json(job_response)


class APIJobCancelHandler(BaseHandler):
    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, job_id):
        """
        With this endpoint you can try to cancel an existing Job. All jobs can be cancelled if they are in the "waiting"
        status, but you can't cancel a Job in "done" or "error" status.

        In the case of the job of type "populate", you can cancel it in the "working" state.

        After successfully starting the cancellation process, you will see two different status in the job:
        - "cancelling": The Job can't be immediately cancelled as it's doing some work, but the cancellation will eventually happen.
        - "cancelled": The Job has been completely cancelled.

        A Job cancellation doesn't guarantee a complete rollback of the changes being made by it, sometimes you will need to delete new inserted rows or datasources created.

        The fastest way to know if a job is cancellable, is just reading the "is_cancellable" key inside the job JSON description.

        Depending on the Job and its status, when you try to cancel it you may get different responses:
        - HTTP Code 200: The Job has successfully started the cancellation process. Remember that if the Job has now a "cancelling" status, it may need some time to completely cancel itself. This request will return the status of the job.
        - HTTP Code 404: Job not found.
        - HTTP Code 403: The token provided doesn't have access to this Job.
        - HTTP Code 400: Job is not in a cancellable status or you are trying to cancel a job which is already in the "cancelling" state.

        .. code-block:: bash
            :caption: Try to cancel a Job

            curl \\
            -H "Authorization: Bearer <token>" \\
            -X POST "https://api.tinybird.co/v0/jobs/:job_id/cancel"

        .. sourcecode:: json
            :caption: Populate Job in cancelling state right after the cancellation request.

            {
                "kind": "populateview",
                "id": "32c3438d-582e-4a6f-9b57-7d7a3bfbeb8c",
                "job_id": "32c3438d-582e-4a6f-9b57-7d7a3bfbeb8c",
                "status": "cancelling",
                "created_at": "2021-03-17 18:56:23.939380",
                "updated_at": "2021-03-17 18:56:44.343245",
                "is_cancellable": false,
                "datasource": {
                    "id": "t_02043945875b4070ae975f3812444b76",
                    "name": "your_datasource_name",
                    "cluster": null,
                    "tags": {},
                    "created_at": "2020-07-15 10:55:12.427269",
                    "updated_at": "2020-07-15 10:55:12.427270",
                    "statistics": null,
                    "replicated": false,
                    "version": 0,
                    "project": null,
                    "used_by": []
                },
                "query_id": "01HSZ9WJES5QEZZM4TGDD3YFZ2",
                "pipe_id": "t_7fa8009023a245b696b4f2f7195b23c3",
                "pipe_name": "top_product_per_day",
                "queries": [
                    {
                        "query_id": "01HSZ9WJES5QEZZM4TGDD3YFZ2",
                        "status": "done"
                    },
                    {
                        "query_id": "01HSZ9WY6QS6XAMBHZMSNB1G75",
                        "status": "done"
                    },
                    {
                        "query_id": "01HSZ9X8YVEQ0PXA6T2HZQFFPX",
                        "status": "working"
                    },
                    {
                        "query_id": "01HSZQ5YX0517X81JBF9G9HB2P",
                        "status": "waiting"
                    },
                    {
                        "query_id": "01HSZQ6PZJA3P81RC6Q6EF6HMK",
                        "status": "waiting"
                    },
                    {
                        "query_id": "01HSZQ76D7YYFB16TFT32KXMCY",
                        "status": "waiting"
                    }
                ],
                "progress_percentage": 50.0
            }

        """
        workspace = self.get_workspace_from_db()

        job = Job.get_by_id(job_id)

        if not job:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.job_not_found(id=job_id))

        if not Job.is_owned_by(job_id, workspace.id):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

        try:
            job.try_to_cancel(self.application.job_executor)

        except JobNotInCancellableStatusException:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.job_not_in_cancellable_status())

        except JobAlreadyBeingCancelledException:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.job_already_being_canceled())

        job = Job.get_by_id(job_id)
        if not job:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.job_not_found(id=job_id))

        debug = self.get_argument("debug", None)
        job_response = job.to_json(workspace, debug=debug)
        progress_details = await job.progress_details()
        job_response.update(progress_details)

        self.write_json(job_response)


class APIJobsListHandler(BaseHandler):
    @authenticated
    @with_scope(scopes.DATASOURCES_CREATE)
    async def get(self):
        """
        We can get a list of the last 100 jobs in the last 48 hours, with the possibility of filtering them by kind, status, pipe_id, pipe_name, created_after, and created_before.

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "kind", "String", "This will return only the jobs with that particular kind. Example: ``kind=populateview`` or ``kind=copy`` or ``kind=import``"
            "status", "String", "This will return only the jobs with the status provided. Example: ``status=done`` or ``status=waiting`` or ``status=working`` or ``status=error``"
            "pipe_id", "String", "This will return only the jobs associated with the provided pipe id. Example: ``pipe_id=t_31a0ff508c9843b59c32f7f81a156968``"
            "pipe_name", "String", "This will return only the jobs associated with the provided pipe name. Example: ``pipe_name=test_pipe``"
            "created_after", "String", "This will return jobs that were created after the provided date in the ISO 8601 standard date format. Example: ``created_after=2023-06-15T18:13:25.855Z``"
            "created_before", "String", "This will return jobs that were created before the provided date in the ISO 8601 standard date format. Example: ``created_before=2023-06-19T18:13:25.855Z``"

        .. code-block:: bash
            :caption: Getting the latest jobs

            curl \\
            -H "Authorization: Bearer <token>" \\
            "https://api.tinybird.co/v0/jobs" \\

        You will get a list of jobs with the ``kind``, ``status``, ``id``, and the ``url`` to access the specific information about that job.

        .. sourcecode:: json
            :caption: Jobs list

            {
                "jobs": [
                    {
                        "id": "c8ae13ef-e739-40b6-8bd5-b1e07c8671c2",
                        "kind": "import",
                        "status": "done",
                        "created_at": "2020-12-04 15:08:33.214377",
                        "updated_at": "2020-12-04 15:08:33.396286",
                        "job_url": "https://api.tinybird.co/v0/jobs/c8ae13ef-e739-40b6-8bd5-b1e07c8671c2",
                        "datasource": {
                            "id": "t_31a0ff508c9843b59c32f7f81a156968",
                            "name": "my_datasource_1"
                        }
                    },
                    {
                        "id": "1f6a5a3d-cfcb-4244-ba0b-0bfa1d1752fb",
                        "kind": "import",
                        "status": "error",
                        "created_at": "2020-12-04 15:08:09.051310",
                        "updated_at": "2020-12-04 15:08:09.263055",
                        "job_url": "https://api.tinybird.co/v0/jobs/1f6a5a3d-cfcb-4244-ba0b-0bfa1d1752fb",
                        "datasource": {
                            "id": "t_49806938714f4b72a225599cdee6d3ab",
                            "name": "my_datasource_2"
                        }
                    }
                ]
            }

        Job details in ``job_url`` will be available for 48h after its creation.
        """
        workspace = self.get_workspace_from_db()
        kind = self.get_argument("kind", None)
        status = self.get_argument("status", None)
        created_after = self.get_argument("created_after", None)
        created_before = self.get_argument("created_before", None)
        pipe_id = self.get_argument("pipe_id", None)
        pipe_name = self.get_argument("pipe_name", None)

        max_jobs_linked_workspace = Job.get_owner_max_children()
        prepared_get_jobs_from_workspace = functools.partial(
            Job.get_all_by_owner, workspace.id, limit=max_jobs_linked_workspace
        )
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, prepared_get_jobs_from_workspace)
        workspace_jobs = sorted(res, key=lambda j: j.created_at, reverse=True)
        try:
            if kind or status or created_before or created_after or pipe_id or pipe_name:
                workspace_jobs = filter_jobs(
                    workspace_jobs=workspace_jobs,
                    filters={
                        "kind": kind,
                        "status": status,
                        "created_after": created_after,
                        "created_before": created_before,
                        "pipe_id": pipe_id,
                        "pipe_name": pipe_name,
                    },
                )
            jobs = []
            for job in workspace_jobs[:100]:
                workspace_job = job.to_public_json(job, self.application.settings["api_host"])
                jobs.append(workspace_job)
            self.write_json({"jobs": jobs})
        except (TypeError, ValueError) as e:
            raise ApiHTTPError.from_request_error(JobFilterError.invalid_date_format(error=str(e).lower()))


def handlers():
    return [
        url(r"/v0/jobs/?", APIJobsListHandler),
        url(r"/v0/jobs/(.+)/cancel", APIJobCancelHandler),
        url(r"/v0/jobs/(.+)", APIJobHandler),
    ]
