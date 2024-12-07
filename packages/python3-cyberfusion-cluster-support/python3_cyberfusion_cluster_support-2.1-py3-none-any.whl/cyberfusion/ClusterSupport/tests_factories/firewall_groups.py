"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.firewall_groups import FirewallGroup
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class FirewallGroupFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallGroup

        exclude = ("cluster",)

    name = factory.Faker(
        "password", special_chars=False, upper_case=False, digits=False
    )
    ip_networks = ["2001:db8::/32"]
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
