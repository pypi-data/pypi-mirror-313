"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_DATABASE_USER_GRANTS = "database-user-grants"
MODEL_DATABASE_USER_GRANTS = "database_user_grants"


class Privilege(str, Enum):
    """Privileges."""

    ALL: str = "ALL"
    SELECT: str = "SELECT"


class DatabaseUserGrant(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Database",
        "Table",
        "User",
        "Privilege",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "_database_name",
        "table_name",
        "_database_user_name",
        "privilege_name",
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
        self.database_id = obj["database_id"]
        self.database_user_id = obj["database_user_id"]
        self.table_name = obj["table_name"]
        self.privilege_name = obj["privilege_name"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.database = self.support.get_databases(id_=self.database_id)[0]
        self.database_user = self.support.get_database_users(id_=self.database_user_id)[
            0
        ]
        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label
        self._database_name = self.database.name
        self._database_user_name = self.database_user.name

    def create(
        self,
        *,
        database_id: int,
        database_user_id: int,
        table_name: Optional[str],
        privilege_name: Privilege,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_DATABASE_USER_GRANTS}"
        data = {
            "database_id": database_id,
            "database_user_id": database_user_id,
            "table_name": table_name,
            "privilege_name": privilege_name,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.database_user_grants.append(self)
