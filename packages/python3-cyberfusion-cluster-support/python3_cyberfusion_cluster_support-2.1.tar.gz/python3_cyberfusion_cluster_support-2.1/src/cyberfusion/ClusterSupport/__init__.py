"""Helper classes for scripts for cluster support packages.

We use cached_property for objects that are retrieved from GETs without parameters.

We do not use cached_property for objects that are retrieved from GETs with
parameters as these require arguments.
"""

import configparser
import hashlib
import json
import os
import pwd
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union
from urllib.parse import urlparse

from cached_property import cached_property
from rich.table import Table

from cyberfusion.ClusterApiCli import ClusterApiRequest
from cyberfusion.ClusterSupport._interfaces import APIObjectInterface
from cyberfusion.ClusterSupport.api_keys import ENDPOINT_API_KEYS, APIKey
from cyberfusion.ClusterSupport.api_users import ENDPOINT_API_USERS, APIUser
from cyberfusion.ClusterSupport.api_users_to_clusters import (
    ENDPOINT_API_USERS_TO_CLUSTERS,
    APIUserToCluster,
)
from cyberfusion.ClusterSupport.basic_authentication_realms import (
    ENDPOINT_BASIC_AUTHENTICATION_REALMS,
    MODEL_BASIC_AUTHENTICATION_REALMS,
    BasicAuthenticationRealm,
)
from cyberfusion.ClusterSupport.borg_archive_contents import BorgArchiveContent
from cyberfusion.ClusterSupport.borg_archives import (
    ENDPOINT_BORG_ARCHIVES,
    MODEL_BORG_ARCHIVES,
    BorgArchive,
)
from cyberfusion.ClusterSupport.borg_repositories import (
    ENDPOINT_BORG_REPOSITORIES,
    MODEL_BORG_REPOSITORIES,
    BorgRepository,
)
from cyberfusion.ClusterSupport.certificate_managers import (
    ENDPOINT_CERTIFICATE_MANAGERS,
    MODEL_CERTIFICATE_MANAGERS,
    CertificateManager,
)
from cyberfusion.ClusterSupport.certificates import (
    ENDPOINT_CERTIFICATES,
    MODEL_CERTIFICATES,
    Certificate,
)
from cyberfusion.ClusterSupport.cluster_ip_addresses_products import (
    ENDPOINT_CLUSTER_IP_ADDRESSES_PRODUCTS,
    ClusterIPAddressProduct,
)
from cyberfusion.ClusterSupport.clusters import ENDPOINT_CLUSTERS, Cluster
from cyberfusion.ClusterSupport.clusters_cephfs_credentials import (
    ClusterCephFSCredentials,
)
from cyberfusion.ClusterSupport.clusters_rabbitmq_credentials import (
    ClusterRabbitMQCredentials,
)
from cyberfusion.ClusterSupport.cmses import CMS, ENDPOINT_CMSES, MODEL_CMSES
from cyberfusion.ClusterSupport.crons import ENDPOINT_CRONS, MODEL_CRONS, Cron
from cyberfusion.ClusterSupport.custom_config_snippets import (
    ENDPOINT_CUSTOM_CONFIG_SNIPPETS,
    MODEL_CUSTOM_CONFIG_SNIPPETS,
    CustomConfigSnippet,
)
from cyberfusion.ClusterSupport.custom_configs import (
    ENDPOINT_CUSTOM_CONFIGS,
    MODEL_CUSTOM_CONFIGS,
    CustomConfig,
)
from cyberfusion.ClusterSupport.customer_ip_addresses_products import (
    ENDPOINT_CUSTOMER_IP_ADDRESSES_PRODUCTS,
    CustomerIPAddressProduct,
)
from cyberfusion.ClusterSupport.customers import ENDPOINT_CUSTOMERS, Customer
from cyberfusion.ClusterSupport.daemons import (
    ENDPOINT_DAEMONS,
    MODEL_DAEMONS,
    Daemon,
)
from cyberfusion.ClusterSupport.database_user_grants import (
    ENDPOINT_DATABASE_USER_GRANTS,
    MODEL_DATABASE_USER_GRANTS,
    DatabaseUserGrant,
)
from cyberfusion.ClusterSupport.database_users import (
    ENDPOINT_DATABASE_USERS,
    MODEL_DATABASE_USERS,
    DatabaseUser,
)
from cyberfusion.ClusterSupport.databases import (
    ENDPOINT_DATABASES,
    MODEL_DATABASES,
    Database,
)
from cyberfusion.ClusterSupport.databases_usages import (
    ENDPOINT_DATABASES_USAGES,
    DatabaseUsage,
)
from cyberfusion.ClusterSupport.domain_routers import (
    ENDPOINT_DOMAIN_ROUTERS,
    MODEL_DOMAIN_ROUTERS,
    DomainRouter,
)
from cyberfusion.ClusterSupport.exceptions import (
    ClusterIDNotSetException,
    ClusterInaccessibleException,
)
from cyberfusion.ClusterSupport.firewall_groups import (
    ENDPOINT_FIREWALL_GROUPS,
    MODEL_FIREWALL_GROUPS,
    FirewallGroup,
)
from cyberfusion.ClusterSupport.firewall_rules import (
    ENDPOINT_FIREWALL_RULES,
    MODEL_FIREWALL_RULES,
    FirewallRule,
)
from cyberfusion.ClusterSupport.fpm_pools import (
    ENDPOINT_FPM_POOLS,
    MODEL_FPM_POOLS,
    FPMPool,
)
from cyberfusion.ClusterSupport.ftp_users import (
    ENDPOINT_FTP_USERS,
    MODEL_FTP_USERS,
    FTPUser,
)
from cyberfusion.ClusterSupport.haproxy_listens import (
    ENDPOINT_HAPROXY_LISTENS,
    MODEL_HAPROXY_LISTENS,
    HAProxyListen,
)
from cyberfusion.ClusterSupport.haproxy_listens_to_nodes import (
    ENDPOINT_HAPROXY_LISTENS_TO_NODES,
    MODEL_HAPROXY_LISTENS_TO_NODES,
    HAProxyListenToNode,
)
from cyberfusion.ClusterSupport.hosts_entries import (
    ENDPOINT_HOSTS_ENTRIES,
    MODEL_HOSTS_ENTRIES,
    HostsEntry,
)
from cyberfusion.ClusterSupport.htpasswd_files import (
    ENDPOINT_HTPASSWD_FILES,
    MODEL_HTPASSWD_FILES,
    HtpasswdFile,
)
from cyberfusion.ClusterSupport.htpasswd_users import (
    ENDPOINT_HTPASSWD_USERS,
    MODEL_HTPASSWD_USERS,
    HtpasswdUser,
)
from cyberfusion.ClusterSupport.logs import (
    ENDPOINT_ACCESS_LOGS,
    ENDPOINT_ERROR_LOGS,
    AccessLog,
    ErrorLog,
)
from cyberfusion.ClusterSupport.mail_accounts import (
    ENDPOINT_MAIL_ACCOUNTS,
    MODEL_MAIL_ACCOUNTS,
    MailAccount,
)
from cyberfusion.ClusterSupport.mail_accounts_usages import (
    ENDPOINT_MAIL_ACCOUNTS_USAGES,
    MailAccountUsage,
)
from cyberfusion.ClusterSupport.mail_aliases import (
    ENDPOINT_MAIL_ALIASES,
    MODEL_MAIL_ALIASES,
    MailAlias,
)
from cyberfusion.ClusterSupport.mail_domains import (
    ENDPOINT_MAIL_DOMAINS,
    MODEL_MAIL_DOMAINS,
    MailDomain,
)
from cyberfusion.ClusterSupport.mail_hostnames import (
    ENDPOINT_MAIL_HOSTNAMES,
    MODEL_MAIL_HOSTNAMES,
    MailHostname,
)
from cyberfusion.ClusterSupport.malwares import (
    ENDPOINT_MALWARES,
    MODEL_MALWARES,
    Malware,
)
from cyberfusion.ClusterSupport.mariadb_encryption_keys import (
    ENDPOINT_MARIADB_ENCRYPTION_KEYS,
    MODEL_MARIADB_ENCRYPTION_KEYS,
    MariaDBEncryptionKey,
)
from cyberfusion.ClusterSupport.node_add_ons import (
    ENDPOINT_NODE_ADD_ONS,
    MODEL_NODE_ADD_ONS,
    NodeAddOn,
)
from cyberfusion.ClusterSupport.node_add_ons_products import (
    ENDPOINT_NODE_ADD_ONS_PRODUCTS,
    NodeAddOnProduct,
)
from cyberfusion.ClusterSupport.nodes import ENDPOINT_NODES, MODEL_NODES, Node
from cyberfusion.ClusterSupport.nodes_products import (
    ENDPOINT_NODES_PRODUCTS,
    NodeProduct,
)
from cyberfusion.ClusterSupport.passenger_apps import (
    ENDPOINT_PASSENGER_APPS,
    MODEL_PASSENGER_APPS,
    PassengerApp,
)
from cyberfusion.ClusterSupport.redis_instances import (
    ENDPOINT_REDIS_INSTANCES,
    MODEL_REDIS_INSTANCES,
    RedisInstance,
)
from cyberfusion.ClusterSupport.root_ssh_keys import (
    ENDPOINT_ROOT_SSH_KEYS,
    MODEL_ROOT_SSH_KEYS,
    RootSSHKey,
)
from cyberfusion.ClusterSupport.security_txt_policies import (
    ENDPOINT_SECURITY_TXT_POLICIES,
    MODEL_SECURITY_TXT_POLICIES,
    SecurityTXTPolicy,
)
from cyberfusion.ClusterSupport.service_account_servers import (
    ENDPOINT_SERVICE_ACCOUNT_SERVERS,
    ServiceAccountServer,
)
from cyberfusion.ClusterSupport.service_accounts import (
    ENDPOINT_SERVICE_ACCOUNTS,
    ServiceAccount,
)
from cyberfusion.ClusterSupport.service_accounts_to_clusters import (
    ENDPOINT_SERVICE_ACCOUNTS_TO_CLUSTERS,
    ServiceAccountToCluster,
)
from cyberfusion.ClusterSupport.service_accounts_to_customers import (
    ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS,
    ServiceAccountToCustomer,
)
from cyberfusion.ClusterSupport.sites import ENDPOINT_SITES, Site
from cyberfusion.ClusterSupport.sites_to_customers import (
    ENDPOINT_SITES_TO_CUSTOMERS,
    SiteToCustomer,
)
from cyberfusion.ClusterSupport.ssh_keys import (
    ENDPOINT_SSH_KEYS,
    MODEL_SSH_KEYS,
    SSHKey,
)
from cyberfusion.ClusterSupport.task_collection_results import (
    TaskCollectionResult,
)
from cyberfusion.ClusterSupport.task_collections import (
    ENDPOINT_TASK_COLLECTIONS,
)
from cyberfusion.ClusterSupport.tombstones import (
    ENDPOINT_TOMBSTONES,
    MODEL_TOMBSTONES,
    Tombstone,
)
from cyberfusion.ClusterSupport.unix_users import (
    ENDPOINT_UNIX_USERS,
    MODEL_UNIX_USERS,
    UNIXUser,
)
from cyberfusion.ClusterSupport.unix_users_home_directories_usages import (
    ENDPOINT_UNIX_USERS_HOME_DIRECTORIES_USAGES,
    UNIXUsersHomeDirectoryUsage,
)
from cyberfusion.ClusterSupport.unix_users_rabbitmq_credentials import (
    ENDPOINT_UNIX_USERS_RABBITMQ_CREDENTIALS,
    MODEL_UNIX_USERS_RABBITMQ_CREDENTIALS,
    UNIXUserRabbitMQCredentials,
)
from cyberfusion.ClusterSupport.unix_users_usages import (
    ENDPOINT_UNIX_USERS_USAGES,
    UNIXUserUsage,
)
from cyberfusion.ClusterSupport.url_redirects import (
    ENDPOINT_URL_REDIRECTS,
    MODEL_URL_REDIRECTS,
    URLRedirect,
)
from cyberfusion.ClusterSupport.virtual_hosts import (
    ENDPOINT_VIRTUAL_HOSTS,
    MODEL_VIRTUAL_HOSTS,
    VirtualHost,
)
from cyberfusion.Common import find_executable, get_hostname
from cyberfusion.Common.Config import CyberfusionConfig

