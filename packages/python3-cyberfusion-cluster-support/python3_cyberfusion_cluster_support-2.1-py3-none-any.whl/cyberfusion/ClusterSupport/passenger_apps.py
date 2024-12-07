"""Helper classes for scripts for cluster support packages."""

import os
from enum import Enum
from typing import Dict, Optional

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_PASSENGER_APPS = "passenger-apps"
MODEL_PASSENGER_APPS = "passenger_apps"

BASE_DIRECTORY_NODEJS_INSTALLATIONS = os.path.join(
    os.path.sep, "usr", "local", "lib", "nodejs"
)


def get_unit_name(name: str) -> str:
    """Get unit name."""
    return f"passenger-cf@{name}.service"


class NodeJSBinaryName(str, Enum):
    """NodeJS binary names."""

    COREPACK: str = "corepack"
    NPX: str = "npx"
    NPM: str = "npm"
    NODE: str = "node"


class PassengerAppType(str, Enum):
    """Passenger app types."""

    NODEJS: str = "NodeJS"


class PassengerEnvironment(str, Enum):
    """Passenger environments."""

    PRODUCTION: str = "Production"
    DEVELOPMENT: str = "Development"


class PassengerApp(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "UNIX User",
        "App Type",
        "Environment",
        "NodeJS\nVersion",
        "App Root",
        "Startup File",
        "Environment\nVariables",
        "Max Pool Size",
        "Max Requests",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Pool Idle\nTime",
        "CPU Limit",
        "Namespaced",
        "Port",
        "Unit Name",
    ]

    _TABLE_FIELDS = [
        "id",
        "name",
        "_unix_user_username",
        "app_type",
        "environment",
        "nodejs_version",
        "app_root",
        "startup_file",
        "environment_variables",
        "max_pool_size",
        "max_requests",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "pool_idle_time",
        "cpu_limit",
        "is_namespaced",
        "port",
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
        self.environment = obj["environment"]
        self.environment_variables = obj["environment_variables"]
        self.max_pool_size = obj["max_pool_size"]
        self.max_requests = obj["max_requests"]
        self.pool_idle_time = obj["pool_idle_time"]
        self.port = obj["port"]
        self.app_type = obj["app_type"]
        self.nodejs_version = obj["nodejs_version"]
        self.startup_file = obj["startup_file"]
        self.is_namespaced = obj["is_namespaced"]
        self.cpu_limit = obj["cpu_limit"]
        self.app_root = obj["app_root"]
        self.unix_user_id = obj["unix_user_id"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.unit_name = get_unit_name(self.name)
        self.pid = os.path.join(
            os.path.sep,
            "run",
            f"passenger-cf@{self.name}",
            f"passenger-cf.{self.name}.pid",
        )

        self.log_file_path = os.path.join(
            os.path.sep,
            "var",
            "log",
            f"passenger-cf@{self.name}",
            f"passenger-cf.{self.name}.log",
        )

        self.override_directory = os.path.join(
            self.support.DIRECTORY_SYSTEMD_OVERRIDE,
            self.unit_name + ".d",
        )

        self.nodejs_version_node_binary = os.path.join(
            BASE_DIRECTORY_NODEJS_INSTALLATIONS,
            self.nodejs_version,
            "bin",
            NodeJSBinaryName.NODE.value,
        )

        self.major_version, self.minor_version = [
            int(x) for x in self.nodejs_version.split(".")
        ]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self._cluster_label = self.cluster._label
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        name: str,
        unix_user_id: int,
        environment: PassengerEnvironment,
        environment_variables: Optional[Dict[str, str]],
        max_pool_size: Optional[int],
        max_requests: Optional[int],
        pool_idle_time: Optional[int],
        nodejs_version: str,
        startup_file: str,
        is_namespaced: bool,
        cpu_limit: Optional[int],
        app_root: str,
    ) -> None:
        """Create object."""
        self.create_nodejs(
            name=name,
            unix_user_id=unix_user_id,
            environment=environment,
            environment_variables=environment_variables,
            max_pool_size=max_pool_size,
            max_requests=max_requests,
            pool_idle_time=pool_idle_time,
            nodejs_version=nodejs_version,
            startup_file=startup_file,
            is_namespaced=is_namespaced,
            cpu_limit=cpu_limit,
            app_root=app_root,
        )

    def create_nodejs(
        self,
        *,
        name: str,
        unix_user_id: int,
        environment: PassengerEnvironment,
        environment_variables: Optional[Dict[str, str]],
        max_pool_size: Optional[int],
        max_requests: Optional[int],
        pool_idle_time: Optional[int],
        nodejs_version: str,
        startup_file: str,
        is_namespaced: bool,
        cpu_limit: Optional[int],
        app_root: str,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_PASSENGER_APPS}/nodejs"
        data = {
            "name": name,
            "unix_user_id": unix_user_id,
            "environment": environment,
            "environment_variables": environment_variables,
            "max_pool_size": max_pool_size,
            "max_requests": max_requests,
            "pool_idle_time": pool_idle_time,
            "nodejs_version": nodejs_version,
            "startup_file": startup_file,
            "is_namespaced": is_namespaced,
            "cpu_limit": cpu_limit,
            "app_root": app_root,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.passenger_apps.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_PASSENGER_APPS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "unix_user_id": self.unix_user_id,
            "environment": self.environment,
            "environment_variables": self.environment_variables,
            "max_pool_size": self.max_pool_size,
            "max_requests": self.max_requests,
            "pool_idle_time": self.pool_idle_time,
            "port": self.port,
            "app_type": self.app_type,
            "nodejs_version": self.nodejs_version,
            "startup_file": self.startup_file,
            "is_namespaced": self.is_namespaced,
            "cpu_limit": self.cpu_limit,
            "app_root": self.app_root,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_PASSENGER_APPS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.passenger_apps.remove(self)

    def restart(self) -> TaskCollection:
        """Restart Passenger app."""
        url = f"/api/v1/{ENDPOINT_PASSENGER_APPS}/{self.id}/restart"
        data: dict = {}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
