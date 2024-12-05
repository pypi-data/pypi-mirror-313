from enum import Enum


class ElasticCacheRedisClusterMode(Enum):
    """
    Redis Cluster Mode in Elasticache (AWS)
    """

    CLUSTER_ENABLED = "cluster_mode_enabled"
    CLUSTER_DISABLED = "cluster_mode_not_enabled"
