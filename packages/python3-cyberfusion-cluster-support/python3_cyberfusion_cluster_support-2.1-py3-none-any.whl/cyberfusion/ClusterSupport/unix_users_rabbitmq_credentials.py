"""Helper classes for scripts for cluster support packages."""

import os

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_UNIX_USERS_RABBITMQ_CREDENTIALS = "unix-users-rabbitmq-credentials"
MODEL_UNIX_USERS_RABBITMQ_CREDENTIALS = "unix_users_rabbitmq_credentials"


def get_unit_name(rabbitmq_virtual_host_name: str) -> str:
    """Get unit name."""
    return f"rabbitmq-consume@{rabbitmq_virtual_host_name}.service"


class UNIXUserRabbitMQCredentials(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.rabbitmq_username = obj["rabbitmq_username"]
        self.rabbitmq_virtual_host_name = obj["rabbitmq_virtual_host_name"]
        self.rabbitmq_host = obj["rabbitmq_host"]
        self.rabbitmq_ssl_enabled = obj["rabbitmq_ssl_enabled"]
        self.rabbitmq_amqp_port = obj["rabbitmq_amqp_port"]
        self.rabbitmq_management_port = obj["rabbitmq_management_port"]
        self.unix_user_id = obj["unix_user_id"]
        self.rabbitmq_password = obj["rabbitmq_password"]
        self.rabbitmq_encryption_key = obj["rabbitmq_encryption_key"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

        self.rabbitmq_consumer_unit_name = get_unit_name(
            self.rabbitmq_virtual_host_name
        )
        self.rabbitmq_consumer_override_directory = os.path.join(
            self.support.DIRECTORY_SYSTEMD_OVERRIDE,
            self.rabbitmq_consumer_unit_name + ".d",
        )
