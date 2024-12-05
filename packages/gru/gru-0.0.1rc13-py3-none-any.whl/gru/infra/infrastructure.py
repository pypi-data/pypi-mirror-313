"""
Register Infrastructure for different Data & ML Use Cases.
"""
import json
from typing import Mapping
from datetime import datetime
from gru.utils.entity_type import EntityType
from typing import Dict


class Infrastructure:
    """
    Infrastructure baiscally contains all the details regarding the infra set up for the entire pipeline.

    Parameters
    ----------
    self: str
        Python self object
    client_id: str
        Id of the client data object
    cloud_provider:str
       Name of the cloud provider
    cluster_name: str
        Name of the cluster
    region: str
        Name of the region in which cluster is to deployed.
    subnet_ids: list
        List of subnet ids
    resource_node_group_instance_types: Mapping[str, Mapping[str, str]]
        It is is dictionary containing details about the different sizes of nodegroups.
    resource_node_group_scaling_config: Mapping[str, Mapping[str, Mapping[str, int]]]
        Corresponding to every node group it will have details about max_size, min_size ,desired_size of the node group

    admins: list
        List of all admins
    airflow_users: Mapping[str, Mapping[str, str]]
        dictionary having details about airflow users
    slack_details: Mapping[str, Mapping[str, str]]
      It will contain  host_url and host_password of slack for failure alerts and any notifications
    created_at=datetime.now()
       Time when it is created


    Returns
    -------
    None

    Notes
    -----
    Time to register the Infrastructure data  in Stuart and then will be written to DB. 

    Examples
    --------
    """

    def __init__(
        self,
        client_id: str,
        cloud_provider: str,
        cluster_name: str,
        region: str,
        subnet_ids: list,
        resource_node_group_instance_types: Mapping[str, Mapping[str, str]],
        resource_node_group_scaling_config: Mapping[
            str, Mapping[str, Mapping[str, int]]
        ],
        admins: list,
        airflow_users: Mapping[str, Mapping[str, str]],
        slack_details: Mapping[str, Mapping[str, str]],
        created_at=datetime.now(),
    ):
        self.type = EntityType.INFRASTRUCTURE.value
        self.entity_type = self.type
        self.client_id = client_id
        self.cloud_provider = cloud_provider
        self.cluster_name = cluster_name
        self.region = region
        self.subnet_ids = subnet_ids
        self.resource_node_group_instance_types = resource_node_group_instance_types
        self.resource_node_group_scaling_config = resource_node_group_scaling_config
        self.admins = admins
        self.airflow_users = airflow_users
        self.slack_details = slack_details
        self.created_at = created_at

    def to_json(self) -> Dict:
        return {
            "type": self.type,
            "client_id": self.client_id,
            "cloud_provider": self.cloud_provider,
            "cluster_name": self.cluster_name,
            "region": self.region,
            "subnet_ids": self.subnet_ids,
            "resource_node_group_instance_types": json.dumps(
                self.resource_node_group_instance_types
            ),
            "resource_node_group_scaling_config": json.dumps(
                self.resource_node_group_scaling_config
            ),
            "admins": self.admins,
            "airflow_users": json.dumps(self.airflow_users),
            "slack_details": json.dumps(self.slack_details),
            "created_at": str(self.created_at),
        }
