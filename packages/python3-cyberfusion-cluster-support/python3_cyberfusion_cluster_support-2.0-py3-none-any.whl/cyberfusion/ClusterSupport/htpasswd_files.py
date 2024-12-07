"""Helper classes for scripts for cluster support packages."""

import os

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_HTPASSWD_FILES = "htpasswd-files"
MODEL_HTPASSWD_FILES = "htpasswd_files"


class HtpasswdFile(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "UNIX User",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Path",
    ]

    _TABLE_FIELDS = ["id", "_unix_user_username", "_cluster_label"]
    _TABLE_FIELDS_DETAILED = ["path"]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self.path = os.path.join(
            self.unix_user.htpasswd_files_directory,
            f".htpasswd_file-{self.id}",
        )

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_HTPASSWD_FILES}"
        data = {
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.htpasswd_files.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_HTPASSWD_FILES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.htpasswd_files.remove(self)
