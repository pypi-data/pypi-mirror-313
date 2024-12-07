"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.security_txt_policies import (
    PreferredLanguage,
    SecurityTXTPolicy,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class SecurityTXTPolicyFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = SecurityTXTPolicy

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    expires_timestamp = factory.Faker("iso8601")
    email_contacts = ["foo@example.com"]
    url_contacts = ["https://example.com"]
    encryption_key_urls = ["https://example.com"]
    acknowledgment_urls = ["https://example.com"]
    policy_urls = ["https://example.com"]
    opening_urls = ["https://example.com"]
    preferred_languages = [PreferredLanguage.NL]
