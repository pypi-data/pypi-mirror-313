"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_FIREWALL_RULES = "firewall-rules"
MODEL_FIREWALL_RULES = "firewall_rules"


class FirewallRuleServiceName(str, Enum):
    """Firewall rule service names."""

    SSH: str = "SSH"
    PROFTPD: str = "ProFTPD"
    NGINX: str = "nginx"
    APACHE: str = "Apache"


class FirewallRuleExternalProviderName(str, Enum):
    """Firewall rule external provider names."""

    ATLASSIAN: str = "Atlassian"
    BUDDY: str = "Buddy"
    GOOGLE_CLOUD: str = "Google Cloud"
    AWS: str = "AWS"


class FirewallRule(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Access Source",
        "Access Destination",
        "Node",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "id",
        "_access_source_label",
        "_access_destination_label",
        "_node_hostname",
        "_cluster_label",
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
        self.firewall_group_id = obj["firewall_group_id"]
        self.external_provider_name = (
            FirewallRuleExternalProviderName(obj["external_provider_name"]).value
            if obj["external_provider_name"]
            else None
        )
        self.service_name = (
            FirewallRuleServiceName(obj["service_name"]).value
            if obj["service_name"]
            else None
        )
        self.haproxy_listen_id = obj["haproxy_listen_id"]
        self.port = obj["port"]
        self.node_id = obj["node_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

        self.node = self.support.get_nodes(id_=self.node_id)[0]
        self._node_hostname = self.node.hostname

        if self.firewall_group_id:
            self.firewall_group = self.support.get_firewall_groups(
                id_=self.firewall_group_id
            )[0]

        if self.haproxy_listen_id:
            self.haproxy_listen = self.support.get_haproxy_listens(
                id_=self.haproxy_listen_id
            )[0]

        if self.firewall_group_id:
            self._access_source_label = self.firewall_group.name + " (Firewall Group)"
        elif self.external_provider_name:
            self._access_source_label = (
                self.external_provider_name + " (External Provider)"
            )
        else:
            self._access_source_label = "Allow All"

        if self.service_name:
            self._access_destination_label = self.service_name + " (Service)"
        elif self.haproxy_listen_id:
            self._access_destination_label = (
                self.haproxy_listen.name + " (HAProxy Listen)"
            )
        elif self.port:
            self._access_destination_label = str(self.port) + " (Port)"

    def create(
        self,
        *,
        node_id: int,
        firewall_group_id: Optional[int],
        external_provider_name: Optional[FirewallRuleExternalProviderName],
        service_name: Optional[FirewallRuleServiceName],
        haproxy_listen_id: Optional[int],
        port: Optional[int],
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_FIREWALL_RULES}"
        data = {
            "node_id": node_id,
            "firewall_group_id": firewall_group_id,
            "external_provider_name": external_provider_name,
            "service_name": service_name,
            "haproxy_listen_id": haproxy_listen_id,
            "port": port,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.firewall_rules.append(self)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_FIREWALL_RULES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.firewall_rules.remove(self)
