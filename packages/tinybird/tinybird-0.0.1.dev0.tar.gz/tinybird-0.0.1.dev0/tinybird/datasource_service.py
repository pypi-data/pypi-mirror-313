import logging
from functools import partial
from typing import Optional

from tinybird import tracker
from tinybird.ch import ch_database_exists
from tinybird.data_connector import DataConnectors, DataLinker, DataSourceNotConnected, _get_resource_id_from_branch
from tinybird.datasource import Datasource
from tinybird.hook import (
    DeleteCompleteDatasourceHook,
    LandingDatasourceHook,
    LastDateDatasourceHook,
    PGSyncDatasourceHook,
)
from tinybird.ingest.cdk_utils import CDKUtils, is_cdk_service_datasource
from tinybird.ingest.data_connectors import ConnectorContext
from tinybird.ingest.preview_connectors.amazon_s3_connector import S3PreviewConnector
from tinybird.ingest.preview_connectors.amazon_s3_iam_connector import S3IAMPreviewConnector
from tinybird.ingest.preview_connectors.base_connector import BasePreviewConnector
from tinybird.ingest.preview_connectors.gcs_sa_connector import GCSSAPreviewConnector
from tinybird.iterating.branching_modes import BranchMode
from tinybird.iterating.hook import allow_force_delete_materialized_views
from tinybird.job import JobExecutor
from tinybird.pipe import DependentMaterializedNodeException, NodeNotFound, Pipe, PipeNode
from tinybird.syncasync import sync_to_async
from tinybird.table import drop_table
from tinybird.user import PipeNotFound, UserAccount
from tinybird.user import User as Workspace
from tinybird.user import Users as Workspaces
from tinybird.views.api_errors import RequestErrorException
from tinybird.views.api_errors.datasources import ClientErrorConflict, ServerErrorInternal
from tinybird.views.api_pipes import NodeUtils, PipeUtils
from tinybird.views.base import ApiHTTPError


