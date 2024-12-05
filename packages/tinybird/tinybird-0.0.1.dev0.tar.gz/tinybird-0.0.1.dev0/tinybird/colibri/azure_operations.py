import os
from typing import List, Optional, Tuple

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from click import secho

from .logging import log_info

# Types
SanTuple = List[int]


DEFAULT_GROUP_NAME = "azure-us-east"


def get_resource_group(resource_group: str | None) -> str:
    if not resource_group:
        resource_group = os.environ.get("RESORCE_GROUP", "")

        if not resource_group:
            resource_group = DEFAULT_GROUP_NAME

    return resource_group


def get_subscription_id(subscription_id: str | None) -> str:
    if not subscription_id:
        subscription_id = os.environ.get("SUBSCRIPTION_ID", "")

        if not subscription_id:
            raise Exception("Missing environment variable SUBSCRIPTION_ID")

    return subscription_id


def get_resource_client(subscription_id: str) -> ResourceManagementClient:
    """
    Initialize the Azure resource management client lazily in order not to break colibri if one doesn't
    have the Azure credentials.
    """

    return ResourceManagementClient(credential=DefaultAzureCredential(), subscription_id=subscription_id)


def get_compute_client(subscription_id: str) -> ComputeManagementClient:
    """
    Initialize the Azure compute management client lazily in order not to break colibri if one doesn't
    have the Azure credentials.
    """

    return ComputeManagementClient(credential=DefaultAzureCredential(), subscription_id=subscription_id)


def parse_lsscsi_output(output: str) -> List[Tuple[SanTuple, str, float]]:
    """
    Parse the output of lsscsi -b --size, which is of the form
    [H:C:T:L] <dev> <size>
    """
    ret = []
    for line in output.splitlines():
        san_tuple_str, dev, size_str = line.split()

        san_tuple = [int(n) for n in san_tuple_str.strip("[]").split(":")]
        size = float(size_str.strip("GB"))

        ret.append((san_tuple, dev, (size)))

    return ret


def find_instance_in_subscription(subscription_id: str, instance_name: str) -> List[str]:
    """
    Finds an instance by name in all resource groups of a subscription and returns a list of resource groups
    where there are instances with that name.
    """
    resource_client = get_resource_client(subscription_id)

    resource_groups = []

    for rg in resource_client.resource_groups.list():
        for _res in resource_client.resources.list_by_resource_group(
            rg.name, f"name eq '{instance_name}' and resourceType eq 'Microsoft.Compute/virtualMachines'"
        ):
            resource_groups.append(rg.name)
            break

    return resource_groups


def start_instance(subscription_id: str, resource_group_name: str, instance_name: str) -> None:
    compute_client = get_compute_client(subscription_id)
    operation = compute_client.virtual_machines.begin_start(resource_group_name, instance_name)
    operation.wait()


def stop_instance(subscription_id: str, resource_group_name: str, instance_name: str) -> None:
    compute_client = get_compute_client(subscription_id)
    operation = compute_client.virtual_machines.begin_deallocate(resource_group_name, instance_name)
    operation.wait()


def resize_server_disk(
    instance: str,
    disk_name: str,
    new_size: int,
    subscription_id: Optional[str] = None,
    resource_group: Optional[str] = None,
) -> int:
    """
    Resize data disk of `instance`. The instance should be stopped, disk rezised and the instance started back.

    Params:
    - instance: virtual machine name
    - disk_lun: logical unit name (LUN) of the disk
    - new_size: requested size in GB
    - subscription_id: Azure subscription ID, default: value from environment variable SUBSCRIPTION_ID
    - resource_group: resource group name, default: azure-us-east
    """

    resource_group = get_resource_group(resource_group)

    subscription_id = get_subscription_id(subscription_id)

    compute_client = get_compute_client(subscription_id)

    log_info(f"Deallocating VM `{instance}`...")
    stop_instance(subscription_id, resource_group, instance)
    secho("Done.\n", bold=True)

    log_info(f"Resizing disk `{disk_name}`...")
    disk_object = compute_client.disks.get(resource_group, disk_name)
    disk_object.disk_size_gb = new_size
    async_update = compute_client.disks.begin_create_or_update(resource_group, disk_name, disk_object)
    async_update.wait()
    secho("Done.\n", bold=True)

    log_info(f"Starting VM {instance}...")
    start_instance(subscription_id, resource_group, instance)
    secho("Done.\n", bold=True)

    # find data disk lun for resizing
    vm = compute_client.virtual_machines.get(resource_group, instance)
    for disk in vm.storage_profile.data_disks:
        if disk.name == disk_name:
            return int(disk.lun)

    # if no data disk found - return 100 - the highest lun is 63
    return 100


def check_disk_name(vm_name: str, disk_name: str) -> bool:
    return vm_name in disk_name


def list_server_data_disks(
    instance: str,
    subscription_id: Optional[str] = None,
    resource_group: Optional[str] = None,
) -> List[Tuple[str, int]]:  # name, size
    """
    List all data disks attached to the provided server.

    Params:
    - instance: virtual machine name
    - subscription_id: Azure subscription ID, default: value from environment variable SUBSCRIPTION_ID
    - resource_group: resource group name, default: azure-us-east
    """

    resource_group = get_resource_group(resource_group)

    subscription_id = get_subscription_id(subscription_id)

    compute_client = get_compute_client(subscription_id)

    all_disks = compute_client.disks.list_by_resource_group(resource_group)
    vmDisks = filter(lambda d: check_disk_name(instance, d.name), all_disks)

    res = []
    for d in vmDisks:
        res.append((d.name, d.disk_size_gb))

    return res
