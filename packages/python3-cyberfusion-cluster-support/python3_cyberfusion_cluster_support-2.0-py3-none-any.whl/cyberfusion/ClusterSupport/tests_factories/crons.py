"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.crons import Cron
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class CronFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Cron

        exclude = (
            "unix_user",
            "node",
            "cluster",
        )

    name = factory.Faker("user_name")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserPHPFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    command = factory.Faker("sentence")
    email_address = factory.Faker("email")
    schedule = "* * * * *"
    error_count = factory.Faker("random_int", min=1, max=10)
    random_delay_max_seconds = factory.Faker("random_int", min=1, max=10)
    timeout_seconds = factory.Faker("random_int", min=1, max=10)
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeAdminFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    node_id = factory.SelfAttribute("node.id")
    locking_enabled = factory.Faker("boolean")
    is_active = factory.Faker("boolean")
