"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_SITES = "sites"


class Site(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "Name",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "name",
    ]
    _TABLE_FIELDS_DETAILED: list = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]

    def create(
        self,
        *,
        name: str,
        netbox_site_group_id: int,
        netbox_admin_prefix_ipv4_id: int,
        netbox_admin_prefix_ipv6_id: int,
        netbox_customer_prefix_container_ipv4_id: int,
        netbox_customer_prefix_container_ipv6_id: int,
        netbox_vlan_group_id: int,
        netbox_default_vm_cluster_id: int,
        netbox_borg_server_vm_cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SITES}"
        data = {
            "name": name,
            "netbox_site_group_id": netbox_site_group_id,
            "netbox_admin_prefix_ipv4_id": netbox_admin_prefix_ipv4_id,
            "netbox_admin_prefix_ipv6_id": netbox_admin_prefix_ipv6_id,
            "netbox_customer_prefix_container_ipv4_id": netbox_customer_prefix_container_ipv4_id,
            "netbox_customer_prefix_container_ipv6_id": netbox_customer_prefix_container_ipv6_id,
            "netbox_vlan_group_id": netbox_vlan_group_id,
            "netbox_default_vm_cluster_id": netbox_default_vm_cluster_id,
            "netbox_borg_server_vm_cluster_id": netbox_borg_server_vm_cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.sites.append(self)
