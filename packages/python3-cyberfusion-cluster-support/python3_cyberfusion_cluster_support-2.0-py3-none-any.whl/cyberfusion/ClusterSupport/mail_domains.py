"""Helper classes for scripts for cluster support packages."""

import os
from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MAIL_DOMAINS = "mail-domains"
MODEL_MAIL_DOMAINS = "mail_domains"


class MailDomain(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Domain",
        "UNIX User",
        "Catch All\nForward Addresses",
        "Local",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "domain",
        "_unix_user_username",
        "catch_all_forward_email_addresses",
        "is_local",
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
        self.domain = obj["domain"]
        self.catch_all_forward_email_addresses = obj[
            "catch_all_forward_email_addresses"
        ]
        self.is_local = obj["is_local"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self.mail_domain_root = os.path.join(
            self.unix_user.mail_domains_directory, self.domain
        )

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        domain: str,
        catch_all_forward_email_addresses: List[str],
        is_local: bool,
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MAIL_DOMAINS}"
        data = {
            "domain": domain,
            "catch_all_forward_email_addresses": catch_all_forward_email_addresses,
            "is_local": is_local,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.mail_domains.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_MAIL_DOMAINS}/{self.id}"
        data = {
            "id": self.id,
            "domain": self.domain,
            "catch_all_forward_email_addresses": self.catch_all_forward_email_addresses,
            "is_local": self.is_local,
            "unix_user_id": self.unix_user_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_MAIL_DOMAINS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.mail_domains.remove(self)
