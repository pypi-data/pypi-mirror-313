from enum import Enum

class SinkFamily(Enum):
    """
    Enum class representing various sink families
    """

    REDIS = "redis"
    OBJECT_STORAGE = "object_storage"

    @classmethod
    def get_key(cls, value: str):
        """
        Retrieve the key (name) of a sink family based on its string value.

        Args:
            value: The string value representing a sink family.
        
        Returns:
            str: The key (name) of the sink family.

        Raises:
            ValueError: If no key is found for the given value.

        Example:
        >>> SinkFamily.get_key("redis")
        'REDIS'
        """
        for item in cls:
            if item.value == value:
                return item.name
        raise ValueError(f"sink family \"{value}\" isn't supported yet.")