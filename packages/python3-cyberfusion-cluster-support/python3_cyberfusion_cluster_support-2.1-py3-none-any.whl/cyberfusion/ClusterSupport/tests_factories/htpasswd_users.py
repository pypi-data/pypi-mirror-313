"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.htpasswd_users import HtpasswdUser
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class HtpasswdUserFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = HtpasswdUser

        exclude = ("htpasswd_file",)

    htpasswd_file = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.htpasswd_files.HtpasswdFileFactory",
    )
    htpasswd_file_id = factory.SelfAttribute("htpasswd_file.id")
    username = factory.Faker("user_name")
    password = factory.Faker("password", special_chars=False, length=24)
