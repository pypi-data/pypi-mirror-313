import collections
import os
import sys
from typing import Callable, Optional, OrderedDict

from ansible.cli import init_plugin_loader
from ansible.errors import AnsibleError
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from click.termui import confirm, secho, style

from .logging import log_error, log_header, log_info, log_warning


class AnsibleGlobalConfig:
    """Class to hold different objects related to Ansible configuration"""

    def __init__(self, interactive: bool):
        log_info("Processing the ansible config")
        self.loader = DataLoader()
        init_plugin_loader()
        try:
            self.inventory = InventoryManager(
                loader=self.loader, sources=[f"{os.environ['ANSIBLE_CONFIG']}/inventories"]
            )
        except AnsibleError:
            log_error(
                "Could not parse the ansible inventory. Check that you have access to AWS (aws sso login --sso-session local), Azure, and GCP"
            )
            sys.exit(1)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.task_manager = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=dict(),
        )
        self.interactive = interactive
        # Manage cancel requests (Ctrl+C) in a controlled fashion
        self.quit = False
        self.shutting_down = False
        self.pending_cleanup_actions: OrderedDict[str, Callable[..., None]] = collections.OrderedDict()
        self.check_writers_inventory: Optional[InventoryManager] = None

    def cleanup_if_needed(self, force_cleanup: bool = False) -> None:
        if not self.shutting_down and (self.quit or force_cleanup):
            self.shutting_down = True
            if len(self.pending_cleanup_actions):
                log_header("Cleanup")
                log_warning(
                    f"There are several **CLEANUP** steps pending: **{list(self.pending_cleanup_actions.keys())}**"
                )
                if not self.interactive or not confirm(
                    style("Do you want to ignore these pending steps?", blink=False), default=False
                ):
                    pending_actions = self.pending_cleanup_actions.copy()
                    # Most of the time we need to execute the pending operations in the reverse order where they
                    # where inserted. For example, first start CH, then remove the alerts
                    for action in reversed(pending_actions):
                        log_warning(action)
                        pending_actions[action]()
            if self.quit:
                log_warning("Process cancelled")
                sys.exit(1)


_ansible_singleton = None


def get_ansible_config(interactive: bool = True) -> AnsibleGlobalConfig:
    global _ansible_singleton
    if not _ansible_singleton:
        _ansible_singleton = AnsibleGlobalConfig(interactive)
    _ansible_singleton.cleanup_if_needed()
    return _ansible_singleton


def reset_ansible_config() -> None:
    global _ansible_singleton
    _ansible_singleton = None


def log_fatal(msg: str) -> None:
    secho("")
    log_error(msg)
    get_ansible_config().cleanup_if_needed(force_cleanup=True)
    sys.exit(1)
