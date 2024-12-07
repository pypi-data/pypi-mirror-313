"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_BASIC_AUTHENTICATION_REALMS = "basic-authentication-realms"
MODEL_BASIC_AUTHENTICATION_REALMS = "basic_authentication_realms"


class BasicAuthenticationRealm(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Virtual Host",
        "Htpasswd File",
        "Directory Path",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "_virtual_host_domain",
        "_htpasswd_file_path",
        "directory_path",
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
        self.name = obj["name"]
        self.directory_path = obj["directory_path"]
        self.htpasswd_file_id = obj["htpasswd_file_id"]
        self.virtual_host_id = obj["virtual_host_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.htpasswd_file = self.support.get_htpasswd_files(id_=self.htpasswd_file_id)[
            0
        ]
        self.virtual_host = self.support.get_virtual_hosts(id_=self.virtual_host_id)[0]

        self._cluster_label = self.cluster._label
        self._htpasswd_file_path = self.htpasswd_file.path
        self._virtual_host_domain = self.virtual_host.domain

    def create(
        self,
        *,
        name: str,
        directory_path: str,
        htpasswd_file_id: int,
        virtual_host_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_BASIC_AUTHENTICATION_REALMS}"
        data = {
            "name": name,
            "directory_path": directory_path,
            "htpasswd_file_id": htpasswd_file_id,
            "virtual_host_id": virtual_host_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.basic_authentication_realms.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_BASIC_AUTHENTICATION_REALMS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "directory_path": self.directory_path,
            "htpasswd_file_id": self.htpasswd_file_id,
            "virtual_host_id": self.virtual_host_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_BASIC_AUTHENTICATION_REALMS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.basic_authentication_realms.remove(self)
