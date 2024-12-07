"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.mariadb_encryption_keys import (
    MariaDBEncryptionKey,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class MariaDBEncryptionKeyFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = MariaDBEncryptionKey

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterDatabaseFactory",
    )
    cluster_id = factory.SelfAttribute("cluster.id")
