"""Factories for API object."""

import random

import factory

from cyberfusion.ClusterSupport.haproxy_listens_to_nodes import (
    HAProxyListenToNode,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _HAProxyListenToNodeFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = HAProxyListenToNode


class HAProxyListenToNodeFactory(_HAProxyListenToNodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = (
            "haproxy_listen",
            "node",
            "cluster",
        )

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory"
    )
    haproxy_listen = factory.SubFactory(
        f"cyberfusion.ClusterSupport.tests_factories.haproxy_listens.{random.choice(['HAProxyListenMariaDBPortFactory','HAProxyListenMariaDBSocketPathFactory','HAProxyListenPostgreSQLPortFactory','HAProxyListenPostgreSQLSocketPathFactory'])}",
        cluster=factory.SelfAttribute("..cluster"),
    )
    node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeHAProxyFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    node_id = factory.SelfAttribute("node.id")
    haproxy_listen_id = factory.SelfAttribute("haproxy_listen.id")
