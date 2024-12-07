"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.custom_config_snippets import (
    CustomConfigSnippet,
    CustomConfigSnippetTemplateName,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)


class _CustomConfigSnippetFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = CustomConfigSnippet

        exclude = (
            "cluster",
            "node",
        )

    name = factory.Faker(
        "password", special_chars=False, upper_case=False, digits=False
    )
    server_software_name = VirtualHostServerSoftwareName.NGINX
    is_default = factory.Faker("boolean")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeNginxFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    cluster_id = factory.SelfAttribute("cluster.id")


class CustomConfigSnippetTemplateFactory(_CustomConfigSnippetFactory):
    """Factory for specific object."""

    template_name = factory.fuzzy.FuzzyChoice(CustomConfigSnippetTemplateName)


class CustomConfigSnippetContentsFactory(_CustomConfigSnippetFactory):
    """Factory for specific object."""

    contents = factory.Faker("text")
