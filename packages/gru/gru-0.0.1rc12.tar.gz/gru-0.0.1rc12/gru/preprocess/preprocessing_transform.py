"""
Pre-Processing Transforms are used to schedule pipelines by providing a custom business logic. This helps create additional Datasources on top of which features can be defined.
testind in production
Functions:
- register
- deploy
"""

from datetime import datetime
from typing import Optional, Dict
from gru.schema.registrable import Registrable
from gru.utils.entity_type import EntityType
from gru.features.processing_engine_configs import BatchProcessingEngineConfigs
from gru.utils.processing_engine import ProcessingEngine

class PreProcessingTransform(Registrable):
    """
    A preprocessing transform represents a custom pipeline used to create intermediate datasources

    Parameters
    ----------
    name: str
        name of the preprocess transform job
    description: str
        description of the preprocess transform job
    data_source_names: list
        list of names of the data sources registered in our platform
    data_source_lookback_config: Dict
        a dict of keys as feature name and value as the lookback window for that particular feature
    logic: str
        SQL logic of the preprocess tranform job
    schedule: str
        schedule of the preprocess transform job
    output_schema: Schema
        schema of the output data persisted in final blob storage
    owners: list
        list of the owners of Preprocess transform job
    active: Optional[str]
        if True, PPT job will start running startdate onwards. And if False, PPT job will be registered and deployed but execution won't begin
    stage: Optional[str]
        stage is the environment e.g. dev or prod
    timeout: Optional[str]
        if job takes more than timeout value, then users will be notified over slack.
    cluster: Optional[str]
        Kubernetes cluster on which the job will run, default values set by Yugen
    k8s_namespace: Optional[str]
        namespace of Kubernetes cluster, default values set by Yugen
    transform_start_time: Optional[datetime]
        start time of the PPT job, default values set by Yugen to datetime.now()

    Returns
    -------
    None

    Methods
    -------
    register(): takes self as an argument and register the Preprocess transform job to the database.
    deploy(): takes self as an argument and deploys the Preprocess transform job. PPT job starts execution as per the PPT start date.

    Notes
    -----

    See Also
    --------

    Examples
    --------
    >>>     ppt_obj = PreProcessingTransform(
    ...         name = "test_transform_demo_v9_sm",
    ...         description = "test preprocess transform",
    ...         data_source_names = ["survey_tracking3", "feedback3"],
    ...         data_source_lookback_config = {
    ...         "survey_tracking3": "1d",
    ...         "feedback3": "2d",
    ...         },
    ...         logic = sql_logic,
    ...         schedule = "0 0 * * *",
    ...         output_schema = schema_obj,
    ...         owners = ["manik.malhotra@yugen.ai"],
    ...         active = True,
    ...         stage = "dev",
    ...         timeout = "5m",
    ...         cluster = "demo_cluster",
    ...         k8s_namespace = "airflow",
    ...         transform_start_time = date(2022, 8, 28),
    ...         )
    """

    def __init__(
        self,
        transform_name: str,
        description: str,
        data_source_names: list,
        data_source_lookback_config: Dict,
        logic: str,
        schedule: str,
        output_schema: object,
        owners: list,
        staging_sink: list[str],
        active: bool = False,
        timeout: str = "5m",
        processing_engine: Optional[ProcessingEngine] = ProcessingEngine.PYSPARK_K8S,
        processing_engine_configs: Optional[BatchProcessingEngineConfigs] = None,
        k8s_configs: Dict = {},
        transform_start_time: Optional[datetime] = datetime.now(),
        online_sink: Optional[list[str]] = None,
    ):
        self.sink = {"staging": staging_sink, "online": online_sink}
        self.type = EntityType.PRE_PROCESSING_TRANSFORM
        self.entity_type = self.type.value
        self.transform_name = transform_name
        self.description = description
        self.data_source_names = data_source_names
        self.data_source_lookback_config = data_source_lookback_config
        self.logic = logic
        self.schedule = schedule
        self.output_schema = output_schema
        self.owners = owners
        self.active = active
        self.processing_engine = processing_engine
        self.processing_engine_configs = (
            processing_engine_configs or BatchProcessingEngineConfigs()
        )
        self.k8s_configs = k8s_configs
        self.timeout = timeout
        self.airflow_config = {
            "active": self.active,
            "schedule": self.schedule,
            "timeout": self.timeout,
        }
        self.transform_start_time = transform_start_time
        self.creation_time = datetime.now()

    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        return {
            "transform_name": self.transform_name,
            "description": self.description,
            "data_source_names": self.data_source_names,
            "data_source_lookbacks": self.data_source_lookback_config,
            "logic": self.logic,
            "output_schema": self.output_schema.schema,
            "owners": self.owners,
            "processing_engine": self.processing_engine.value,
            "processing_engine_configs": self.processing_engine_configs.to_json(),
            "k8s_configs": self.k8s_configs,
            "transform_start_time": str(self.transform_start_time),
            "creation_time": str(self.creation_time),
            "airflow_configs": self.airflow_config,
            "type": self.type.value,
            "sink": self.sink,
        }

    def to_register_json(self) -> Dict:
        return self.to_json()
