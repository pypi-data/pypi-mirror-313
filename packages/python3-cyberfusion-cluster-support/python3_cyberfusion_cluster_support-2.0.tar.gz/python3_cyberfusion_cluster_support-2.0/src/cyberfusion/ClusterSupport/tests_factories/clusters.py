"""Factories for API object."""

from typing import Any, Dict, List, Optional

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.clusters import (
    Cluster,
    ClusterGroup,
    MeilisearchEnvironment,
    UNIXUserHomeDirectory,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ClusterFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = Cluster

        exclude = (
            "customer",
            "cluster",
            "site",
            "site_to_customer",
            "service_account_phpmyadmin",
            "service_account_security_txt_policy_server",
            "service_account_mail_gateway",
            "service_account_load_balancer",
            "service_account_mail_proxy",
            "service_account_server_phpmyadmin",
            "service_account_server_security_txt_policy_server",
            "service_account_server_mail_gateway",
            "service_account_server_load_balancer",
            "service_account_server_mail_proxy",
        )

    customer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.customers.CustomerFactory"
    )
    customer_id = factory.SelfAttribute("customer.id")
    php_ioncube_enabled: bool = False
    meilisearch_master_key: Optional[str] = None
    meilisearch_environment: Optional[MeilisearchEnvironment] = None
    meilisearch_backup_interval: Optional[int] = None
    new_relic_apm_license_key: Optional[str] = None
    new_relic_mariadb_password: Optional[str] = None
    new_relic_infrastructure_license_key: Optional[str] = None
    php_sessions_spread_enabled: bool = False
    http_retry_properties: Optional[dict] = None
    kernelcare_license_key: Optional[str] = None
    grafana_domain: Optional[str] = None
    singlestore_studio_domain: Optional[str] = None
    singlestore_api_domain: Optional[str] = None
    singlestore_root_password: Optional[str] = None
    elasticsearch_default_users_password: Optional[str] = None
    rabbitmq_erlang_cookie: Optional[str] = None
    rabbitmq_admin_password: Optional[str] = None
    singlestore_license_key: Optional[str] = None
    metabase_domain: Optional[str] = None
    metabase_database_password: Optional[str] = None
    kibana_domain: Optional[str] = None
    rabbitmq_management_domain: Optional[str] = None
    wordpress_toolkit_enabled: bool = False
    sync_toolkit_enabled: bool = False
    bubblewrap_toolkit_enabled: bool = False
    automatic_upgrades_enabled: bool = False
    database_toolkit_enabled: bool = False
    description = factory.Faker("word")
    firewall_rules_external_providers_enabled: bool = False
    unix_users_home_directory: Optional[str] = None
    php_versions: List[str] = []
    redis_password: Optional[str] = None
    postgresql_backup_interval: Optional[int] = None
    mariadb_backup_interval: Optional[int] = None
    mariadb_backup_local_retention: Optional[int] = None
    postgresql_backup_local_retention: Optional[int] = None
    meilisearch_backup_local_retention: Optional[int] = None
    mariadb_cluster_name: Optional[str] = None
    redis_memory_limit: Optional[int] = None
    mariadb_version: Optional[str] = None
    postgresql_version: Optional[int] = None
    nodejs_version: Optional[int] = None
    nodejs_versions: List[str] = []
    custom_php_modules_names: List[str] = []
    php_settings: Dict[str, Any] = {}
    automatic_borg_repositories_prune_enabled: bool = False
    groups: List[str] = []
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_id = factory.SelfAttribute("site.id")
    site_to_customer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites_to_customers.SiteToCustomerFactory",
        customer=factory.SelfAttribute("..customer"),
        site=factory.SelfAttribute("..site"),
    )
    service_account_phpmyadmin = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountPhpMyAdminFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_security_txt_policy_server = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountSecurityTXTPolicyServerFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_mail_gateway = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountMailGatewayFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_load_balancer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountLoadBalancerFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_mail_proxy = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountMailProxyFactory",
        site=factory.SelfAttribute("..site"),
    )
    service_account_server_phpmyadmin = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_account_servers.ServiceAccountServerPhpMyAdminFactory",
        service_account=factory.SelfAttribute("..service_account_phpmyadmin"),
    )
    service_account_server_security_txt_policy_server = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_account_servers.ServiceAccountServerSecurityTXTPolicyServerFactory",
        service_account=factory.SelfAttribute(
            "..service_account_security_txt_policy_server"
        ),
    )
    service_account_server_mail_gateway = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_account_servers.ServiceAccountServerMailGatewayFactory",
        service_account=factory.SelfAttribute("..service_account_mail_gateway"),
    )
    service_account_server_load_balancer = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_account_servers.ServiceAccountServerLoadBalancerFactory",
        service_account=factory.SelfAttribute("..service_account_load_balancer"),
    )
    service_account_server_mail_proxy = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_account_servers.ServiceAccountServerMailProxyFactory",
        service_account=factory.SelfAttribute("..service_account_mail_proxy"),
    )


class ClusterWebFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.WEB]
    unix_users_home_directory = factory.fuzzy.FuzzyChoice(UNIXUserHomeDirectory)
    php_versions = ["8.1", "8.0", "7.4", "7.3", "7.2", "7.1", "7.0", "5.6"]
    nodejs_versions = ["14.0"]
    nodejs_version = 18
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterRedirectFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.REDIRECT]
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterDatabaseFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.DB]
    mariadb_version = "10.10"
    postgresql_version = 15
    mariadb_cluster_name = factory.Faker(
        "password",
        special_chars=False,
        upper_case=False,
        digits=False,
    )
    redis_password = factory.Faker("password", special_chars=False, length=24)
    redis_memory_limit = factory.Faker("random_int", min=32, max=1024)
    mariadb_backup_interval = factory.Faker("random_int", min=1, max=24)
    postgresql_backup_interval = factory.Faker("random_int", min=1, max=24)
    meilisearch_backup_interval = factory.Faker("random_int", min=1, max=24)
    mariadb_backup_local_retention = factory.Faker("random_int", min=1, max=24)
    postgresql_backup_local_retention = factory.Faker("random_int", min=1, max=24)
    meilisearch_backup_local_retention = factory.Faker("random_int", min=1, max=24)
    grafana_domain = factory.Faker("domain_name")
    singlestore_studio_domain = factory.Faker("domain_name")
    singlestore_license_key = "BDU3ZWI5ODkyYTJhMDRhODY4MWRkMDI2ZTlhOTRiMDVmAAAAAAAAAAAEAAAAAAAAACgwNgIZAI8ktJBlGbs+aZ45gVy+63/fNBnAenoJWgIZAPMGnzzQRF3UBB9yMvTiF2ktUtKVPRGUFg=="
    singlestore_api_domain = factory.Faker("domain_name")
    singlestore_root_password = factory.Faker(
        "password", special_chars=False, length=24
    )
    elasticsearch_default_users_password = factory.Faker(
        "password", special_chars=False, length=24
    )
    rabbitmq_erlang_cookie = factory.Faker(
        "password", special_chars=False, length=20, lower_case=False
    )
    rabbitmq_admin_password = factory.Faker("password", special_chars=False, length=24)
    metabase_domain = factory.Faker("domain_name")
    metabase_database_password = factory.Faker(
        "password", special_chars=False, length=24
    )
    kibana_domain = factory.Faker("domain_name")
    rabbitmq_management_domain = factory.Faker("domain_name")


class ClusterMailFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.MAIL]
    unix_users_home_directory = UNIXUserHomeDirectory.MNT_MAIL


class ClusterBorgClientFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.BORG_CLIENT, ClusterGroup.WEB]
    unix_users_home_directory = factory.fuzzy.FuzzyChoice(UNIXUserHomeDirectory)
    http_retry_properties: dict = {
        "tries_amount": None,
        "tries_failover_amount": None,
        "conditions": [],
    }


class ClusterBorgServerFactory(ClusterFactory):
    """Factory for specific object."""

    groups = [ClusterGroup.BORG_SERVER]
    unix_users_home_directory = UNIXUserHomeDirectory.MNT_BACKUPS
