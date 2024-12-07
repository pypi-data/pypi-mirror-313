"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.unix_users_home_directories_usages import (
    UNIXUsersHomeDirectoryUsage,
)


class UNIXUsersHomeDirectoryUsageFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = UNIXUsersHomeDirectoryUsage

        exclude = ("cluster",)

    usage = factory.Faker("pyfloat", positive=True)
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
