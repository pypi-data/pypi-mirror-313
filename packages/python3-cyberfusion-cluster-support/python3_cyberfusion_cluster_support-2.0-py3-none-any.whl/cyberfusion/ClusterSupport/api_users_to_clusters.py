"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_API_USERS_TO_CLUSTERS = "api-users-to-clusters"


class APIUserToCluster(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "API User",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "_api_user_username",
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
        self.api_user_id = obj["api_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.api_user = self.support.get_api_users(id_=self.api_user_id)[0]
        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._api_user_username = self.api_user.username
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        api_user_id: int,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_API_USERS_TO_CLUSTERS}"
        data = {
            "api_user_id": api_user_id,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.api_users_to_clusters.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_API_USERS_TO_CLUSTERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.api_users_to_clusters.remove(self)
