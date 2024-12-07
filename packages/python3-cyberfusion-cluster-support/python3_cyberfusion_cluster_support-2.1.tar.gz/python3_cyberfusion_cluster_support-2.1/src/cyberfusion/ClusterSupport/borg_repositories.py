"""Helper classes for scripts for cluster support packages."""

from typing import Optional

from cached_property import cached_property

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_BORG_REPOSITORIES = "borg-repositories"
MODEL_BORG_REPOSITORIES = "borg_repositories"


class BorgRepository(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "UNIX User",
        "Hourly",
        "Daily",
        "Weekly",
        "Monthly",
        "Yearly",
        "Remote Host",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Remote Path",
        "Remote Username",
        "Identity File",
    ]

    _TABLE_FIELDS = [
        "id",
        "name",
        "_unix_user_username",
        "keep_hourly",
        "keep_daily",
        "keep_weekly",
        "keep_monthly",
        "keep_yearly",
        "remote_host",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "remote_path",
        "remote_username",
        "identity_file_path",
    ]

    @sort_lists
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.keep_hourly = obj["keep_hourly"]
        self.keep_daily = obj["keep_daily"]
        self.keep_weekly = obj["keep_weekly"]
        self.keep_monthly = obj["keep_monthly"]
        self.keep_yearly = obj["keep_yearly"]
        self.remote_host = obj["remote_host"]
        self.remote_path = obj["remote_path"]
        self.remote_username = obj["remote_username"]
        self.identity_file_path = obj["identity_file_path"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.passphrase = obj["passphrase"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = None

        if self.unix_user_id:
            self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]
            self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        name: str,
        passphrase: str,
        keep_hourly: Optional[int],
        keep_daily: Optional[int],
        keep_weekly: Optional[int],
        keep_monthly: Optional[int],
        keep_yearly: Optional[int],
        remote_host: str,
        remote_path: str,
        remote_username: str,
        identity_file_path: Optional[str],
        unix_user_id: Optional[int],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}"
        data = {
            "name": name,
            "passphrase": passphrase,
            "keep_hourly": keep_hourly,
            "keep_daily": keep_daily,
            "keep_weekly": keep_weekly,
            "keep_monthly": keep_monthly,
            "keep_yearly": keep_yearly,
            "remote_host": remote_host,
            "remote_path": remote_path,
            "remote_username": remote_username,
            "identity_file_path": identity_file_path,
            "unix_user_id": unix_user_id,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.borg_repositories.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "passphrase": self.passphrase,
            "keep_hourly": self.keep_hourly,
            "keep_daily": self.keep_daily,
            "keep_weekly": self.keep_weekly,
            "keep_monthly": self.keep_monthly,
            "keep_yearly": self.keep_yearly,
            "remote_host": self.remote_host,
            "remote_path": self.remote_path,
            "remote_username": self.remote_username,
            "identity_file_path": self.identity_file_path,
            "unix_user_id": self.unix_user_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.borg_repositories.remove(self)

    def prune(self) -> TaskCollection:
        """Prune Borg repository."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}/{self.id}/prune"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def check(self) -> TaskCollection:
        """Check Borg repository."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}/{self.id}/check"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    @cached_property
    def archives_metadata(self) -> list:
        """Get Borg repository archives metadata."""
        url = f"/api/v1/{ENDPOINT_BORG_REPOSITORIES}/{self.id}/archives-metadata"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response

    def get_archive_metadata(self, borg_archive_id: int) -> dict:
        """Get Borg archive metadata from Borg repository."""
        return next(
            filter(
                lambda x: x["borg_archive_id"] == borg_archive_id,
                self.archives_metadata,
            )
        )
