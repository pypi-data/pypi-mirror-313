"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_VIRTUAL_HOSTS = "virtual-hosts"
MODEL_VIRTUAL_HOSTS = "virtual_hosts"


class VirtualHostServerSoftwareName(str, Enum):
    """Virtual host server software names."""

    APACHE: str = "Apache"
    NGINX: str = "nginx"


class AllowOverrideDirective(str, Enum):
    """AllowOverride directives."""

    ALL: str = "All"
    AUTHCONFIG: str = "AuthConfig"
    FILEINFO: str = "FileInfo"
    INDEXES: str = "Indexes"
    LIMIT: str = "Limit"
    NONE: str = "None"


class AllowOverrideOptionDirective(str, Enum):
    """AllowOverride option directives."""

    ALL: str = "All"
    FOLLOWSYMLINKS: str = "FollowSymLinks"
    INDEXES: str = "Indexes"
    MULTIVIEWS: str = "MultiViews"
    SYMLINKSIFOWNERMATCH: str = "SymLinksIfOwnerMatch"
    NONE: str = "None"


class VirtualHost(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Domain",
        "Server Aliases",
        "UNIX User",
        "Document Root",
        "FPM Pool",
        "Passenger App",
        "Server Software",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Public Root",
        "Custom Config",
        "Allow Override\nDirectives",
        "Allow Override\nOption Directives",
    ]

    _TABLE_FIELDS = [
        "id",
        "domain",
        "server_aliases",
        "_unix_user_username",
        "document_root",
        "_fpm_pool_name",
        "_passenger_app_name",
        "server_software_name",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "public_root",
        "custom_config",
        "allow_override_directives",
        "allow_override_option_directives",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.domain = obj["domain"]
        self.server_aliases = obj["server_aliases"]
        self.unix_user_id = obj["unix_user_id"]
        self.document_root = obj["document_root"]
        self.public_root = obj["public_root"]
        self.fpm_pool_id = obj["fpm_pool_id"]
        self.passenger_app_id = obj["passenger_app_id"]
        self.custom_config = obj["custom_config"]
        self.server_software_name = VirtualHostServerSoftwareName(
            obj["server_software_name"]
        ).value

        self.allow_override_option_directives = None

        if obj["allow_override_option_directives"] is not None:
            self.allow_override_option_directives = [
                AllowOverrideOptionDirective(x).value
                for x in obj["allow_override_option_directives"]
            ]

        self.allow_override_directives = None

        if obj["allow_override_directives"] is not None:
            self.allow_override_directives = [
                AllowOverrideDirective(x).value
                for x in obj["allow_override_directives"]
            ]

        self.domain_root = obj["domain_root"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.server_names = []
        self.server_names.append(self.domain)
        self.server_names.extend(self.server_aliases)

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username
        self._fpm_pool_name = None
        self._passenger_app_name = None

        self.fpm_pool = None
        self.passenger_app = None

        if self.fpm_pool_id:
            self.fpm_pool = self.support.get_fpm_pools(id_=self.fpm_pool_id)[0]
            self._fpm_pool_name = self.fpm_pool.name

        if self.passenger_app_id:
            self.passenger_app = self.support.get_passenger_apps(
                id_=self.passenger_app_id
            )[0]
            self._passenger_app_name = self.passenger_app.name

    def create(
        self,
        *,
        domain: str,
        server_aliases: List[str],
        unix_user_id: int,
        document_root: str,
        public_root: str,
        fpm_pool_id: Optional[int],
        passenger_app_id: Optional[int],
        custom_config: Optional[str],
        server_software_name: VirtualHostServerSoftwareName,
        allow_override_directives: Optional[List[AllowOverrideDirective]],
        allow_override_option_directives: Optional[List[AllowOverrideOptionDirective]],
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_VIRTUAL_HOSTS}"
        data = {
            "domain": domain,
            "server_aliases": server_aliases,
            "unix_user_id": unix_user_id,
            "document_root": document_root,
            "public_root": public_root,
            "fpm_pool_id": fpm_pool_id,
            "passenger_app_id": passenger_app_id,
            "custom_config": custom_config,
            "server_software_name": server_software_name,
            "allow_override_directives": allow_override_directives,
            "allow_override_option_directives": allow_override_option_directives,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.virtual_hosts.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_VIRTUAL_HOSTS}/{self.id}"
        data = {
            "id": self.id,
            "domain": self.domain,
            "server_aliases": self.server_aliases,
            "unix_user_id": self.unix_user_id,
            "document_root": self.document_root,
            "public_root": self.public_root,
            "fpm_pool_id": self.fpm_pool_id,
            "passenger_app_id": self.passenger_app_id,
            "custom_config": self.custom_config,
            "server_software_name": self.server_software_name,
            "allow_override_directives": self.allow_override_directives,
            "allow_override_option_directives": self.allow_override_option_directives,
            "domain_root": self.domain_root,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self, delete_on_cluster: bool = False) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_VIRTUAL_HOSTS}/{self.id}"

        params = {"delete_on_cluster": delete_on_cluster}

        self.support.request.DELETE(url, params)
        self.support.request.execute()

        self.support.virtual_hosts.remove(self)

    def get_document_root_contains_files(self) -> str:
        """Get virtual host document root contains files."""
        url = f"/api/v1/{ENDPOINT_VIRTUAL_HOSTS}/{self.id}/document-root"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response["contains_files"]

    def sync_domain_root(self, *, right_virtual_host_id: int) -> TaskCollection:
        """Sync virtual host domain root."""
        url = f"/api/v1/{ENDPOINT_VIRTUAL_HOSTS}/{self.id}/domain-root/sync"
        data: dict = {}
        params = {"right_virtual_host_id": right_virtual_host_id}

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
