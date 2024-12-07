"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.enums import ObjectModelName

ENDPOINT_TOMBSTONES = "tombstones"
MODEL_TOMBSTONES = "tombstones"


class Tombstone(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Object ID", "Object Type", "Cluster ID"]
    _TABLE_HEADERS_DETAILED = ["Data"]

    _TABLE_FIELDS = ["id", "object_id", "object_model_name", "cluster_id"]
    _TABLE_FIELDS_DETAILED = [
        "data",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.object_model_name = ObjectModelName(obj["object_model_name"]).value
        self.object_id = obj["object_id"]
        self.data = obj["data"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        # Tombstone may belong to deleted cluster, so do not set relationship
        #
        # self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
