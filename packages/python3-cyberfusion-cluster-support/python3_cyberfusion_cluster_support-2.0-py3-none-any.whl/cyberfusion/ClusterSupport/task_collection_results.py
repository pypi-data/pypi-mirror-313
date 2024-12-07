"""Helper classes for scripts for cluster support packages."""

from enum import Enum

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)


class TaskState(str, Enum):
    """Task states."""

    PENDING: str = "pending"
    STARTED: str = "started"
    SUCCESS: str = "success"
    FAILURE: str = "failure"
    RETRY: str = "retry"
    REVOKED: str = "revoked"


TASK_STATES_DEFINITIVE = [
    TaskState.SUCCESS,
    TaskState.FAILURE,
    TaskState.REVOKED,
]


class TaskCollectionResult(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "Description",
        "Message",
        "State",
    ]
    _TABLE_HEADERS_DETAILED = [
        "UUID",
    ]

    _TABLE_FIELDS = [
        "description",
        "message",
        "state",
    ]
    _TABLE_FIELDS_DETAILED = [
        "uuid",
    ]

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.description = obj["description"]
        self.uuid = obj["uuid"]
        self.message = obj["message"]
        self.state = TaskState(obj["state"]).value
