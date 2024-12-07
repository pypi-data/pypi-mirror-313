"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_accounts import (
    ServiceAccount,
    ServiceAccountGroup,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _ServiceAccountFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccount

        exclude = ("site",)

    name = factory.Faker("domain_name")
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_id = factory.SelfAttribute("site.id")


class _ServiceAccountWithNetworkInformationFactory(_ServiceAccountFactory):
    """Factory for specific object."""

    default_ipv6_ip_address = factory.Faker("ipv6")
    default_ipv4_ip_address = factory.Faker("ipv4")
    default_ipv6_netbox_id = factory.Faker("random_int", min=500, max=2000)
    default_ipv4_netbox_id = factory.Faker("random_int", min=500, max=2000)
    netbox_additional_prefix_ipv6_id = factory.Faker("random_int", min=500, max=2000)
    netbox_additional_prefix_ipv4_id = factory.Faker("random_int", min=500, max=2000)
    netbox_fhrp_group_ipv6_id = factory.Faker("random_int", min=500, max=2000)
    netbox_fhrp_group_ipv4_id = factory.Faker("random_int", min=500, max=2000)


class _ServiceAccountWithoutNetworkInformationFactory(_ServiceAccountFactory):
    """Factory for specific object."""

    default_ipv6_ip_address = None
    default_ipv4_ip_address = None
    default_ipv6_netbox_id = None
    default_ipv4_netbox_id = None
    netbox_additional_prefix_ipv4_id = None
    netbox_fhrp_group_ipv6_id = None
    netbox_fhrp_group_ipv4_id = None
    netbox_additional_prefix_ipv6_id = None


class ServiceAccountInternetRouterFactory(_ServiceAccountWithNetworkInformationFactory):
    """Factory for specific object."""

    group = ServiceAccountGroup.INTERNET_ROUTER


class ServiceAccountStorageRouterFactory(
    _ServiceAccountWithoutNetworkInformationFactory
):
    """Factory for specific object."""

    group = ServiceAccountGroup.STORAGE_ROUTER


class ServiceAccountPhpMyAdminFactory(_ServiceAccountWithoutNetworkInformationFactory):
    """Factory for specific object."""

    group = ServiceAccountGroup.PHPMYADMIN


class ServiceAccountSecurityTXTPolicyServerFactory(
    _ServiceAccountWithoutNetworkInformationFactory
):
    """Factory for specific object."""

    group = ServiceAccountGroup.SECURITY_TXT_POLICY_SERVER


class ServiceAccountMailGatewayFactory(_ServiceAccountWithoutNetworkInformationFactory):
    """Factory for specific object."""

    group = ServiceAccountGroup.MAIL_GATEWAY


class ServiceAccountLoadBalancerFactory(_ServiceAccountWithNetworkInformationFactory):
    """Factory for specific object."""

    group = ServiceAccountGroup.LOAD_BALANCER


class ServiceAccountMailProxyFactory(_ServiceAccountWithoutNetworkInformationFactory):
    """Factory for specific object."""

    group = ServiceAccountGroup.MAIL_PROXY
