"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.certificate_managers import (
    CertificateManager,
    ProviderName,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class CertificateManagerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = CertificateManager

        exclude = (
            "cluster",
            "virtual_host",
        )

    common_names = ["example.com", "www.example.com"]
    provider_name = factory.fuzzy.FuzzyChoice(ProviderName)
    request_callback_url = factory.Faker("url")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        bubblewrap_toolkit_enabled=True,
    )
    cluster_id = factory.SelfAttribute("cluster.id")

    # Domain router required to create certificate manager

    virtual_host = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.virtual_hosts.VirtualHostFactory",
        domain="example.com",
        server_aliases=["www.example.com"],
        cluster=factory.SelfAttribute("..cluster"),
    )
