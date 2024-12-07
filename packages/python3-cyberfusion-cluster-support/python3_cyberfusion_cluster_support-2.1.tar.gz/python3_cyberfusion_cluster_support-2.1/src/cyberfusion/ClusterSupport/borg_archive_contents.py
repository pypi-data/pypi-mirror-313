"""Helper classes for scripts for cluster support packages."""

from enum import Enum
from typing import List

from humanize import naturalsize

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)


class ContentObjectType(str, Enum):
    """Content object types."""

    REGULAR_FILE: str = "regular_file"
    DIRECTORY: str = "directory"
    SYMBOLIC_LINK: str = "symbolic_link"


class BorgArchiveContent(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "Path",
        "Object Type",
        "UNIX User",
        "UNIX Group",
        "Permissions",
        "Link Target",
        "Modification Time",
        "Size",
    ]
    _TABLE_HEADERS_DETAILED: List[str] = []

    _TABLE_FIELDS = [
        "_relative_path",
        "object_type",
        "username",
        "group_name",
        "symbolic_mode",
        "link_target",
        "modification_time",
        "_human_readable_size",
    ]
    _TABLE_FIELDS_DETAILED: List[str] = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.object_type = obj["object_type"]
        self.symbolic_mode = obj["symbolic_mode"]
        self.username = obj["username"]
        self.group_name = obj["group_name"]
        self.path = obj["path"]
        self.link_target = obj["link_target"]
        self.modification_time = obj["modification_time"]
        self.size = obj["size"]

        self._human_readable_size = None

        if self.size:
            self._human_readable_size = naturalsize(self.size, binary=True)
