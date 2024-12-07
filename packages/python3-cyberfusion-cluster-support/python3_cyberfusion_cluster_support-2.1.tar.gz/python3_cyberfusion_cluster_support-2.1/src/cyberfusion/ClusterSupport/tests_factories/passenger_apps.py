"""Factories for API object."""

import os
import random

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.passenger_apps import (
    PassengerApp,
    PassengerEnvironment,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class PassengerAppFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = PassengerApp

        exclude = ("unix_user",)

    name = factory.Faker("user_name")
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserPHPFactory",
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    environment = factory.fuzzy.FuzzyChoice(PassengerEnvironment)
    environment_variables: dict = {}
    max_pool_size = factory.Faker("random_int", min=1, max=10)
    max_requests = factory.Faker("random_int", min=500, max=2000)
    pool_idle_time = factory.Faker("random_int", min=5000, max=10000)
    nodejs_version = factory.LazyAttribute(
        lambda obj: random.choice(obj.unix_user.cluster.nodejs_versions)
    )
    startup_file = factory.Faker("file_name", extension="js")
    is_namespaced = factory.Faker("boolean")
    cpu_limit = factory.Faker("random_int", min=100, max=600)
    app_root = factory.LazyAttribute(
        lambda obj: os.path.join(obj.unix_user.home_directory, obj.name)
    )
