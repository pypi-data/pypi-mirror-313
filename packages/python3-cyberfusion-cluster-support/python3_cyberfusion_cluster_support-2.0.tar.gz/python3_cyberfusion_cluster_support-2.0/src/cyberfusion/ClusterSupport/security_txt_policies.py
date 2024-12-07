"""Helper classes for scripts for cluster support packages."""

from datetime import datetime
from enum import Enum
from typing import List

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_SECURITY_TXT_POLICIES = "security-txt-policies"
MODEL_SECURITY_TXT_POLICIES = "security_txt_policies"


class PreferredLanguage(str, Enum):
    """Preferred languages."""

    NL: str = "nl"
    EN: str = "en"


class SecurityTXTPolicy(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Expires",
        "Email Contacts",
        "URL Contacts",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Encryption Key URLs",
        "Acknowledgment URLs",
        "Policy URLs",
        "Opening URLs",
        "Preferred Languages",
    ]

    _TABLE_FIELDS = [
        "id",
        "expires_timestamp",
        "email_contacts",
        "url_contacts",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "encryption_key_urls",
        "acknowledgment_urls",
        "policy_urls",
        "opening_urls",
        "preferred_languages",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.expires_timestamp = obj["expires_timestamp"]
        self.email_contacts = obj["email_contacts"]
        self.url_contacts = obj["url_contacts"]
        self.encryption_key_urls = obj["encryption_key_urls"]
        self.acknowledgment_urls = obj["acknowledgment_urls"]
        self.policy_urls = obj["policy_urls"]
        self.opening_urls = obj["opening_urls"]
        self.preferred_languages = obj["preferred_languages"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        expires_timestamp: datetime,
        email_contacts: List[str],
        url_contacts: List[str],
        encryption_key_urls: List[str],
        acknowledgment_urls: List[str],
        policy_urls: List[str],
        opening_urls: List[str],
        preferred_languages: List[PreferredLanguage],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SECURITY_TXT_POLICIES}"
        data = {
            "expires_timestamp": expires_timestamp,
            "email_contacts": email_contacts,
            "url_contacts": url_contacts,
            "encryption_key_urls": encryption_key_urls,
            "acknowledgment_urls": acknowledgment_urls,
            "policy_urls": policy_urls,
            "opening_urls": opening_urls,
            "preferred_languages": preferred_languages,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.security_txt_policies.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_SECURITY_TXT_POLICIES}/{self.id}"
        data = {
            "id": self.id,
            "expires_timestamp": self.expires_timestamp,
            "email_contacts": self.email_contacts,
            "url_contacts": self.url_contacts,
            "encryption_key_urls": self.encryption_key_urls,
            "acknowledgment_urls": self.acknowledgment_urls,
            "policy_urls": self.policy_urls,
            "opening_urls": self.opening_urls,
            "preferred_languages": self.preferred_languages,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_SECURITY_TXT_POLICIES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.security_txt_policies.remove(self)
