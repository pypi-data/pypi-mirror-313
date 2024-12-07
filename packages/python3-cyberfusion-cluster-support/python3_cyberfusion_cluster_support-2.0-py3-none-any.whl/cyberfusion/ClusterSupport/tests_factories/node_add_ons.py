"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.node_add_ons import NodeAddOn
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class NodeAddOnFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = NodeAddOn

        exclude = ("node",)

    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeAdminFactory",
    )
    node_id = factory.SelfAttribute("node.id")
    product = "20 GiB Disk Storage"
    quantity = 1
