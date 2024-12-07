"""Factories for API object."""

import os
import random
from typing import Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.virtual_hosts import (
    AllowOverrideDirective,
    AllowOverrideOptionDirective,
    VirtualHost,
    VirtualHostServerSoftwareName,
)


class VirtualHostFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = VirtualHost

        exclude = (
            "cluster",
            "unix_user",
            "apache_node",
            "nginx_node",
        )

    domain = factory.Faker("domain_name")
    server_aliases: list = []
    custom_config = None
    server_software_name = factory.fuzzy.FuzzyChoice(VirtualHostServerSoftwareName)
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        bubblewrap_toolkit_enabled=True,  # For if unix_user = UNIXUserNodeJSFactory
    )
    unix_user = factory.SubFactory(
        f"cyberfusion.ClusterSupport.tests_factories.unix_users.{random.choice(['UNIXUserPHPFactory','UNIXUserNodeJSFactory'])}",
        cluster=factory.SelfAttribute("..cluster"),
    )
    unix_user_id = factory.SelfAttribute("unix_user.id")
    document_root = factory.LazyAttribute(
        lambda obj: os.path.join(
            obj.unix_user.virtual_hosts_directory, obj.domain, "htdocs"
        )
    )
    public_root = factory.LazyAttribute(
        lambda obj: os.path.join(
            obj.unix_user.virtual_hosts_directory, obj.domain, "htdocs"
        )
    )
    fpm_pool_id = None
    passenger_app_id = None

    # No way to get needed node from server_software_name, so create both

    apache_node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeApacheFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    nginx_node = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.nodes.NodeNginxFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )

    @factory.lazy_attribute
    def allow_override_directives(self) -> Optional[AllowOverrideDirective]:
        """Get allow override directives depending on server software."""
        if self.server_software_name == VirtualHostServerSoftwareName.NGINX:
            return None

        return random.sample(list(AllowOverrideDirective), 1)

    @factory.lazy_attribute
    def allow_override_option_directives(
        self,
    ) -> Optional[AllowOverrideOptionDirective]:
        """Get allow override option directives depending on server software."""
        if self.server_software_name == VirtualHostServerSoftwareName.NGINX:
            return None

        return random.sample(list(AllowOverrideOptionDirective), 1)


class VirtualHostFPMPoolFactory(VirtualHostFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = VirtualHost

        exclude = (
            "cluster",
            "unix_user",
            "fpm_pool",
            "apache_node",
            "nginx_node",
        )

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserPHPFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    fpm_pool = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.fpm_pools.FPMPoolFactory",
        unix_user=factory.SelfAttribute("..unix_user"),
    )
    fpm_pool_id = factory.SelfAttribute("fpm_pool.id")
    server_software_name = factory.fuzzy.FuzzyChoice(VirtualHostServerSoftwareName)


class VirtualHostPassengerAppFactory(VirtualHostFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = VirtualHost

        exclude = (
            "cluster",
            "unix_user",
            "passenger_app",
            "apache_node",
            "nginx_node",
        )

    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserNodeJSFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        bubblewrap_toolkit_enabled=True,
    )
    passenger_app = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.passenger_apps.PassengerAppFactory",
        unix_user=factory.SelfAttribute("..unix_user"),
    )
    passenger_app_id = factory.SelfAttribute("passenger_app.id")
    server_software_name = VirtualHostServerSoftwareName.NGINX
