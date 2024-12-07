"""Factories for API object."""

import random
from typing import Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.database_users import (
    DatabaseServerSoftwareName,
    DatabaseUser,
    Host,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class DatabaseUserFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = DatabaseUser

        exclude = ("cluster",)

    name = factory.Faker(
        "password", special_chars=False, upper_case=False, digits=False
    )
    password = factory.Faker("password", length=24)
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory",
        database_toolkit_enabled=True,
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    server_software_name = factory.fuzzy.FuzzyChoice(DatabaseServerSoftwareName)
    phpmyadmin_firewall_groups_ids: list[int] = []

    @factory.lazy_attribute
    def host(self) -> Optional[Host]:
        """Get host depending on server software."""
        if self.server_software_name == DatabaseServerSoftwareName.POSTGRESQL:
            return None

        return random.choice(list(Host))


class DatabaseUserMariaDBFactory(DatabaseUserFactory):
    """Factory for specific object."""

    server_software_name = DatabaseServerSoftwareName.MARIADB


class DatabaseUserPostgreSQLFactory(DatabaseUserFactory):
    """Factory for specific object."""

    server_software_name = DatabaseServerSoftwareName.POSTGRESQL
