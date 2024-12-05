import time
from typing import List, Optional, Tuple

import boto3

from .logging import log_info


def resize_volume(vol_id: str, new_size: int, region: str, aws_profile: Optional[str] = None) -> None:
    session = boto3.Session(profile_name=aws_profile)

    ec2_client = session.client("ec2", region)
    ec2_client.modify_volume(VolumeId=vol_id, Size=new_size)

    time.sleep(3)
    while True:
        volume_modifications = ec2_client.describe_volumes_modifications(VolumeIds=[vol_id])["VolumesModifications"][0]
        wait_for_resize = volume_modifications["ModificationState"] not in ["optimizing", "completed"]

        if volume_modifications["ModificationState"] == "failed":
            raise Exception(f"Volume resize failed for volume {vol_id}")

        if wait_for_resize:
            log_info("Waiting for the volume to pass the optimizing state")
            time.sleep(5)
        else:
            break


def find_instance_id_and_region(instance_name: str, aws_profile: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Finds an instance by name in every region and returns a list of region and instance id tuples of
    all the found instances.
    """
    session = boto3.Session(profile_name=aws_profile)
    ec2 = session.client("ec2", "us-east-1")
    regions = [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

    instances = []

    for region in regions:
        ec2 = session.client("ec2", region_name=region)
        response = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": [instance_name]}])

        if "Reservations" in response and len(response["Reservations"]) > 0:
            instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]
            instances.append((region, instance_id))

    return instances


def start_instance(region: str, instance_id: str, aws_profile: Optional[str] = None) -> None:
    session = boto3.Session(profile_name=aws_profile)
    ec2 = session.client("ec2", region_name=region)

    ec2.start_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    # Disable stopping the instance via the API
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        DisableApiStop={"Value": True},
    )


def stop_instance(region: str, instance_id: str, aws_profile: Optional[str] = None) -> bool:
    session = boto3.Session(profile_name=aws_profile)
    ec2 = session.client("ec2", region_name=region)

    # Allow to stop the instance via the API
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        DisableApiStop={"Value": False},
    )

    ec2.stop_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter("instance_stopped")
    waiter.wait(InstanceIds=[instance_id])
    return True


def scale_instance(region: str, instance_id: str, instance_type: str, aws_profile: Optional[str] = None) -> None:
    session = boto3.Session(profile_name=aws_profile)
    ec2 = session.client("ec2", region_name=region)

    ec2.modify_instance_attribute(InstanceId=instance_id, Attribute="instanceType", Value=instance_type)
