import pytest
from unittest.mock import patch, MagicMock
from gru.features.processing_engine_configs import ProcessingEngineConfigs, StreamingProcessingEngineConfigs, BatchProcessingEngineConfigs

@pytest.fixture
def mock_config_reader():
    with patch('gru.features.processing_engine_configs.ConfigReader') as mock:
        config = MagicMock()
        config.deploy_mode = "cluster"
        config.driver_memory = "4g"
        config.executor_memory = "2g"
        config.service_account = "spark"
        config.aws_credential_provider = "com.amazonaws.auth.WebIdentityTokenCredentialsProvider"
        config.container_image = "spark:latest"
        config.container_image_pull_secrets = "regcred"
        config.file_upload_path = "s3a://bucket/path"
        config.name_space = "default"
        config.num_executors = 2
        config.executor_cores = 2
        config.driver_cores = 1
        config.driver_limit_cores = "1200m"
        config.executor_limit_cores = "1200m"
        config.executor_instances = 2
        mock.return_value = config
        yield mock

def test_processing_engine_configs_initialization(mock_config_reader):
    configs = ProcessingEngineConfigs(
        deploy_mode="client",
        driver_memory="8g",
        executor_memory="4g",
        service_account="test-account",
        aws_credential_provider="test-provider",
        container_image="test-image:latest",
        container_image_pull_secrets="test-secret",
        file_upload_path="s3a://test-bucket/path",
        name_space="test-namespace",
        num_executors=4,
        executor_cores=4,
        driver_cores=2,
        driver_limit_cores="2400m",
        executor_limit_cores="2400m",
        executor_instances=4
    )

    assert configs.deploy_mode == "client"
    assert configs.driver_memory == "8g"
    assert configs.executor_memory == "4g"
    assert configs.service_account == "test-account"
    assert configs.aws_credential_provider == "test-provider"
    assert configs.container_image == "test-image:latest"
    assert configs.container_image_pull_secrets == "test-secret"
    assert configs.file_upload_path == "s3a://test-bucket/path"
    assert configs.name_space == "test-namespace"
    assert configs.num_executors == 4
    assert configs.executor_cores == 4
    assert configs.driver_cores == 2
    assert configs.driver_limit_cores == "2400m"
    assert configs.executor_limit_cores == "2400m"
    assert configs.executor_instances == 4

def test_processing_engine_configs_to_json(mock_config_reader):
    configs = ProcessingEngineConfigs()
    json_output = configs.to_json()

    assert json_output["deploy-mode"] == "cluster"
    assert json_output["spark.kubernetes.driver.memory"] == "4g"
    assert json_output["spark.kubernetes.executor.memory"] == "2g"
    assert json_output["spark.kubernetes.authenticate.driver.serviceAccountName"] == "spark"
    assert json_output["spark.hadoop.fs.s3a.aws.credentials.provider"] == "com.amazonaws.auth.WebIdentityTokenCredentialsProvider"
    assert json_output["spark.kubernetes.container.image"] == "spark:latest"
    assert json_output["spark.kubernetes.container.image.pullSecrets"] == "regcred"
    assert json_output["spark.kubernetes.file.upload.path"] == "s3a://bucket/path"
    assert json_output["spark.kubernetes.namespace"] == "default"
    assert json_output["num-executors"] == 2
    assert json_output["spark.executor.cores"] == 2
    assert json_output["spark.driver.cores"] == 1
    assert json_output["spark.kubernetes.driver.limit.cores"] == "1200m"
    assert json_output["spark.kubernetes.executor.limit.cores"] == "1200m"
    assert json_output["spark.executor.instances"] == 2

def test_streaming_processing_engine_configs(mock_config_reader):
    configs = StreamingProcessingEngineConfigs()
    assert configs.default_config_path == "./gru/config/features/default_processing_engine_configs_streaming.yaml"
    mock_config_reader.assert_called_once_with(config_path="./gru/config/features/default_processing_engine_configs_streaming.yaml")

def test_batch_processing_engine_configs(mock_config_reader):
    configs = BatchProcessingEngineConfigs()
    assert configs.default_config_path == "./gru/config/features/default_processing_engine_configs_batch.yaml"
    mock_config_reader.assert_called_once_with(config_path="./gru/config/features/default_processing_engine_configs_batch.yaml")

def test_processing_engine_configs_override_default(mock_config_reader):
    configs = ProcessingEngineConfigs(
        deploy_mode="client",
        driver_memory="8g",
        executor_memory="4g"
    )
    json_output = configs.to_json()

    assert json_output["deploy-mode"] == "client"
    assert json_output["spark.kubernetes.driver.memory"] == "8g"
    assert json_output["spark.kubernetes.executor.memory"] == "4g"
    # Other fields should still use default values
    assert json_output["spark.kubernetes.authenticate.driver.serviceAccountName"] == "spark"

if __name__ == "__main__":
    pytest.main()