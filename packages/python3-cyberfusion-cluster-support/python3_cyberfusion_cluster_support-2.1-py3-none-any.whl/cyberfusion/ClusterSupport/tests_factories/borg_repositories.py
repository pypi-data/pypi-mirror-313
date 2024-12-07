"""Factories for API object."""

from typing import Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.borg_repositories import BorgRepository
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class BorgRepositoryFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgRepository

        exclude = ("cluster",)

    passphrase = factory.Faker("password", length=24)
    name = factory.Faker("user_name")
    keep_hourly = factory.Faker("random_int", min=1, max=100)
    keep_daily = factory.Faker("random_int", min=1, max=100)
    keep_weekly = factory.Faker("random_int", min=1, max=100)
    keep_monthly = factory.Faker("random_int", min=1, max=100)
    keep_yearly = factory.Faker("random_int", min=1, max=100)
    remote_host = factory.Faker("domain_name")
    remote_path = "/tmp"
    remote_username = factory.Faker("user_name")
    identity_file_path: Optional[str] = None
    unix_user_id = None
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterBorgClientFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")


class BorgRepositoryUNIXUserFactory(BorgRepositoryFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BorgRepository

        exclude = (
            "unix_user",
            "cluster",
        )

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    identity_file_path = "/tmp/key"
