"""Helper classes for scripts for cluster support packages."""

import os
from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MAIL_ACCOUNTS = "mail-accounts"
MODEL_MAIL_ACCOUNTS = "mail_accounts"


def get_mail_account_directory(mail_domain_root: str, local_part: str) -> str:
    return os.path.join(mail_domain_root, local_part)


class MailAccount(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = ["ID", "Address", "Aliases", "Quota", "Cluster"]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "email_address",
        "mail_aliases_email_addresses",
        "quota",
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
        self.password = obj["password"]
        self.quota = obj["quota"]
        self.mail_domain_id = obj["mail_domain_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.mail_domain = self.support.get_mail_domains(id_=self.mail_domain_id)[0]

        self.email_address = self.local_part + "@" + self.mail_domain.domain

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self.mail_account_directory = get_mail_account_directory(
            self.mail_domain.mail_domain_root, self.local_part
        )

        self._cluster_label = self.cluster._label

    @property
    def mail_aliases_email_addresses(self) -> List[str]:
        """Get mail aliases that forward to this mail account."""
        result = []

        mail_aliases = self.support.get_mail_aliases(
            forward_email_addresses=self.email_address
        )

        for mail_alias in mail_aliases:
            result.append(mail_alias.email_address)

        return result

    def create(
        self,
        *,
        local_part: str,
        password: str,
        quota: Optional[int],
        mail_domain_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ACCOUNTS}"
        data = {
            "local_part": local_part,
            "password": password,
            "quota": quota,
            "mail_domain_id": mail_domain_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.mail_accounts.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ACCOUNTS}/{self.id}"
        data = {
            "id": self.id,
            "local_part": self.local_part,
            "password": self.password,
            "quota": self.quota,
            "mail_domain_id": self.mail_domain_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self, delete_on_cluster: bool = False) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ACCOUNTS}/{self.id}"

        params = {"delete_on_cluster": delete_on_cluster}

        self.support.request.DELETE(url, params)
        self.support.request.execute()

        self.support.mail_accounts.remove(self)
