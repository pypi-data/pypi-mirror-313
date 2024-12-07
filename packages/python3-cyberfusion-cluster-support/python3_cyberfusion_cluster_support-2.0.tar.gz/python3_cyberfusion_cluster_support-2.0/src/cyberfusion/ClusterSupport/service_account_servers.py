"""Helper classes for scripts for cluster support packages."""

from enum import Enum

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_SERVICE_ACCOUNT_SERVERS = "service-account-servers"


class NetBoxResourceType(str, Enum):
    """NetBox resource types."""

    VM: str = "VM"
    DEVICE: str = "Device"


class ServiceAccountServer(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.hostname = obj["hostname"]
        self.netbox_resource_type = obj["netbox_resource_type"]
        self.netbox_parent_interface_id = obj["netbox_parent_interface_id"]
        self.netbox_resource_id = obj["netbox_resource_id"]
        self.service_account_id = obj["service_account_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.service_account = self.support.get_service_accounts(
            id_=self.service_account_id
        )[0]

    def create(
        self,
        *,
        hostname: str,
        service_account_id: int,
        netbox_resource_type: NetBoxResourceType,
        netbox_parent_interface_id: int,
        netbox_resource_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNT_SERVERS}"
        data = {
            "hostname": hostname,
            "service_account_id": service_account_id,
            "netbox_resource_type": netbox_resource_type,
            "netbox_parent_interface_id": netbox_parent_interface_id,
            "netbox_resource_id": netbox_resource_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.service_account_servers.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNT_SERVERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.service_account_servers.remove(self)

    def get_network_configuration(self) -> dict:
        """Get network configuration."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNT_SERVERS}/{self.id}/network-configuration"

        self.support.request.GET(url)

        return self.support.request.execute()
