import pytest
from gru.utils.processing_engine import ProcessingEngine


def test_processing_engines():
    """
    Unittest to validate all possible processing engines
    """
    assert ProcessingEngine.PYSPARK_K8S.value == "pyspark_k8s"
    assert ProcessingEngine.PYTHON.value == "python"
    assert ProcessingEngine.DASK.value == "dask"


def test_supported_processing_engines():
    """
    Unittest to validate processing engines currently supported by Yugen.ai platform
    """
    assert ProcessingEngine.get_key("pyspark_k8s") == ProcessingEngine.PYSPARK_K8S


def test_unsupported_processing_engines():
    """
    Unittest to validate the platforms that are not supported by Yugen.ai platform
    """
    with pytest.raises(
        ValueError,
        match="python isn't supported yet. Support expected to be available around Feb, 2024.",
    ):
        ProcessingEngine.get_key("python")

    with pytest.raises(
        ValueError,
        match="dask isn't supported yet. Support expected to be available around Feb, 2024.",
    ):
        ProcessingEngine.get_key("dask")


def test_unexpected_processing_engines():
    """
    Unittest to validate the unexpected/unwanted processing engine
    """
    with pytest.raises(
        ValueError,
        match=f"""Unexpected engine foo. Supported Engines are {', '.join(engine.value for engine in ProcessingEngine)}.""",
    ):
        ProcessingEngine.get_key("foo")
