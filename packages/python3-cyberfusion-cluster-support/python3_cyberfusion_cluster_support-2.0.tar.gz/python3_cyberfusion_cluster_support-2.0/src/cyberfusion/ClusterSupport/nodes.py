"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from http import HTTPStatus
from typing import List, Optional

from cyberfusion.ClusterApiCli import ClusterApiCallException
from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_NODES = "nodes"
MODEL_NODES = "nodes"


class NodeGroup(str, Enum):
    """Node groups."""

    ADMIN: str = "Admin"
    APACHE: str = "Apache"
    NEW_RELIC: str = "New Relic"
    PROFTPD: str = "ProFTPD"
    NGINX: str = "nginx"
    DOVECOT: str = "Dovecot"
    MEILISEARCH: str = "Meilisearch"
    MARIADB: str = "MariaDB"
    POSTGRESQL: str = "PostgreSQL"
    PHP: str = "PHP"
    BORG: str = "Borg"
    NODEJS: str = "NodeJS"
    FAST_REDIRECT: str = "Fast Redirect"
    PASSENGER: str = "Passenger"
    REDIS: str = "Redis"
    HAPROXY: str = "HAProxy"
    WP_CLI: str = "WP-CLI"
    COMPOSER: str = "Composer"
    KERNELCARE: str = "KernelCare"
    IMAGEMAGICK: str = "ImageMagick"
    WKHTMLTOPDF: str = "wkhtmltopdf"
    GNU_MAILUTILS: str = "GNU Mailutils"
    CLAMAV: str = "ClamAV"
    PUPPETEER: str = "Puppeteer"
    LIBREOFFICE: str = "LibreOffice"
    GHOSTSCRIPT: str = "Ghostscript"
    FFMPEG: str = "FFmpeg"
    DOCKER: str = "Docker"
    MALDET: str = "maldet"
    GRAFANA: str = "Grafana"
    SINGLESTORE: str = "SingleStore"
    METABASE: str = "Metabase"
    ELASTICSEARCH: str = "Elasticsearch"
    RABBITMQ: str = "RabbitMQ"


class Node(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Hostname",
        "Groups",
        "Comment",
        "Groups Properties",
        "Load Balancer Health Checks Groups Pairs",
        "Product",
        "Ready",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "id",
        "hostname",
        "groups",
        "comment",
        "groups_properties",
        "load_balancer_health_checks_groups_pairs",
        "product",
        "is_ready",
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
        self.hostname = obj["hostname"]
        self.comment = obj["comment"]
        self.groups = [NodeGroup(x).value for x in obj["groups"]]
        self.load_balancer_health_checks_groups_pairs = obj[
            "load_balancer_health_checks_groups_pairs"
        ]
        self.groups_properties = obj["groups_properties"]
        self.product = obj["product"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]
        self.is_ready = obj["is_ready"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self._cluster_label = self.cluster._label

    def create(
        self,
        *,
        comment: Optional[str],
        groups: List[NodeGroup],
        load_balancer_health_checks_groups_pairs: dict,
        groups_properties: dict,
        cluster_id: int,
        product: str,
    ) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_NODES}"
        data = {
            "comment": comment,
            "groups": groups,
            "load_balancer_health_checks_groups_pairs": load_balancer_health_checks_groups_pairs,
            "groups_properties": groups_properties,
            "cluster_id": cluster_id,
            "product": product,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_NODES}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.nodes.append(self)

        return obj

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}"
        data = {
            "id": self.id,
            "hostname": self.hostname,
            "comment": self.comment,
            "groups": self.groups,
            "load_balancer_health_checks_groups_pairs": self.load_balancer_health_checks_groups_pairs,
            "groups_properties": self.groups_properties,
            "cluster_id": self.cluster_id,
            "product": self.product,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.nodes.remove(self)

    def get_sensu_configuration(self) -> Optional[dict]:
        """Get Sensu configuration."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}/sensu"

        self.support.request.GET(url)

        try:
            return self.support.request.execute()
        except ClusterApiCallException as e:
            if e.status_code == HTTPStatus.NOT_FOUND:
                return None

            raise

    def get_infscape_configuration(self) -> Optional[dict]:
        """Get Infscape configuration."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}/infscape"

        self.support.request.GET(url)

        try:
            return self.support.request.execute()
        except ClusterApiCallException as e:
            if e.status_code == HTTPStatus.NOT_FOUND:
                return None

            raise

    def get_ip_addresses(self) -> dict:
        """Get node IP addresses."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}/ip-addresses"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response

    def get_network_routes(self) -> dict:
        """Get node IP addresses."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}/network-routes"

        self.support.request.GET(url)
        response = self.support.request.execute()

        return response

    def xgrade(self, product: str) -> TaskCollection:
        """Xgrade node."""
        url = f"/api/v1/{ENDPOINT_NODES}/{self.id}/xgrade"
        data: dict = {}
        params = {
            "product": product,
        }

        self.support.request.POST(url, data, params)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
