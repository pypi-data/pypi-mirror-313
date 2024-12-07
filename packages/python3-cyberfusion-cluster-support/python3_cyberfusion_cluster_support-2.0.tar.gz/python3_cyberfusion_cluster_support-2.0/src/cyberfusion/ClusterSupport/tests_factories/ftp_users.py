"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.ftp_users import FTPUser
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class FTPUserFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FTPUser

        exclude = ("unix_user",)

    username = factory.Faker("user_name")
    password = factory.Faker("password", length=24)
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory"
    )
    directory_path = factory.SelfAttribute("unix_user.home_directory")
    unix_user_id = factory.SelfAttribute("unix_user.id")
