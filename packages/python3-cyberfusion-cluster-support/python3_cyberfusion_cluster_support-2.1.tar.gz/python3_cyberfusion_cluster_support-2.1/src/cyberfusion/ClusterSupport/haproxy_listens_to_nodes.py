"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_HAPROXY_LISTENS_TO_NODES = "haproxy-listens-to-nodes"
MODEL_HAPROXY_LISTENS_TO_NODES = "haproxy_listens_to_nodes"


class HAProxyListenToNode(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "HAProxy Listen",
        "Node",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "_haproxy_listen_name",
        "_node_hostname",
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
        self.haproxy_listen_id = obj["haproxy_listen_id"]
        self.node_id = obj["node_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.haproxy_listen = self.support.get_haproxy_listens(
            id_=self.haproxy_listen_id
        )[0]
        self.node = self.support.get_nodes(id_=self.node_id)[0]

        self._haproxy_listen_name = self.haproxy_listen.name
        self._node_hostname = self.node.hostname

    def create(
        self,
        *,
        haproxy_listen_id: int,
        node_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_HAPROXY_LISTENS_TO_NODES}"
        data = {
            "haproxy_listen_id": haproxy_listen_id,
            "node_id": node_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.haproxy_listens_to_nodes.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_HAPROXY_LISTENS_TO_NODES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.haproxy_listens_to_nodes.remove(self)
