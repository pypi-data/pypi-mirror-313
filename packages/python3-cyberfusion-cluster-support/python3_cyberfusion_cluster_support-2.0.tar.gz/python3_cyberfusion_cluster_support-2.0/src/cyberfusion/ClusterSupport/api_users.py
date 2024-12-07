"""Helper classes for scripts for cluster support packages."""

from typing import List, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_API_USERS = "api-users"


class APIUser(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Username",
        "Active",
        "Superuser",
        "Trusted IP Networks",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "username",
        "is_active",
        "is_superuser",
        "trusted_ip_networks",
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
        self.is_active = obj["is_active"]
        self.is_superuser = obj["is_superuser"]
        self.username = obj["username"]
        self.trusted_ip_networks = obj["trusted_ip_networks"]
        self.hashed_password = obj["hashed_password"]
        self.customer_id = obj["customer_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

    def create(
        self,
        *,
        is_active: bool,
        is_superuser: bool,
        username: str,
        trusted_ip_networks: Optional[List[str]],
        password: str,
        customer_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_API_USERS}"
        data = {
            "is_active": is_active,
            "is_superuser": is_superuser,
            "username": username,
            "trusted_ip_networks": trusted_ip_networks,
            "password": password,
            "customer_id": customer_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.api_users.append(self)

    def update(self, password: Optional[str] = None) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_API_USERS}/{self.id}"
        data = {
            "id": self.id,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "username": self.username,
            "trusted_ip_networks": self.trusted_ip_networks,
            "customer_id": self.customer_id,
        }

        if password:
            data["password"] = password

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_API_USERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.api_users.remove(self)
