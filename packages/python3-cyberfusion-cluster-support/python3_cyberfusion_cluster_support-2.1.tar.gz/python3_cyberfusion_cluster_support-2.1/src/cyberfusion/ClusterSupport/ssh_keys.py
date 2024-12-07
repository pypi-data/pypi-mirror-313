"""Helper classes for scripts for cluster support packages."""

from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_SSH_KEYS = "ssh-keys"
MODEL_SSH_KEYS = "ssh_keys"


class SSHKey(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "UNIX User",
        "Private Key Path",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "_unix_user_username",
        "identity_file_path",
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
        self.identity_file_path = obj["identity_file_path"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.private_key = obj["private_key"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        name: str,
        public_key: Optional[str],
        private_key: Optional[str],
        unix_user_id: int,
    ) -> None:
        """Create object."""
        if public_key:
            self.create_public(
                name=name, public_key=public_key, unix_user_id=unix_user_id
            )
        elif private_key:
            self.create_private(
                name=name, private_key=private_key, unix_user_id=unix_user_id
            )

    def create_public(
        self,
        *,
        name: str,
        public_key: str,
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SSH_KEYS}/public"
        data = {
            "name": name,
            "public_key": public_key,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.ssh_keys.append(self)

    def create_private(
        self,
        *,
        name: str,
        private_key: str,
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SSH_KEYS}/private"
        data = {
            "name": name,
            "private_key": private_key,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.ssh_keys.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_SSH_KEYS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.ssh_keys.remove(self)
