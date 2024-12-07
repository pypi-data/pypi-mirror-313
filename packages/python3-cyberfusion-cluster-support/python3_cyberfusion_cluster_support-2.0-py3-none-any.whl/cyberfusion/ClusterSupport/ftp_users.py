"""Helper classes for scripts for cluster support packages."""

from typing import Tuple

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_FTP_USERS = "ftp-users"
MODEL_FTP_USERS = "ftp_users"


class FTPUser(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Username",
        "UNIX User",
        "Directoy Path",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "username",
        "_unix_user_username",
        "directory_path",
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
        self.username = obj["username"]
        self.password = obj["password"]
        self.directory_path = obj["directory_path"]
        self.unix_user_id: int = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]
        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._unix_user_username = self.unix_user.username
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        username: str,
        password: str,
        directory_path: str,
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_FTP_USERS}"
        data = {
            "username": username,
            "password": password,
            "directory_path": directory_path,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.ftp_users.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_FTP_USERS}/{self.id}"
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "directory_path": self.directory_path,
            "unix_user_id": self.unix_user_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_FTP_USERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.ftp_users.remove(self)

    def create_temporary(
        self,
        *,
        unix_user_id: int,
        node_id: int,
    ) -> Tuple[str, str, str]:
        """Create temporary FTP user."""
        url = f"/api/v1/{ENDPOINT_FTP_USERS}/temporary"
        data = {
            "unix_user_id": unix_user_id,
            "node_id": node_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        return (
            response["username"],
            response["password"],
            response["file_manager_url"],
        )
