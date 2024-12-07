"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mail_domains import MailDomain
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MailDomainFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MailDomain

        exclude = ("unix_user",)

    domain = factory.Faker("domain_name")
    catch_all_forward_email_addresses: list = []
    is_local = factory.Faker("boolean")
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserMailFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
