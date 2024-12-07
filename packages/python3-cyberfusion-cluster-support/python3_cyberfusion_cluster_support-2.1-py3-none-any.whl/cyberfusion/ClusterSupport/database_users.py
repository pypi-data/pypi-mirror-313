"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_DATABASE_USERS = "database-users"
MODEL_DATABASE_USERS = "database_users"


class DatabaseServerSoftwareName(str, Enum):
    """Database server software names."""

    MARIADB: str = "MariaDB"
    POSTGRESQL: str = "PostgreSQL"


class Host(str, Enum):
    """Hosts."""

    ALL: str = "%"
    LOCALHOST_IPV6: str = "::1"


class DatabaseUser(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Server Software",
        "Host",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = ["phpMyAdmin Firewall Groups"]

    _TABLE_FIELDS = [
        "id",
        "name",
        "server_software_name",
        "host",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = ["_phpmyadmin_firewall_groups_label"]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.host = Host(obj["host"]).value if obj["host"] is not None else None
        self.server_software_name = DatabaseServerSoftwareName(
            obj["server_software_name"]
        ).value
        self.phpmyadmin_firewall_groups_ids = obj["phpmyadmin_firewall_groups_ids"]
        self.cluster_id: int = obj["cluster_id"]
        self.password = obj["password"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

        if self.phpmyadmin_firewall_groups_ids is not None:
            self._phpmyadmin_firewall_groups_label = [
                self.support.get_firewall_groups(id_=id_)[0].name
                for id_ in self.phpmyadmin_firewall_groups_ids
            ]
        else:
            self._phpmyadmin_firewall_groups_label = []

    def create(
        self,
        *,
        name: str,
        host: Optional[Host],
        password: str,
        server_software_name: DatabaseServerSoftwareName,
        phpmyadmin_firewall_groups_ids: Optional[List[int]],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_DATABASE_USERS}"
        data = {
            "name": name,
            "host": host,
            "password": password,
            "server_software_name": server_software_name,
            "phpmyadmin_firewall_groups_ids": phpmyadmin_firewall_groups_ids,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.database_users.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_DATABASE_USERS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "host": self.host,
            "password": self.password,
            "server_software_name": self.server_software_name,
            "phpmyadmin_firewall_groups_ids": self.phpmyadmin_firewall_groups_ids,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_DATABASE_USERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.database_users.remove(self)
