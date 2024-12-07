"""Helper classes for scripts for cluster support packages."""

from enum import Enum

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_ACCESS_LOGS = "logs/access"
ENDPOINT_ERROR_LOGS = "logs/error"


class LogMethod(str, Enum):
    """Log methods."""

    GET: str = "GET"
    POST: str = "POST"
    PUT: str = "PUT"
    PATCH: str = "PATCH"
    OPTIONS: str = "OPTIONS"
    DELETE: str = "DELETE"
    HEAD: str = "HEAD"


class AccessLog(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.remote_address = obj["remote_address"]
        self.raw_message = obj["raw_message"]
        self.method = (
            LogMethod(obj["method"]).value if obj["method"] is not None else None
        )

        self.uri = obj["uri"]
        self.timestamp = obj["timestamp"]
        self.status_code = obj["status_code"]
        self.bytes_sent = obj["bytes_sent"]


class ErrorLog(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.remote_address = obj["remote_address"]
        self.raw_message = obj["raw_message"]
        self.method = (
            LogMethod(obj["method"]).value if obj["method"] is not None else None
        )
        self.uri = obj["uri"]
        self.timestamp = obj["timestamp"]
        self.error_message = obj["error_message"]
