import pytest, os
from gru.features.raw_feature import RawFeature
from gru.utils.data_types import DataType
from gru.features.feature_logic import FeatureLogic
from gru.utils.processing_engine import ProcessingEngine
from gru.utils.read_options import KafkaReadOptions
from gru.features.processing_engine_configs import BatchProcessingEngineConfigs
from datetime import datetime
from gru.features.aggregations import SlidingWindowAggregation


@pytest.fixture
def raw_feature_fixture():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    configs_path = os.path.join(
        current_dir, "data", "test_default_processing_config_batch.yaml"
    )
    raw_feature = RawFeature(
        name="testing_raw_feature",
        description="test",
        data_type=DataType.FLOAT,
        staging_sink=["foo"],
        staging_sink_write_option_configs={
            "foo": {
                "bucket": "internal-ml-demos",
            },
        },
        online_sink=["bar"],
        online_sink_write_option_configs={
            "bar": {"file_type_properties": {"type": "PARQUET", "mergeSchema": False}},
        },
        data_sources=["analytics_data", "survey_telemetry_data"],
        read_option_configs=[
            {
                "name": "kafka_streaming_source",
                "options": KafkaReadOptions(
                    watermark_delay_threshold="10 seconds",
                    processing_time="120 seconds",
                    starting_offsets="earliest",
                    include_headers=True,
                ).to_json(),
            }
        ],
        owners=["foo2@yugen.ai"],
        entity=["quux"],
        feature_logic=FeatureLogic(
            field=["corge"],
            filter="grault",
            transform=SlidingWindowAggregation(
                function="garply",
                partition_by="waldo",
                order_by="fred",
                rowsBetween={"frame_start": 1, "frame_end": 2},
            ),
            time_window="3d",
            groupby_keys=["plugh"],
            timestamp_field="time",
            timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
        ),
        processing_engine=ProcessingEngine.PYSPARK_K8S,
        processing_engine_configs=BatchProcessingEngineConfigs(config_path=configs_path),
        online=True,
        offline=True,
        schedule="0 0 * * *",
        active=True,
        start_time=datetime(2023, 12, 5, 0, 0, 0),
        creation_time="2023-12-05 18:06:57.175721",
    )
    return raw_feature


def test_to_json(raw_feature_fixture):
    """
    Takes a custom raw fixture to test the default parameters

    Parameters
    ----------
    raw_feature_fixture : fixture object

    Returns
    -------
    pytest true/false
    """
    expected_result = {
        "name": "testing_raw_feature",
        "type": "raw_feature",
        "data_type": "float",
        "data_sources": ["analytics_data", "survey_telemetry_data"],
        "owners": ["foo2@yugen.ai"],
        "description": "test",
        "start_time": "2023-12-05 00:00:00",
        "online": True,
        "offline": True,
        "entity": ["quux"],
        "feature_logic": {
            "is_feature_logic_custom": False,
            "name": "",
            "transform": {
                "function": "garply",
                "partition_by": "waldo",
                "order_by": "fred",
                "rowsBetween": {"frame_start": 1, "frame_end": 2},
                "function_type": "SlidingWindowAggregation",
            },
            "time_window": "3d",
            "groupby_keys": ["plugh"],
            "field": ["corge"],
            "filter": "grault",
            "timestamp_field": "time",
            "timestamp_format": "yyyy-MM-dd HH:mm:ssXXX",
        },
        "k8s_configs": {},
        "processing_engine": "pyspark_k8s",
        "processing_engine_configs": {
            "deploy-mode": "foo1",
            "num-executors": 10,
            "spark.driver.cores": 1,
            "spark.executor.cores": 1,
            "spark.executor.instances": 1,
            "spark.hadoop.fs.s3a.aws.credentials.provider": "foo3",
            "spark.kubernetes.authenticate.driver.serviceAccountName": "bar2",
            "spark.kubernetes.container.image.pullSecrets": "bar3",
            "spark.kubernetes.driver.limit.cores": "bar4",
            "spark.kubernetes.driver.memory": "bar1",
            "spark.kubernetes.executor.limit.cores": "foo5",
            "spark.kubernetes.executor.memory": "foo2",
            "spark.kubernetes.file.upload.path": "/path/to/config/file",
            "spark.kubernetes.namespace": "foo4",
        },
        "sink": {"staging": ["foo"], "online": ["bar"]},
        "read_option_configs": [
            {
                "name": "kafka_streaming_source",
                "options": {
                    "delimiter": "|",
                    "fail_on_data_loss": False,
                    "include_headers": True,
                    "infer_schema": True,
                    "processing_time": "120 seconds",
                    "starting_offsets": "earliest",
                    "starting_offsets_by_timestamp": None,
                    "starting_timestamp": None,
                    "watermark_delay_threshold": "10 " "seconds",
                },
            }
        ],
        "online_sink_write_option_configs": {
            "bar": {"file_type_properties": {"type": "PARQUET", "mergeSchema": False}}
        },
        "staging_sink_write_option_configs": {"foo": {"bucket": "internal-ml-demos"}},
        "creation_time": "2023-12-05 18:06:57.175721",
        "airflow_configs": {"active": True, "timeout": "5m", "schedule": "0 0 * * *"},
        "created_at": "2023-12-05 18:06:57.175721",
        "metadata": {},
    }

    assert raw_feature_fixture.to_json() == expected_result
