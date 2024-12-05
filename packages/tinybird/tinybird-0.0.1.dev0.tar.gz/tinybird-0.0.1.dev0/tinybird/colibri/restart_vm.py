from .aws_operations import find_instance_id_and_region as find_instance_id_and_region_aws
from .aws_operations import start_instance as start_instance_aws
from .aws_operations import stop_instance as stop_instance_aws
from .azure_operations import find_instance_in_subscription as find_instance_in_subscription_azure
from .azure_operations import start_instance as start_instance_azure
from .azure_operations import stop_instance as stop_instance_azure
from .gcp_operations import get_zone_from_name as get_zone_from_name_gcp
from .gcp_operations import start_instance as start_instance_gcp
from .gcp_operations import stop_instance as stop_instance_gcp
from .logging import log_info


def restart_instance(instance_name: str) -> None:
    if instance_name.startswith("aws-wadus"):
        restart_instance_aws(instance_name, "development")
    elif instance_name.startswith("gcp-wadus"):
        restart_instance_gcp(instance_name, "development-353413")
    elif instance_name.startswith("aws-"):
        restart_instance_aws(instance_name, "production")
    elif instance_name.startswith("azure-"):
        restart_instance_azure(instance_name, "6ef6dabf-c7ec-464c-8f1e-0640987ad1d5")
    else:
        # The default is prod GCP because there are still a lot of funny names here
        restart_instance_gcp(instance_name, "stddevco")


def restart_instance_aws(instance_name: str, aws_profile: str) -> None:
    log_info(f"Searching instance `{instance_name}` using AWS profile `{aws_profile}`...")
    instances = find_instance_id_and_region_aws(instance_name, aws_profile=aws_profile)

    if not instances:
        raise Exception(f"Instance '{instance_name}' not found")

    if len(instances) > 1:
        raise Exception(
            f"Found {len(instances)} instances with the name '{instance_name}' in the following regions {[i[1] for i in instances]}, expected only one instance in one region."
        )

    log_info(f"Found instance in region `{instances[0][0]}` with id `{instances[0][1]}`!")

    log_info("Stopping instance...")
    stop_instance_aws(instances[0][0], instances[0][1], aws_profile)
    log_info("Starting instance...")
    start_instance_aws(instances[0][0], instances[0][1], aws_profile)


def restart_instance_gcp(instance_name: str, project_id: str) -> None:
    log_info(f"Searching instance `{instance_name}` in GCP project `{project_id}`...")
    zone = get_zone_from_name_gcp(project_id, instance_name)

    if not zone:
        raise Exception(f"Instance '{instance_name}' not found")

    log_info(f"Found instance in zone `{zone}`!")

    log_info("Stopping instance...")
    stop_instance_gcp(project_id, zone, instance_name)
    log_info("Starting instance...")
    start_instance_gcp(project_id, zone, instance_name)


def restart_instance_azure(instance_name: str, subscription_id: str) -> None:
    log_info(f"Searching instance`{instance_name}` in Azure subscription `{subscription_id}`...")
    resource_group_names = find_instance_in_subscription_azure(subscription_id, instance_name)

    if not resource_group_names:
        raise Exception(f"Instance '{instance_name}' not found")

    if len(resource_group_names) > 1:
        raise Exception(
            f"Found {len(resource_group_names)} instances with the name '{instance_name}' in the resource groups {resource_group_names}, expected only one instance in one resource group."
        )

    log_info(f"Found instance in resource group `{resource_group_names[0]}`!")

    log_info("Stopping instance...")
    stop_instance_azure(subscription_id, resource_group_names[0], instance_name)
    log_info("Starting instance...")
    start_instance_azure(subscription_id, resource_group_names[0], instance_name)
