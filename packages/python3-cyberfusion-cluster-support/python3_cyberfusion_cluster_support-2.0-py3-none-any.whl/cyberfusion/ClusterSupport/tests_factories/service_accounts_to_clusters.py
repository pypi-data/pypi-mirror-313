"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.service_accounts import ServiceAccountGroup
from cyberfusion.ClusterSupport.service_accounts_to_clusters import (
    ServiceAccountToCluster,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountToClusterFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountToCluster

        exclude = (
            "service_account",
            "cluster",
            "site",
        )

    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory",
        site=factory.SelfAttribute("..site"),
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountMailProxyFactory",
        group=ServiceAccountGroup.MAIL_PROXY,
        site=factory.SelfAttribute("..site"),
    )
    service_account_id = factory.SelfAttribute("service_account.id")
