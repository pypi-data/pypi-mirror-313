"""Helper classes for scripts for cluster support packages."""

import os
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_ROOT_SSH_KEYS = "root-ssh-keys"
MODEL_ROOT_SSH_KEYS = "root_ssh_keys"


class RootSSHKey(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
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
        self.public_key = obj["public_key"]
        self.cluster_id: int = obj["cluster_id"]
        self.private_key = obj["private_key"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        if self.private_key:
            self.identity_file_path = os.path.join(
                self.support.root_ssh_directory, self.name
            )

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        name: str,
        public_key: Optional[str],
        private_key: Optional[str],
        cluster_id: int,
    ) -> None:
        """Create object."""
        if public_key:
            self.create_public(name=name, public_key=public_key, cluster_id=cluster_id)
        elif private_key:
            self.create_private(
                name=name, private_key=private_key, cluster_id=cluster_id
            )

    def create_public(self, *, name: str, public_key: str, cluster_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_ROOT_SSH_KEYS}/public"
        data = {
            "name": name,
            "public_key": public_key,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.root_ssh_keys.append(self)

    def create_private(self, *, name: str, private_key: str, cluster_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_ROOT_SSH_KEYS}/private"
        data = {
            "name": name,
            "private_key": private_key,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.root_ssh_keys.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_ROOT_SSH_KEYS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.root_ssh_keys.remove(self)
