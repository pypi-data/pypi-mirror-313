"""Helper classes for scripts for cluster support packages."""

from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_BORG_ARCHIVES = "borg-archives"
MODEL_BORG_ARCHIVES = "borg_archives"


class BorgArchive(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Database",
        "UNIX User",
        "Exists",
        "Path",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "name",
        "_database_name",
        "_unix_user_username",
        "_exists_on_server",
        "_contents_path",
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
        self.borg_repository_id = obj["borg_repository_id"]
        self.database_id = obj["database_id"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.borg_repository = self.support.get_borg_repositories(
            id_=self.borg_repository_id
        )[0]
        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = None
        self._database_name = None

        if self.unix_user_id:
            self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]
            self._unix_user_username = self.unix_user.username

        if self.database_id:
            self.database = self.support.get_databases(id_=self.database_id)[0]
            self._database_name = self.database.name

    def create(
        self,
        *,
        name: str,
        borg_repository_id: int,
        database_id: Optional[int],
        unix_user_id: Optional[int],
    ) -> TaskCollection:
        """Create object."""
        if database_id:
            return self.create_database(
                name=name,
                borg_repository_id=borg_repository_id,
                database_id=database_id,
            )

        return self.create_unix_user(
            name=name,
            borg_repository_id=borg_repository_id,
            unix_user_id=unix_user_id,  # type: ignore[arg-type]
        )

    def create_database(
        self, *, name: str, borg_repository_id: int, database_id: int
    ) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/database"
        data = {
            "name": name,
            "borg_repository_id": borg_repository_id,
            "database_id": database_id,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.borg_archives.append(self)

        return obj

    def create_unix_user(
        self, *, name: str, borg_repository_id: int, unix_user_id: int
    ) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/unix-user"
        data = {
            "name": name,
            "borg_repository_id": borg_repository_id,
            "unix_user_id": unix_user_id,
        }

        # Create task collection

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Set attributes by getting new Borg archive by returned task collection

        self.support.request.GET(f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/{obj.object_id}")
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.borg_archives.append(self)

        return obj

    def restore(self, path: Optional[str]) -> TaskCollection:
        """Restore Borg archive."""
        url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/{self.id}/restore"
        data: dict = {}
        params = {"path": path}

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def download(self, path: Optional[str]) -> TaskCollection:
        """Download Borg archive."""
        url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/{self.id}/download"
        data: dict = {}
        params = {"path": path}

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def get_metadata(self, *, single: bool = True) -> dict:
        """Get Borg archive metadata.

        When 'single' is set to false, metadata for all Borg archives is retrieved
        via the Borg repository and then cached. Although that call may take longer
        than the one which retrieves metadata for a single Borg archive, it is
        of course more efficient when needing metadata for multiple Borg archives.
        """
        if single:
            url = f"/api/v1/{ENDPOINT_BORG_ARCHIVES}/{self.id}/metadata"

            self.support.request.GET(url)
            response = self.support.request.execute()

            return response

        return self.borg_repository.get_archive_metadata(self.id)

    @property
    def _contents_path(self) -> str:
        """Get contents path."""
        return self.get_metadata(single=False)["contents_path"]

    @property
    def _exists_on_server(self) -> bool:
        """Get exists on server."""
        return self.get_metadata(single=False)["exists_on_server"]
