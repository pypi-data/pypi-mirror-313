"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.database_users import (
    DatabaseServerSoftwareName,
)
from cyberfusion.ClusterSupport.databases import Database
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class DatabaseFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Database

        exclude = ("cluster",)

    name = factory.Faker(
        "password", special_chars=False, upper_case=False, digits=False
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory",
        database_toolkit_enabled=True,
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    server_software_name = factory.fuzzy.FuzzyChoice(DatabaseServerSoftwareName)
    backups_enabled = True
    optimizing_enabled = False


class DatabaseMariaDBFactory(DatabaseFactory):
    """Factory for specific object."""

    server_software_name = DatabaseServerSoftwareName.MARIADB


class DatabasePostgreSQLFactory(DatabaseFactory):
    """Factory for specific object."""

    server_software_name = DatabaseServerSoftwareName.POSTGRESQL
