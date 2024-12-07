"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_HTPASSWD_USERS = "htpasswd-users"
MODEL_HTPASSWD_USERS = "htpasswd_users"


class HtpasswdUser(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Username",
        "File Path",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "username",
        "_htpasswd_file_path",
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
        self.htpasswd_file_id = obj["htpasswd_file_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.htpasswd_file = self.support.get_htpasswd_files(id_=self.htpasswd_file_id)[
            0
        ]

        self._cluster_label = self.cluster._label
        self._htpasswd_file_path = self.htpasswd_file.path

    def create(self, *, username: str, password: str, htpasswd_file_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_HTPASSWD_USERS}"
        data = {
            "username": username,
            "password": password,
            "htpasswd_file_id": htpasswd_file_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.htpasswd_users.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_HTPASSWD_USERS}/{self.id}"
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "htpasswd_file_id": self.htpasswd_file_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_HTPASSWD_USERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.htpasswd_users.remove(self)
