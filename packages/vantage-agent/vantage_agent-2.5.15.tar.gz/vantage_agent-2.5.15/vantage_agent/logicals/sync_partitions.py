"""Core module for defining partitions related operations."""

import json
import subprocess
from shutil import copyfile
from textwrap import dedent

from vantage_agent.logger import logger
from vantage_agent.settings import SETTINGS
from vantage_agent.vantage_api_client import AsyncBackendClient


def create_backup(file_path: str):
    """Create a backup of slurm.conf."""
    bkp_name = str(file_path).split("/").pop()
    backup_path = f"{SETTINGS.CACHE_DIR}/{bkp_name}.bkp"
    copyfile(file_path, backup_path)
    logger.info(f"Backup of {bkp_name} created at {backup_path}")


async def update_slurm_config(partitions):
    """Update the slurm.conf file with the given partitions."""
    # Backup slurm.conf file
    create_backup(SETTINGS.SLURM_CONF_PATH)
    logger.debug(f"Current SLURM path: {SETTINGS.SLURM_CONF_PATH}")

    with open(SETTINGS.SLURM_CONF_PATH, "r") as f:
        slurm_config = f.readlines()

    logger.debug(f"Current SLURM config: {slurm_config}")
    new_partition_configs = []
    node_names_seen = set()

    for partition in partitions:
        logger.debug(f"Processing partition: {partition}. Type: {type(partition)}")
        instance_info = await get_node_type_info(partition["nodeType"])

        # Build the new config for each partition
        is_default = "Yes" if partition.get("isDefault", None) else "No"
        node_range = f"[0-{partition['maxNodeCount'] - 1}]"
        node_name = f"NodeName={partition['name']}-{partition['name']}-{node_range} State=CLOUD Weight=1 Feature=cloud CPUs={instance_info['numCpus']}\n"  # noqa
        partition_name = f"PartitionName={partition['name']} Nodes={partition['name']}-{partition['name']}-{node_range} MaxNodes={partition['maxNodeCount']} MaxTime=INFINITE State=UP Default={is_default}\n"  # noqa

        new_partition_configs.append(node_name)
        new_partition_configs.append(partition_name)

        # Toggle node as done
        node_names_seen.add(partition["name"])

    # Filter the lines that aren't Partition or Node configs
    filtered_config = []
    for line in slurm_config:
        if line.startswith("NodeName=") or line.startswith("PartitionName="):
            continue
        filtered_config.append(line)

    logger.debug(f"Filtered lines from SLURM {filtered_config}")

    # Add the new partitions to the end of slurm.conf file and write a new file
    filtered_config += new_partition_configs
    with open(SETTINGS.SLURM_CONF_PATH, "w") as f:
        f.writelines(filtered_config)
    # Copy file to the nfs directory
    copyfile(SETTINGS.SLURM_CONF_PATH, "/nfs/slurm/etc/slurm/slurm.conf")

    node_names = ", ".join(node_names_seen)
    logger.info(f"SLURM conf file updated with the partitions {node_names}.")


async def update_partition_config(partitions):
    """Update the partitions.json file with the given partitions."""
    create_backup(SETTINGS.PARTITIONS_JSON_PATH)
    logger.debug(f"Current partitions.json path: {SETTINGS.PARTITIONS_JSON_PATH}")

    with open(SETTINGS.PARTITIONS_JSON_PATH, "r", encoding="utf-8") as f:
        partitions_config = json.load(f)

    new_partitions = []
    for partition in partitions:
        is_default = "Yes" if partition.get("isDefault", None) else "No"
        instance_info = await get_node_type_info(partition["nodeType"])
        new_partition = {
            "PartitionName": partition["name"],
            "NodeGroups": [
                {
                    "NodeGroupName": partition["name"],
                    "MaxNodes": partition["maxNodeCount"],
                    "Region": partitions_config["Partitions"][0]["NodeGroups"][0]["Region"],
                    "SlurmSpecifications": {
                        "Weight": 1,
                        "Feature": "cloud",
                        "CPUs": instance_info["numCpus"],
                    },
                    "PurchasingOption": "on-demand",
                    "OnDemandOptions": {"AllocationStrategy": "lowest-price"},
                    "LaunchTemplateSpecification": {
                        "LaunchTemplateId": partitions_config["Partitions"][0]["NodeGroups"][0][
                            "LaunchTemplateSpecification"
                        ]["LaunchTemplateId"],  # noqa
                        "Version": "$Latest",
                    },
                    "LaunchTemplateOverrides": [{"InstanceType": partition["nodeType"]}],
                    "SubnetIds": partitions_config["Partitions"][0]["NodeGroups"][0]["SubnetIds"],
                }
            ],
            "PartitionOptions": {"Default": is_default},
        }
        new_partitions.append(new_partition)

    with open(SETTINGS.PARTITIONS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"Partitions": new_partitions}, f, indent=4, ensure_ascii=False)


async def get_node_type_info(instance_type: str):
    """Get the node type specifications from the api."""
    query = dedent(
        """
        query($filters: JSONScalar!, $first: Int, $after: Int) {
            awsNodePicker(filters: $filters, after: $after, first: $first) {
                edges {
                    node {
                        awsRegion
                        cpuName
                        cpuManufacturer
                        cpuArch
                        gpuName
                        gpuManufacturer
                        id
                        instanceType
                        memory
                        numCpus
                        numGpus
                        pricePerHour
                    }
                }
            }
        }
        """
    )

    body = {
        "query": query,
        "variables": {"filters": {"instanceType": {"eq": instance_type}}, "after": 1, "first": 100},
    }

    async with AsyncBackendClient() as backend_client:
        res = await backend_client.post("/cluster/graphql", json=body)
        res = res.json()
    instance_info = res["data"]["awsNodePicker"]["edges"][0]["node"]
    return instance_info


async def get_cluster_partitions():
    """Get the partitions from the api."""
    query = dedent(
        """
        query($filters: JSONScalar!, $first: Int, $after: Int) {
            partitions(filters: $filters, after: $after, first: $first) {
                edges {
                    node {
                        clusterName
                        id
                        isDefault
                        maxNodeCount
                        name
                        nodeType
                    }
                }
            }
        }
        """
    )

    body = {
        "query": query,
        "variables": {"filters": {"clusterName": {"eq": SETTINGS.CLUSTER_NAME}}, "after": 1, "first": 100},
    }

    async with AsyncBackendClient() as backend_client:
        res = await backend_client.post("/cluster/graphql", json=body)
        res = res.json()
    partitions = res["data"]["partitions"]["edges"]
    return [partition["node"] for partition in partitions]


def reconfigure_slurm():
    """Reload the slurm.conf to get the new changes in the slurm.conf."""
    try:
        logger.debug("Reloading SLURM config.")
        result = subprocess.run(
            ["systemctl", "restart", "slurmctld"], check=True, capture_output=True, text=True
        )
        logger.info(f"SLURM config reloaded:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while reloading SLURM conf:\n{e.stderr}")
        raise e


async def sync_cluster_partitions():
    """Sync the slurm partitions with the current partitions in the API."""
    try:
        logger.info("Syncing SLURM partitions.")

        partitions = await get_cluster_partitions()

        logger.debug(f"Updating SLURM config file with partition: {partitions}.")
        await update_slurm_config(partitions=partitions)

        logger.debug(f"Updating partitions.json config file with partition: {partitions}.")
        await update_partition_config(partitions=partitions)

        logger.debug("Reloading SLURM config.")
        reconfigure_slurm()

        logger.info("SLURM partitions synced.")
    except Exception as e:
        logger.error(f"Error while syncing the partitions: {str(e)}")
