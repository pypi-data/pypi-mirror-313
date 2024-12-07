"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mail_accounts_usages import MailAccountUsage
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MailAccountUsageFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MailAccountUsage

        exclude = ("mail_account",)

    usage = factory.Faker("pyfloat", positive=True)
    mail_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.mail_accounts.MailAccountFactory",
    )
    mail_account_id = factory.SelfAttribute("mail_account.id")
