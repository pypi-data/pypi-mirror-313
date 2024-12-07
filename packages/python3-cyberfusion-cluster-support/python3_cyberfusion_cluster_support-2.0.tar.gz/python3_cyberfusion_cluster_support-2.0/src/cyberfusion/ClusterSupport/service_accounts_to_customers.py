"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS = "service-accounts-to-customers"


class ServiceAccountToCustomer(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.json_body = obj

        self.id = obj["id"]
        self.service_account_id = obj["service_account_id"]
        self.customer_id: int = obj["customer_id"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

        self.service_account = self.support.get_service_accounts(
            id_=self.service_account_id
        )[0]
        self.customer = self.support.get_customers(id_=self.customer_id)[0]

    def create(
        self,
        *,
        service_account_id: int,
        customer_id: int,
    ) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS}"
        data = {
            "service_account_id": service_account_id,
            "customer_id": customer_id,
        }

        # Create object and create and set attributes on TaskCollection
        # class

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        # Get object and set attributes on local class

        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS}/{obj.object_id}"

        self.support.request.GET(url)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)

        self.support.service_accounts_to_customers.append(self)

        return obj

    def delete(self) -> None:
        """Delete object."""
        url = f"/api/v1/{ENDPOINT_SERVICE_ACCOUNTS_TO_CUSTOMERS}/{self.id}"

        self.support.request.DELETE(url)
        self.support.request.execute()

        self.support.service_accounts_to_customers.remove(self)
