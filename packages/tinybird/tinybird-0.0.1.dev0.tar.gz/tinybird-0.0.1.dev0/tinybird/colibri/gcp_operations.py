import os
import sys
from datetime import datetime
from typing import Any, Optional

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1

from .disks import ServerDisk
from .logging import log_error, log_info, log_warning


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", verbose: bool = True, timeout: int = 1800
) -> Any:
    """
    Waits for the extended (long-running) operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        verbose: run on verbose mode.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    if verbose:
        log_info(f"Waiting for {verbose_name} ... ")

    result = operation.result(timeout=timeout)  # type: ignore[no-untyped-call]

    if operation.error_code:
        log_error(f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}")
        log_error(f"Operation ID: {operation.name}")
        raise operation.exception() or RuntimeError(operation.error_message)  # type: ignore[no-untyped-call]

    if operation.warnings:
        log_warning(f"Warnings during {verbose_name}:")
        for warning in operation.warnings:
            log_warning(f" - {warning.code}: {warning.message}")

    if verbose:
        delta = datetime.fromisoformat(operation.end_time) - datetime.fromisoformat(operation.start_time)
        log_info(f"OK (Completed in {delta.total_seconds()} seconds)")

    return result


def region_from_zone(project_id: str, zone: str) -> str:
    zc = compute_v1.ZonesClient()
    zone = zc.get(project=project_id, zone=zone)
    return os.path.basename(zone.region)


def create_snapshot(
    project_id: str, zone: str, disk_name: str, snapshot_name: Optional[str] = None
) -> compute_v1.Snapshot:
    """
    Create a zonal snapshot of a disk.

    Args:
        project_id: project ID or project number of the Cloud project you want
            to use to store the snapshot.
        disk_name: name of the disk you want to snapshot.
        zone: zone of the disk
        snapshot_name: name of the snapshot to be created.

    Returns:
        The new snapshot instance.
    """

    disk_client = compute_v1.DisksClient()
    disk = disk_client.get(project=project_id, zone=zone, disk=disk_name)
    snapshot = compute_v1.Snapshot()
    snapshot.source_disk = disk.self_link
    region = region_from_zone(project_id, zone)
    snapshot.storage_locations = [region]
    if snapshot_name:
        snapshot.name = snapshot_name
    else:
        snapshot.name = disk.name + "-autosnapshot"
    snapshot.description = "Automatic snapshot to disk creation"
    snapshot.labels = {"auto": "true"}

    snapshot_client = compute_v1.SnapshotsClient()
    operation = snapshot_client.insert(project=project_id, snapshot_resource=snapshot)

    wait_for_extended_operation(operation, f"creating snapshot {snapshot.name}")

    return snapshot_client.get(project=project_id, snapshot=snapshot.name)


def delete_snapshot(project_id: str, snapshot_name: str) -> None:
    """
    Delete the specified zonal snapshot

    Args:
        project_id: project ID or project number of the Cloud project containing the snapshot
        snapshot_name: name of the snapshot to be created.
    """

    snapshot_client = compute_v1.SnapshotsClient()
    operation = snapshot_client.delete(project=project_id, snapshot=snapshot_name)
    wait_for_extended_operation(operation, f"deleting snapshot {snapshot_name}")


def create_disk_from_snapshot(
    project_id: str,
    zone: str,
    disk_name: str,
    disk_type: str,
    disk_size_gb: int,
    snapshot_link: str,
) -> compute_v1.Disk:
    """
    Creates a new disk in a project in given zone.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which you want to create the disk.
        disk_name: name of the disk you want to create.
        disk_type: the type of disk you want to create. This value uses the following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        snapshot_link: a link to the snapshot you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        An unattached Disk instance.
    """
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.zone = zone
    disk.size_gb = disk_size_gb
    disk.source_snapshot = snapshot_link
    disk.type_ = f"zones/{zone}/diskTypes/{disk_type}"
    disk.name = disk_name
    operation = disk_client.insert(project=project_id, zone=zone, disk_resource=disk)
    wait_for_extended_operation(operation, f"creation of disk {disk.name}")

    return disk_client.get(project=project_id, zone=zone, disk=disk_name)


def get_zone_from_name(project: str, instance_name: str) -> str:
    ic = compute_v1.InstancesClient()
    request = compute_v1.types.AggregatedListInstancesRequest(project=project, filter=f"name = {instance_name}")
    for zone_key, value in ic.aggregated_list(request):
        if value.warning.code != "NO_RESULTS_ON_PAGE":  # type: ignore[attr-defined]
            return os.path.basename(zone_key)
    raise Exception(f"Instance '{instance_name}' not found")


def migrate_server_disk(instance_name: str, disk_type: str) -> None:
    project = "stddevco"
    zone = get_zone_from_name(project, instance_name)

    ic = compute_v1.InstancesClient()
    zone = get_zone_from_name(project, instance_name)
    if zone is None:
        sys.exit("Impossible to find the zone of the instance, check the server name")

    wait_for_extended_operation(
        ic.stop(project=project, zone=zone, instance=instance_name), f"stopping machine {instance_name}"
    )

    instance = ic.get(project=project, zone=zone, instance=instance_name)
    current_attach = instance.disks[0]
    old_disk_name = os.path.basename(current_attach.source)

    snapshot = create_snapshot(project, zone, old_disk_name)
    new_disk = create_disk_from_snapshot(
        project,
        zone,
        instance_name + f"-disk-{disk_type}",
        f"pd-{disk_type}",
        snapshot.disk_size_gb,
        snapshot.self_link,
    )
    delete_snapshot(project, snapshot.name)

    op = ic.detach_disk(project=project, zone=zone, instance=instance_name, device_name=current_attach.device_name)
    wait_for_extended_operation(op, f"detaching disk {old_disk_name}")
    new_attach = current_attach
    new_attach.source = new_disk.self_link
    op = ic.attach_disk(project=project, zone=zone, instance=instance_name, attached_disk_resource=new_attach)
    wait_for_extended_operation(op, f"attaching disk {new_disk.name}")

    wait_for_extended_operation(
        ic.start(project=project, zone=zone, instance=instance_name), f"starting machine {instance_name}"
    )


def get_server_disk(disk: ServerDisk) -> compute_v1.types.Disk:
    dc = compute_v1.DisksClient()

    instance = compute_v1.InstancesClient().get(
        project=disk.cloud_project_id, zone=disk.cloud_disk_zone, instance=disk.server
    )

    # This assumes each disk has only one data partition, as it is how we are working
    device_name = disk.cloud_id.replace("scsi-0Google_PersistentDisk_", "").replace("-part1", "")
    disk_id = next(d for d in instance.disks if d.device_name == device_name).source
    disk_name = disk_id.split("/")[-1]

    request_disk = compute_v1.GetDiskRequest(
        disk=disk_name,
        project=disk.cloud_project_id,
        zone=disk.cloud_disk_zone,
    )

    response = dc.get(request=request_disk)

    return response


def resize_server_disk(disk: ServerDisk, new_size: int) -> None:
    dc = compute_v1.DisksClient()

    request_resize = compute_v1.ResizeDiskRequest(
        disk=disk.cloud_disk_name,
        project=disk.cloud_project_id,
        zone=disk.cloud_disk_zone,
        disks_resize_request_resource=compute_v1.types.DisksResizeRequest(size_gb=new_size),
    )

    operation = dc.resize(request=request_resize)
    wait_for_extended_operation(operation, f"Rezising disk {disk.cloud_disk_name}")


def stop_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Stops a running Google Compute Engine instance.
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to stop.
    """
    instance_client = compute_v1.InstancesClient()

    # Initialize request argument(s)
    request = compute_v1.StopInstanceRequest(
        project=project_id, zone=zone, instance=instance_name, discard_local_ssd=False
    )

    operation = instance_client.stop(request=request)
    wait_for_extended_operation(operation, "instance stopping")


def start_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Starts a stopped Google Compute Engine instance (with unencrypted disks).
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to start.
    """
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(project=project_id, zone=zone, instance=instance_name)
    wait_for_extended_operation(operation, "instance start")


def scale_instance(project_id: str, zone: str, instance_name: str, instance_type: str) -> None:
    """
    Scale the instance to the instance_type
    """
    instance_client = compute_v1.InstancesClient()

    instance = instance_client.get(project=project_id, zone=zone, instance=instance_name)

    instance.machine_type = (
        f"https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/machineTypes/{instance_type}"
    )

    operation = instance_client.update(
        project=project_id, zone=zone, instance=instance_name, instance_resource=instance
    )

    wait_for_extended_operation(operation, "scaling instance")
