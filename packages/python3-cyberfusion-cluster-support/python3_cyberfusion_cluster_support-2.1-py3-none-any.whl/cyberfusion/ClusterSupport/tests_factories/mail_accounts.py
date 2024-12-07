"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mail_accounts import MailAccount
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MailAccountFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MailAccount

        exclude = ("mail_domain",)

    local_part = factory.Faker("user_name")
    password = factory.Faker("password", special_chars=False, length=24)
    quota = factory.Faker("random_int", min=1, max=10000)
    mail_domain = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.mail_domains.MailDomainFactory",
    )
    mail_domain_id = factory.SelfAttribute("mail_domain.id")
