"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)


class ClusterCephFSCredentials(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.username = obj["username"]
        self.secret_key = obj["secret_key"]
        self.monitors_ip_addresses = obj["monitors_ip_addresses"]
        self.path = obj["path"]
        self.cluster_id = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
