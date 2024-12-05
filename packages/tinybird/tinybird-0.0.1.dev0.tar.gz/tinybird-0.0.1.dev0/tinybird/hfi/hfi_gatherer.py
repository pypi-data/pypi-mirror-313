import logging
import random
from typing import Optional

from tinybird import context
from tinybird.ch import url_from_host
from tinybird.gatherer_common import (
    GATHERER_HFI_SOURCE_TAG,
    SAFE_TAG,
    UNSAFE_TAG,
    get_gatherer_config_from_workspace,
    render_gatherer_table_name,
)
from tinybird.gatherer_common.gatherer_config import get_gatherer_config
from tinybird.hfi.hfi_defaults import HfiDefaults
from tinybird.hfi.hfi_settings import hfi_settings
from tinybird.hfi.utils import HFI_LOGGER_USER_AGENT
from tinybird.limits import Limit
from tinybird.user import User as Workspace

HFI_USER_AGENT = "tb-hfi"


class HfiGatherer:
    def __init__(
        self,
        endpoint,
        database,
        table_id,
        columns_list,
        columns_types_list,
        user_agent,
    ):
        self.url = url_from_host(endpoint)
        self.gatherer_config = None
        self.gatherer_ch_config = None
        self.gatherer_table_name = None

        wait_parameter: bool = context.wait_parameter.get(False)
        workspace: Optional[Workspace] = context.workspace.get(None)

        if workspace is None:
            if user_agent == HFI_USER_AGENT:
                logging.error("Failed to retrieve the workspace from the context in HFI")
            self.in_use = False
            self.allow_gatherer_fallback: Optional[bool] = False
            self.gatherer_allow_s3_backup_on_user_errors: Optional[bool] = True
        else:
            self.allow_gatherer_fallback = workspace.allow_gatherer_fallback
            self.gatherer_allow_s3_backup_on_user_errors = workspace.gatherer_allow_s3_backup_on_user_errors
            self.in_use = self._should_use_gatherer(workspace, user_agent, wait_parameter)

        if self.in_use and workspace is not None:
            self.gatherer_available = True
            safety_tag = SAFE_TAG if wait_parameter else UNSAFE_TAG
            self.gatherer_ch_config = get_gatherer_config_from_workspace(workspace, table_id)

            additional_content_for_hash = ""
            if workspace.gatherer_allow_s3_backup_on_user_errors is True:
                additional_content_for_hash += "allow_backup_on_user_errors"
            else:
                additional_content_for_hash += "disallow_backup_on_user_errors"

            self.workspace_multiwriter_enabled = Limit.gatherer_multiwriter_enabled
            self.workspace_multiwriter_type = Limit.gatherer_multiwriter_type
            self.workspace_multiwriter_tables = Limit.gatherer_multiwriter_tables
            self.workspace_multiwriter_tables_excluded = Limit.gatherer_multiwriter_tables_excluded
            self.workspace_multiwriter_hint_backend_ws = Limit.gatherer_multiwriter_hint_backend_ws
            self.workspace_multiwriter_hint_backend_tables = Limit.gatherer_multiwriter_hint_backend_tables

            workspace_multiwriter_config = workspace.get_limits(prefix="gatherer_multiwriter")
            if workspace_multiwriter_config:
                self.workspace_multiwriter_enabled = workspace_multiwriter_config.get(
                    "multiwriter_enabled", Limit.gatherer_multiwriter_enabled
                )
                self.workspace_multiwriter_type = workspace_multiwriter_config.get(
                    "multiwriter_type", Limit.gatherer_multiwriter_type
                )
                self.workspace_multiwriter_tables = workspace_multiwriter_config.get(
                    "multiwriter_tables", Limit.gatherer_multiwriter_tables
                )
                self.workspace_multiwriter_tables_excluded = workspace_multiwriter_config.get(
                    "multiwriter_tables_excluded", Limit.gatherer_multiwriter_tables_excluded
                )
                self.workspace_multiwriter_hint_backend_ws = workspace_multiwriter_config.get(
                    "multiwriter_hint_backend_ws", Limit.gatherer_multiwriter_hint_backend_ws
                )
                self.workspace_multiwriter_hint_backend_tables = workspace_multiwriter_config.get(
                    "multiwriter_hint_backend_tables", Limit.gatherer_multiwriter_hint_backend_tables
                )

            additional_content_for_hash += str(self.workspace_multiwriter_enabled)
            additional_content_for_hash += self.workspace_multiwriter_type
            additional_content_for_hash += self.workspace_multiwriter_tables
            additional_content_for_hash += self.workspace_multiwriter_tables_excluded
            additional_content_for_hash += self.workspace_multiwriter_hint_backend_ws
            additional_content_for_hash += self.workspace_multiwriter_hint_backend_tables

            self.gatherer_table_name = render_gatherer_table_name(
                url=self.url,
                database=database,
                table=table_id,
                columns=columns_list,
                columns_types=columns_types_list,
                source=GATHERER_HFI_SOURCE_TAG,
                safety=safety_tag,
                gatherer_config=self.gatherer_ch_config,
                additional_content_for_hash=additional_content_for_hash,
            )
            self.gatherer_config = get_gatherer_config(self.gatherer_table_name, hfi_settings.get("tb_region"))

            if self.gatherer_config is None:
                self.gatherer_available = False

    @staticmethod
    def _should_use_gatherer(workspace: Workspace, user_agent: str, wait_parameter: bool) -> bool:
        if workspace.use_gatherer is False or user_agent == HFI_LOGGER_USER_AGENT:
            return False

        # Filter traffic through the gatherer according to the % set in workspace
        if wait_parameter:
            limit = (
                workspace.gatherer_wait_true_traffic
                if workspace.gatherer_wait_true_traffic is not None
                else HfiDefaults.WAIT_TRUE_TRAFFIC_THROUGH_GATHERER
            )
        else:
            limit = (
                workspace.gatherer_wait_false_traffic
                if workspace.gatherer_wait_false_traffic is not None
                else HfiDefaults.WAIT_FALSE_TRAFFIC_THROUGH_GATHERER
            )

        return random.uniform(0, 1) <= limit
