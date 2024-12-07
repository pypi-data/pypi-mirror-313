"""Factories for API object."""

import factory

from cyberfusion.ClusterSupport.api_users_to_clusters import APIUserToCluster
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class APIUserToClusterFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = APIUserToCluster

        exclude = (
            "api_user",
            "cluster",
        )

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    api_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.api_users.APIUserFactory",
    )
    api_user_id = factory.SelfAttribute("api_user.id")
