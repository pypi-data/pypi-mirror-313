"""Helper classes for scripts for cluster support packages."""

from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MAIL_ALIASES = "mail-aliases"
MODEL_MAIL_ALIASES = "mail_aliases"


class MailAlias(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Address", "Forward\nAddresses", "Cluster"]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "email_address",
        "forward_email_addresses",
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
        self.local_part = obj["local_part"]
        self.forward_email_addresses = obj["forward_email_addresses"]
        self.mail_domain_id = obj["mail_domain_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.mail_domain = self.support.get_mail_domains(id_=self.mail_domain_id)[0]

        self.email_address = self.local_part + "@" + self.mail_domain.domain

        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        local_part: str,
        forward_email_addresses: List[str],
        mail_domain_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ALIASES}"
        data = {
            "local_part": local_part,
            "forward_email_addresses": forward_email_addresses,
            "mail_domain_id": mail_domain_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.mail_aliases.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ALIASES}/{self.id}"
        data = {
            "id": self.id,
            "local_part": self.local_part,
            "forward_email_addresses": self.forward_email_addresses,
            "mail_domain_id": self.mail_domain_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ALIASES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.mail_aliases.remove(self)
