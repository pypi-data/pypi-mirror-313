"""Helper classes for scripts for cluster support packages."""

from typing import Any

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.enums import IPAddressFamily
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_CUSTOMERS = "customers"


class Customer(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Identifier",
        "Team Code",
    ]
    _TABLE_HEADERS_DETAILED = ["DNS Subdomain", "Internal"]

    _TABLE_FIELDS = [
        "id",
        "identifier",
        "team_code",
    ]
    _TABLE_FIELDS_DETAILED = [
        "dns_subdomain",
        "is_internal",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.team_code = obj["team_code"]
        self.is_internal = obj["is_internal"]
        self.identifier = obj["identifier"]
        self.dns_subdomain = obj["dns_subdomain"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

    def create(self, *, team_code: str, is_internal: bool) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}"
        data = {"team_code": team_code, "is_internal": is_internal}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.customers.append(self)

    def get_ip_addresses(self) -> dict[str, Any]:
        """Get IP addresses."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}/{self.id}/ip-addresses"

        self.support.request.GET(url)

        return self.support.request.execute()

    def get_customer_network_configurations(self) -> dict[str, Any]:
        """Get network configurations."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}/{self.id}/network-configurations"

        self.support.request.GET(url)

        return self.support.request.execute()

    def create_ip_address(
        self,
        *,
        service_account_name: str,
        dns_name: str,
        address_family: IPAddressFamily,
    ) -> TaskCollection:
        """Create IP address."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}/{self.id}/ip-addresses"
        data = {
            "service_account_name": service_account_name,
            "dns_name": dns_name,
            "address_family": address_family,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def delete_ip_address(self, ip_address: str) -> TaskCollection:
        """Delete IP address."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}/{self.id}/ip-addresses/{ip_address}"

        self.support.request.DELETE(url)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
