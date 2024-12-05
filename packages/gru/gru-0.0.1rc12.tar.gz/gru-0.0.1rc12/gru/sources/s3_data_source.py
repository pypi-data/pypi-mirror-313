"""
Defines a S3 Data Source
"""

from datetime import datetime
from typing import Any, Optional, Union, Dict
from gru.sources.datasource import DataSource
from gru.sources.file_types import CSVType, ParquetType
from gru.utils.data_processing_paradigms import DataProcessingParadigm
from gru.utils.cloud_providers import CloudProviders


class S3DataSource(DataSource):
    """
    Represents an AWS S3 Data Source.

    Parameters:
    ----------
    name (str):
        Name of the S3 data source object.
    bucket (str):
        S3 bucket name.
    base_key (str):
        Fixed data path inside the bucket.
    varying_key_suffix_format (str):
        Varying key format of data based on loading date in S3 (default is "d=%Y-%m-%d/h=%H%M").
    varying_key_suffix_freq (str):
        Frequency of data loading into the S3 object.
    description (str):
        Description of the S3 data source object.
    owners (Union[List[str], str]):
        List of owners of the data source.
    event_timestamp_field (str):
        Timestamp field in the data.
    file_type (Union[CSVType, ParquetType]):
        Type of the file (e.g., CSV, PARQUET).
    schema (Schema):
        Object of the `Schema` class defining the data schema in S3.
    time_offset (int):
        Time offset from 00:00:00 in minutes (default is 0, e.g., 60 means data starts at 00:01:00).
    event_timestamp_format (str):
        Format of the timestamp field in the data source (default is "%Y-%m-%d %H:%M").
    created_at (datetime):
        Timestamp when the data source was registered (default is the current timestamp).

    Notes:
    ------
    This class represents an S3 data source for batch data processing.

    Examples:
    ---------
    >>> data_source_obj = S3DataSource(
    ...     name="my_data_source_11",
    ...     bucket="market-intelligence-platform",
    ...     base_key="sales/raw_data",
    ...     varying_key_suffix_format="d=%Y-%m-%d/h=%H%M",
    ...     varying_key_suffix_freq="15min",
    ...     time_offset=5*60,
    ...     description="random desc of data source",
    ...     owners=["xyz"],
    ...     created_at=datetime(2022, 12, 20, 00, 00, 00),
    ...     file_type=CSVType(header=True),
    ...     schema=schema_obj,
    ...     event_timestamp_field="viewed_at",
    ...     event_timestamp_format="%Y-%m-%d %H:%M",
    ... )
    """

    def __init__(
        self,
        name,
        bucket,
        base_key,
        varying_key_suffix_format,
        varying_key_suffix_freq,
        description,
        owners,
        event_timestamp_field,
        file_type: Union[CSVType, ParquetType],
        schema,
        time_offset=0,
        metadata: Optional[Dict[str, str]] = {},
        additional_read_configs: Optional[Dict[str, Any]] = {},
        event_timestamp_format="%Y-%m-%d %H:%M",
        created_at=datetime.now(),
    ):
        physical_uri = {
            "bucket": bucket,
            "base_key": base_key,
            "varying_key_suffix_format": varying_key_suffix_format,
            "varying_key_suffix_freq": varying_key_suffix_freq,
            "time_offset": time_offset,
            "uri_scheme": "s3",
            "uri_scheme_pyspark": "s3a"
        }
        super().__init__(
            name=name,
            description=description,
            family="object_storage",
            processing_paradigm=DataProcessingParadigm.Batch,
            cloud_provider=CloudProviders.AWS,
            additional_read_configs=additional_read_configs,
            physical_uri=physical_uri,
            schema=schema,
            file_type=file_type,
            type="S3DataSource",
            event_timestamp_field=event_timestamp_field,
            event_timestamp_format=event_timestamp_format,
            metadata=metadata,
            owners=owners,
            created_at=created_at,
        )

    def to_json(self) -> Dict:
        """
        Convert the S3DataSource instance to a JSON-compatible dictionary.

        Returns:
        Dict: A dictionary representing the S3DataSource.
        """
        return {
            "name": self.name,
            "description": self.description,
            "family": self.family,
            "processing_paradigm": self.processing_paradigm.value,
            "cloud_provider": self.cloud_provider.value
            if self.cloud_provider
            else None,
            "additional_read_configs": self.additional_read_configs,
            "physical_uri": self.physical_uri,
            "file_type": self.file_type.type if self.file_type else None,
            "file_type_properties": self.file_type.options
            if self.file_type.options
            else {},
            "schema": self.schema.schema,
            "type": self.type,
            "event_timestamp_field": self.event_timestamp_field,
            "event_timestamp_format": self.event_timestamp_format,
            "metadata": self.metadata,
            "owners": self.owners,
            "created_at": str(self.created_at),
        }
