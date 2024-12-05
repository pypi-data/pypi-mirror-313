import logging
from typing import List, Optional

from tinybird.datasource import BranchDatasource, Datasource
from tinybird.hook import Hook, MVToRecalculate
from tinybird.iterating.branching_modes import BranchMode
from tinybird.pipe import PipeNode
from tinybird.resource import Resource
from tinybird.syncasync import async_to_sync
from tinybird.table import drop_table
from tinybird.user import User, Users
from tinybird.views.shared.utils import NodeUtils
from tinybird.workspace_service import CreateBranchResourceError, WorkspaceService


class CreateCascadeDatasourceHook(Hook):
    def should_run_after_create(self, datasource: Datasource) -> bool:
        return not should_drop_table_on_create_table(self.user, datasource.name)

    def before_create(self, datasource: Datasource):
        if should_drop_table_on_create_table(self.user, datasource.name):
            # As we reuse the same id and ZK path, we need to drop the table with SYNC
            async_to_sync(drop_table)(self.user, datasource.id, sync=True)

    def after_create(self, datasource: Datasource):
        if not self.should_run_after_create(datasource):
            return

        snapshot: Optional[User] = self.user.get_snapshot()
        if not snapshot:
            raise ValueError("Iterating hook error: snapshot not found")

        ds = self.user.get_datasource(datasource.name)
        if not ds:
            # it's a new data source, nothing to do here
            # note self.user is not a fresh copy from Redis
            return

        # get materialized nodes pointing at the data source
        other_mvs_to_recalculate: List[MVToRecalculate] = []
        for p in self.user.get_pipes():
            for _node in p.pipeline.nodes:
                if _node.materialized == ds.id:
                    other_mvs_to_recalculate.append(MVToRecalculate(p, _node, False))

        fn = async_to_sync(self.update_user_after_create)
        self.user = fn(datasource, other_mvs_to_recalculate)

    async def update_user_after_create(
        self, datasource: Datasource, other_mvs_to_recalculate: List[MVToRecalculate]
    ) -> User:
        response_mv: List[CreateBranchResourceError] = []
        user = User.get_by_id(self.user.id)
        new_datasource = user.get_datasource(datasource.name)
        if not new_datasource:
            raise ValueError(f"Iterating hook error: datasource {datasource.name} not found")
        for mv in other_mvs_to_recalculate:
            await self.process_mv(user, mv.node.id)
            pipe = user.get_pipe(mv.pipe.id)
            if not pipe:
                logging.error("pipe %s not found", mv.pipe.id)
                continue
            node = pipe.pipeline.get_node(mv.node.name)
            if not node:
                logging.error("node %s not found", mv.node.name)
                continue

            if not node.materialized:
                node.materialized = new_datasource.id
            await WorkspaceService.clone_view(user, pipe, node, response_mv)
            if len(response_mv) and any([r for r in response_mv if r["error"]]):
                raise ValueError("Iterating hook error:" + "\n".join([r["error"] for r in response_mv if r["error"]]))
            Users.update_pipe(user, pipe)
        return User.get_by_id(self.user.id)

    def unlink_node_in_branch(self, branch: User, node: PipeNode) -> Optional[PipeNode]:
        pipe = branch.get_pipe_by_node(node.id)
        if not pipe:
            logging.error("pipe not found for node %s", node.id)
            return None
        _node = pipe.pipeline.get_node(node.id)
        if not _node:
            raise ValueError(f"Iterating hook error: node {node.id} not found")
        branch.drop_node_from_pipe(pipe.id, _node.id, "")
        _node.id = Resource.guid()
        _node.materialized = None
        branch.append_node_to_pipe(pipe.id, _node, "")
        return _node

    async def unlink_materialized_view_in_branch(self, branch: User, node_id: str) -> Optional[PipeNode]:
        node = branch.get_node(node_id)
        await NodeUtils.delete_node_materialized_view(branch, node, cancel_fn=None, force=False)
        return node

    async def process_mv(self, workspace: User, node_id: str) -> Optional[PipeNode]:
        snapshot = workspace.get_snapshot()
        if not snapshot:
            raise ValueError("Iterating hook error: snapshot not found")
        node_exists_in_snapshot = snapshot.get_node(node_id)
        if node_exists_in_snapshot:
            node = self.unlink_node_in_branch(workspace, node_exists_in_snapshot)
        else:
            node = await self.unlink_materialized_view_in_branch(workspace, node_id)
        return node


