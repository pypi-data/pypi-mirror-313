"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.service_accounts_to_customers import (
    ServiceAccountToCustomer,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountToCustomerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountToCustomer

        exclude = (
            "service_account",
            "customer",
            "site",
            "site_to_customer",
        )

    customer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.customers.CustomerFactory"
    )
    customer_id = factory.SelfAttribute("customer.id")
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_to_customer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites_to_customers.SiteToCustomerFactory",
        site=factory.SelfAttribute("..site"),
        customer=factory.SelfAttribute("..customer"),
    )
    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountInternetRouterFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_id = factory.SelfAttribute("service_account.id")
