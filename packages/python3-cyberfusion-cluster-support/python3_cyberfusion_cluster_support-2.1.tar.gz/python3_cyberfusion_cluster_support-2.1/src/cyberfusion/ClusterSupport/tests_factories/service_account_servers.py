"""Factories for API object."""

from typing import Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_account_servers import (
    NetBoxResourceType,
    ServiceAccountServer,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _ServiceAccountServerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

    hostname = factory.Faker("domain_name")
    netbox_resource_type = factory.fuzzy.FuzzyChoice(NetBoxResourceType)
    netbox_resource_id = factory.Faker("random_int")
    netbox_parent_interface_id: Optional[int] = factory.Faker("random_int")
    service_account_id = factory.SelfAttribute("service_account.id")


class ServiceAccountServerInternetRouterFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountInternetRouterFactory",
    )


class ServiceAccountServerStorageRouterFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountStorageRouterFactory",
    )


class ServiceAccountServerPhpMyAdminFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountPhpMyAdminFactory",
    )


class ServiceAccountServerSecurityTXTPolicyServerFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountSecurityTXTPolicyServerFactory",
    )
    netbox_parent_interface_id = None


class ServiceAccountServerMailGatewayFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountMailGatewayFactory",
    )


class ServiceAccountServerLoadBalancerFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountLoadBalancerFactory",
    )


class ServiceAccountServerMailProxyFactory(_ServiceAccountServerFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountMailProxyFactory",
    )
