"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MARIADB_ENCRYPTION_KEYS = "mariadb-encryption-keys"
MODEL_MARIADB_ENCRYPTION_KEYS = "mariadb_encryption_keys"


class MariaDBEncryptionKey(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Identifier",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Key",
    ]

    _TABLE_FIELDS = [
        "id",
        "identifier",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = ["key"]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.identifier = obj["identifier"]
        self.key = obj["key"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label

    def create(self, *, cluster_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MARIADB_ENCRYPTION_KEYS}"
        data = {
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.mariadb_encryption_keys.append(self)
