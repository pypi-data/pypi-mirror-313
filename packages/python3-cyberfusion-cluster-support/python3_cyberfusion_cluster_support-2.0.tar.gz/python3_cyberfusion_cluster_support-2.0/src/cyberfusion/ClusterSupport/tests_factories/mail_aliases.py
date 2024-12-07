"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mail_aliases import MailAlias
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MailAliasFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MailAlias

        exclude = ("mail_domain",)

    local_part = factory.Faker("user_name")
    forward_email_addresses = ["example@example.com"]
    mail_domain = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.mail_domains.MailDomainFactory",
    )
    mail_domain_id = factory.SelfAttribute("mail_domain.id")
