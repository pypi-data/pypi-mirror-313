"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.borg_archives import BorgArchive
from cyberfusion.ClusterSupport.clusters import ClusterGroup
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _BorgArchiveFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgArchive

    name = factory.Faker("user_name")
    borg_repository_id = factory.SelfAttribute("borg_repository.id")
    unix_user_id = None
    database_id = None


class BorgArchiveUNIXUserFactory(_BorgArchiveFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgArchive

        exclude = (
            "borg_repository",
            "unix_user",
            "cluster",
        )

    borg_repository = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.borg_repositories.BorgRepositoryUNIXUserFactory",
        cluster=factory.SelfAttribute("..cluster"),
        unix_user=factory.SelfAttribute("..unix_user"),
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        groups=[ClusterGroup.BORG_CLIENT, ClusterGroup.WEB],
    )
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")


class BorgArchiveDatabaseFactory(_BorgArchiveFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgArchive

        exclude = (
            "borg_repository",
            "database",
            "cluster",
        )

    borg_repository = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.borg_repositories.BorgRepositoryFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory",
        groups=[ClusterGroup.BORG_CLIENT, ClusterGroup.DB],
        database_toolkit_enabled=True,
    )
    database = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.databases.DatabaseFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    database_id = factory.SelfAttribute("database.id")
