"""Factories for API object."""

import factory.fuzzy

from cyberfusion.ClusterSupport.daemons import Daemon
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _DaemonFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Daemon

        exclude = (
            "unix_user",
            "node",
            "cluster",
        )

    name = factory.Faker("word")
    command = factory.Faker("sentence")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeAdminFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )

    @factory.LazyAttribute
    def nodes_ids(self) -> list[int]:
        """Build nodes_ids for Daemon."""
        node_id = self.node.id

        return [node_id]


class DaemonFactoryPHP(_DaemonFactory):
    """Factory for specific object."""

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserPHPFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )


class DaemonFactory(_DaemonFactory):
    """Factory for specific object."""

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
