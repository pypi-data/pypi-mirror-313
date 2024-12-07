"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_NODE_ADD_ONS = "node-add-ons"
MODEL_NODE_ADD_ONS = "node_add_ons"


class NodeAddOn(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Product",
        "Quantity",
        "Node",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "product",
        "quantity",
        "_node_hostname",
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
        self.product = obj["product"]
        self.quantity = obj["quantity"]
        self.node_id = obj["node_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.node = self.support.get_nodes(id_=self.node_id)[0]

        self._cluster_label = self.cluster._label
        self._node_hostname = self.node.hostname

    def create(self, *, product: str, node_id: int, quantity: int) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_NODE_ADD_ONS}"
        data = {
            "product": product,
            "node_id": node_id,
            "quantity": quantity,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_NODE_ADD_ONS}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.node_add_ons.append(self)

        return obj

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_NODE_ADD_ONS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.node_add_ons.remove(self)
