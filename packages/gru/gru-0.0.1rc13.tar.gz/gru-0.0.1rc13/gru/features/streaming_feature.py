from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from gru.features.ml_feature import MLFeature
from gru.features.feature_logic import FeatureLogic
from gru.features.custom_feature_logic import CustomFeatureLogic
from gru.utils.data_types import DataType
from gru.utils.entity_type import EntityType
from gru.utils.processing_engine import ProcessingEngine
from gru.features.processing_engine_configs import StreamingProcessingEngineConfigs


class StreamingFeature(MLFeature):
    """
    A streaming raw feature is a computed column, calculated on top of a field by performing an aggregation funciton for a given timeperiod of data.

    Parameters
    ----------
    self: str
        Python self object
    name: str
        name of the feature
    description: str
        description of the feature definition
    source_name: List[str]
        data source name on which feature will be calculated
    sink_name List[str]:
        The name of the destination where the feature will be stored.
    owners: List[str]
        list of owner names
    online: bool
        If True, then feature will be persisted to Online Feature Store. By default, False
    offline: bool
        If True, then feature will be persisted to Offline Feature Store. By default, True
    feature_logic: FeatureLogic object
        FeatureLogic object that will be the logic part of feature definition

    Returns
    -------
    None

    Notes
    -----
    Use the class to create and deploy Raw features for streaming sources.

    Examples
    --------
    >>> streaming_feature_obj = StreamingFeature(
    ...     name="test_kafka_streaming_f1_v1.0.2",
    ...     description="Sample ML Feature on a Kafka Topic",
    ...     source_name=["test_kafka_streaming_source_v1.0.2"],
    ...     sink_name="demosink",
    ...     owners=["platform@yugen.ai"],
    ...     feature_logic=FeatureLogic(
    ...         field=["salary"],
    ...         time_window="3d",
    ...         timestamp_field="timestamp",
    ...         timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
    ...         transform=SlidingWindowAggregation(
    ...             function="sum",
    ...             partition_by="salary",
    ...             order_by="id",
    ...             window_period="5 seconds",
    ...             window_duration="5 seconds",
    ...         ),
    ...         groupby_keys=["id", "salary"],
    ...     ),
    ...     online=True,
    ...     offline=True,
    ... )
    """

    def __init__(
        self,
        name: str,
        data_type: DataType,
        data_sources: List[str],
        offline: bool,
        feature_logic: Union[FeatureLogic,CustomFeatureLogic],
        read_option_configs: Optional[List[Dict[str, Any]]] = None,
        staging_sink_write_option_configs: Optional[Dict[str, Any]] = None,
        online_sink_write_option_configs: Optional[Dict[str, Any]] = None,
        entity: List[str] = [],
        online: bool = False,
        staging_sink: List[str] = [],
        online_sink: List[str] = [],
        description: str = "",
        owners: List[str] = [],
        k8s_configs: Dict = {},
        processing_engine: Optional[ProcessingEngine] = ProcessingEngine.PYSPARK_K8S,
        processing_engine_configs: Optional[StreamingProcessingEngineConfigs] = None,
        creation_time: datetime = datetime.now(),
        start_time: datetime = datetime.now(),
    ):
        sink = {"staging": staging_sink, "online": online_sink}
        super().__init__(
            name=name,
            type=EntityType.STREAMING_FEATURE.value,
            data_type=data_type,
            online=online,
            offline=offline,
            entity=entity,
            data_sources=data_sources,
            sink=sink,
            feature_logic=feature_logic,
            description=description,
            owners=owners,
            k8s_configs=k8s_configs,
            processing_engine=processing_engine,
            processing_engine_configs=processing_engine_configs
            or StreamingProcessingEngineConfigs(),
            creation_time=creation_time,
            start_time=start_time,
            read_option_configs=read_option_configs,
            staging_sink_write_option_configs=staging_sink_write_option_configs,
            online_sink_write_option_configs=online_sink_write_option_configs,
        )

    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        return {
            "name": self.name,
            "type": self.type,
            "data_type": self.data_type.value,
            "data_sources": self.data_sources,
            "owners": self.owners,
            "description": self.description,
            "start_time": str(self.start_time)
            if self.start_time
            else str(datetime.now()),
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
            "created_at": str(self.creation_time),  # For backward compatibility
            "metadata": self.tags,
            "read_option_configs": self.read_option_configs,
            "staging_sink_write_option_configs": self.staging_sink_write_option_configs,
            "online_sink_write_option_configs": self.online_sink_write_option_configs,
        }

    def to_register_json(self) -> Dict:
        return self.to_json()
