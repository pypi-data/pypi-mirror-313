"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_URL_REDIRECTS = "url-redirects"
MODEL_URL_REDIRECTS = "url_redirects"


class StatusCode(int, Enum):
    """Status codes."""

    MOVED_PERMANENTLY: int = 301
    FOUND: int = 302
    SEE_OTHER: int = 303
    TEMPORARY_REDIRECT: int = 307
    PERMANENT_REDIRECT: int = 308


class URLRedirect(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Domain",
        "Description",
        "Server Aliases",
        "Destination URL",
        "Status Code",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Keep Query\nParameters",
        "Keep Path",
    ]

    _TABLE_FIELDS = [
        "id",
        "domain",
        "description",
        "server_aliases",
        "destination_url",
        "status_code",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "keep_query_parameters",
        "keep_path",
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
        self.destination_url = obj["destination_url"]
        self.status_code = StatusCode(obj["status_code"]).value
        self.keep_query_parameters = obj["keep_query_parameters"]
        self.keep_path = obj["keep_path"]
        self.description = obj["description"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.server_names = []
        self.server_names.append(self.domain)
        self.server_names.extend(self.server_aliases)

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        domain: str,
        server_aliases: List[str],
        destination_url: str,
        status_code: StatusCode,
        keep_query_parameters: bool,
        keep_path: bool,
        description: Optional[str],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_URL_REDIRECTS}"
        data = {
            "domain": domain,
            "server_aliases": server_aliases,
            "destination_url": destination_url,
            "status_code": status_code,
            "keep_query_parameters": keep_query_parameters,
            "keep_path": keep_path,
            "description": description,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.url_redirects.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_URL_REDIRECTS}/{self.id}"
        data = {
            "id": self.id,
            "domain": self.domain,
            "server_aliases": self.server_aliases,
            "destination_url": self.destination_url,
            "status_code": self.status_code,
            "keep_query_parameters": self.keep_query_parameters,
            "keep_path": self.keep_path,
            "description": self.description,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_URL_REDIRECTS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.url_redirects.remove(self)
