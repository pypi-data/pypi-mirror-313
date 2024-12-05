from enum import Enum

class CloudProviders(Enum):
    """
    Enum class representing various cloud providers.
    """

    AWS = "aws"
    GCP = "gcp"
    Azure = "azure"
    IBM = "ibm"
    Oracle = "oci"
    RedisCloud = "redis_cloud"


    @classmethod
    def get_key(cls, value: str):
        """
        Retrieve the key (name) of a cloud provider based on its string value.

        Args:
            value: The string value representing a cloud provider.
        
        Returns:
            str: The key (name) of the managed cloud provider.

        Raises:
            ValueError: If no key is found for the given value.

        Example:
        >>> CloudProviders.get_key("gcp")
        'GCP'
        """
        if value == cls.AWS.value:
            return cls.AWS
        else:
            raise ValueError(f"{value} is in the Platform roadmap but isn't supported yet.")