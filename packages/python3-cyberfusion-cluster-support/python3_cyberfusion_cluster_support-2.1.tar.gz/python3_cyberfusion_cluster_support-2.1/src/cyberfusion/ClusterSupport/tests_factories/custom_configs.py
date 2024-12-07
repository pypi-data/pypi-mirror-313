"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.custom_configs import (
    CustomConfig,
    CustomConfigServerSoftwareName,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _CustomConfigFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = CustomConfig

    name = factory.Faker(
        "password", special_chars=False, upper_case=False, digits=False
    )
    contents = factory.Faker("text")
    cluster_id = factory.SelfAttribute("cluster.id")


class CustomConfigNginxFactory(_CustomConfigFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = CustomConfig

        exclude = (
            "cluster",
            "node",
        )

    server_software_name = CustomConfigServerSoftwareName.NGINX
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeNginxFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
