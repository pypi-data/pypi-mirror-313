"""
    Enum-like class defining entity types supported by our Platform

    EntityType is an enumeration class that defines various entity types supported by the platform. 
    These entity types are used to categorize and manage different types of objects and components in the system.
"""

from enum import Enum, unique


@unique
class EntityType(Enum):
    """
    Enum-like class defining entity types supported by our Platform
    """

    DATA_SOURCE = "data_source"
    DATA_SINK = "data_sink"
    RAW_FEATURE = "raw_feature"
    DERIVED_FEATURE = "derived_batch_feature"
    STREAMING_FEATURE = "streaming_feature"
    PRE_PROCESSING_TRANSFORM = "pre_processing_transform"
    TRAINING_DATA = "training_data"
    INFRASTRUCTURE = "infra_details"

    @classmethod
    def get_key(cls, value):
        """
        Get the key (name) of a data type based on its value.

        Args:
            value (str): The value of the data type.

        Returns:
            str: The key (name) of the data type, or None if not found.
        """
        for item in cls:
            if item.value == value:
                return item.name
        return None
