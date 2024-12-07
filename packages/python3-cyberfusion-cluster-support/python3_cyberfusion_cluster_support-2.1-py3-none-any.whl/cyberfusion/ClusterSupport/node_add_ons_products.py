"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_NODE_ADD_ONS_PRODUCTS = "node-add-ons/products"


class NodeAddOnProduct(APIObjectInterface):
    """Represents object."""

    _TABLE_HEADERS = [
        "Name",
        "RAM in GB",
        "Cores",
        "Disk in GB",
        "Price",
        "Currency",
        "Period",
    ]
    _TABLE_HEADERS_DETAILED: list = []

    _TABLE_FIELDS = [
        "name",
        "ram",
        "cores",
        "disk",
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
        self.ram = obj["ram"]
        self.cores = obj["cores"]
        self.disk = obj["disk"]
        self.price = obj["price"]
        self.currency = obj["currency"]
        self.period = obj["period"]
