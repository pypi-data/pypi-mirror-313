"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.customers import Customer
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class CustomerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Customer

    team_code = factory.Faker(
        "bothify", text="##??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    is_internal = factory.Faker("boolean")
