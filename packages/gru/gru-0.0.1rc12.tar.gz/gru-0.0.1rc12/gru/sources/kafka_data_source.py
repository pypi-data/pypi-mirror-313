"""
Defines a Kafka Data Source
"""

import json
from typing import Any, List, Optional, Union, Mapping, Dict
from datetime import datetime

from gru.sources.datasource import DataSource
from gru.utils.data_processing_paradigms import DataProcessingParadigm
from gru.utils.cloud_providers import CloudProviders


class KafkaSource(DataSource):
    """
    Represents an Apache Kafka Data Source.

    Parameters:
    ----------
    name (str):
        Name of the streaming Kafka data source.
    description (str):
        Description of the Kafka streaming data source.
    bootstrap_server (str):
        IP address or URL of the server hosting the Kafka Data Source.
    topic (Union[List[str], str]):
        Name of the topic(s) from which data will be extracted.
    schema (Dict):
        The schema of the payload in the Kafka topic, using the same format as for batch data sources.
    timestamp_field (str):
        Field in the incoming Kafka data used to individually identify each event.
    timestamp_format (str):
        Format of the timestamp field mentioned above.
    owners (Union[List[str], str]):
        List of owners of the data source.
    read_configs (Mapping[str, any]):
        Additional read configurations.
    cloud_provider (CloudProviders):
        The cloud provider associated with this data source (default is None).
    metadata (Optional[Dict[str, str]]):
        Additional metadata for the data source (default is an empty dictionary).
    additional_read_configs (Optional[Dict[str, Any]]):
        Additional read configurations (default is an empty dictionary).
    created_at (datetime):
        Date and time when the data source was created (default is the current timestamp).


    Notes:
    ------
    This class represents an Kafka Data Source for streaming data processing.

    Examples:
    ---------
    >>> streaming_kafka_source_obj = KafkaSource(
    ...     name="test_kafka_streaming_source_v1.0.4",
    ...     description="random desc of data source",
    ...     owners=["platform@yugen.ai"],
    ...     topic="numtest",
    ...     schema={
    ...         "type": "struct",
    ...         "fields": [
    ...             {"name": "id", "type": "integer", "nullable": True, "metadata": {}},
    ...             {"name": "salary", "type": "integer", "nullable": True, "metadata": {}},
    ...             {"name": "incentive", "type": "integer", "nullable": True, "metadata": {}},
    ...             {
    ...                 "name": "timestamp",
    ...                 "type": "timestamp",
    ...                 "nullable": True,
    ...                 "metadata": {},
    ...             },
    ...         ],
    ...     },
    ...     timestamp_field="timestamp",
    ...     timestamp_format="yyyy-MM-dd HH:mm:ssXXX",
    ...     bootstrap_server="3.110.47.157:9092",
    ...     read_configs={
    ...         "watermark_delay_threshold": 5,
    ...         "starting_timestamp": None,
    ...         "starting_offset_by_timestamp": {},
    ...         "starting_offsets": "latest",
    ...         "fail_on_data_loss": True,
    ...         "include_headers": True,
    ...     },
    ...     cloud_provider=CloudProviders.AWS
    ... )
    """

    def __init__(
        self,
        name: str,
        description: str,
        bootstrap_server: str,
        topic: Union[List[str], str],
        schema: Dict,
        timestamp_field: str,
        timestamp_format: str,
        owners: Union[List[str], str],
        read_configs: Mapping[str, any],
        cloud_provider: CloudProviders = None,
        metadata: Optional[Dict[str, str]] = {},
        additional_read_configs: Optional[Dict[str, Any]] = {},
        created_at=datetime.now(),
    ):
        """
        Constructor of Kafka Class
        """
        super().__init__(
            name=name,
            description=description,
            family="kafka",
            processing_paradigm=DataProcessingParadigm.Streaming,
            cloud_provider=cloud_provider,
            additional_read_configs=additional_read_configs,
            physical_uri=read_configs,
            schema=schema,
            type="KafkaSource",
            event_timestamp_field=timestamp_field,
            event_timestamp_format=timestamp_format,
            metadata=metadata,
            owners=owners,
            created_at=created_at,
        )

        self.physical_uri["topic"] = topic
        self.physical_uri["kafka_bootstrap_servers"] = bootstrap_server

    def to_json(self) -> Dict:
        """
        Convert the KafkaSource instance to a JSON-compatible dictionary.

        Returns:
        Dict: A dictionary representing the KafkaSource.
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
            "file_type": self.file_type.type if self.file_type else "",
            "file_type_properties": json.dumps(self.file_type.options)
            if self.file_type
            else {},
            "schema": self.schema,
            "type": self.type,
            "event_timestamp_field": self.event_timestamp_field,
            "event_timestamp_format": self.event_timestamp_format,
            "metadata": self.metadata,
            "owners": self.owners,
            "created_at": str(self.created_at),
        }
