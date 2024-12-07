"""Helper classes for scripts for cluster support packages."""

from datetime import datetime

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)

ENDPOINT_MAIL_ACCOUNTS_USAGES = "mail-accounts/usages"


class MailAccountUsage(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.usage = obj["usage"]
        self.mail_account_id = obj["mail_account_id"]
        self.timestamp = obj["timestamp"]

        self.datetime_object = datetime.strptime(self.timestamp, "%Y-%m-%dT%H:%M:%S.%f")

        self.mail_account = self.support.get_mail_accounts(id_=self.mail_account_id)[0]

    def create(self, *, usage: float, mail_account_id: int) -> None:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_MAIL_ACCOUNTS_USAGES}"
        data = {
            "usage": usage,
            "mail_account_id": mail_account_id,
        }

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        self._set_attributes_from_model(response)
