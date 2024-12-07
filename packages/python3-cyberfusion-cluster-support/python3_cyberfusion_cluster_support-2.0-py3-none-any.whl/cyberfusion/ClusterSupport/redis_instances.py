"""Helper classes for scripts for cluster support packages."""

import os
from enum import Enum
from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_REDIS_INSTANCES = "redis-instances"
MODEL_REDIS_INSTANCES = "redis_instances"


def get_unit_name(name: str) -> str:
    """Get unit name."""
    return f"redis-server-cf@{name}.service"


def get_working_directory(name: str) -> str:
    """Get working directory."""
    return os.path.join(os.path.sep, "var", "lib", "redis", name)


class EvictionPolicy(str, Enum):
    """Eviction policies."""

    VOLATILE_TTL: str = "volatile-ttl"
    VOLATILE_RANDOM: str = "volatile-random"
    ALLKEYS_RANDOM: str = "allkeys-random"
    VOLATILE_LFU: str = "volatile-lfu"
    VOLATILE_LRU: str = "volatile-lru"
    ALLKEYS_LFU: str = "allkeys-lfu"
    ALLKEYS_LRU: str = "allkeys-lru"
    NOEVICTION: str = "noeviction"


class RedisInstance(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = [
        "Eviction Policy",
        "Memory Limit",
        "Max Databases",
        "Port",
    ]

    _TABLE_FIELDS = [
        "id",
        "name",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED: List[str] = [
        "eviction_policy",
        "memory_limit",
        "max_databases",
        "port",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.port = obj["port"]
        self.memory_limit = obj["memory_limit"]
        self.eviction_policy = obj["eviction_policy"]
        self.max_databases = obj["max_databases"]
        self.cluster_id: int = obj["cluster_id"]
        self.password = obj["password"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.unit_name = get_unit_name(self.name)
        self.pid = os.path.join(
            os.path.sep, "run", f"redis-{self.name}", "redis-server.pid"
        )
        self.working_directory = get_working_directory(self.name)
        self.base_config_file_path = os.path.join(
            os.path.sep, "etc", "redis", "redis.conf"
        )
        self.log_file_path = os.path.join(
            os.path.sep,
            "var",
            "log",
            "redis",
            f"redis-server.{self.name}.log",  # /etc/logrotate.d/redis-server rotates /var/log/redis/redis-server*.log,
        )

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        password: str,
        memory_limit: int,
        eviction_policy: EvictionPolicy,
        max_databases: int,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_REDIS_INSTANCES}"
        data = {
            "name": name,
            "password": password,
            "memory_limit": memory_limit,
            "eviction_policy": eviction_policy,
            "max_databases": max_databases,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.redis_instances.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_REDIS_INSTANCES}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "port": self.port,
            "password": self.password,
            "memory_limit": self.memory_limit,
            "eviction_policy": self.eviction_policy,
            "max_databases": self.max_databases,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self, delete_on_cluster: bool = False) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_REDIS_INSTANCES}/{self.id}"

        params = {"delete_on_cluster": delete_on_cluster}

        self.support.request.DELETE(url, params)
        self.support.request.execute()

        self.support.redis_instances.remove(self)
