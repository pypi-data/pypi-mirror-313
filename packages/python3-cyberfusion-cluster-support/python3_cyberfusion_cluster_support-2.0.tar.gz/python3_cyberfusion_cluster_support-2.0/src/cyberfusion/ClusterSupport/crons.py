"""Helper classes for scripts for cluster support packages."""

import os
from typing import Optional

from cyberfusion.ClusterSupport.unix_users import UNIXUser
from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_CRONS = "crons"
MODEL_CRONS = "crons"


def get_tuxis_cron_path(unix_user: UNIXUser, name: str) -> str:
    return os.path.join(unix_user.cronscripts_directory, name + ".cron")


class Cron(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Name",
        "Command",
        "Schedule",
        "Email Address",
        "UNIX User",
        "Active",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Error Count",
        "Random Delay\nMax Seconds",
        "Timeout Seconds",
        "Locking",
        "Node",
    ]

    _TABLE_FIELDS = [
        "id",
        "name",
        "command",
        "schedule",
        "email_address",
        "_unix_user_username",
        "is_active",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "error_count",
        "random_delay_max_seconds",
        "timeout_seconds",
        "locking_enabled",
        "_node_hostname",
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
        self.command = obj["command"]
        self.email_address = obj["email_address"]
        self.schedule = obj["schedule"]
        self.unix_user_id = obj["unix_user_id"]
        self.error_count = obj["error_count"]
        self.random_delay_max_seconds = obj["random_delay_max_seconds"]
        self.timeout_seconds = obj["timeout_seconds"]
        self.node_id = obj["node_id"]
        self.locking_enabled = obj["locking_enabled"]
        self.is_active = obj["is_active"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]
        self.node = self.support.get_nodes(id_=self.node_id)[0]

        self.tuxis_cron_path = get_tuxis_cron_path(self.unix_user, self.name)
        self.tuxis_cron_log_file_path = os.path.join(
            self.unix_user.cronscripts_logs_directory,
            f"{self.name}-{self.node.id}.log",
        )
        self.tuxis_cron_lock_file_path = os.path.join(
            self.unix_user.cronscripts_directory,
            f".{self.name}.lock",
        )

        self._cluster_label = self.cluster._label
        self._node_hostname = self.node.hostname
        self._unix_user_username = self.unix_user.username

    def create(
        self,
        *,
        name: str,
        command: str,
        email_address: Optional[str],
        schedule: str,
        unix_user_id: int,
        error_count: int,
        random_delay_max_seconds: int,
        timeout_seconds: Optional[int],
        node_id: int,
        locking_enabled: bool,
        is_active: bool,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CRONS}"
        data = {
            "name": name,
            "command": command,
            "email_address": email_address,
            "schedule": schedule,
            "unix_user_id": unix_user_id,
            "error_count": error_count,
            "random_delay_max_seconds": random_delay_max_seconds,
            "timeout_seconds": timeout_seconds,
            "node_id": node_id,
            "locking_enabled": locking_enabled,
            "is_active": is_active,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.crons.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_CRONS}/{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "email_address": self.email_address,
            "schedule": self.schedule,
            "unix_user_id": self.unix_user_id,
            "error_count": self.error_count,
            "random_delay_max_seconds": self.random_delay_max_seconds,
            "timeout_seconds": self.timeout_seconds,
            "node_id": self.node_id,
            "locking_enabled": self.locking_enabled,
            "is_active": self.is_active,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_CRONS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.crons.remove(self)
