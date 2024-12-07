"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.unix_users_usages import UNIXUserUsage


class UNIXUserUsageFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = UNIXUserUsage

        exclude = ("unix_user",)

    usage = factory.Faker("pyfloat", positive=True)
    files: list = []
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
