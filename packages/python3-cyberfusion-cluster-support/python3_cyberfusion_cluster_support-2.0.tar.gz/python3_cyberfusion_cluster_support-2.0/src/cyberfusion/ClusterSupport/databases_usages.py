"""Helper classes for scripts for cluster support packages."""

from datetime import datetime

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_DATABASES_USAGES = "databases/usages"


class DatabaseUsage(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.usage = obj["usage"]
        self.database_id = obj["database_id"]
        self.timestamp = obj["timestamp"]

        self.datetime_object = datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S.%f")

        self.database = self.support.get_databases(id_=self.database_id)[0]

    def create(self, *, usage: float, database_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_DATABASES_USAGES}"
        data = {
            "usage": usage,
            "database_id": database_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)
