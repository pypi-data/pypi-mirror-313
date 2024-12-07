"""Helper classes for scripts for cluster support packages."""

import enum
from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_SERVICE_ACCOUNTS = "service-accounts"


class ServiceAccountGroup(str, enum.Enum):
    """Service account groups."""

    SECURITY_TXT_POLICY_SERVER: str = "Security TXT Policy Server"
    LOAD_BALANCER: str = "Load Balancer"
    MAIL_PROXY: str = "Mail Proxy"
    MAIL_GATEWAY: str = "Mail Gateway"
    INTERNET_ROUTER: str = "Internet Router"
    STORAGE_ROUTER: str = "Storage Router"
    PHPMYADMIN: str = "phpMyAdmin"


class ServiceAccount(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.group = obj["group"]
        self.site_id = obj["site_id"]
        self.default_ipv6_ip_address = obj["default_ipv6_ip_address"]
        self.default_ipv4_ip_address = obj["default_ipv4_ip_address"]
        self.default_ipv6_netbox_id = obj["default_ipv6_netbox_id"]
        self.default_ipv4_netbox_id = obj["default_ipv4_netbox_id"]
        self.netbox_additional_prefix_ipv4_id = obj["netbox_additional_prefix_ipv4_id"]
        self.netbox_fhrp_group_ipv6_id = obj["netbox_fhrp_group_ipv6_id"]
        self.netbox_fhrp_group_ipv4_id = obj["netbox_fhrp_group_ipv4_id"]
        self.netbox_additional_prefix_ipv6_id = obj["netbox_additional_prefix_ipv6_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.site = self.support.get_sites(id_=self.site_id)[0]

    def create(
        self,
        *,
        name: str,
        group: ServiceAccountGroup,
        site_id: int,
        default_ipv6_ip_address: Optional[str],
        default_ipv4_ip_address: Optional[str],
        default_ipv6_netbox_id: Optional[str],
        default_ipv4_netbox_id: Optional[str],
        netbox_additional_prefix_ipv4_id: Optional[str],
        netbox_fhrp_group_ipv6_id: Optional[str],
        netbox_fhrp_group_ipv4_id: Optional[str],
        netbox_additional_prefix_ipv6_id: Optional[str],
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNTS}"
        data = {
            "name": name,
            "group": group,
            "site_id": site_id,
            "default_ipv6_ip_address": default_ipv6_ip_address,
            "default_ipv4_ip_address": default_ipv4_ip_address,
            "default_ipv6_netbox_id": default_ipv6_netbox_id,
            "default_ipv4_netbox_id": default_ipv4_netbox_id,
            "netbox_additional_prefix_ipv4_id": netbox_additional_prefix_ipv4_id,
            "netbox_fhrp_group_ipv6_id": netbox_fhrp_group_ipv6_id,
            "netbox_fhrp_group_ipv4_id": netbox_fhrp_group_ipv4_id,
            "netbox_additional_prefix_ipv6_id": netbox_additional_prefix_ipv6_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.service_accounts.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNTS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.service_accounts.remove(self)
