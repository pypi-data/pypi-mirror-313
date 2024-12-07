"""Helper classes for scripts for cluster support packages."""

from typing import List, Tuple

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.database_users import (
    DatabaseServerSoftwareName,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_DATABASES = "databases"
MODEL_DATABASES = "databases"


class Database(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Server Software",
        "Backups",
        "Optimizing",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "server_software_name",
        "backups_enabled",
        "optimizing_enabled",
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
        self.server_software_name = DatabaseServerSoftwareName(
            obj["server_software_name"]
        ).value
        self.backups_enabled = obj["backups_enabled"]
        self.optimizing_enabled = obj["optimizing_enabled"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        server_software_name: DatabaseServerSoftwareName,
        backups_enabled: bool,
        optimizing_enabled: bool,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_DATABASES}"
        data = {
            "name": name,
            "server_software_name": server_software_name,
            "backups_enabled": backups_enabled,
            "optimizing_enabled": optimizing_enabled,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.databases.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_DATABASES}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "server_software_name": self.server_software_name,
            "backups_enabled": self.backups_enabled,
            "optimizing_enabled": self.optimizing_enabled,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self, delete_on_cluster: bool = False) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_DATABASES}/{self.id}"

        params = {"delete_on_cluster": delete_on_cluster}

        self.support.request.DELETE(url, params)
        self.support.request.execute()

        self.support.databases.remove(self)

    def get_comparison(
        self, *, right_database_id: int
    ) -> Tuple[List[str], List[str], List[str], List[str]]:
        """Get comparison."""
        url = f"/api/v1/{ENDPOINT_DATABASES}/{self.id}/comparison"
        data = {"right_database_id": right_database_id}

        self.support.request.GET(url, data)
        response = self.support.request.execute()

        return (
            response["identical_tables_names"],
            response["not_identical_tables_names"],
            response["only_left_tables_names"],
            response["only_right_tables_names"],
        )

    def sync(self, *, right_database_id: int) -> TaskCollection:
        """Sync database."""
        url = f"/api/v1/{ENDPOINT_DATABASES}/{self.id}/sync"
        data: dict = {}
        params = {"right_database_id": right_database_id}

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
