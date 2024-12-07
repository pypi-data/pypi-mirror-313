"""Helper classes for scripts for cluster support packages."""

from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MAIL_HOSTNAMES = "mail-hostnames"
MODEL_MAIL_HOSTNAMES = "mail_hostnames"


class MailHostname(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Domain",
        "Certificate",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "domain",
        "certificate_id",
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
        self.domain = obj["domain"]
        self.certificate_id = obj["certificate_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        if self.certificate_id:
            self.certificate = self.support.get_certificates(id_=self.certificate_id)[0]

    def create(
        self,
        *,
        domain: str,
        certificate_id: Optional[str],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MAIL_HOSTNAMES}"
        data = {
            "domain": domain,
            "certificate_id": certificate_id,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.mail_hostnames.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_MAIL_HOSTNAMES}/{self.id}"
        data = {
            "id": self.id,
            "domain": self.domain,
            "certificate_id": self.certificate_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_MAIL_HOSTNAMES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.mail_hostnames.remove(self)
