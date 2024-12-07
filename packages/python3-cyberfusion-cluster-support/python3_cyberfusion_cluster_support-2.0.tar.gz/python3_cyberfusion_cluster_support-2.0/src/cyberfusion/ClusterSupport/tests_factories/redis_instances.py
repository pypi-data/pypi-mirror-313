"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.redis_instances import (
    EvictionPolicy,
    RedisInstance,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class RedisInstanceFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = RedisInstance

        exclude = ("cluster",)

    name = factory.Faker("user_name")
    password = factory.Faker("password", special_chars=False, length=24)
    memory_limit = factory.Faker("random_int", min=32, max=1024)
    eviction_policy = factory.fuzzy.FuzzyChoice(EvictionPolicy)
    max_databases = factory.Faker("random_int", min=1, max=10)
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory",
    )

    cluster_id = factory.SelfAttribute("cluster.id")
