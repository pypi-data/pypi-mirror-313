"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.sites_to_customers import SiteToCustomer
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class SiteToCustomerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = SiteToCustomer

        exclude = (
            "site",
            "customer",
            "service_account_internet_router",
            "service_account_storage_router",
            "service_account_server_internet_router",
            "service_account_server_storage_router",
        )

    customer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.customers.CustomerFactory"
    )
    customer_id = factory.SelfAttribute("customer.id")
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_id = factory.SelfAttribute("site.id")
