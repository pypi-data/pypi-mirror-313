"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_CUSTOM_CONFIGS = "custom-configs"
MODEL_CUSTOM_CONFIGS = "custom_configs"


class CustomConfigServerSoftwareName(str, Enum):
    """Custom config server software names."""

    NGINX: str = "nginx"


class CustomConfig(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Server Software",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "server_software_name",
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
        self.contents = obj["contents"]
        self.server_software_name = CustomConfigServerSoftwareName(
            obj["server_software_name"]
        ).value
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        contents: str,
        server_software_name: CustomConfigServerSoftwareName,
        cluster_id: str,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIGS}"
        data = {
            "name": name,
            "contents": contents,
            "server_software_name": server_software_name,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.custom_configs.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIGS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "contents": self.contents,
            "server_software_name": self.server_software_name,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIGS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.custom_configs.remove(self)
