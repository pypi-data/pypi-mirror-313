"""Helper classes for scripts for cluster support packages."""

from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.nodes import NodeGroup

ENDPOINT_HAPROXY_LISTENS = "haproxy-listens"
MODEL_HAPROXY_LISTENS = "haproxy_listens"


class HAProxyListen(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Nodes Group",
        "Port",
        "Socket Path",
        "Destination Cluster",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "nodes_group",
        "port",
        "socket_path",
        "_destination_cluster_label",
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
        self.nodes_group = obj["nodes_group"]
        self.port = obj["port"]
        self.socket_path = obj["socket_path"]
        self.destination_cluster_id = obj["destination_cluster_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

        self.destination_cluster = None
        self._destination_cluster_label = None

        if self.destination_cluster_id in self.support.accessible_core_api_clusters:
            self.destination_cluster = self.support.get_clusters(
                id_=self.destination_cluster_id
            )[0]
            self._destination_cluster_label = self.destination_cluster._label

    def create(
        self,
        *,
        name: str,
        nodes_group: NodeGroup,
        port: Optional[int],
        socket_path: Optional[str],
        destination_cluster_id: int,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_HAPROXY_LISTENS}"
        data = {
            "name": name,
            "nodes_group": nodes_group,
            "port": port,
            "socket_path": socket_path,
            "destination_cluster_id": destination_cluster_id,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.haproxy_listens.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_HAPROXY_LISTENS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.haproxy_listens.remove(self)