async def on_create_new_datasource(
    workspace: User, ds_name: str, branch_mode: BranchMode = BranchMode.NONE
) -> Optional[str]:
    if not branch_mode.is_default() and (not workspace.is_branch and not workspace.is_release):
        raise ValueError("Iterating hook error: Operation not supported in a live Release of a Workspace")

    if not workspace.is_branch and not workspace.is_release:
        return None

    ds = workspace.get_datasource(ds_name, include_read_only=True)
    if not ds:
        return None
    origin_ds = None
    if (
        (workspace.is_branch and isinstance(ds, BranchDatasource)) or workspace.is_release
    ) and branch_mode == BranchMode.FORK:
        # snapshot metadata of an branch is a copy of the main workspace metadata at the time when the Branch was created
        # we want to keep the snapshot metadata immutable in the Branch for regression testing and other stuff (like comparing resources)
        if workspace.is_branch:
            origin_ws = workspace.get_snapshot()
        else:
            origin_ws = User.get_by_id(workspace.origin) if workspace.origin else None
        if not origin_ws:
            return None
        origin_ds = origin_ws.get_datasource(ds_name, include_read_only=True)
        # drop it to create it with a new ID if it exists in the snapshot metadata
        # drop it and create it with the same ID if it exists only in the new metadata
        # after that, the CreateCascadeDatasourceHook hooks will do their stuff
        await Users.drop_datasource_async(workspace, ds.id)
        return ds.id if ds and (not origin_ds or ds.id != origin_ds.id) else None
    return None


def allow_reuse_datasource_name(workspace: User, branch_mode: BranchMode = BranchMode.NONE) -> bool:
    if not branch_mode.is_default() and (not workspace.is_branch and not workspace.is_release):
        raise ValueError("Iterating hook error: Operation not supported in a live Release of a Workspace")

    result = (workspace.is_branch or workspace.is_release) and branch_mode == BranchMode.FORK
    if result:
        return True
    else:
        return False


def allow_force_delete_materialized_views(workspace: User, branch_mode: BranchMode = BranchMode.NONE) -> bool:
    if not branch_mode.is_default() and (not workspace.is_branch and not workspace.is_release):
        raise ValueError("Iterating hook error: workspace is not a branch")

    return (workspace.is_branch or workspace.is_release) and branch_mode == BranchMode.FORK


def install_iterating_hooks(
    workspace: User, datasource: Datasource, branch_mode: BranchMode = BranchMode.NONE
) -> Optional[List[Hook]]:
    if not branch_mode.is_default() and (not workspace.is_branch and not workspace.is_release):
        raise ValueError("Iterating hook error: Operation not supported in a live Release of a Workspace")

    if not workspace.is_branch and not workspace.is_release:
        return None

    return [datasource.install_hook(CreateCascadeDatasourceHook(workspace))] if branch_mode == BranchMode.FORK else None


def should_drop_table_on_create_table(workspace: User, ds_name: str) -> bool:
    if not workspace.is_branch and not workspace.is_release:
        return False

    if workspace.is_branch:
        snapshot = workspace.get_snapshot()
        live = workspace
        if not snapshot:
            return False
    else:
        snapshot = workspace
        live = User.get_by_id(workspace.origin) if workspace.origin else None  # type: ignore

    main_ds = snapshot.get_datasource(ds_name)
    branch_ds = User.get_by_id(live.id).get_datasource(ds_name)
    if main_ds is None:
        return True

    if branch_ds is None:
        return False

    old_ds = live.get_datasource(ds_name)
    if old_ds is None or (old_ds and old_ds.id != branch_ds.id):
        return False

    return main_ds.id != branch_ds.id
