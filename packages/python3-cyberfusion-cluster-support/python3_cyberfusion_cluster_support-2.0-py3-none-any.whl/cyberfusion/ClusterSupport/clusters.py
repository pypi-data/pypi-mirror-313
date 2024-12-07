"""Helper classes for scripts for cluster support packages."""

import os
from enum import Enum
from typing import Any, Dict, List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.enums import IPAddressFamily
from cyberfusion.ClusterSupport.nodes import NodeGroup
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_CLUSTERS = "clusters"


class MeilisearchEnvironment(str, Enum):
    """Meilisearch environments."""

    PRODUCTION: str = "production"
    DEVELOPMENT: str = "development"


class HTTPRetryCondition(str, Enum):
    """HTTP retry conditions."""

    CONNECTION_FAILURE: str = "Connection failure"
    EMPTY_RESPONSE: str = "Empty response"
    JUNK_RESPONSE: str = "Junk response"
    RESPONSE_TIMEOUT: str = "Response timeout"
    ZERO_RTT_REJECTED: str = "0-RTT rejected"
    HTTP_STATUS_401: str = "HTTP status 401"
    HTTP_STATUS_403: str = "HTTP status 403"
    HTTP_STATUS_404: str = "HTTP status 404"
    HTTP_STATUS_408: str = "HTTP status 408"
    HTTP_STATUS_425: str = "HTTP status 425"
    HTTP_STATUS_500: str = "HTTP status 500"
    HTTP_STATUS_501: str = "HTTP status 501"
    HTTP_STATUS_502: str = "HTTP status 502"
    HTTP_STATUS_503: str = "HTTP status 503"
    HTTP_STATUS_504: str = "HTTP status 504"


class UNIXUserHomeDirectory(str, Enum):
    """UNIX user home directories."""

    VAR_WWW_VHOSTS: str = "/var/www/vhosts"
    VAR_WWW: str = "/var/www"
    HOME: str = "/home"
    MNT_MAIL: str = "/mnt/mail"
    MNT_BACKUPS: str = "/mnt/backups"


class PHPExtension(str, Enum):
    """PHP extensions."""

    REDIS: str = "redis"
    IMAGICK: str = "imagick"
    SQLITE3: str = "sqlite3"
    XMLRPC: str = "xmlrpc"
    INTL: str = "intl"
    BCMATH: str = "bcmath"
    XDEBUG: str = "xdebug"
    PGSQL: str = "pgsql"
    SSH2: str = "ssh2"
    LDAP: str = "ldap"
    MCRYPT: str = "mcrypt"
    APCU: str = "apcu"
    SQLSRV: str = "sqlsrv"
    GMP: str = "gmp"
    VIPS: str = "vips"
    EXCIMER: str = "excimer"
    TIDEWAYS: str = "tideways"
    MAILPARSE: str = "mailparse"
    UV: str = "uv"


class ClusterGroup(str, Enum):
    """Cluster groups."""

    WEB: str = "Web"
    MAIL: str = "Mail"
    DB: str = "Database"
    BORG_CLIENT: str = "Borg Client"
    BORG_SERVER: str = "Borg Server"
    REDIRECT: str = "Redirect"


