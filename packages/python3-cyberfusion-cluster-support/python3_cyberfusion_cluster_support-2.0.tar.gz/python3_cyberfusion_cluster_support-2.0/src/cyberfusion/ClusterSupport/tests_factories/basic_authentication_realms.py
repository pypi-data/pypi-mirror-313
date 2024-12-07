"""Factories for API object."""

import os

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.basic_authentication_realms import (
    BasicAuthenticationRealm,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class BasicAuthenticationRealmFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = BasicAuthenticationRealm

        exclude = (
            "cluster",
            "unix_user",
            "virtual_host",
            "htpasswd_file",
        )

    name = factory.Faker("user_name")
    directory_path = factory.LazyAttribute(
        lambda obj: os.path.join(obj.virtual_host.document_root, "directory")
    )
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
    )
    unix_user = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.unix_users.UNIXUserWebFactory",
        cluster=factory.SelfAttribute("..cluster"),
    )
    virtual_host = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.virtual_hosts.VirtualHostFactory",
        unix_user=factory.SelfAttribute("..unix_user"),
        cluster=factory.SelfAttribute("..cluster"),
    )
    virtual_host_id = factory.SelfAttribute("virtual_host.id")
    htpasswd_file = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.htpasswd_files.HtpasswdFileFactory",
        unix_user=factory.SelfAttribute("..unix_user"),
    )
    htpasswd_file_id = factory.SelfAttribute("htpasswd_file.id")
