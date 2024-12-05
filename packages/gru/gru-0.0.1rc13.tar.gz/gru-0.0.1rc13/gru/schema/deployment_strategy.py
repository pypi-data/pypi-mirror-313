from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional
from gru.utils.commons import dt_to_str
from gru.utils.commons import is_duration_valid_for_dry_run
from gru.utils.config_reader import ConfigReader
from gru.utils.entity_type import EntityType


class DeploymentRequest(ABC):
    """
    Abstract base class representing a deployment strategy.
    """

    def __init__(
        self,
        workflow_name: str,
        entity_type: EntityType,
        dry_run: bool = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        config=None,
    ):
        self.dry_run = dry_run
        self.start_date = start_date
        self.end_date = end_date
        self.config = config
        self.workflow_name = workflow_name
        self.entity_type = entity_type

    @abstractmethod
    def create_deployment_options(self) -> dict:
        """
        Creates a dictionary containing options specific to the deployment strategy.

        Returns:
            dict: The deployment options dictionary.
        """

        pass

    @abstractmethod
    def is_entity_deployable(self):
        pass


class AirflowDeploymentRequest(DeploymentRequest):
    """
    Deployment strategy using Airflow workflows.
    """

    deployable_entities = {EntityType.RAW_FEATURE, 
                           EntityType.DERIVED_FEATURE, 
                           EntityType.PRE_PROCESSING_TRANSFORM,
                           EntityType.STREAMING_FEATURE}

    def __init__(
        self,
        workflow_name: str,
        entity_type: EntityType,
        config: ConfigReader,
        dry_run: bool = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        """
        Args:
            workflow_name (str): Name of the Airflow workflow to trigger.
            **kwargs: Additional keyword arguments passed to the parent class constructor.
        """
        super().__init__(
            workflow_name=workflow_name,
            entity_type=entity_type,
            config=config,
            dry_run=dry_run,
            start_date=start_date,
            end_date=end_date,
        )

    def create_deployment_options(self) -> dict:
        """
        Returns options specific to Airflow deployment.

        Returns:
            dict: A dictionary containing the Airflow workflow name and optional start/end dates.
        """

        url_path = self.config.deploy_paths[self.entity_type.value]
        json_req = {
            "name": self.workflow_name,
            "type": self.entity_type.value,
            "airflow_dags_backup_path": (
                self.config.airflow_dags_backup_path
                if self.config.airflow_dags_backup_path
                else None
            ),
        }

        if self.dry_run:
            self._validate_dry_run()
            json_req.update({
                "is_dry_run": True,
                "start_date": str(dt_to_str(self.start_date)),
                "end_date": str(dt_to_str(self.end_date))
            })

        return {"url_path": url_path, "json": json_req}
    
    def _validate_dry_run(self):
        max_days = self.config.dry_run["max_dry_run_duration_days"]
        if not is_duration_valid_for_dry_run(self.start_date, self.end_date, max_days):
            raise ValueError(
                f"""max_dry_run_duration_days is set to {max_days}. Adjust your start and end date accordingly."""
            )
        if self.end_date is None:
            self.end_date = self.start_date + timedelta(
                days=self.config.dry_run["default_dry_run_duration"]
            )
    
    def is_entity_deployable(self):
        if self.entity_type not in self.deployable_entities:
            return False
        
        return True
