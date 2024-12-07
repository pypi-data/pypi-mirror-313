"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_CERTIFICATE_MANAGERS = "certificate-managers"
MODEL_CERTIFICATE_MANAGERS = "certificate_managers"


class ProviderName(str, Enum):
    """Provider names."""

    LETS_ENCRYPT: str = "lets_encrypt"


class CertificateManager(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Main Common Name",
        "Common Names",
        "Provider Name",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Last Request Task Collection UUID",
        "Request Callback URL",
        "Certificate ID",
    ]

    _TABLE_FIELDS = [
        "id",
        "main_common_name",
        "common_names",
        "provider_name",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "last_request_task_collection_uuid",
        "request_callback_url",
        "certificate_id",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.common_names = obj["common_names"]
        self.provider_name = ProviderName(obj["provider_name"]).value
        self.last_request_task_collection_uuid = obj[
            "last_request_task_collection_uuid"
        ]
        self.request_callback_url = obj["request_callback_url"]
        self.certificate_id = obj["certificate_id"]
        self.main_common_name = obj["main_common_name"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        common_names: str,
        provider_name: ProviderName,
        request_callback_url: Optional[str],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATE_MANAGERS}"
        data = {
            "common_names": common_names,
            "provider_name": provider_name,
            "request_callback_url": request_callback_url,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.certificate_managers.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATE_MANAGERS}/{self.id}"
        data = {
            "id": self.id,
            "common_names": self.common_names,
            "provider_name": self.provider_name,
            "last_request_task_collection_uuid": self.last_request_task_collection_uuid,
            "request_callback_url": self.request_callback_url,
            "main_common_name": self.main_common_name,
            "certificate_id": self.certificate_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATE_MANAGERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.certificate_managers.remove(self)

    def request(self) -> TaskCollection:
        """Request certificate."""
        url = f"/api/v1/{ENDPOINT_CERTIFICATE_MANAGERS}/{self.id}/request"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
