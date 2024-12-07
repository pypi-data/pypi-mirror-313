"""Helper classes for scripts for cluster support packages."""

from datetime import datetime
from typing import Dict, List, Optional, Union

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_UNIX_USERS_USAGES = "unix-users/usages"


class UNIXUserUsage(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.usage = obj["usage"]
        self.unix_user_id = obj["unix_user_id"]
        self.files = obj["files"]
        self.timestamp = obj["timestamp"]

        self.datetime_object = datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S.%f")

        self.unix_user = self.support.get_unix_users(id_=self.unix_user_id)[0]

    def create(
        self,
        *,
        usage: float,
        files: Optional[List[Dict[str, Union[str, float]]]],
        unix_user_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_UNIX_USERS_USAGES}"
        data = {
            "usage": usage,
            "files": files,
            "unix_user_id": unix_user_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)
