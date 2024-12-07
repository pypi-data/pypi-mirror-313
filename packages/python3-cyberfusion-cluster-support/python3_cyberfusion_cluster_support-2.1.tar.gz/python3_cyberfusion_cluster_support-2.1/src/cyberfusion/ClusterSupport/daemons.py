"""Helper classes for scripts for cluster support packages."""

import os
from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_DAEMONS = "daemons"
MODEL_DAEMONS = "daemons"

BASE_DIRECTORY_SYSTEMD_UNITS = os.path.join(os.path.sep, "etc", "systemd", "system")


class Daemon(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Name", "Command", "UNIX User", "Cluster", "Nodes"]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "command",
        "_unix_user_username",
        "_cluster_label",
        "_nodes_hostnames",
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
        self.command = obj["command"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]
        self.nodes_ids = obj["nodes_ids"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id = obj["cluster_id"]

        self.nodes = [self.support.get_nodes(id_=id_)[0] for id_ in obj["nodes_ids"]]
        self._nodes_hostnames = [node.hostname for node in self.nodes]

        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]
        self._unix_user_username = self.unix_user.username

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        command: str,
        unix_user_id: int,
        nodes_ids: list[int],
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_DAEMONS}"
        data = {
            "name": name,
            "command": command,
            "nodes_ids": nodes_ids,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.daemons.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_DAEMONS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "unix_user_id": self.unix_user_id,
            "nodes_ids": self.nodes_ids,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_DAEMONS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.daemons.remove(self)
