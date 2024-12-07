"""Factories for API object."""

import os
import random

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory
from cyberfusion.ClusterSupport.unix_users import ShellPath, UNIXUser


class _UNIXUserFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = UNIXUser

    username = factory.Faker("user_name")
    password = factory.Faker("password", length=24)
    description = factory.Faker("domain_word")
    record_usage_files = False
    default_php_version = None
    default_nodejs_version = None
    borg_repositories_directory = None
    virtual_hosts_directory = None
    mail_domains_directory = None
    cluster_id = factory.SelfAttribute("cluster.id")
    shell_path = ShellPath.BASH


class UNIXUserWebFactory(_UNIXUserFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory"
    )
    virtual_hosts_directory = factory.LazyAttribute(
        lambda obj: os.path.join(
            obj.cluster.unix_users_home_directory,
            obj.username,
            obj.virtual_hosts_subdirectory or "",
        )
    )

    class Params:
        """Parameters."""

        virtual_hosts_subdirectory = None


class UNIXUserBorgServerFactory(_UNIXUserFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterBorgServerFactory"
    )
    borg_repositories_directory = factory.LazyAttribute(
        lambda obj: os.path.join(
            obj.cluster.unix_users_home_directory,
            obj.username,
            obj.borg_repositories_subdirectory or "",
        )
    )

    class Params:
        """Parameters."""

        borg_repositories_subdirectory = None


class UNIXUserMailFactory(_UNIXUserFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        exclude = ("cluster",)

    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterMailFactory"
    )
    mail_domains_directory = factory.LazyAttribute(
        lambda obj: os.path.join(
            obj.cluster.unix_users_home_directory,
            obj.username,
            obj.mail_domains_subdirectory or "",
        )
    )

    class Params:
        """Parameters."""

        mail_domains_subdirectory = None


class UNIXUserPHPFactory(UNIXUserWebFactory):
    """Factory for specific object."""

    default_php_version = factory.LazyAttribute(
        lambda obj: random.choice(obj.cluster.php_versions)
    )
    shell_path = ShellPath.BASH


class UNIXUserNodeJSFactory(UNIXUserWebFactory):
    """Factory for specific object."""

    default_nodejs_version = factory.LazyAttribute(
        lambda obj: random.choice(obj.cluster.nodejs_versions)
    )
    shell_path = ShellPath.JAILSHELL
    default_php_version = None
    cluster = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.clusters.ClusterWebFactory",
        bubblewrap_toolkit_enabled=True,
    )
