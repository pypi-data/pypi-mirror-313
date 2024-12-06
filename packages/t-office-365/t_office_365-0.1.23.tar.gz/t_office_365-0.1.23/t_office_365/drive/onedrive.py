"""OneDrive class."""
from abc import ABC

import requests
from O365 import Account

from t_office_365.drive.drive import Drive, DriveSite
from t_office_365.utils import check_result


class OnedriveSite(DriveSite, ABC):
    """Represents a OneDrive site in Microsoft Office 365.

    Provides access to OneDrive-specific services and Excel functionality.
    """

    def __init__(self, account: Account, email_id: str, drive_id: str = None) -> None:
        """Initializes instance of the OnedriveService class.

        :param:
        - account: The account object containing the authentication information.
        - site_name: The name of microsoft office site.
        """
        self.__email_id = email_id
        super().__init__(account, drive_id)

    def _get_drive_id(self) -> str:
        """Get the drive ID for the site.

        :return:
        - str: The drive ID for the site.
        """
        result = requests.get(self.get_url(f"/users/{self.__email_id}/drives"), headers=self.headers())
        check_result(result, "Drive")

        return result.json()["value"][0]["id"]


class Onedrive(Drive):
    """Onedrive class is used for API calls to Onedrive."""

    def site(self, email_id: str, drive_id: str = None) -> OnedriveSite:
        """Get an Onedrive site by its email_id.

        :param:
        - email_id: The name of the Onedrive site.

        :return:
        - A OnedriveSite object representing the specified Onedrive site.
        """
        return OnedriveSite(self.account, email_id, drive_id)
