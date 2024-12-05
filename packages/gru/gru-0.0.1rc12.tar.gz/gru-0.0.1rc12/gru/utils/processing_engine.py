from enum import Enum


class ProcessingEngine(Enum):
    """
    Enum class representing processing engines.
    """

    PYSPARK_K8S = "pyspark_k8s"
    PYTHON = "python"
    DASK = "dask"

    @classmethod
    def get_key(cls, value: str):
        if value == cls.PYSPARK_K8S.value:
            return cls.PYSPARK_K8S
        elif value == cls.PYTHON.value or value == cls.DASK.value:
            raise ValueError(
                f"{value} isn't supported yet. Support expected to be available around Feb, 2024."
            )
        else:
            raise ValueError(
                f"""Unexpected engine {value}. Supported Engines are {', '.join(engine.value for engine in ProcessingEngine)}."""
            )