class Cluster(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Description",
        "Groups",
        "Site",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "description",
        "groups",
        "_site_name",
    ]
    _TABLE_FIELDS_DETAILED: list = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.groups = [ClusterGroup(x).value for x in obj["groups"]]
        self.unix_users_home_directory = obj["unix_users_home_directory"]
        self.php_versions = obj["php_versions"]
        self.redis_password = obj["redis_password"]
        self.postgresql_backup_interval = obj["postgresql_backup_interval"]
        self.mariadb_backup_interval = obj["mariadb_backup_interval"]
        self.mariadb_backup_local_retention = obj["mariadb_backup_local_retention"]
        self.postgresql_backup_local_retention = obj[
            "postgresql_backup_local_retention"
        ]
        self.meilisearch_backup_local_retention = obj[
            "meilisearch_backup_local_retention"
        ]
        self.mariadb_cluster_name = obj["mariadb_cluster_name"]
        self.redis_memory_limit = obj["redis_memory_limit"]
        self.mariadb_version = obj["mariadb_version"]
        self.postgresql_version = obj["postgresql_version"]
        self.nodejs_version = obj["nodejs_version"]
        self.nodejs_versions = obj["nodejs_versions"]
        self.automatic_borg_repositories_prune_enabled = obj[
            "automatic_borg_repositories_prune_enabled"
        ]
        self.custom_php_modules_names = [
            PHPExtension(x).value for x in obj["custom_php_modules_names"]
        ]
        self.php_settings = obj["php_settings"]
        self.php_ioncube_enabled = obj["php_ioncube_enabled"]
        self.meilisearch_master_key = obj["meilisearch_master_key"]
        self.meilisearch_environment = (
            MeilisearchEnvironment(obj["meilisearch_environment"]).value
            if obj["meilisearch_environment"] is not None
            else None
        )
        self.meilisearch_backup_interval = obj["meilisearch_backup_interval"]
        self.new_relic_apm_license_key = obj["new_relic_apm_license_key"]
        self.new_relic_mariadb_password = obj["new_relic_mariadb_password"]
        self.new_relic_infrastructure_license_key = obj[
            "new_relic_infrastructure_license_key"
        ]
        self.php_sessions_spread_enabled = obj["php_sessions_spread_enabled"]
        self.http_retry_properties = obj["http_retry_properties"]
        self.wordpress_toolkit_enabled = obj["wordpress_toolkit_enabled"]
        self.database_toolkit_enabled = obj["database_toolkit_enabled"]
        self.bubblewrap_toolkit_enabled = obj["bubblewrap_toolkit_enabled"]
        self.automatic_upgrades_enabled = obj["automatic_upgrades_enabled"]
        self.firewall_rules_external_providers_enabled = obj[
            "firewall_rules_external_providers_enabled"
        ]
        self.sync_toolkit_enabled = obj["sync_toolkit_enabled"]
        self.customer_id = obj["customer_id"]
        self.kernelcare_license_key = obj["kernelcare_license_key"]
        self.grafana_domain = obj["grafana_domain"]
        self.singlestore_studio_domain = obj["singlestore_studio_domain"]
        self.singlestore_api_domain = obj["singlestore_api_domain"]
        self.singlestore_root_password = obj["singlestore_root_password"]
        self.elasticsearch_default_users_password = obj[
            "elasticsearch_default_users_password"
        ]
        self.rabbitmq_erlang_cookie = obj["rabbitmq_erlang_cookie"]
        self.rabbitmq_admin_password = obj["rabbitmq_admin_password"]
        self.singlestore_license_key = obj["singlestore_license_key"]
        self.metabase_domain = obj["metabase_domain"]
        self.metabase_database_password = obj["metabase_database_password"]
        self.kibana_domain = obj["kibana_domain"]
        self.rabbitmq_management_domain = obj["rabbitmq_management_domain"]
        self.description = obj["description"]
        self.site_id = obj["site_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.site = self.support.get_sites(id_=self.site_id)[0]
        self._site_name = self.site.name

        if self.unix_users_home_directory:
            self.php_sessions_directory = os.path.join(
                self.unix_users_home_directory, "sessions"
            )

        if self.php_versions:
            self.default_php_version = self.php_versions[-1]

        if self.nodejs_versions:
            self.default_nodejs_version = self.nodejs_versions[-1]

        self._label = f"{self.description} ({self.name})"

    @property
    def redis_master_node_hostname(self) -> Optional[str]:
        """Get hostname of Redis master node."""
        for node in self.support.get_nodes(cluster_id=self.id):
            if not node.groups_properties[NodeGroup.REDIS]:
                continue

            if not node.groups_properties[NodeGroup.REDIS]["is_master"]:
                continue

            return node.hostname

        return None

    @property
    def mariadb_master_node_hostname(self) -> Optional[str]:
        """Get hostname of MariaDB master node."""
        for node in self.support.get_nodes(cluster_id=self.id):
            if not node.groups_properties[NodeGroup.MARIADB]:
                continue

            if not node.groups_properties[NodeGroup.MARIADB]["is_master"]:
                continue

            return node.hostname

        return None

    @property
    def rabbitmq_master_node_hostname(self) -> Optional[str]:
        """Get hostname of RabbitMQ master node."""
        for node in self.support.get_nodes(cluster_id=self.id):
            if not node.groups_properties[NodeGroup.RABBITMQ]:
                continue

            if not node.groups_properties[NodeGroup.RABBITMQ]["is_master"]:
                continue

            return node.hostname

        return None

    def create(
        self,
        *,
        groups: List[ClusterGroup],
        unix_users_home_directory: Optional[UNIXUserHomeDirectory],
        php_versions: List[str],
        redis_password: Optional[str],
        postgresql_backup_interval: Optional[int],
        mariadb_backup_interval: Optional[int],
        mariadb_backup_local_retention: Optional[int],
        postgresql_backup_local_retention: Optional[int],
        meilisearch_backup_local_retention: Optional[int],
        mariadb_cluster_name: Optional[str],
        redis_memory_limit: Optional[int],
        mariadb_version: Optional[str],
        postgresql_version: Optional[int],
        nodejs_version: Optional[int],
        nodejs_versions: List[str],
        custom_php_modules_names: List[PHPExtension],
        php_settings: Dict[str, Any],
        automatic_borg_repositories_prune_enabled: bool,
        php_ioncube_enabled: bool,
        meilisearch_master_key: Optional[str],
        meilisearch_environment: Optional[MeilisearchEnvironment],
        meilisearch_backup_interval: Optional[int],
        new_relic_apm_license_key: Optional[str],
        new_relic_mariadb_password: Optional[str],
        new_relic_infrastructure_license_key: Optional[str],
        php_sessions_spread_enabled: bool,
        http_retry_properties: dict,
        customer_id: int,
        kernelcare_license_key: Optional[str],
        grafana_domain: Optional[str],
        singlestore_studio_domain: Optional[str],
        singlestore_api_domain: Optional[str],
        singlestore_root_password: Optional[str],
        elasticsearch_default_users_password: Optional[str],
        rabbitmq_erlang_cookie: Optional[str],
        rabbitmq_admin_password: Optional[str],
        singlestore_license_key: Optional[str],
        metabase_domain: Optional[str],
        metabase_database_password: Optional[str],
        kibana_domain: Optional[str],
        rabbitmq_management_domain: Optional[str],
        wordpress_toolkit_enabled: bool,
        sync_toolkit_enabled: bool,
        bubblewrap_toolkit_enabled: bool,
        automatic_upgrades_enabled: bool,
        firewall_rules_external_providers_enabled: bool,
        database_toolkit_enabled: bool,
        description: str,
        site_id: int,
    ) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}"
        data = {
            "groups": groups,
            "unix_users_home_directory": unix_users_home_directory,
            "php_versions": php_versions,
            "redis_password": redis_password,
            "postgresql_backup_interval": postgresql_backup_interval,
            "mariadb_backup_interval": mariadb_backup_interval,
            "mariadb_backup_local_retention": mariadb_backup_local_retention,
            "postgresql_backup_local_retention": postgresql_backup_local_retention,
            "meilisearch_backup_local_retention": meilisearch_backup_local_retention,
            "mariadb_cluster_name": mariadb_cluster_name,
            "redis_memory_limit": redis_memory_limit,
            "mariadb_version": mariadb_version,
            "postgresql_version": postgresql_version,
            "nodejs_version": nodejs_version,
            "nodejs_versions": nodejs_versions,
            "custom_php_modules_names": custom_php_modules_names,
            "php_settings": php_settings,
            "automatic_borg_repositories_prune_enabled": automatic_borg_repositories_prune_enabled,
            "php_ioncube_enabled": php_ioncube_enabled,
            "meilisearch_master_key": meilisearch_master_key,
            "meilisearch_environment": meilisearch_environment,
            "meilisearch_backup_interval": meilisearch_backup_interval,
            "new_relic_apm_license_key": new_relic_apm_license_key,
            "new_relic_mariadb_password": new_relic_mariadb_password,
            "new_relic_infrastructure_license_key": new_relic_infrastructure_license_key,
            "php_sessions_spread_enabled": php_sessions_spread_enabled,
            "http_retry_properties": http_retry_properties,
            "customer_id": customer_id,
            "kernelcare_license_key": kernelcare_license_key,
            "grafana_domain": grafana_domain,
            "singlestore_studio_domain": singlestore_studio_domain,
            "singlestore_api_domain": singlestore_api_domain,
            "singlestore_root_password": singlestore_root_password,
            "elasticsearch_default_users_password": elasticsearch_default_users_password,
            "rabbitmq_erlang_cookie": rabbitmq_erlang_cookie,
            "rabbitmq_admin_password": rabbitmq_admin_password,
            "singlestore_license_key": singlestore_license_key,
            "metabase_domain": metabase_domain,
            "metabase_database_password": metabase_database_password,
            "kibana_domain": kibana_domain,
            "rabbitmq_management_domain": rabbitmq_management_domain,
            "wordpress_toolkit_enabled": wordpress_toolkit_enabled,
            "sync_toolkit_enabled": sync_toolkit_enabled,
            "bubblewrap_toolkit_enabled": bubblewrap_toolkit_enabled,
            "automatic_upgrades_enabled": automatic_upgrades_enabled,
            "firewall_rules_external_providers_enabled": firewall_rules_external_providers_enabled,
            "database_toolkit_enabled": database_toolkit_enabled,
            "description": description,
            "site_id": site_id,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.clusters.append(self)

        return obj

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "groups": self.groups,
            "unix_users_home_directory": self.unix_users_home_directory,
            "php_versions": self.php_versions,
            "redis_password": self.redis_password,
            "postgresql_backup_interval": self.postgresql_backup_interval,
            "mariadb_backup_interval": self.mariadb_backup_interval,
            "mariadb_backup_local_retention": self.mariadb_backup_local_retention,
            "postgresql_backup_local_retention": self.postgresql_backup_local_retention,
            "meilisearch_backup_local_retention": self.meilisearch_backup_local_retention,
            "mariadb_cluster_name": self.mariadb_cluster_name,
            "redis_memory_limit": self.redis_memory_limit,
            "mariadb_version": self.mariadb_version,
            "postgresql_version": self.postgresql_version,
            "nodejs_version": self.nodejs_version,
            "nodejs_versions": self.nodejs_versions,
            "custom_php_modules_names": self.custom_php_modules_names,
            "php_settings": self.php_settings,
            "automatic_borg_repositories_prune_enabled": self.automatic_borg_repositories_prune_enabled,
            "php_ioncube_enabled": self.php_ioncube_enabled,
            "meilisearch_master_key": self.meilisearch_master_key,
            "meilisearch_environment": self.meilisearch_environment,
            "meilisearch_backup_interval": self.meilisearch_backup_interval,
            "new_relic_apm_license_key": self.new_relic_apm_license_key,
            "new_relic_mariadb_password": self.new_relic_mariadb_password,
            "new_relic_infrastructure_license_key": self.new_relic_infrastructure_license_key,
            "php_sessions_spread_enabled": self.php_sessions_spread_enabled,
            "http_retry_properties": self.http_retry_properties,
            "customer_id": self.customer_id,
            "kernelcare_license_key": self.kernelcare_license_key,
            "grafana_domain": self.grafana_domain,
            "singlestore_studio_domain": self.singlestore_studio_domain,
            "singlestore_api_domain": self.singlestore_api_domain,
            "singlestore_root_password": self.singlestore_root_password,
            "elasticsearch_default_users_password": self.elasticsearch_default_users_password,
            "rabbitmq_erlang_cookie": self.rabbitmq_erlang_cookie,
            "rabbitmq_admin_password": self.rabbitmq_admin_password,
            "singlestore_license_key": self.singlestore_license_key,
            "metabase_domain": self.metabase_domain,
            "metabase_database_password": self.metabase_database_password,
            "kibana_domain": self.kibana_domain,
            "rabbitmq_management_domain": self.rabbitmq_management_domain,
            "wordpress_toolkit_enabled": self.wordpress_toolkit_enabled,
            "sync_toolkit_enabled": self.sync_toolkit_enabled,
            "bubblewrap_toolkit_enabled": self.bubblewrap_toolkit_enabled,
            "automatic_upgrades_enabled": self.automatic_upgrades_enabled,
            "firewall_rules_external_providers_enabled": self.firewall_rules_external_providers_enabled,
            "database_toolkit_enabled": self.database_toolkit_enabled,
            "description": self.description,
            "site_id": self.site_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.clusters.remove(self)

    def get_borg_public_ssh_key(self) -> str:
        """Get Borg public SSH key."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}/borg-ssh-key"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response["public_key"]

    def get_common_properties(self) -> dict[str, Any]:
        """Get common properties."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/common-properties"

        self.support.request.GET(url)

        return self.support.request.execute()

    def get_ip_addresses(self) -> dict[str, Any]:
        """Get IP addresses."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}/ip-addresses"

        self.support.request.GET(url)

        return self.support.request.execute()

    def create_ip_address(
        self,
        *,
        service_account_name: str,
        dns_name: str,
        address_family: IPAddressFamily,
    ) -> TaskCollection:
        """Create IP address."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}/ip-addresses"
        data = {
            "service_account_name": service_account_name,
            "dns_name": dns_name,
            "address_family": address_family,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def delete_ip_address(self, ip_address: str) -> TaskCollection:
        """Delete IP address."""
        url = f"/api/v1/{ENDPOINT_CLUSTERS}/{self.id}/ip-addresses/{ip_address}"

        self.support.request.DELETE(url)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
