"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_CUSTOMER_IP_ADDRESSES_PRODUCTS = "customers/ip-addresses/products"


class CustomerIPAddressProduct(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "Name",
        "Type",
        "Price",
        "Currency",
        "Period",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "name",
        "type",
        "price",
        "currency",
        "period",
    ]
    _TABLE_FIELDS_DETAILED: list = []

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.name = obj["name"]
        self.type = obj["type"]
        self.price = obj["price"]
        self.currency = obj["currency"]
        self.period = obj["period"]
