from gru.features.processing_engine_configs import StreamingProcessingEngineConfigs
from gru.features.aggregations import SlidingWindowAggregation
from gru.features.streaming_feature import StreamingFeature
from gru.utils.processing_engine import ProcessingEngine
from gru.utils.read_options import KafkaReadOptions
from gru.utils.data_types import DataType
from gru.features.raw_feature import (
    FeatureLogic,
)
import pytest, os


@pytest.fixture
def streaming_feature_fixture():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    configs_path = os.path.join(
        current_dir, "data", "test_default_processing_engine_configs_streaming.yaml"
    )
    streaming_feature_obj = StreamingFeature(
        name="foo",
        description="bar",
        data_type=DataType.FLOAT,
        data_sources=["baz"],
        read_option_configs=[
            {
                "name": "baz",
                "options": KafkaReadOptions(
                    watermark_delay_threshold="10 seconds",
                    processing_time="120 seconds",
                    starting_offsets="earliest",
                    include_headers=True,
                ).to_json(),
            },
        ],
        staging_sink=["quux"],
        staging_sink_write_option_configs={
            "quux": {
                "output_mode": "append",
                "processing_time": "120 seconds",
                "output_partitions": 20,
            }
        },
        online_sink=["corge"],
        owners=["grault@yugen.ai"],
        feature_logic=FeatureLogic(
            field=["garply"],
            time_window="waldo",
            timestamp_field="fred",
            timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
            transform=SlidingWindowAggregation(
                function="plugh",
                partition_by="xyzzy",
                order_by="thud",
                window_period="spam",
                window_duration="eggs",
            ),
            groupby_keys=["ham", "zork"],
        ),
        processing_engine=ProcessingEngine.PYSPARK_K8S,
        processing_engine_configs=StreamingProcessingEngineConfigs(config_path=configs_path),
        online=True,
        offline=True,
        creation_time="2024-05-21 16:32:19.365631",
        start_time="2024-05-21 16:32:46.711044",
    )
    return streaming_feature_obj


def test_to_json(streaming_feature_fixture):
    expected_result = {
        "name": "foo",
        "type": "streaming_feature",
        "data_type": "float",
        "data_sources": ["baz"],
        "owners": ["grault@yugen.ai"],
        "description": "bar",
        "start_time": "2024-05-21 16:32:46.711044",
        "online": True,
        "online_sink_write_option_configs": None,
        "offline": True,
        "entity": [],
        "feature_logic": {
            "name": "",
            "transform": {
                "function": "plugh",
                "partition_by": "xyzzy",
                "order_by": "thud",
                "window_period": "spam",
                "window_duration": "eggs",
                "function_type": "SlidingWindowAggregation",
            },
            "time_window": "waldo",
            "groupby_keys": ["ham", "zork"],
            "field": ["garply"],
            "filter": None,
            "timestamp_field": "fred",
            "timestamp_format": "yyyy-MM-dd HH:mm:ssXXX",
            "is_feature_logic_custom": False,
        },
        "k8s_configs": {},
        "processing_engine": "pyspark_k8s",
        "processing_engine_configs": {
            "deploy-mode": "foo",
            "spark.kubernetes.driver.memory": "bar",
            "spark.kubernetes.executor.memory": "baz",
            "spark.kubernetes.authenticate.driver.serviceAccountName": "qux",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "quux",
            "spark.kubernetes.container.image.pullSecrets": "corge",
            "spark.kubernetes.file.upload.path": "/opt/spark/work-dir",
            "spark.kubernetes.namespace": "grault",
            "num-executors": 1,
            "spark.executor.cores": 1,
            "spark.driver.cores": 1,
            "spark.kubernetes.driver.limit.cores": "garply",
            "spark.kubernetes.executor.limit.cores": "waldo",
            "spark.executor.instances": 1,
        },
        "sink": {"staging": ["quux"], "online": ["corge"]},
        "creation_time": "2024-05-21 16:32:19.365631",
        "airflow_configs": {},
        "created_at": "2024-05-21 16:32:19.365631",
        "metadata": {},
        "read_option_configs": [
            {
                "name": "baz",
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
        "staging_sink_write_option_configs": {
            "quux": {
                "output_mode": "append",
                "processing_time": "120 seconds",
                "output_partitions": 20,
            }
        },
    }

    assert streaming_feature_fixture.to_json() == expected_result
