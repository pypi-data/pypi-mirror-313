"""
Sinks are an abstraction that define where outputs from various jobs should be persisted
"""

from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union
import json
from datetime import datetime
from gru.schema.registrable import Registrable
from gru.sources.file_types import CSVType, ParquetType
from gru.utils.entity_type import EntityType


class Sink(Registrable):
    """
    Base class for all Sinks
    """

    def __init__(
        self,
        name: str,
        family: str,
        physical_uri: Dict[str, Any],
        type: str = None,
        file_type: Union[CSVType, ParquetType] = None,
        file_type_properties: Optional[Dict[str, Any]] = None,
        cloud_provider: str = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = {},
        owners: Optional[List] = None,
        created_at=datetime.now(),
        # Maybe Default value comes from a separate owners class?
    ):
        """

        Arguments
        ---------
        name: Unique indentifier for the Sink
        family: Unique indentifier for the Sink Family e.g. ObjectStorage, Kafka, MySQL etc.
        physical_uri: All properties that identify the sink resource
        type: Unique name of a sink within a cloud provider
        file_type (optional) - If not None, it specifies the format of the data, e.g. csv, json, parquet, etc.
        file_type_properties (optional) Properties of the file_type.
        cloud_provider - The cloud provider e.g. aws, gcp, etc
        description (optional) - A human-readable description.
        """
        self.name = name
        self.family = family
        self.physical_uri = physical_uri
        self.entity_type = EntityType.DATA_SINK.value
        self.type = type
        self.file_type = file_type
        self.file_type_properties = file_type_properties
        self.cloud_provider = cloud_provider
        self.description = description
        self.metadata = metadata
        self.owners = owners
        self.created_at = created_at

    @abstractmethod
    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        pass

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=2, sort_keys=True)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.to_json() == other.to_json()
    
    def to_register_json(self) -> Dict:
        return self.to_json()
