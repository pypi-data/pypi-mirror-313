"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import Dict, List, Optional, Union

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_CMSES = "cmses"
MODEL_CMSES = "cmses"


class CMSSoftwareName(str, Enum):
    """CMS software names."""

    WP: str = "WordPress"
    NEXTCLOUD: str = "NextCloud"


class CMSOptionName(str, Enum):
    """CMS option names."""

    BLOG_PUBLIC: str = "blog_public"


class CMS(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Virtual Host\nDomain",
        "Software Name",
        "Manually Created",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "_virtual_host_domain",
        "software_name",
        "is_manually_created",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED: List[str] = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.software_name = CMSSoftwareName(obj["software_name"]).value
        self.is_manually_created = obj["is_manually_created"]
        self.virtual_host_id = obj["virtual_host_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.virtual_host = self.support.get_virtual_hosts(id_=self.virtual_host_id)[0]
        self._cluster_label = self.cluster._label
        self._virtual_host_domain = self.virtual_host.domain

    def create(
        self,
        *,
        software_name: CMSSoftwareName,
        virtual_host_id: int,
        is_manually_created: bool,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CMSES}"
        data = {
            "software_name": software_name,
            "virtual_host_id": virtual_host_id,
            "is_manually_created": is_manually_created,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.cmses.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.cmses.remove(self)

    def install_wordpress(
        self,
        database_name: str,
        database_user_name: str,
        database_user_password: str,
        database_host: str,
        site_title: str,
        site_url: str,
        locale: str,
        version: str,
        admin_username: str,
        admin_password: str,
        admin_email_address: str,
    ) -> TaskCollection:
        """Install WordPress."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/install/wordpress"
        data = {
            "database_name": database_name,
            "database_user_name": database_user_name,
            "database_user_password": database_user_password,
            "database_host": database_host,
            "site_title": site_title,
            "site_url": site_url,
            "locale": locale,
            "version": version,
            "admin_username": admin_username,
            "admin_password": admin_password,
            "admin_email_address": admin_email_address,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def install_nextcloud(
        self,
        database_name: str,
        database_user_name: str,
        database_user_password: str,
        database_host: str,
        admin_username: str,
        admin_password: str,
    ) -> TaskCollection:
        """Install NextCloud."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/install/nextcloud"
        data = {
            "database_name": database_name,
            "database_user_name": database_user_name,
            "database_user_password": database_user_password,
            "database_host": database_host,
            "admin_username": admin_username,
            "admin_password": admin_password,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def get_one_time_login_url(self) -> str:
        """Get CMS one time login URL."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/one-time-login"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response["url"]

    def update_option(self, *, name: CMSOptionName, value: str) -> dict:
        """Update CMS option."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/options/{name.value}"
        data = {"value": value}

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        return response

    def update_configuration_constant(
        self,
        *,
        name: str,
        value: Union[str, int, float, bool],
        index: Optional[int],
    ) -> dict:
        """Update CMS configuration constant."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/configuration-constants/{name}"
        data = {"value": value, "index": index}

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        return response

    def search_replace(
        self, *, search_string: str, replace_string: str
    ) -> TaskCollection:
        """Search & replace in CMS."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/search-replace"
        data: dict = {}
        params = {
            "search_string": search_string,
            "replace_string": replace_string,
        }

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def regenerate_salts(self) -> None:
        """Regenerate CMS salts."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/regenerate-salts"
        data: dict = {}

        self.support.request.POST(url, data)
        self.support.request.execute()

    def update_user_credentials(self, *, user_id: int, password: str) -> None:
        """Update CMS user credentials."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/users/{user_id}/credentials"
        data = {"password": password}

        self.support.request.PATCH(url, data)
        self.support.request.execute()

    def install_theme_from_repository(
        self, *, name: str, version: Optional[str]
    ) -> None:
        """Install CMS theme from repository."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/themes"
        data = {"name": name, "version": version}

        self.support.request.POST(url, data)
        self.support.request.execute()

    def install_theme_from_url(self, *, url: str) -> None:
        """Install CMS theme from URL."""
        _url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/themes"
        data = {"url": url}

        self.support.request.POST(_url, data)
        self.support.request.execute()

    def get_plugins(self) -> List[Dict[str, Union[str, bool, None]]]:
        """Get CMS plugins."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/plugins"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response

    def update_core(self) -> TaskCollection:
        """Update CMS core."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/core/update"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def update_plugin(self, *, name: str) -> TaskCollection:
        """Update CMS plugin."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/plugins/{name}/update"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def enable_plugin(self, *, name: str) -> TaskCollection:
        """Enable CMS plugin."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/plugins/{name}/enable"
        data: dict = {}

        self.support.request.POST(url, data)
        self.support.request.execute()

    def disable_plugin(self, *, name: str) -> TaskCollection:
        """Disable CMS plugin."""
        url = f"/api/v1/{ENDPOINT_CMSES}/{self.id}/plugins/{name}/disable"
        data: dict = {}

        self.support.request.POST(url, data)
        self.support.request.execute()
