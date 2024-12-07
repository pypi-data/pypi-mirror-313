"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)


class ClusterRabbitMQCredentials(APIObjectInterface):
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
        self.cluster_id = obj["cluster_id"]
        self.rabbitmq_password = obj["rabbitmq_password"]
        self.rabbitmq_borg_virtual_host_name = obj["rabbitmq_borg_virtual_host_name"]
        self.rabbitmq_host = obj["rabbitmq_host"]
        self.rabbitmq_ssl_enabled = obj["rabbitmq_ssl_enabled"]
        self.rabbitmq_amqp_port = obj["rabbitmq_amqp_port"]
        self.rabbitmq_management_port = obj["rabbitmq_management_port"]
        self.rabbitmq_encryption_key = obj["rabbitmq_encryption_key"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.cluster = self.support.get_clusters(id_=self.cluster_id)[0]
