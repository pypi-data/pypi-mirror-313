"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.databases_usages import DatabaseUsage
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class DatabaseUsageFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = DatabaseUsage

        exclude = ("database",)

    usage = factory.Faker("pyfloat", positive=True)
    database = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.databases.DatabaseFactory",
    )
    database_id = factory.SelfAttribute("database.id")
