"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_API_KEYS = "api-keys"


class APIKey(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.hashed_key = obj["hashed_key"]
        self.object_id = obj["object_id"]
        self.object_model_name = obj["object_model_name"]
        self.api_user_id = obj["api_user_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.api_user = self.support.get_api_users(id_=self.api_user_id)[0]
