"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_CERTIFICATES = "certificates"
MODEL_CERTIFICATES = "certificates"


class Certificate(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Main Common Name", "Common Names", "Expires"]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = ["id", "main_common_name", "common_names", "expires_at"]
    _TABLE_FIELDS_DETAILED: List[str] = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.common_names = obj["common_names"]
        self.main_common_name = obj["main_common_name"]
        self.certificate = obj["certificate"]
        self.ca_chain = obj["ca_chain"]
        self.expires_at = obj["expires_at"]
        self.cluster_id: int = obj["cluster_id"]
        self.private_key = obj["private_key"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

    def create(
        self,
        *,
        certificate: str,
        ca_chain: str,
        private_key: str,
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATES}"
        data = {
            "certificate": certificate,
            "ca_chain": ca_chain,
            "private_key": private_key,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.certificates.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.certificates.remove(self)
