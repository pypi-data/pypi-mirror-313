"""
Deploy Infrastructure Components for different Data & ML Use Cases
This includes 
- A Managed Kubernetes Custer (EKS in AWS)
- Airflow
- Grafana
- Prometheus
- Loki
- Managed Postgres Database (RDS in AWS)
"""
import requests
from gru.utils.utils import Constants


class DeployInfrastructure:
    def __init__(
        self, deployment_id: str, access_token: str,
    ):
        self.deployment_id = deployment_id
        self.access_token = access_token

        self.deploy_infra_details = {
            "deployment_id": self.deployment_id,
            "access_token": self.access_token,
        }

    def deploy_infra(self):
        """deploy/spin-up infra."""
        result = requests.get(
            url=Constants.API_DEPLOY_INFRA_PROD,
            json=self.deploy_infra_details,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        print(result.json())
