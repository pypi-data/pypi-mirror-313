"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)

ENDPOINT_CUSTOM_CONFIG_SNIPPETS = "custom-config-snippets"
MODEL_CUSTOM_CONFIG_SNIPPETS = "custom_config_snippets"


class CustomConfigSnippetTemplateName(str, Enum):
    """Custom config snippet template names."""

    LARAVEL: str = "Laravel"
    COMPRESSION: str = "Compression"


class CustomConfigSnippet(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Name", "Server Software", "Default", "Cluster"]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "server_software_name",
        "is_default",
        "_cluster_label",
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
        self.contents = obj["contents"]
        self.server_software_name = VirtualHostServerSoftwareName(
            obj["server_software_name"]
        ).value
        self.is_default = obj["is_default"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        template_name: Optional[CustomConfigSnippetTemplateName] = None,
        contents: Optional[str] = None,
        server_software_name: VirtualHostServerSoftwareName,
        is_default: bool,
        cluster_id: int,
    ) -> None:
        """Create object."""
        if template_name:
            self.create_template(
                name=name,
                template_name=template_name,
                server_software_name=server_software_name,
                is_default=is_default,
                cluster_id=cluster_id,
            )
        elif contents:
            self.create_contents(
                name=name,
                contents=contents,
                server_software_name=server_software_name,
                is_default=is_default,
                cluster_id=cluster_id,
            )

    def create_template(
        self,
        *,
        name: str,
        template_name: CustomConfigSnippetTemplateName,
        server_software_name: VirtualHostServerSoftwareName,
        is_default: bool,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIG_SNIPPETS}"
        data = {
            "name": name,
            "template_name": template_name,
            "server_software_name": server_software_name,
            "is_default": is_default,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.custom_config_snippets.append(self)

    def create_contents(
        self,
        *,
        name: str,
        contents: str,
        server_software_name: VirtualHostServerSoftwareName,
        is_default: bool,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIG_SNIPPETS}"
        data = {
            "name": name,
            "contents": contents,
            "server_software_name": server_software_name,
            "is_default": is_default,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.custom_config_snippets.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIG_SNIPPETS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "contents": self.contents,
            "server_software_name": self.server_software_name,
            "is_default": self.is_default,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CUSTOM_CONFIG_SNIPPETS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.custom_config_snippets.remove(self)
