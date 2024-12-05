"""
In Machine Leaning, a feature is an individual measurable property or characteristic of a phenomenon. Features are used for

 - model training
 - inference/model prediction
 - exploratory analyses
 - Features can be defined using the FeatureLogic class 1. Other operational inputs such as feature_start_time, schedule etc are used to convert the a Feature Definition to a DAG.

 Function:
    - print_feature
    - register_feature
    - deploy_feature
"""
import datetime
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from gru.features.ml_feature import MLFeature
from gru.utils.data_types import DataType
from gru.features.custom_feature_logic import CustomFeatureLogic
from gru.features.feature_logic import FeatureLogic
from gru.utils.entity_type import EntityType
from gru.utils.processing_engine import ProcessingEngine
from gru.features.processing_engine_configs import BatchProcessingEngineConfigs


class RawFeature(MLFeature):
    """
    A raw feature is a computed column, calculated on top of a field by performing an aggregation funciton for a given timeperiod of data.

    Parameters
    ----------
    self: str
        Python self object
    name : str
        The name of the feature.
    source_name : List(str
        The name of the data source from which the feature is calculated.
    sink_name : List(str
        The name of the destination where the feature is stored.
    online : bool
        If True, the feature will be persisted to the Online Feature Store. Default is False.
    offline : bool
        If True, the feature will be persisted to the Offline Feature Store. Default is True.
    schedule : str
        Cron schedule for the feature generation. Ref: https://crontab.guru/
    entity : List[str]
        List of entities associated with the feature.
    feature_logic : FeatureLogic
        FeatureLogic object defining the logic of the feature.
    description : str
        Description of the feature. Default is an empty string.
    data_type : DataTypes
        Data type of the feature
    owners : List[str]
        List of owner names. Default is an empty list.
    active : bool
        If True, the feature will start running as soon as it's deployed. Default is True.
    timeout : str
        Maximum time for feature calculation before sending an alert. (Not supported as part of MVP)
    k8s_configs : Dict
        Kubernetes configurations for feature processing.
    processing_engine_configs : Dict
        Processing engine configurations.
    start_time : datetime
        Start time of the feature. Default is the current datetime.
    creation_time : datetime
        Timestamp of feature creation. Default is the current datetime.


    Returns
    -------
    None

    Notes
    -----
    Use the class to create Raw features for both batch and streaming sources

    Examples:
    >>> create_raw_feature = RawFeature(
    ...     name="va_testing_rows_4",
    ...     description="test",
    ...     data_type=DataType.FLOAT,
    ...     source_name=["svt_half_hour2"],
    ...     sink_name=["sink_test"],
    ...     owners=["vanshika@yugen.ai"],
    ...     entity=["test"],
    ...     feature_logic=FeatureLogic(
    ...         field=["ad_id"],
    ...         filter="ad_id is NOT NULL",
    ...         transform=SlidingWindowAggregation(
    ...             function="avg",
    ...             partition_by="provider",
    ...             order_by="cpi",
    ...             # rangeBetween= {"frame_start": 1, "frame_end": 6},
    ...             rowsBetween={"frame_start": 1, "frame_end": 2},
    ...         ),
    ...         time_window="3d",
    ...         groupby_keys=["project_id"],
    ...         timestamp_field="time",
    ...         timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
    ...     ),
    ...     processing_engine=ProcessingEngine.PYSPARK_K8S,
    ...     processing_engine_configs=ProcessingEngineConfigs(config_path="/user_specific/path/config.yaml"),
    ...     online=True,
    ...     offline=True,
    ...     schedule="0 0 * * *",
    ...     active=True,
    ...     start_time=datetime(2023, 3, 29, 0, 0, 0),
    ... )
    """

    def __init__(
        self,
        name: str,
        data_type: DataType,
        data_sources: List[str],
        offline: bool,
        staging_sink: List[str],
        schedule: str,
        entity: List[str],
        feature_logic: Union[FeatureLogic, CustomFeatureLogic],
        start_time: datetime,
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
        tags: Dict[str, Any] = {},
    ):
        airflow_configs = {"active": active, "timeout": timeout, "schedule": schedule}
        sink = {"staging": staging_sink, "online": online_sink}
        super().__init__(
            name=name,
            type=EntityType.RAW_FEATURE.value,
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
            tags=tags,
            read_option_configs=read_option_configs,
            staging_sink_write_option_configs=staging_sink_write_option_configs,
            online_sink_write_option_configs=online_sink_write_option_configs,
        )

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
            "feature_logic": self.feature_logic.to_json(),
            "k8s_configs": self.k8s_configs,
            "processing_engine": self.processing_engine.value,
            "processing_engine_configs": self.processing_engine_configs.to_json(),
            "sink": self.sink,
            "creation_time": str(self.creation_time),
            "airflow_configs": self.airflow_configs,
            "created_at": str(self.creation_time),
            "metadata" : self.tags,
            "read_option_configs": self.read_option_configs,
            "staging_sink_write_option_configs": self.staging_sink_write_option_configs,
            "online_sink_write_option_configs": self.online_sink_write_option_configs,
        }

    def to_register_json(self) -> Dict:
        return self.to_json()
