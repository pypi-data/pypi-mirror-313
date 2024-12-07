"""Factories for API object."""

from typing import Optional

import factory

from cyberfusion.ClusterSupport.nodes import Node, NodeGroup
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class _NodeFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Node

    comment = None
    load_balancer_health_checks_groups_pairs: dict = {}
    groups_properties: dict[str, Optional[dict]] = {
        "Redis": None,
        "MariaDB": None,
        "RabbitMQ": None,
    }
    product = "S"


class NodeProFTPDFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.PROFTPD]


class NodeBorgFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterBorgClientFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.BORG]


class NodeRedisFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.REDIS]
    groups_properties = {
        "Redis": {"is_master": True},
        "MariaDB": None,
        "RabbitMQ": None,
    }


class NodeHAProxyFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.HAPROXY]


class NodeMariaDBFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.MARIADB]
    groups_properties = {
        "MariaDB": {"is_master": True},
        "Redis": None,
        "RabbitMQ": None,
    }


class NodeAdminFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.ADMIN]


class NodePHPFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.PHP]


class NodePostgreSQLFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.POSTGRESQL]


class NodeApacheFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.APACHE]


class NodeFastRedirectFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterRedirectFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.FAST_REDIRECT]


class NodeNginxFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.NGINX]


class NodeDovecotFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterMailFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.DOVECOT]


class NodeMeilisearchFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.MEILISEARCH]


class NodeDockerFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.DOCKER]


class NodeNewRelicFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.NEW_RELIC]


class NodeGrafanaFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.GRAFANA]


class NodeSingleStoreFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.SINGLESTORE]


class NodeMetabaseFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.METABASE]


class NodeElasticsearchFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.ELASTICSEARCH]


class NodeRabbitMQFactory(_NodeFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory"
    )
    cluster_id = factory.SelfAttribute("cluster.id")
    groups = [NodeGroup.RABBITMQ]
    groups_properties = {
        "MariaDB": None,
        "Redis": None,
        "RabbitMQ": {"is_master": True},
    }
