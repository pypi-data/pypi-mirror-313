"""Helper classes for scripts for cluster support packages."""

import os
from typing import Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_FPM_POOLS = "fpm-pools"
MODEL_FPM_POOLS = "fpm_pools"


def get_socket_path(name: str) -> str:
    """Get socket path."""
    return os.path.join(os.path.sep, "var", "run", "php", f"php-fpm.{name}.sock")


def get_unit_name(name: str, version: str) -> str:
    """Get unit name."""
    return f"fpm{version}-cf@{name}.service"


class FPMPool(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "UNIX User",
        "Version",
        "Max Children",
        "Max Requests",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Process Idle\nTimeout",
        "CPU Limit",
        "Log Slow Requests\nThreshold",
        "Namespaced",
        "Unit Name",
    ]

    _TABLE_FIELDS = [
        "id",
        "name",
        "_unix_user_username",
        "version",
        "max_children",
        "max_requests",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "process_idle_timeout",
        "cpu_limit",
        "log_slow_requests_threshold",
        "is_namespaced",
        "unit_name",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.name = obj["name"]
        self.unix_user_id = obj["unix_user_id"]
        self.version = obj["version"]
        self.max_children = obj["max_children"]
        self.max_requests = obj["max_requests"]
        self.process_idle_timeout = obj["process_idle_timeout"]
        self.cpu_limit = obj["cpu_limit"]
        self.log_slow_requests_threshold = obj["log_slow_requests_threshold"]
        self.is_namespaced = obj["is_namespaced"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.unit_name = get_unit_name(self.name, self.version)
        self.override_directory = os.path.join(
            self.support.DIRECTORY_SYSTEMD_OVERRIDE,
            self.unit_name + ".d",
        )
        self.socket = get_socket_path(self.name)
        self.pid = os.path.join(os.path.sep, "run", f"php-fpm.{self.name}.pid")
        self.log_slow_requests_path = os.path.join(
            os.path.sep, "var", "log", f"php{self.version}-fpm.log.slow"
        )  # Honours default format, see https://www.php.net/manual/en/install.fpm.configuration.php

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        name: str,
        unix_user_id: int,
        version: str,
        max_children: int,
        max_requests: Optional[int],
        process_idle_timeout: Optional[int],
        cpu_limit: Optional[int],
        log_slow_requests_threshold: Optional[int],
        is_namespaced: bool,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_FPM_POOLS}"
        data = {
            "name": name,
            "unix_user_id": unix_user_id,
            "version": version,
            "max_children": max_children,
            "max_requests": max_requests,
            "process_idle_timeout": process_idle_timeout,
            "cpu_limit": cpu_limit,
            "log_slow_requests_threshold": log_slow_requests_threshold,
            "is_namespaced": is_namespaced,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.fpm_pools.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_FPM_POOLS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "unix_user_id": self.unix_user_id,
            "version": self.version,
            "max_children": self.max_children,
            "max_requests": self.max_requests,
            "process_idle_timeout": self.process_idle_timeout,
            "cpu_limit": self.cpu_limit,
            "log_slow_requests_threshold": self.log_slow_requests_threshold,
            "is_namespaced": self.is_namespaced,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_FPM_POOLS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.fpm_pools.remove(self)

    def restart(self) -> TaskCollection:
        """Restart FPM pool."""
        url = f"/api/v1/{ENDPOINT_FPM_POOLS}/{self.id}/restart"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj

    def reload(self) -> TaskCollection:
        """Reload FPM pool."""
        url = f"/api/v1/{ENDPOINT_FPM_POOLS}/{self.id}/reload"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
