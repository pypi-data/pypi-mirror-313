"""
Derived Features are transformations on existing registered features. A few use-cases could be -

Binarizing a spend feature to create a new is_spend_high feature, which assumes values 0 and 1, depending on a threshold
Binning a continuous feature to create custom buckets, e.g. age_bucket or spend_level based on age or spend
OneHotEncoding
LabelEncoding
... and more
Function:
print_feature
register_feature
deploy_feature
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from gru.features.feature_logic import FeatureLogic
from gru.utils.data_types import DataType
from gru.features.ml_feature import MLFeature
from gru.utils.entity_type import EntityType
from gru.utils.processing_engine import ProcessingEngine
from gru.features.processing_engine_configs import BatchProcessingEngineConfigs


class DerivedFeature(MLFeature):
    """
    Derived features are transformations on top of one or more existing feature.

    Parameters
    ----------
    name (str):
        The name of the feature.
    data_type (DataType):
        Data type of the feature.
    transform (Dict):
        Aggregation function that returns a Python dictionary from Aggregations Module.
    sink_name (List[str]):
        The name of the destination where the feature will be stored.
    offline (bool):
        If True, the feature will be persisted to the Offline Feature Store. Default is True.
    schedule (str):
        Cron schedule for the feature generation. Ref: https://crontab.guru/
    entity (List[str]):
        List of entities associated with the feature.
    feature_logic (FeatureLogic):
        FeatureLogic object defining the logic of the feature.
    online (bool):
        If True, the feature will be persisted to the Online Feature Store. Default is False.
    description (str):
        Description of the feature definition.
    owners (List[str]):
        List of owner names.
    active (bool):
        If True, the feature will start running as soon as it's deployed. Default is True.
    timeout (str):
        Maximum time for feature calculation before sending an alert. (Not supported as part of MVP)
    k8s_configs (Dict):
        Kubernetes configurations for feature processing.
    processing_engine (str):
        processing engine, Currently platform supports pyspark.
    processing_engine_configs (Dict):
        Processing engine configurations specific to the defined processing engine.
    start_time (datetime):
        Start time of the feature. Default is the current datetime.
    creation_time (datetime):
        Timestamp of feature creation. Default is the current datetime.


    Returns
    -------
    None

    Notes
    -----

    Examples
    --------
    >>> derived_feature = DerivedFeature(
    ...     name="test_derived_14DEC_v11",
    ...     description="Total purchase amount for the store",
    ...     staging_sink=["s3_sink_ml_yugen_internal"],
    ...     online_sink=["elasticache-redis-yugen"],
    ...     data_type=DataType.FLOAT,
    ...     owners=["rutvik.shah@yugen.ai"],
    ...     schedule="0 0 * * *",
    ...     entity=["CASE WHEN cpi> 0.5 THEN 10 ELSE 0 END"],
    ...     processing_engine=ProcessingEngine.PYSPARK_K8S,
    ...     processing_engine_configs=BatchProcessingEngineConfigs(),
    ...     online=False,
    ...     offline=True,
    ...     transform=multiply(
    ...         "raw_to_1_derived_13DEC_v123", "raw_to_2_derived_13DEC_v123"
    ...     ),
    ...     start_time=datetime(2022, 8, 26, 0, 0, 0),
    ... )
    """

    def __init__(
        self,
        name: str,
        data_type: DataType,
        transform: Dict,
        offline: bool,
        staging_sink: List[str],
        schedule: str,
        entity: List[str],
        start_time: datetime,
        feature_logic: FeatureLogic = None,
        online: bool = False,
        online_sink: List[str] = [],
        description: str = "",
        owners: List[str] = [],
        active: bool = False,
        timeout: str = "5m",
        k8s_configs: Dict = {},
        read_option_configs: Optional[List[Dict[str, Any]]] = None,
        staging_sink_write_option_configs: Optional[Dict[str, Any]] = None,
        online_sink_write_option_configs: Optional[Dict[str, Any]] = None,
        processing_engine: Optional[ProcessingEngine] = ProcessingEngine.PYSPARK_K8S,
        processing_engine_configs: Optional[BatchProcessingEngineConfigs] = None,
        creation_time: datetime = datetime.now(),
        tags: Dict[str, Any] = {}
    ):
        data_sources = transform["feature_list"]

        feature_logic = {
            "transformation_function": transform["transform"],
            "transform_args": self._get_feature_transform_args(transform),
            "groupby_keys": transform["groupby_keys"]
        }
        airflow_configs = {"active": active, "timeout": timeout, "schedule": schedule}
        sink = {"staging": staging_sink, "online": online_sink}

        super().__init__(
            name=name,
            type=EntityType.DERIVED_FEATURE.value,
            data_type=data_type,
            online=online,
            offline=offline,
            entity=entity,
            data_sources=data_sources,
            sink=sink,
            feature_logic=feature_logic,
            description=description,
            owners=owners,
            start_time=start_time,
            k8s_configs=k8s_configs,
            processing_engine=processing_engine,
            processing_engine_configs=processing_engine_configs
            or BatchProcessingEngineConfigs(),
            airflow_configs=airflow_configs,
            creation_time=creation_time,
            tags = tags,
            read_option_configs = read_option_configs,
            staging_sink_write_option_configs = staging_sink_write_option_configs,
            online_sink_write_option_configs = online_sink_write_option_configs,
        )

    def _get_feature_transform_args(self, transform: dict):
        if transform.get("feature_transform_args") is None:
            return {}
        else:
            return transform["feature_transform_args"]

    def to_json(self) -> Dict:
        return {
            "name": self.name,
            "type": self.type,
            "data_type": self.data_type.value,
            "data_sources": self.data_sources,
            "owners": self.owners,
            "description": self.description,
            "start_time": str(self.start_time),
            "online": self.online,
            "offline": self.offline,
            "entity": self.entity,
            "feature_logic": self.feature_logic,
            "k8s_configs": self.k8s_configs,
            "processing_engine": self.processing_engine.value,
            "processing_engine_configs": self.processing_engine_configs.to_json(),
            "sink": self.sink,
            "creation_time": str(self.creation_time),
            "airflow_configs": self.airflow_configs,
            "created_at": str(self.creation_time),  # For backward compatibility
            "metadata" : self.tags,
            "read_option_configs": self.read_option_configs,
            "staging_sink_write_option_configs": self.staging_sink_write_option_configs,
            "online_sink_write_option_configs": self.online_sink_write_option_configs,
        }

    def to_register_json(self) -> Dict:
        return self.to_json()