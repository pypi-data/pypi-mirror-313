"""Helper classes for scripts for cluster support packages."""

import os
from enum import Enum
from typing import Optional, Tuple

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.passenger_apps import (
    BASE_DIRECTORY_NODEJS_INSTALLATIONS,
    NodeJSBinaryName,
)

ENDPOINT_UNIX_USERS = "unix-users"
MODEL_UNIX_USERS = "unix_users"


class ShellPath(str, Enum):
    """Shell paths."""

    BASH: str = "/bin/bash"
    JAILSHELL: str = "/usr/local/bin/jailshell"
    NOLOGIN: str = "/usr/sbin/nologin"


class UNIXUser(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "ID",
        "Username",
        "Description",
        "Home Directory",
        "Virtual Hosts\nSubdirectory",
        "Mail Domains\nSubdirectory",
        "Borg Repositories\nSubdirectory",
        "Default\nPHP Version",
        "Default\nNodeJS Version",
        "Cluster",
    ]
    _TABLE_HEADERS_DETAILED = [
        "Shell Path",
        "Record\nUsage Files",
        "UNIX ID",
    ]

    _TABLE_FIELDS = [
        "id",
        "username",
        "description",
        "home_directory",
        "_table_virtual_hosts_subdirectory",
        "_table_mail_domains_subdirectory",
        "_table_borg_repositories_subdirectory",
        "default_php_version",
        "default_nodejs_version",
        "_cluster_label",
    ]
    _TABLE_FIELDS_DETAILED = [
        "shell_path",
        "record_usage_files",
        "unix_id",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.username = obj["username"]
        self.password = obj["password"]
        self.unix_id = obj["unix_id"]
        self.default_php_version = obj["default_php_version"]
        self.default_nodejs_version = obj["default_nodejs_version"]
        self.shell_path = ShellPath(obj["shell_path"]).value
        self.record_usage_files = obj["record_usage_files"]
        self.description = obj["description"]
        self.virtual_hosts_directory = obj["virtual_hosts_directory"]
        self.mail_domains_directory = obj["mail_domains_directory"]
        self.borg_repositories_directory = obj["borg_repositories_directory"]
        self.home_directory = obj["home_directory"]
        self.ssh_directory = obj["ssh_directory"]
        self.cluster_id: int = obj["cluster_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        if self.default_php_version:
            self.default_php_version_binary = "php" + self.default_php_version

        if self.default_nodejs_version:
            self.default_nodejs_version_corepack_binary = os.path.join(
                BASE_DIRECTORY_NODEJS_INSTALLATIONS,
                self.default_nodejs_version,
                "bin",
                NodeJSBinaryName.COREPACK.value,
            )

            self.default_nodejs_version_node_binary = os.path.join(
                BASE_DIRECTORY_NODEJS_INSTALLATIONS,
                self.default_nodejs_version,
                "bin",
                NodeJSBinaryName.NODE.value,
            )

            self.default_nodejs_version_npm_binary = os.path.join(
                BASE_DIRECTORY_NODEJS_INSTALLATIONS,
                self.default_nodejs_version,
                "bin",
                NodeJSBinaryName.NPM.value,
            )

            self.default_nodejs_version_npx_binary = os.path.join(
                BASE_DIRECTORY_NODEJS_INSTALLATIONS,
                self.default_nodejs_version,
                "bin",
                NodeJSBinaryName.NPX.value,
            )

            (
                self.default_nodejs_major_version,
                self.default_nodejs_minor_version,
            ) = [int(x) for x in self.default_nodejs_version.split(".")]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]

        self.tmp_directory = os.path.join(os.path.sep, "tmp", self.username)
        self.cronscripts_directory = os.path.join(self.home_directory, "cronscripts")
        self.cronscripts_logs_directory = os.path.join(
            self.cronscripts_directory, "logs"
        )
        self.xdg_config_home_directory = os.path.join(self.home_directory, ".config")
        self.xdg_config_cluster_directory = os.path.join(
            self.xdg_config_home_directory, "cluster"
        )
        self.htpasswd_files_directory = os.path.join(
            self.home_directory, ".htpasswd_files"
        )

        self._cluster_label = self.cluster._label
        self._table_virtual_hosts_subdirectory = "None"
        self._table_mail_domains_subdirectory = "None"
        self._table_borg_repositories_subdirectory = "None"

        if self.virtual_hosts_directory:
            if self.virtual_hosts_directory == self.home_directory:
                self._table_virtual_hosts_subdirectory = ""
            else:
                self._table_virtual_hosts_subdirectory = os.path.relpath(
                    path=self.virtual_hosts_directory,
                    start=self.home_directory,
                )

        if self.mail_domains_directory:
            if self.mail_domains_directory == self.home_directory:
                self._table_mail_domains_subdirectory = ""
            else:
                self._table_mail_domains_subdirectory = os.path.relpath(
                    path=self.mail_domains_directory, start=self.home_directory
                )

        if self.borg_repositories_directory:
            if self.borg_repositories_directory == self.home_directory:
                self._table_borg_repositories_subdirectory = ""
            else:
                self._table_borg_repositories_subdirectory = os.path.relpath(
                    path=self.borg_repositories_directory,
                    start=self.home_directory,
                )

    def create(
        self,
        *,
        username: str,
        password: Optional[str],
        shell_path: ShellPath,
        record_usage_files: bool,
        default_php_version: Optional[str],
        default_nodejs_version: Optional[str],
        virtual_hosts_directory: Optional[str],
        mail_domains_directory: Optional[str],
        borg_repositories_directory: Optional[str],
        description: Optional[str],
        cluster_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS}"
        data = {
            "username": username,
            "password": password,
            "shell_path": shell_path,
            "record_usage_files": record_usage_files,
            "default_php_version": default_php_version,
            "default_nodejs_version": default_nodejs_version,
            "virtual_hosts_directory": virtual_hosts_directory,
            "mail_domains_directory": mail_domains_directory,
            "borg_repositories_directory": borg_repositories_directory,
            "description": description,
            "cluster_id": cluster_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.unix_users.append(self)

    def update(self) -> None:
        """Update object."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS}/{self.id}"
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "shell_path": self.shell_path,
            "record_usage_files": self.record_usage_files,
            "description": self.description,
            "default_php_version": self.default_php_version,
            "default_nodejs_version": self.default_nodejs_version,
            "virtual_hosts_directory": self.virtual_hosts_directory,
            "mail_domains_directory": self.mail_domains_directory,
            "borg_repositories_directory": self.borg_repositories_directory,
            "home_directory": self.home_directory,
            "ssh_directory": self.ssh_directory,
            "unix_id": self.unix_id,
            "cluster_id": self.cluster_id,
        }

        self.support.request.PATCH(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

    def delete(self, delete_on_cluster: bool = False) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS}/{self.id}"

        params = {"delete_on_cluster": delete_on_cluster}

        self.support.request.DELETE(url, params)
        self.support.request.execute()

        self.support.unix_users.remove(self)

    def get_comparison(
        self, *, right_unix_user_id: int
    ) -> Tuple[dict, dict, dict, dict, dict]:
        """Get comparison."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS}/{self.id}/comparison"
        data = {"right_unix_user_id": right_unix_user_id}

        self.support.request.GET(url, data)
        response = self.support.request.execute()

        return (
            response["not_identical_paths"],
            response["only_left_files_paths"],
            response["only_right_files_paths"],
            response["only_left_directories_paths"],
            response["only_right_directories_paths"],
        )
