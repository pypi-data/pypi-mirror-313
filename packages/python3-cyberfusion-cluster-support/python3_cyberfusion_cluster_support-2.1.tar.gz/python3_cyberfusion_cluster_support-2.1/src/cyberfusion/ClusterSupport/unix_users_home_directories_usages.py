"""Helper classes for scripts for cluster support packages."""

from datetime import datetime

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_UNIX_USERS_HOME_DIRECTORIES_USAGES = (
    "clusters/unix-users-home-directories/usages"
)


class UNIXUsersHomeDirectoryUsage(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.usage = obj["usage"]
        self.cluster_id: int = obj["cluster_id"]
        self.timestamp = obj["timestamp"]

        self.datetime_object = datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S.%f")

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

    def create(self, *, usage: float, cluster_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS_HOME_DIRECTORIES_USAGES}"
        data = {
            "usage": usage,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)
