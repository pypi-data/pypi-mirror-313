"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.firewall_rules import (
    FirewallRule,
    FirewallRuleExternalProviderName,
    FirewallRuleServiceName,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _FirewallRuleFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallRule

        exclude = (
            "node",
            "cluster",
        )

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        firewall_rules_external_providers_enabled=True,
    )
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeAdminFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    node_id = factory.SelfAttribute("node.id")
    firewall_group_id = None
    external_provider_name = None
    service_name = None
    haproxy_listen_id = None
    port = None


class _FirewallRuleFirewallGroupFactory(_FirewallRuleFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallRule

        exclude = (
            "node",
            "firewall_group",
            "cluster",
        )

    firewall_group = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.firewall_groups.FirewallGroupFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    firewall_group_id = factory.SelfAttribute("firewall_group.id")


class _FirewallRuleExternalProviderFactory(_FirewallRuleFactory):
    """Factory for specific object."""

    external_provider_name = factory.fuzzy.FuzzyChoice(FirewallRuleExternalProviderName)


class FirewallRuleExternalProviderServiceFactory(_FirewallRuleExternalProviderFactory):
    """Factory for specific object."""

    service_name = factory.fuzzy.FuzzyChoice(FirewallRuleServiceName)


class FirewallRuleExternalProviderHAProxyListenFactory(
    _FirewallRuleExternalProviderFactory
):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallRule

        exclude = (
            "node",
            "cluster",
            "haproxy_listen",
        )

    haproxy_listen = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.haproxy_listens.HAProxyListenMariaDBPortFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    haproxy_listen_id = factory.SelfAttribute("haproxy_listen.id")


class FirewallRuleExternalProviderPortFactory(_FirewallRuleExternalProviderFactory):
    """Factory for specific object."""

    port = factory.Faker("random_int", min=1024, max=65535)


class FirewallRuleFirewallGroupServiceFactory(_FirewallRuleFirewallGroupFactory):
    """Factory for specific object."""

    service_name = factory.fuzzy.FuzzyChoice(FirewallRuleServiceName)


class FirewallRuleFirewallGroupHAProxyListenFactory(_FirewallRuleFirewallGroupFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallRule

        exclude = (
            "node",
            "firewall_group",
            "cluster",
            "haproxy_listen",
        )

    haproxy_listen = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.haproxy_listens.HAProxyListenMariaDBPortFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    haproxy_listen_id = factory.SelfAttribute("haproxy_listen.id")


class FirewallRuleFirewallGroupPortFactory(_FirewallRuleFirewallGroupFactory):
    """Factory for specific object."""

    port = factory.Faker("random_int", min=1024, max=65535)


class FirewallRuleServiceFactory(_FirewallRuleFactory):
    """Factory for specific object."""

    service_name = factory.fuzzy.FuzzyChoice(FirewallRuleServiceName)


class FirewallRuleHAProxyListenFactory(_FirewallRuleFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = FirewallRule

        exclude = (
            "node",
            "cluster",
            "haproxy_listen",
        )

    haproxy_listen = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.haproxy_listens.HAProxyListenMariaDBPortFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    haproxy_listen_id = factory.SelfAttribute("haproxy_listen.id")


class FirewallRulePortFactory(_FirewallRuleFactory):
    """Factory for specific object."""

    port = factory.Faker("random_int", min=1024, max=65535)
