"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_SITES_TO_CUSTOMERS = "sites-to-customers"


class SiteToCustomer(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.site_id = obj["site_id"]
        self.customer_id: int = obj["customer_id"]
        self.netbox_default_prefix_ipv4_id = obj["netbox_default_prefix_ipv4_id"]
        self.netbox_default_prefix_ipv6_id = obj["netbox_default_prefix_ipv6_id"]
        self.netbox_default_vlan_id = obj["netbox_default_vlan_id"]
        self.netbox_vlan_ids = obj["netbox_vlan_ids"]
        self.netbox_prefixes = obj["netbox_prefixes"]
        self.netbox_default_prefix_ipv6 = obj["netbox_default_prefix_ipv6"]
        self.netbox_default_prefix_ipv4 = obj["netbox_default_prefix_ipv4"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.site = self.support.get_sites(id_=self.site_id)[0]
        self.customer = self.support.get_customers(id_=self.customer_id)[0]

    def create(
        self,
        *,
        site_id: int,
        customer_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SITES_TO_CUSTOMERS}"
        data = {
            "site_id": site_id,
            "customer_id": customer_id,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_SITES_TO_CUSTOMERS}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.sites_to_customers.append(self)

        return obj
