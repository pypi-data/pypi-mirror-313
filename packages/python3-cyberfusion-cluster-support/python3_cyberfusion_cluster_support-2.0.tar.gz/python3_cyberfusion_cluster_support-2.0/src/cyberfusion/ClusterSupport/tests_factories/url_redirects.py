"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.url_redirects import StatusCode, URLRedirect


class URLRedirectFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = URLRedirect

        exclude = ("cluster",)

    domain = factory.Faker("domain_name")
    server_aliases: list = []
    destination_url = factory.Faker("uri")
    status_code = factory.fuzzy.FuzzyChoice(StatusCode)
    keep_query_parameters = factory.Faker("boolean")
    keep_path = factory.Faker("boolean")
    description = factory.Faker("domain_word")
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterRedirectFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
