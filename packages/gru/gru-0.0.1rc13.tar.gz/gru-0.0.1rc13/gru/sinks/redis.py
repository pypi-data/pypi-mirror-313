from typing import Dict, Union
from datetime import datetime
from gru.sinks.sink import Sink
from gru.redis_helpers.elasticache import ElasticCacheRedisClusterMode
from gru.sinks.sink_family import SinkFamily
from gru.utils.cloud_providers import CloudProviders


class ElasticCacheRedisSink(Sink):
    """Sink module for Redis on AWS ElasticCache."""

    def __init__(
        self,
        name: str,
        host: str,
        port: int = 6379,
        mode: Union[
            ElasticCacheRedisClusterMode, str
        ] = ElasticCacheRedisClusterMode.CLUSTER_ENABLED,
        created_at=datetime.now(),
        **kwargs,
    ):
        """
        Initialize the ElasticCacheRedisSink.

        Arguments:
        - host (str): Primary Endpoint of the ElasticCache Redis Cluster.
        - port (int): The port of the Redis instance to connect. Default is 6379.
        - mode (Union[ElasticCacheRedisClusterMode, str]): Whether Cluster mode is enabled or Cluster mode is disabled.
          Default is ElasticCacheRedisClusterMode.CLUSTER_ENABLED.

        Raises:
        - ValueError: If host is not a string or port is not an integer.
        """
        super().__init__(
            name=name,
            family=SinkFamily.REDIS.value,
            cloud_provider=CloudProviders.AWS,
            physical_uri={"host": host, "port": port, "mode": mode.value},
            type="ElasticCacheRedisSink",
            **kwargs,
        )
        self.host = host
        self.port = port
        self.mode = (
            mode
            if isinstance(mode, ElasticCacheRedisClusterMode)
            else ElasticCacheRedisClusterMode(mode)
        )

        self._validate_host_port()
        self._validate_mode()
        self.created_at = created_at

    def _validate_host_port(self):
        """
        Validate that host is a string and port is an integer.

        Raises:
        - ValueError: If host is not a string or port is not an integer.
        """
        if not isinstance(self.host, str):
            raise ValueError("Host must be a string.")
        if not isinstance(self.port, int):
            raise ValueError("Port must be an integer.")

    def _validate_mode(self):
        """
        Validate the mode value.

        Raises:
        - ValueError: If mode is not an instance of ElasticCacheRedisClusterMode or if mode is missing in JSON data.
        """
        if not isinstance(self.mode, ElasticCacheRedisClusterMode):
            raise ValueError(
                "Mode must be an instance of ElasticCacheRedisClusterMode."
            )
        if self.mode is None:
            raise ValueError("Missing 'mode' value in JSON data.")

    def to_json(self) -> Dict:
        """
        Convert the ElasticCacheRedisSink instance to a JSON-serializable dictionary.

        Returns:
        - Dict: A dictionary containing the name, family, host, port, and mode values.
        """
        return {
            "name": self.name,
            "family": self.family,
            "physical_uri": self.physical_uri,
            "type": self.type,
            "file_type": self.file_type.type if self.file_type else None,
            "file_type_properties": self.file_type.options if self.file_type else None,
            "cloud_provider": self.cloud_provider.value,
            "description": self.description,
            "metadata": self.metadata,
            "owners": self.owners,
            "created_at": str(self.created_at),
        }

    @classmethod
    def from_json(cls, json_dict: Dict) -> "ElasticCacheRedisSink":
        """
        Create an ElasticCacheRedisSink instance from a JSON dictionary.

        Arguments:
        - json_dict (Dict): A dictionary containing the host, port, and mode values.

        Returns:
        - ElasticCacheRedisSink: An instance of ElasticCacheRedisSink.

        Raises:
        - ValueError: If host is missing in the JSON data.
        """
        host = json_dict.get("host")
        port = json_dict.get("port")
        mode = json_dict.get("mode")

        return ElasticCacheRedisSink(host=host, port=port, mode=mode)