class DatasourceService:
    @classmethod
    async def drop_datasource(
        cls,
        workspace: Workspace,
        ds: Datasource,
        force: bool,
        branch_mode: str,
        job_executor: Optional[JobExecutor],
        request_id: str,
        user_account: Optional[UserAccount],
        edited_by: Optional[str],
        hard_delete: bool = False,
        track_log: Optional[bool] = True,
    ) -> bool:
        pipe: Optional[Pipe]
        data_linker: Optional[DataLinker] = None

        # When using force, we remove the dependent resources automatically
        if force:
            # Remove dependent materialized views
            dep_pipes, _, _, mat_nodes_ids, _, _ = Workspaces.get_used_by_materialized_nodes(workspace, ds.id)

            for i, mat_node_id in enumerate(mat_nodes_ids):
                node: Optional[PipeNode] = None
                try:
                    pipe = Workspaces.get_pipe(workspace, dep_pipes[i])
                    if not pipe:
                        continue
                    node = pipe.pipeline.get_node(mat_node_id)
                except IndexError:
                    for p in dep_pipes:
                        pipe = Workspaces.get_pipe(workspace, p)
                        if not pipe:
                            continue
                        node = pipe.pipeline.get_node(mat_node_id)
                        if node:
                            break
                if not node:
                    continue

                await NodeUtils.delete_node_materialized_view(
                    workspace=workspace,
                    node=node,
                    cancel_fn=partial(PipeUtils.cancel_populate_jobs, workspace, node.id, job_executor),
                    hard_delete=hard_delete,
                )
                pipe = Workspaces.get_pipe(workspace, dep_pipes[i])
                if not pipe:
                    continue

                try:
                    await Workspaces.update_node_of_pipe(workspace.id, pipe.id, node, edited_by)
                except PipeNotFound:
                    raise ApiHTTPError(404, f"Pipe '{pipe.name}' not found.")

            dep_copy_pipes = Workspaces.get_used_by_copy(workspace, ds.id)

            # Remove dependent copy
            try:
                for copy_pipe in dep_copy_pipes:
                    copy_pipe_workspace_id: Optional[str] = copy_pipe.get("workspace")
                    copy_workspace = (
                        workspace
                        if copy_pipe_workspace_id == workspace.id
                        else (Workspace.get_by_id(copy_pipe_workspace_id) if copy_pipe_workspace_id else None)
                    )
                    assert isinstance(copy_workspace, Workspace)

                    pipe = None
                    pipe_id = copy_pipe.get("id")
                    pipe = copy_workspace.get_pipe(pipe_id) if pipe_id else None
                    if not pipe:
                        raise PipeNotFound()

                    node = pipe.pipeline.get_node(pipe.copy_node)
                    if not node:
                        raise NodeNotFound()

                    await NodeUtils.drop_node_copy(
                        workspace=copy_workspace,
                        pipe=pipe,
                        node_id=node.id,
                        edited_by=edited_by,
                        hard_delete=hard_delete,
                    )
            except Exception as e:
                message = f"There was a problem while trying to delete a copy when deleting the target data source {workspace.id}.{ds.id}: {e}"
                if hard_delete:
                    logging.warning(message)
                else:
                    logging.exception(message)

        for workspace_id in ds.shared_with:
            try:
                destination_workspace = Workspace.get_by_id(workspace_id)
                assert isinstance(destination_workspace, Workspace)
                assert isinstance(user_account, UserAccount)

                await Workspaces.stop_sharing_a_datasource(
                    user_account=user_account,
                    origin_workspace=workspace,
                    destination_workspace=destination_workspace,
                    datasource_id=ds.id,
                    check_used=False,
                )
            except DependentMaterializedNodeException as e:
                b_mode: BranchMode = BranchMode(branch_mode)
                if not allow_force_delete_materialized_views(workspace, branch_mode=b_mode):
                    raise RequestErrorException(
                        ClientErrorConflict.conflict_materialized_node(
                            break_ingestion_message=e.break_ingestion_message,
                            affected_materializations_message=e.affected_materializations_message,
                            dependent_pipes_message=e.dependent_pipes_message,
                        )
                    )

        ds.install_hook(DeleteCompleteDatasourceHook(workspace))
        ds.install_hook(PGSyncDatasourceHook(workspace))
        ds.install_hook(LandingDatasourceHook(workspace))
        ds.install_hook(LastDateDatasourceHook(workspace))

        data_linker_id = None
        data_linker_connector_id = None
        data_linker_service = None

        # The Kafka datasources in a branch will return `DataSourceNotConnected`
        # Therefore, it won't remove the linker from production
        try:
            data_linker = ds.get_data_linker()
            assert isinstance(data_linker, DataLinker)
            data_linker_id = data_linker.id
            data_linker_connector_id = data_linker.data_connector_id
            data_linker_service = data_linker.service
        except Exception:
            # If the datasource doesn't have a linker, might be for two reasons
            # 1. It's a normal datasource
            # 2. It's a Kafka datasource in a branch. Therefore, we can not just get the DataLinker doing `DataLinker.get_by_datasource_id(ds.id)`
            # We need to get the resource key from the branch and then get the DataLinker
            resouce_key = _get_resource_id_from_branch(ds.id, workspace)
            try:
                data_linker = DataLinker.get_by_datasource_id(resouce_key)
                DataLinker._delete(data_linker.id)
            except DataSourceNotConnected:
                pass
            pass
        else:
            DataLinker._delete(data_linker_id)
            await DataLinker.publish(data_linker_id)

        async def delete_bigquery_data():
            if is_cdk_service_datasource(ds.service):
                await CDKUtils.delete_dag(workspace.id, ds.id)

        if ds.service in [
            DataConnectors.AMAZON_DYNAMODB,
        ]:
            await PipeUtils.cancel_dynamodb_jobs(workspace.id, ds.id, job_executor)

        if ds.service in [
            DataConnectors.AMAZON_S3,
            DataConnectors.AMAZON_S3_IAMROLE,
            DataConnectors.GCLOUD_STORAGE,
        ]:
            connector: BasePreviewConnector = BasePreviewConnector()

            if ds.service == DataConnectors.AMAZON_S3:
                connector = S3PreviewConnector()

            if ds.service == DataConnectors.AMAZON_S3_IAMROLE:
                connector = S3IAMPreviewConnector()

            if ds.service == DataConnectors.GCLOUD_STORAGE:
                connector = GCSSAPreviewConnector()

            try:
                connector_context = ConnectorContext(connector)
                await connector_context.remove_linker(workspace.id, ds.id, job_executor)
            except Exception as e:
                logging.exception(e)
                raise RequestErrorException(ServerErrorInternal.failed_delete(error=e))

        ds_deleted = await Workspaces.drop_datasource_async(workspace, ds.id)
        if ds_deleted:
            try:
                main_workspace = workspace.get_main_workspace()
                await Workspaces.remove_resource_from_tags(main_workspace, resource_id=ds.id, resource_name=ds.name)
            except Exception as e:
                logging.exception(
                    f"Exception while removing Data Source from tags {str(e)} - ws: {workspace.id} - ds: {ds.name}"
                )

            try:
                await delete_bigquery_data()

                for hook in ds.hooks:
                    await sync_to_async(hook.before_delete)(ds)

                if not hard_delete or (
                    hard_delete and await ch_database_exists(workspace.database_server, workspace.database)
                ):
                    results = await drop_table(workspace, ds.id)
                    if results:
                        logging.exception(
                            f"Failed to delete some of the Data Source tables: workspace={workspace.id}, datasource={ds.id}, results={results}"
                        )
                for hook in ds.hooks:
                    await sync_to_async(hook.after_delete)(ds)
            except Exception as e:
                if not hard_delete:
                    logging.exception(e)
                raise RequestErrorException(ServerErrorInternal.failed_delete(error=e))
            finally:
                # When running this function from tinybird_tool to do a hard delete, we don't want to try to log this operation since it's time consuming
                if track_log:
                    tracker.track_hooks(ds.hook_log(), request_id=request_id, workspace=workspace)

                    if data_linker_id:
                        tracker.track_datasource_ops(
                            ds.operations_log(),
                            request_id=request_id,
                            connector=data_linker_connector_id,
                            service=data_linker_service,
                            workspace=workspace,
                        )
                    else:
                        tracker.track_datasource_ops(ds.operations_log(), request_id=request_id, workspace=workspace)
            return True
        return False
