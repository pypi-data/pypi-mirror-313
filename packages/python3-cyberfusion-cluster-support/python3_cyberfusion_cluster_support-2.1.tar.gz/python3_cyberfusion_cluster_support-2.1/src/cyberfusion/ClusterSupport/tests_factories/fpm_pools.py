"""Factories for API object."""

import random

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.fpm_pools import FPMPool
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class FPMPoolFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FPMPool

        exclude = ("unix_user",)

    name = factory.Faker("user_name")
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserPHPFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    version = factory.LazyAttribute(
        lambda obj: random.choice(obj.unix_user.cluster.php_versions)
    )
    max_children = factory.Faker("random_int", min=5, max=50)
    max_requests = factory.Faker("random_int", min=500, max=2000)
    process_idle_timeout = factory.Faker("random_int", min=5000, max=10000)
    cpu_limit = factory.Faker("random_int", min=100, max=600)
    log_slow_requests_threshold = factory.Faker("random_int", min=1, max=10)
    is_namespaced = factory.Faker("boolean")
