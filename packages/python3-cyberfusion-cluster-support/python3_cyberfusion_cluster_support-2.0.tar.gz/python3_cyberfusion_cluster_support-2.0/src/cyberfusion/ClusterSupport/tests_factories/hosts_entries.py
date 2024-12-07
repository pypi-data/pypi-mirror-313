"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.hosts_entries import HostsEntry
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class HostsEntryFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = HostsEntry

        exclude = (
            "node",
            "cluster",
        )

    host_name = factory.Faker("domain_name")
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeAdminFactory",
    )
    node_id = factory.SelfAttribute("node.id")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
