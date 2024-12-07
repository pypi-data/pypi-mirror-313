"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.htpasswd_files import HtpasswdFile
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class HtpasswdFileFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = HtpasswdFile

        exclude = ("unix_user",)

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
