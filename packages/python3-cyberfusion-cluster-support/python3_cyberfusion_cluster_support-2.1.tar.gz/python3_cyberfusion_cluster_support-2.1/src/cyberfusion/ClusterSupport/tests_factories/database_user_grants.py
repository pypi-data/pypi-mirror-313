"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.database_user_grants import (
    DatabaseUserGrant,
    Privilege,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class DatabaseUserGrantFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = DatabaseUserGrant

        exclude = ("database", "database_user")

    database = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.databases.DatabaseMariaDBFactory"
    )
    database_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.database_users.DatabaseUserMariaDBFactory",
        cluster=factory.SelfAttribute("..database.cluster"),
    )
    database_id = factory.SelfAttribute("database.id")
    database_user_id = factory.SelfAttribute("database_user.id")
    table_name = factory.Faker("password", special_chars=False, length=24)
    privilege_name = factory.fuzzy.FuzzyChoice(Privilege)
