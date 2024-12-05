"""
Abstract base class representing a batch feature definition.
"""
from abc import abstractmethod
import json
from typing import Any, List, Dict, Union, Optional
from datetime import datetime
from gru.schema.registrable import Registrable
from gru.utils.data_types import DataType
from gru.features.feature_logic import FeatureLogic
from gru.features.custom_feature_logic import CustomFeatureLogic
from gru.features.processing_engine_configs import BatchProcessingEngineConfigs
from gru.utils.processing_engine import ProcessingEngine

class MLFeature(Registrable):
    """
    This abstract class defines the common attributes and methods for batch features
    that are used in data processing pipelines.

    Attributes:
        name (str): The name of the batch feature.
        type (str): The type of the feature.
        data_type (DataTypes): The data type of the feature.
        online (bool): Flag indicating if the feature is available online.
        offline (bool): Flag indicating if the feature is available offline.
        entity (List[str]): List of entities associated with the feature.
        source_name (Union[str, List[str]): The source or sources of the feature.
        sink_name (str): The destination or sink for the feature.
        feature_logic (FeatureLogic): The logic or transformation applied to the feature.
        description (str): Description or additional information about the feature.
        owners (Union[str, List[str]): List of owners responsible for the feature.
        feature_start_time (datetime): The timestamp when the feature starts being available.
        schedule (str): The scheduling interval for batch feature generation.
        active (bool): Flag indicating if the feature is active.
        k8s_configs (Dict): Kubernetes configurations for feature processing.
        creation_time (datetime): The timestamp of feature creation.

    Abstract Methods:
        to_json(self) -> dict:
        Returns a JSON representation of the batch feature.

    """

    def __init__(
        self,
        name: str,
        type: str,
        data_type: DataType,
        processing_engine: Optional[ProcessingEngine],
        processing_engine_configs: Optional[BatchProcessingEngineConfigs],
        online: bool,
        offline: bool,
        read_option_configs: Optional[List[Dict[str, Any]]],
        staging_sink_write_option_configs: Optional[Dict[str, Any]],
        online_sink_write_option_configs: Optional[Dict[str, Any]],
        entity: List[str],
        data_sources: Union[str, List[str]],
        sink: Dict,
        feature_logic: Union[FeatureLogic, CustomFeatureLogic] = None,
        description: str = "",
        owners: Union[str, List[str]] = [],
        start_time: datetime = None,
        schedule: str = "30 0 * * *",
        active: bool = False,
        k8s_configs: Dict = {},
        airflow_configs: Dict = {},
        creation_time: datetime = datetime.now(),
        tags: Dict[str, Any] = {}
    ):
        self.name = name
        self.data_type = data_type
        self.data_sources = data_sources
        self.entity = entity
        self.type = type
        self.entity_type = type
        self.owners = owners
        self.description = description
        self.start_time = start_time
        self.online = online
        self.offline = offline
        self.schedule = schedule
        self.feature_logic = feature_logic
        self.sink = sink
        self.active = active
        self.k8s_configs = k8s_configs
        self.creation_time = creation_time
        self.processing_engine = processing_engine
        self.processing_engine_configs = processing_engine_configs
        self.airflow_configs = airflow_configs
        self.tags = tags
        self.read_option_configs=read_option_configs
        self.staging_sink_write_option_configs=staging_sink_write_option_configs
        self.online_sink_write_option_configs=online_sink_write_option_configs

    @abstractmethod
    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        pass

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=2, sort_keys=True)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.to_json() == other.to_json()

    def to_register_json(self) -> Dict:
        return self.to_json()