ENDPOINTS_USAGES = [
    ENDPOINT_MAIL_ACCOUNTS_USAGES,
    ENDPOINT_UNIX_USERS_USAGES,
    ENDPOINT_DATABASES_USAGES,
    ENDPOINT_UNIX_USERS_HOME_DIRECTORIES_USAGES,
]
ENDPOINTS_LOGS = [ENDPOINT_ERROR_LOGS, ENDPOINT_ACCESS_LOGS]

# Sentinel value to load all objects when `clusterid` is set in config file, which
# is used when `cluster_ids` is None. An instance of `object` is truthy.

ALL_CLUSTERS = TypeVar("ALL_CLUSTERS")


class SortOrder(str, Enum):
    """Sort orders."""

    ASCENDING: str = "ASC"
    DESCENDING: str = "DESC"


class TimeUnit(str, Enum):
    """Time units."""

    HOURLY: str = "hourly"
    DAILY: str = "daily"
    WEEKLY: str = "weekly"
    MONTHLY: str = "monthly"


class ClusterSupport:
    """Helper class for retrieving API objects."""

    DIRECTORY_SYSTEMD_OVERRIDE = os.path.join(os.path.sep, "etc", "systemd", "system")

    TABLE_ITEMS_AMOUNT_NON_DETAILED = 5

    PYTHON3_BIN = find_executable("python3")

    USERNAME_ROOT = "root"

    def __init__(
        self,
        *,
        config_file_path: Optional[str] = None,
        cluster_ids: Optional[Union[List[int], ALL_CLUSTERS]] = None,
    ) -> None:
        """Prepare by setting attributes and calling function to set objects.

        'cluster_ids' may be specified to override used clusters.
        """
        self._config_file_path = config_file_path
        self._clusters_children: Optional[Any] = None

        self._preset_cluster_ids = cluster_ids
        self._check_cluster_ids()

    def get_hash(self, objects: List[APIObjectInterface]) -> str:
        """Get MD5 hash for list of API objects."""
        return hashlib.md5(
            json.dumps([object_.json_body for object_ in objects]).encode()
        ).hexdigest()

    def set_clusters_children(self) -> None:
        """Get children of all clusters that API user has access to.

        Call this function to not load objects on attribute access, but all at
        once. This prevents race conditions, such as the following:

        - Domain router has relationship to certificate.
        - Certificates are loaded on attribute access.
        - New certificate is created in Core API, and relationship on domain
          router is updated. The new certificate does not exist locally, as objects
          were already loaded.
        - Domain routers are loaded. The related certificate cannot be found, as
          it does not exist locally.
        """
        self._clusters_children = self.get_data("api-users/clusters-children")

    @cached_property
    def request(self) -> ClusterApiRequest:
        """Get Core API request."""
        return ClusterApiRequest(config_file_path=self._config_file_path)

    @property
    def root_home_directory(self) -> str:
        """Home directory of root user."""
        return pwd.getpwnam(self.USERNAME_ROOT).pw_dir

    @property
    def root_ssh_directory(self) -> str:
        """SSH directory of root user."""
        return os.path.join(self.root_home_directory, ".ssh")

    @cached_property
    def clusters(self) -> List[Cluster]:
        """Get object(s) from API."""
        return self._get_objects(Cluster, ENDPOINT_CLUSTERS)

    @cached_property
    def nodes(self) -> List[Node]:
        """Get object(s) from API."""
        return self._get_objects(Node, ENDPOINT_NODES, MODEL_NODES)

    @cached_property
    def node_add_ons(self) -> List[Node]:
        """Get object(s) from API."""
        return self._get_objects(NodeAddOn, ENDPOINT_NODE_ADD_ONS, MODEL_NODE_ADD_ONS)

    def get_current_node(self) -> Optional[Node]:
        """Get Node object for node we're running on."""
        try:
            return self.get_nodes(hostname=self.hostname)[0]
        except IndexError:
            # Not running on node

            return None

    def get_support_cluster(self) -> Optional[Cluster]:
        """Get cluster object for first specified cluster ID."""
        if not self.cluster_ids:
            return None

        if len(self.cluster_ids) != 1:
            raise ClusterIDNotSetException(
                "Can only get support cluster when one cluster ID is set"
            )

        return self.get_clusters(id_=self.cluster_ids[0])[0]

    @cached_property
    def node_groups(self) -> Optional[List[str]]:
        """Get groups of current node."""
        current_node = self.get_current_node()

        if not current_node:
            return None

        return current_node.groups

    @cached_property
    def node_id(self) -> Optional[str]:
        """Get ID of current node."""
        current_node = self.get_current_node()

        if not current_node:
            return None

        return current_node.id

    @cached_property
    def cluster_groups(self) -> Optional[List[str]]:
        """Get groups of specified support cluster."""
        support_cluster = self.get_support_cluster()

        if not support_cluster:
            return None

        return support_cluster.groups

    def _get_object(
        self,
        model: APIObjectInterface,
        endpoint: str,
        *,
        data: Optional[dict] = None,
    ) -> APIObjectInterface:
        """Get object from API."""
        response = self.get_data(endpoint, data)

        if "cluster_id" in response:
            if not self._has_cluster_id(response["cluster_id"]):
                raise ClusterInaccessibleException

        obj = model._build(self, response)

        return obj

    def _get_objects(
        self,
        model: APIObjectInterface,
        endpoint: str,
        model_name: Optional[str] = None,
        *,
        data: Optional[dict] = None,
    ) -> List[APIObjectInterface]:
        """Get objects from API."""
        objects: List[APIObjectInterface] = []

        if model_name is not None and self._clusters_children is not None:
            response = self._clusters_children[model_name]

            response = sorted(response, key=lambda d: d["id"])  # Sort ascending by ID
        else:
            response = self.get_data(
                endpoint, data
            )  # _execute_cluster_api_call sorts ascending by ID

        for object_ in response:
            if "cluster_id" in object_:
                if not self._has_cluster_id(object_["cluster_id"]):
                    continue

            obj = model._build(self, object_)

            objects.append(obj)

        return objects

    @cached_property
    def cmses(self) -> List[CMS]:
        """Get object(s) from API."""
        return self._get_objects(CMS, ENDPOINT_CMSES, MODEL_CMSES)

    @cached_property
    def custom_configs(self) -> List[CustomConfig]:
        """Get object(s) from API."""
        return self._get_objects(
            CustomConfig, ENDPOINT_CUSTOM_CONFIGS, MODEL_CUSTOM_CONFIGS
        )

    @cached_property
    def certificates(self) -> List[Certificate]:
        """Get object(s) from API."""
        return self._get_objects(Certificate, ENDPOINT_CERTIFICATES, MODEL_CERTIFICATES)

    @cached_property
    def certificate_managers(self) -> List[CertificateManager]:
        """Get object(s) from API."""
        return self._get_objects(
            CertificateManager,
            ENDPOINT_CERTIFICATE_MANAGERS,
            MODEL_CERTIFICATE_MANAGERS,
        )

    @cached_property
    def domain_routers(self) -> List[DomainRouter]:
        """Get object(s) from API."""
        return self._get_objects(
            DomainRouter, ENDPOINT_DOMAIN_ROUTERS, MODEL_DOMAIN_ROUTERS
        )

    @cached_property
    def api_keys(self) -> List[APIKey]:
        """Get object(s) from API."""
        return self._get_objects(APIKey, ENDPOINT_API_KEYS)

    @cached_property
    def virtual_hosts(self) -> List[VirtualHost]:
        """Get object(s) from API."""
        return self._get_objects(
            VirtualHost, ENDPOINT_VIRTUAL_HOSTS, MODEL_VIRTUAL_HOSTS
        )

    @cached_property
    def url_redirects(self) -> List[URLRedirect]:
        """Get object(s) from API."""
        return self._get_objects(
            URLRedirect, ENDPOINT_URL_REDIRECTS, MODEL_URL_REDIRECTS
        )

    @cached_property
    def mail_domains(self) -> List[MailDomain]:
        """Get object(s) from API."""
        return self._get_objects(MailDomain, ENDPOINT_MAIL_DOMAINS, MODEL_MAIL_DOMAINS)

    @cached_property
    def mail_aliases(self) -> List[MailAlias]:
        """Get object(s) from API."""
        return self._get_objects(MailAlias, ENDPOINT_MAIL_ALIASES, MODEL_MAIL_ALIASES)

    @cached_property
    def mail_accounts(self) -> List[MailAccount]:
        """Get object(s) from API."""
        return self._get_objects(
            MailAccount, ENDPOINT_MAIL_ACCOUNTS, MODEL_MAIL_ACCOUNTS
        )

    @cached_property
    def unix_users(self) -> List[UNIXUser]:
        """Get object(s) from API."""
        return self._get_objects(UNIXUser, ENDPOINT_UNIX_USERS, MODEL_UNIX_USERS)

    @cached_property
    def ftp_users(self) -> List[FTPUser]:
        """Get object(s) from API."""
        return self._get_objects(FTPUser, ENDPOINT_FTP_USERS, MODEL_FTP_USERS)

    @cached_property
    def fpm_pools(self) -> List[FPMPool]:
        """Get object(s) from API."""
        return self._get_objects(FPMPool, ENDPOINT_FPM_POOLS, MODEL_FPM_POOLS)

    @cached_property
    def sites(self) -> List[Site]:
        """Get object(s) from API."""
        return self._get_objects(Site, ENDPOINT_SITES)

    @cached_property
    def customers(self) -> List[Customer]:
        """Get object(s) from API."""
        return self._get_objects(Customer, ENDPOINT_CUSTOMERS)

    @cached_property
    def custom_config_snippets(self) -> List[CustomConfigSnippet]:
        """Get object(s) from API."""
        return self._get_objects(
            CustomConfigSnippet,
            ENDPOINT_CUSTOM_CONFIG_SNIPPETS,
            MODEL_CUSTOM_CONFIG_SNIPPETS,
        )

    @cached_property
    def firewall_groups(self) -> List[CustomConfigSnippet]:
        """Get object(s) from API."""
        return self._get_objects(
            FirewallGroup, ENDPOINT_FIREWALL_GROUPS, MODEL_FIREWALL_GROUPS
        )

    @cached_property
    def firewall_rules(self) -> List[CustomConfigSnippet]:
        """Get object(s) from API."""
        return self._get_objects(
            FirewallRule, ENDPOINT_FIREWALL_RULES, MODEL_FIREWALL_RULES
        )

    @cached_property
    def tombstones(self) -> List[Tombstone]:
        """Get object(s) from API."""
        return self._get_objects(Tombstone, ENDPOINT_TOMBSTONES, MODEL_TOMBSTONES)

    @cached_property
    def redis_instances(self) -> List[RedisInstance]:
        """Get object(s) from API."""
        return self._get_objects(
            RedisInstance, ENDPOINT_REDIS_INSTANCES, MODEL_REDIS_INSTANCES
        )

    @cached_property
    def mail_hostnames(self) -> List[MailHostname]:
        """Get object(s) from API."""
        return self._get_objects(
            MailHostname, ENDPOINT_MAIL_HOSTNAMES, MODEL_MAIL_HOSTNAMES
        )

    @cached_property
    def passenger_apps(self) -> List[PassengerApp]:
        """Get object(s) from API."""
        return self._get_objects(
            PassengerApp, ENDPOINT_PASSENGER_APPS, MODEL_PASSENGER_APPS
        )

    @cached_property
    def daemons(self) -> List[Daemon]:
        """Get object(s) from API."""
        return self._get_objects(Daemon, ENDPOINT_DAEMONS, MODEL_DAEMONS)

    @cached_property
    def ssh_keys(self) -> List[SSHKey]:
        """Get object(s) from API."""
        return self._get_objects(SSHKey, ENDPOINT_SSH_KEYS, MODEL_SSH_KEYS)

    @cached_property
    def root_ssh_keys(self) -> List[RootSSHKey]:
        """Get object(s) from API."""
        return self._get_objects(
            RootSSHKey, ENDPOINT_ROOT_SSH_KEYS, MODEL_ROOT_SSH_KEYS
        )

    @cached_property
    def malwares(self) -> List[Malware]:
        """Get object(s) from API."""
        return self._get_objects(Malware, ENDPOINT_MALWARES, MODEL_MALWARES)

    @cached_property
    def crons(self) -> List[Cron]:
        """Get object(s) from API."""
        return self._get_objects(Cron, ENDPOINT_CRONS, MODEL_CRONS)

    @cached_property
    def customer_ip_addresses_products(self) -> List[CustomerIPAddressProduct]:
        """Get object(s) from API."""
        return self._get_objects(
            CustomerIPAddressProduct,
            ENDPOINT_CUSTOMER_IP_ADDRESSES_PRODUCTS,
        )

    @cached_property
    def cluster_ip_addresses_products(self) -> List[ClusterIPAddressProduct]:
        """Get object(s) from API."""
        return self._get_objects(
            ClusterIPAddressProduct,
            ENDPOINT_CLUSTER_IP_ADDRESSES_PRODUCTS,
        )

    @cached_property
    def nodes_products(self) -> List[NodeProduct]:
        """Get object(s) from API."""
        return self._get_objects(
            NodeProduct,
            ENDPOINT_NODES_PRODUCTS,
        )

    @cached_property
    def node_add_ons_products(self) -> List[NodeAddOnProduct]:
        """Get object(s) from API."""
        return self._get_objects(
            NodeAddOnProduct,
            ENDPOINT_NODE_ADD_ONS_PRODUCTS,
        )

    @cached_property
    def mariadb_encryption_keys(self) -> List[MariaDBEncryptionKey]:
        """Get object(s) from API."""
        return self._get_objects(
            MariaDBEncryptionKey,
            ENDPOINT_MARIADB_ENCRYPTION_KEYS,
            MODEL_MARIADB_ENCRYPTION_KEYS,
        )

    @cached_property
    def hosts_entries(self) -> List[HostsEntry]:
        """Get object(s) from API."""
        return self._get_objects(
            HostsEntry, ENDPOINT_HOSTS_ENTRIES, MODEL_HOSTS_ENTRIES
        )

    @cached_property
    def security_txt_policies(self) -> List[SecurityTXTPolicy]:
        """Get object(s) from API."""
        return self._get_objects(
            SecurityTXTPolicy,
            ENDPOINT_SECURITY_TXT_POLICIES,
            MODEL_SECURITY_TXT_POLICIES,
        )

    @cached_property
    def haproxy_listens(self) -> List[HAProxyListen]:
        """Get object(s) from API."""
        return self._get_objects(
            HAProxyListen, ENDPOINT_HAPROXY_LISTENS, MODEL_HAPROXY_LISTENS
        )

    @cached_property
    def haproxy_listens_to_nodes(self) -> List[HAProxyListenToNode]:
        """Get object(s) from API."""
        return self._get_objects(
            HAProxyListenToNode,
            ENDPOINT_HAPROXY_LISTENS_TO_NODES,
            MODEL_HAPROXY_LISTENS_TO_NODES,
        )

    @cached_property
    def htpasswd_files(self) -> List[HtpasswdFile]:
        """Get object(s) from API."""
        return self._get_objects(
            HtpasswdFile, ENDPOINT_HTPASSWD_FILES, MODEL_HTPASSWD_FILES
        )

    @cached_property
    def htpasswd_users(self) -> List[HtpasswdUser]:
        """Get object(s) from API."""
        return self._get_objects(
            HtpasswdUser, ENDPOINT_HTPASSWD_USERS, MODEL_HTPASSWD_USERS
        )

    @cached_property
    def basic_authentication_realms(self) -> List[BasicAuthenticationRealm]:
        """Get object(s) from API."""
        return self._get_objects(
            BasicAuthenticationRealm,
            ENDPOINT_BASIC_AUTHENTICATION_REALMS,
            MODEL_BASIC_AUTHENTICATION_REALMS,
        )

    @cached_property
    def databases(self) -> List[Database]:
        """Get object(s) from API."""
        return self._get_objects(Database, ENDPOINT_DATABASES, MODEL_DATABASES)

    @cached_property
    def database_users(self) -> List[DatabaseUser]:
        """Get object(s) from API."""
        return self._get_objects(
            DatabaseUser, ENDPOINT_DATABASE_USERS, MODEL_DATABASE_USERS
        )

    @cached_property
    def database_user_grants(self) -> List[DatabaseUserGrant]:
        """Get object(s) from API."""
        return self._get_objects(
            DatabaseUserGrant,
            ENDPOINT_DATABASE_USER_GRANTS,
            MODEL_DATABASE_USER_GRANTS,
        )

    @cached_property
    def borg_repositories(self) -> List[BorgRepository]:
        """Get object(s) from API."""
        return self._get_objects(
            BorgRepository, ENDPOINT_BORG_REPOSITORIES, MODEL_BORG_REPOSITORIES
        )

    @cached_property
    def borg_archives(self) -> List[BorgArchive]:
        """Get object(s) from API."""
        return self._get_objects(
            BorgArchive, ENDPOINT_BORG_ARCHIVES, MODEL_BORG_ARCHIVES
        )

    def borg_archive_contents(
        self, borg_archive_id: int, path: Optional[str]
    ) -> List[BorgArchiveContent]:
        """Get object(s) from API."""
        borg_archive_contents_path = self.get_borg_archives(id_=borg_archive_id)[
            0
        ].get_metadata()["contents_path"]

        objects = self._get_objects(
            BorgArchiveContent,
            ENDPOINT_BORG_ARCHIVES + f"/{borg_archive_id}/contents",
            data={"path": path},
        )

        for object_ in objects:
            object_._relative_path = os.path.relpath(
                path=object_.path, start=borg_archive_contents_path
            )

        return objects

    @cached_property
    def api_users(self) -> List[APIUser]:
        """Get object(s) from API."""
        return self._get_objects(
            APIUser,
            ENDPOINT_API_USERS,
        )

    @cached_property
    def service_accounts(self) -> List[ServiceAccount]:
        """Get object(s) from API."""
        return self._get_objects(
            ServiceAccount,
            ENDPOINT_SERVICE_ACCOUNTS,
        )

    @cached_property
    def service_account_servers(self) -> List[ServiceAccountServer]:
        """Get object(s) from API."""
        return self._get_objects(
            ServiceAccountServer,
            ENDPOINT_SERVICE_ACCOUNT_SERVERS,
        )

    @cached_property
    def api_users_to_clusters(self) -> List[APIUserToCluster]:
        """Get object(s) from API."""
        return self._get_objects(
            APIUserToCluster,
            ENDPOINT_API_USERS_TO_CLUSTERS,
        )

    @cached_property
    def service_accounts_to_clusters(self) -> List[ServiceAccountToCluster]:
        """Get object(s) from API."""
        return self._get_objects(
            ServiceAccountToCluster,
            ENDPOINT_SERVICE_ACCOUNTS_TO_CLUSTERS,
        )

    @cached_property
    def sites_to_customers(self) -> List[ServiceAccountToCluster]:
        """Get object(s) from API."""
        return self._get_objects(SiteToCustomer, ENDPOINT_SITES_TO_CUSTOMERS)

    @cached_property
    def service_accounts_to_customers(self) -> List[ServiceAccountToCustomer]:
        """Get object(s) from API."""
        return self._get_objects(
            ServiceAccountToCustomer,
            ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS,
        )

    def task_collection_results(
        self,
        task_collection_uuid: str,
    ) -> List[TaskCollectionResult]:
        """Get object(s) from API."""
        return self._get_objects(
            TaskCollectionResult,
            ENDPOINT_TASK_COLLECTIONS + f"/{task_collection_uuid}/results",
        )

    @cached_property
    def unix_users_rabbitmq_credentials(
        self,
    ) -> List[UNIXUserRabbitMQCredentials]:
        """Get object(s) from API."""
        return self._get_objects(
            UNIXUserRabbitMQCredentials,
            ENDPOINT_UNIX_USERS_RABBITMQ_CREDENTIALS,
            MODEL_UNIX_USERS_RABBITMQ_CREDENTIALS,
        )

    @lru_cache(maxsize=None)
    def cluster_rabbitmq_credentials(
        self, cluster_id: int
    ) -> ClusterRabbitMQCredentials:
        """Get object(s) from API."""
        return self._get_object(
            ClusterRabbitMQCredentials,
            ENDPOINT_CLUSTERS + f"/{cluster_id}" + "/rabbitmq-credentials",
        )

    @lru_cache(maxsize=None)
    def cluster_cephfs_credentials(self, cluster_id: int) -> ClusterCephFSCredentials:
        """Get object(s) from API."""
        return self._get_object(
            ClusterCephFSCredentials,
            ENDPOINT_CLUSTERS + f"/{cluster_id}" + "/cephfs-credentials",
        )

    def access_logs(
        self,
        virtual_host_id: int,
        timestamp: Optional[float] = None,
        limit: Optional[int] = None,
        sort: SortOrder = SortOrder.ASCENDING,
    ) -> List[AccessLog]:
        """Get object(s) from API."""
        return self._get_objects(
            AccessLog,
            ENDPOINT_ACCESS_LOGS + f"/{virtual_host_id}",
            data={
                "timestamp": timestamp,
                "limit": limit,
                "sort": sort.value,
            },
        )

    def error_logs(
        self,
        virtual_host_id: int,
        timestamp: Optional[float] = None,
        limit: Optional[int] = None,
        sort: SortOrder = SortOrder.ASCENDING,
    ) -> List[ErrorLog]:
        """Get object(s) from API."""
        return self._get_objects(
            ErrorLog,
            ENDPOINT_ERROR_LOGS + f"/{virtual_host_id}",
            data={
                "timestamp": timestamp,
                "limit": limit,
                "sort": sort.value,
            },
        )

    def unix_users_home_directory_usages(
        self,
        cluster_id: int,
        timestamp: float,
        time_unit: TimeUnit = TimeUnit.HOURLY,
    ) -> List[UNIXUsersHomeDirectoryUsage]:
        """Get object(s) from API."""
        return self._get_objects(
            UNIXUsersHomeDirectoryUsage,
            ENDPOINT_UNIX_USERS_HOME_DIRECTORIES_USAGES + f"/{cluster_id}",
            data={"timestamp": timestamp, "time_unit": time_unit.value},
        )

    def unix_user_usages(
        self,
        unix_user_id: int,
        timestamp: float,
        time_unit: TimeUnit = TimeUnit.HOURLY,
    ) -> List[UNIXUserUsage]:
        """Get object(s) from API."""
        return self._get_objects(
            UNIXUserUsage,
            ENDPOINT_UNIX_USERS_USAGES + f"/{unix_user_id}",
            data={"timestamp": timestamp, "time_unit": time_unit.value},
        )

    def database_usages(
        self,
        database_id: int,
        timestamp: float,
        time_unit: TimeUnit = TimeUnit.HOURLY,
    ) -> List[DatabaseUsage]:
        """Get object(s) from API."""
        return self._get_objects(
            DatabaseUsage,
            ENDPOINT_DATABASES_USAGES + f"/{database_id}",
            data={"timestamp": timestamp, "time_unit": time_unit.value},
        )

    def mail_account_usages(
        self,
        mail_account_id: int,
        timestamp: float,
        time_unit: TimeUnit = TimeUnit.HOURLY,
    ) -> List[MailAccountUsage]:
        """Get object(s) from API."""
        return self._get_objects(
            MailAccountUsage,
            ENDPOINT_MAIL_ACCOUNTS_USAGES + f"/{mail_account_id}",
            data={"timestamp": timestamp, "time_unit": time_unit.value},
        )

    def _has_cluster_id(self, cluster_id: int) -> bool:
        """Check if any cluster ID on support object matches API object cluster ID.

        The cluster ID on the support object determines whether we want results for
        a certain cluster ID.
        """

        # If cluster IDs are not set, we want objects for all clusters

        if not self.cluster_ids:
            return True

        # If cluster IDs are set but do not have that of the API object, we don't
        # want the object

        if cluster_id not in self.cluster_ids:
            return False

        # If we get here, cluster IDs are set and have the cluster ID of the API
        # object, so we want the object

        return True

    @cached_property
    def _config(self) -> CyberfusionConfig:
        """Get config."""
        return CyberfusionConfig(path=self._config_file_path)

    @cached_property
    def cluster_ids(self) -> Optional[List[int]]:
        """Get cluster IDs.

        See README for ordering.
        """
        if self._preset_cluster_ids is ALL_CLUSTERS:
            return None

        # Use preset cluster IDs if set

        if self._preset_cluster_ids is not None:
            # At this time, we know self._preset_cluster_ids is not ALL_CLUSTERS
            # (early return above) and it is not None. Given its type of Optional[Union[List[int], ALL_CLUSTERS]],
            # that means it can only be a list. However, mypy does not understand this.

            return self._preset_cluster_ids  # type: ignore[return-value]

        # Set cluster IDs from config

        try:
            return [
                int(self._config.get(ClusterApiRequest.SECTION_CONFIG, "clusterid"))
            ]
        except configparser.NoOptionError:
            # Non node clients may not have cluster ID

            pass

        # Set cluster IDs from service accounts to clusters

        if self.service_account_id:
            return [
                object_["cluster_id"]
                for object_ in self._execute_cluster_api_call(
                    ENDPOINT_SERVICE_ACCOUNTS_TO_CLUSTERS
                )
                if object_["service_account_id"] == self.service_account_id
            ]

        return None

    @cached_property
    def username(self) -> str:
        """Get API user username."""
        return self.request.api_user_info.username

    @cached_property
    def customer_id(self) -> Optional[int]:
        """Get API user customer ID."""
        return self.request.api_user_info.customer_id

    @cached_property
    def is_superuser(self) -> bool:
        """Get if API user is superuser."""
        return self.request.api_user_info.is_superuser

    @cached_property
    def service_account_name(self) -> Optional[str]:
        """Get service account name."""
        if not self.service_account_id:
            return None

        service_accounts = self._execute_cluster_api_call(ENDPOINT_SERVICE_ACCOUNTS)

        service_account = next(
            filter(
                lambda obj: obj["id"] == self.service_account_id,
                service_accounts,
            )
        )

        return service_account["name"]

    @cached_property
    def service_account_id(self) -> Optional[int]:
        """Get service account ID."""
        try:
            return int(
                self._config.get(ClusterApiRequest.SECTION_CONFIG, "serviceaccountid")
            )
        except configparser.NoOptionError:
            # Non service account clients may not have service account ID

            return None

    def _check_cluster_ids(self) -> None:
        """Check if API user can access the selected clusters."""
        if not self.cluster_ids:
            return

        for cluster_id in self.cluster_ids:
            if cluster_id in self.accessible_core_api_clusters:
                continue

            raise ClusterInaccessibleException

    @staticmethod
    def _construct_sort_parameter(
        endpoint: str, *, order: SortOrder, property_: Optional[str]
    ) -> Optional[str]:
        """Construct sort parameter for API."""
        if urlparse(endpoint).path.rsplit("/", 1)[0] in ENDPOINTS_USAGES:
            return None

        return f"{property_}:{order.value}"

    @cached_property
    def clusters_common_properties(self) -> dict:
        """Get clusters common properties."""
        return self.get_data("clusters/common-properties")

    def get_data(self, endpoint: str, data: Optional[dict] = None) -> Any:
        """Get data from backend."""
        return self._execute_cluster_api_call(endpoint, data)

    @property
    def accessible_core_api_clusters(self) -> Dict[int, str]:
        """Get clusters that Core API user has access to."""
        result = {}

        clusters = self._execute_cluster_api_call(ENDPOINT_CLUSTERS)

        for cluster_id in self.request.api_user_info.clusters_ids:
            cluster = next(
                filter(lambda cluster: cluster["id"] == cluster_id, clusters)
            )

            result[cluster_id] = cluster["name"]

        return result

    def _execute_cluster_api_call(
        self, endpoint: str, data: Optional[dict] = None
    ) -> Any:
        """Execute Core API call to gather objects."""
        if not data:
            data = {}

        # Add sort parameter if not set already. The API has defaults for sorting;
        # we also set these here for safety

        if "sort" not in data:
            sort_parameter = self._construct_sort_parameter(
                endpoint, order=SortOrder.ASCENDING, property_="id"
            )

            if sort_parameter:
                data["sort"] = sort_parameter

        # Execute and return

        self.request.GET(f"/api/v1/{endpoint}", data)

        return self.request.execute()

    @cached_property
    def hostname(self) -> str:
        """Get local hostname."""
        return get_hostname()

    def _filter_objects(
        self, objects: List[APIObjectInterface], **kwargs: Any
    ) -> List[APIObjectInterface]:
        """Get object from loaded objects.

        If an argument is passed with the value None, it is not filtered on.

        To filter on the 'id' attribute, pass the 'id_' argument.
        """  # noqa: RST306
        result = []

        for obj in objects:
            skip = False

            for k, v in kwargs.items():
                if v is None:
                    continue

                if k == "id_":  # 'id' is built-in Python function
                    k = "id"

                if isinstance(getattr(obj, k), list):
                    match = v in getattr(obj, k)
                else:
                    match = getattr(obj, k) == v

                if not match:
                    skip = True

                    break

            if not skip:
                result.append(obj)

        return result

    def get_clusters(self, **kwargs: Any) -> List[Cluster]:
        """Get object from loaded objects."""
        return self._filter_objects(self.clusters, **kwargs)

    def get_certificates(self, **kwargs: Any) -> List[Certificate]:
        """Get object from loaded objects."""
        return self._filter_objects(self.certificates, **kwargs)

    def get_certificate_managers(self, **kwargs: Any) -> List[CertificateManager]:
        """Get object from loaded objects."""
        return self._filter_objects(self.certificate_managers, **kwargs)

    def get_virtual_hosts(self, **kwargs: Any) -> List[VirtualHost]:
        """Get object from loaded objects."""
        return self._filter_objects(self.virtual_hosts, **kwargs)

    def get_url_redirects(self, **kwargs: Any) -> List[URLRedirect]:
        """Get object from loaded objects."""
        return self._filter_objects(self.url_redirects, **kwargs)

    def get_mail_domains(self, **kwargs: Any) -> List[MailDomain]:
        """Get object from loaded objects."""
        return self._filter_objects(self.mail_domains, **kwargs)

    def get_mail_aliases(self, **kwargs: Any) -> List[MailAlias]:
        """Get object from loaded objects."""
        return self._filter_objects(self.mail_aliases, **kwargs)

    def get_mail_accounts(self, **kwargs: Any) -> List[MailAccount]:
        """Get object from loaded objects."""
        return self._filter_objects(self.mail_accounts, **kwargs)

    def get_nodes(self, **kwargs: Any) -> List[Node]:
        """Get object from loaded objects."""
        return self._filter_objects(self.nodes, **kwargs)

    def get_unix_users(self, **kwargs: Any) -> List[UNIXUser]:
        """Get object from loaded objects."""
        return self._filter_objects(self.unix_users, **kwargs)

    def get_ftp_users(self, **kwargs: Any) -> List[FTPUser]:
        """Get object from loaded objects."""
        return self._filter_objects(self.ftp_users, **kwargs)

    def get_unix_users_rabbitmq_credentials(
        self, **kwargs: Any
    ) -> List[UNIXUserRabbitMQCredentials]:
        """Get object from loaded objects."""
        return self._filter_objects(self.unix_users_rabbitmq_credentials, **kwargs)

    def get_fpm_pools(self, **kwargs: Any) -> List[FPMPool]:
        """Get object from loaded objects."""
        return self._filter_objects(self.fpm_pools, **kwargs)

    def get_sites(self, **kwargs: Any) -> List[Site]:
        """Get object from loaded objects."""
        return self._filter_objects(self.sites, **kwargs)

    def get_customers(self, **kwargs: Any) -> List[Customer]:
        """Get object from loaded objects."""
        return self._filter_objects(self.customers, **kwargs)

    def get_custom_config_snippets(self, **kwargs: Any) -> List[CustomConfigSnippet]:
        """Get object from loaded objects."""
        return self._filter_objects(self.custom_config_snippets, **kwargs)

    def get_firewall_groups(self, **kwargs: Any) -> List[FirewallGroup]:
        """Get object from loaded objects."""
        return self._filter_objects(self.firewall_groups, **kwargs)

    def get_firewall_rules(self, **kwargs: Any) -> List[FirewallRule]:
        """Get object from loaded objects."""
        return self._filter_objects(self.firewall_rules, **kwargs)

    def get_tombstones(self, **kwargs: Any) -> List[Tombstone]:
        """Get object from loaded objects."""
        return self._filter_objects(self.tombstones, **kwargs)

    def get_mail_hostnames(self, **kwargs: Any) -> List[MailHostname]:
        """Get object from loaded objects."""
        return self._filter_objects(self.mail_hostnames, **kwargs)

    def get_passenger_apps(self, **kwargs: Any) -> List[PassengerApp]:
        """Get object from loaded objects."""
        return self._filter_objects(self.passenger_apps, **kwargs)

    def get_redis_instances(self, **kwargs: Any) -> List[RedisInstance]:
        """Get object from loaded objects."""
        return self._filter_objects(self.redis_instances, **kwargs)

    def get_cmses(self, **kwargs: Any) -> List[CMS]:
        """Get object from loaded objects."""
        return self._filter_objects(self.cmses, **kwargs)

    def get_custom_configs(self, **kwargs: Any) -> List[CustomConfig]:
        """Get object from loaded objects."""
        return self._filter_objects(self.custom_configs, **kwargs)

    def get_domain_routers(self, **kwargs: Any) -> List[DomainRouter]:
        """Get object from loaded objects."""
        return self._filter_objects(self.domain_routers, **kwargs)

    def get_api_keys(self, **kwargs: Any) -> List[APIKey]:
        """Get object from loaded objects."""
        return self._filter_objects(self.api_keys, **kwargs)

    def get_ssh_keys(self, **kwargs: Any) -> List[SSHKey]:
        """Get object from loaded objects."""
        return self._filter_objects(self.ssh_keys, **kwargs)

    def get_root_ssh_keys(self, **kwargs: Any) -> List[RootSSHKey]:
        """Get object from loaded objects."""
        return self._filter_objects(self.root_ssh_keys, **kwargs)

    def get_malwares(self, **kwargs: Any) -> List[Malware]:
        """Get object from loaded objects."""
        return self._filter_objects(self.malwares, **kwargs)

    def get_crons(self, **kwargs: Any) -> List[Cron]:
        """Get object from loaded objects."""
        return self._filter_objects(self.crons, **kwargs)

    def get_mariadb_encryption_keys(self, **kwargs: Any) -> List[MariaDBEncryptionKey]:
        """Get object from loaded objects."""
        return self._filter_objects(self.mariadb_encryption_keys, **kwargs)

    def get_hosts_entries(self, **kwargs: Any) -> List[HostsEntry]:
        """Get object from loaded objects."""
        return self._filter_objects(self.hosts_entries, **kwargs)

    def get_security_txt_policies(self, **kwargs: Any) -> List[SecurityTXTPolicy]:
        """Get object from loaded objects."""
        return self._filter_objects(self.security_txt_policies, **kwargs)

    def get_haproxy_listens(self, **kwargs: Any) -> List[HAProxyListen]:
        """Get object from loaded objects."""
        return self._filter_objects(self.haproxy_listens, **kwargs)

    def get_node_add_ons(self, **kwargs: Any) -> List[NodeAddOn]:
        """Get object from loaded objects."""
        return self._filter_objects(self.node_add_ons, **kwargs)

    def get_haproxy_listens_to_nodes(self, **kwargs: Any) -> List[HAProxyListenToNode]:
        """Get object from loaded objects."""
        return self._filter_objects(self.haproxy_listens_to_nodes, **kwargs)

    def get_htpasswd_files(self, **kwargs: Any) -> List[HtpasswdFile]:
        """Get object from loaded objects."""
        return self._filter_objects(self.htpasswd_files, **kwargs)

    def get_basic_authentication_realms(
        self, **kwargs: Any
    ) -> List[BasicAuthenticationRealm]:
        """Get object from loaded objects."""
        return self._filter_objects(self.basic_authentication_realms, **kwargs)

    def get_htpasswd_users(self, **kwargs: Any) -> List[HtpasswdUser]:
        """Get object from loaded objects."""
        return self._filter_objects(self.htpasswd_users, **kwargs)

    def get_databases(self, **kwargs: Any) -> List[Database]:
        """Get object from loaded objects."""
        return self._filter_objects(self.databases, **kwargs)

    def get_database_users(self, **kwargs: Any) -> List[DatabaseUser]:
        """Get object from loaded objects."""
        return self._filter_objects(self.database_users, **kwargs)

    def get_database_user_grants(self, **kwargs: Any) -> List[DatabaseUserGrant]:
        """Get object from loaded objects."""
        return self._filter_objects(self.database_user_grants, **kwargs)

    def get_borg_repositories(self, **kwargs: Any) -> List[BorgRepository]:
        """Get object from loaded objects."""
        return self._filter_objects(self.borg_repositories, **kwargs)

    def get_borg_archives(self, **kwargs: Any) -> List[BorgArchive]:
        """Get object from loaded objects."""
        return self._filter_objects(self.borg_archives, **kwargs)

    def get_api_users(self, **kwargs: Any) -> List[APIUser]:
        """Get object from loaded objects."""
        return self._filter_objects(self.api_users, **kwargs)

    def get_api_users_to_clusters(self, **kwargs: Any) -> List[APIUserToCluster]:
        """Get object from loaded objects."""
        return self._filter_objects(self.api_users_to_clusters, **kwargs)

    def get_service_accounts(self, **kwargs: Any) -> List[ServiceAccount]:
        """Get object from loaded objects."""
        return self._filter_objects(self.service_accounts, **kwargs)

    def get_service_account_servers(self, **kwargs: Any) -> List[ServiceAccountServer]:
        """Get object from loaded objects."""
        return self._filter_objects(self.service_account_servers, **kwargs)

    def get_sites_to_customers(self, **kwargs: Any) -> List[SiteToCustomer]:
        """Get object from loaded objects."""
        return self._filter_objects(self.sites_to_customers, **kwargs)

    def get_service_accounts_to_clusters(
        self, **kwargs: Any
    ) -> List[ServiceAccountToCluster]:
        """Get object from loaded objects."""
        return self._filter_objects(self.service_accounts_to_clusters, **kwargs)

    def get_service_accounts_to_customers(
        self, **kwargs: Any
    ) -> List[ServiceAccountToCustomer]:
        """Get object from loaded objects."""
        return self._filter_objects(self.service_accounts_to_customers, **kwargs)

    def get_daemons(self, **kwargs: Any) -> List[Daemon]:
        """Get object from loaded objects."""
        return self._filter_objects(self.daemons, **kwargs)

    def get_table(
        self,
        *,
        objs: List[APIObjectInterface],
        detailed: bool = False,
        show_lines: bool = True,
    ) -> Union[Table, str]:
        """Get printable table.

        If you only need a single obj, create a list with that single obj.
        """
        if not objs:
            return "No entries found"

        _show_lines = False

        table = Table()

        headers = (
            objs[0]._TABLE_HEADERS + objs[0]._TABLE_HEADERS_DETAILED
            if detailed
            else objs[0]._TABLE_HEADERS
        )

        for header in headers:
            table.add_column(header, overflow="fold")

        for obj in objs:
            fields = []

            attributes = (
                obj._TABLE_FIELDS + obj._TABLE_FIELDS_DETAILED
                if detailed
                else obj._TABLE_FIELDS
            )

            for attribute in attributes:
                value = getattr(obj, attribute)

                if isinstance(value, dict):
                    _value = []

                    for k, v in value.items():
                        _value.append(f"{k}: {v}")

                    value = _value

                if isinstance(value, list):
                    # Toggle lines if not explicitly disabled

                    if show_lines:
                        _show_lines = True

                    if (
                        detailed
                        or not len(value) > self.TABLE_ITEMS_AMOUNT_NON_DETAILED
                    ):
                        fields.append("\n".join(value))
                    else:
                        # Show N list items to avoid too large output

                        fields.append(
                            "\n".join(value[: self.TABLE_ITEMS_AMOUNT_NON_DETAILED])
                            + f"\n[i](Set --detailed for {len(value) - self.TABLE_ITEMS_AMOUNT_NON_DETAILED} more)[/i]"
                        )
                else:
                    fields.append(str(value) if value is not None else "")

            table.add_row(*fields)

        if _show_lines:
            table.show_lines = True

        return table

    def get_comparison_table(
        self,
        *,
        left_column_name: str = "Path",
        right_column_name: str = "Status",
        left_label: str,
        right_label: str,
        identical: List[str],
        different: List[str],
        left_only: List[str],
        right_only: List[str],
        sort_alphabetically: bool = True,
    ) -> Table:
        """Get printable table for comparison."""
        items: List[Tuple[str, str, str]] = []

        for item in identical:
            items.append((item, "Identical", "green"))

        for item in different:
            items.append((item, "Different", "red"))

        for item in left_only:
            items.append((item, f"'{left_label}' only", "yellow"))

        for item in right_only:
            items.append((item, f"'{right_label}' only", "cyan"))

        if sort_alphabetically:
            items.sort(key=lambda item: item[0])

        table = Table()
        table.add_column(left_column_name, overflow="fold")
        table.add_column(right_column_name, overflow="fold")

        for row in items:
            table.add_row(f"[{row[2]}]{row[0]}", f"[{row[2]}]{row[1]}")

        return table
