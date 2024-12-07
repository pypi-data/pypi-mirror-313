"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_HOSTS_ENTRIES = "hosts-entries"
MODEL_HOSTS_ENTRIES = "hosts_entries"


class HostsEntry(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Host Name",
        "Node",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "host_name",
        "_node_hostname",
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
        self.node_id = obj["node_id"]
        self.host_name = obj["host_name"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

        self.node = None
        self._node_hostname = None

        # The API user may not have access to the node, if it belongs to another
        # cluster. We can't use the more neat approach of checking `accessible_core_api_clusters`
        # (see HAProxy Listens for an example), because if we don't have access
        # to the node's cluster, we don't know its cluster ID.

        try:
            self.node = self.support.get_nodes(id_=self.node_id)[0]
            self._node_hostname = self.node.hostname
        except IndexError:
            pass

    def create(self, *, node_id: int, host_name: str, cluster_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_HOSTS_ENTRIES}"
        data = {
            "node_id": node_id,
            "host_name": host_name,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.hosts_entries.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_HOSTS_ENTRIES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.hosts_entries.remove(self)
