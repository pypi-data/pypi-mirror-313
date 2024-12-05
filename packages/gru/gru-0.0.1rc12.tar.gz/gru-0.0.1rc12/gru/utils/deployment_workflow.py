from enum import Enum
from gru.schema.deployment_strategy import AirflowDeploymentRequest

class Workflow(Enum):
    AIRFLOW = "airflow"

DeploymentRequestMapping = {
    Workflow.AIRFLOW: AirflowDeploymentRequest
}

def get_deployment_request_class(workflow : Workflow):
    if  workflow in DeploymentRequestMapping:
        return DeploymentRequestMapping.get(workflow)
    else:
        raise TypeError(f"workflow type {workflow} not supported yet")

