"""SharePoint class."""
from abc import ABC

import requests
from O365 import Account

from t_office_365.drive.drive import Drive, DriveSite
from t_office_365.utils import check_result


class SharepointSite(DriveSite, ABC):
    """Represents a SharePoint site in Microsoft Office 365.

    Provides access to SharePoint-specific services and Excel functionality.
    """

    def __init__(self, account: Account, site_name: str) -> None:
        """Initializes instance of the SharepointService class.

        :param:
        - account: The account object containing the authentication information.
        - site_name: The name of microsoft office site.
        """
        self.__site_name = site_name
        super().__init__(account)

    def _get_drive_id(self) -> str:
        """Get the Drive ID for SharePoint.

        :param:
        - site_name (str): The name of the site.

        :return:
        - str: The ID of the SharePoint Drive.
        """
        site_id = self.account.sharepoint().get_site("root", self.__site_name).object_id

        url = self.get_url(f"/sites/{site_id}/drives")
        result = requests.get(url, headers=self.headers())
        check_result(result, url)
        return result.json()["value"][0]["id"]


class Sharepoint(Drive):
    """SharePoint class is used for API calls to SharePoint."""

    def site(self, site_name: str) -> SharepointSite:
        """Get a SharePoint site by its name.

        :param:
        - site_name: The name of the SharePoint site.

        :return:
        - A SharepointSite object representing the specified SharePoint site.
        """
        return SharepointSite(self.account, site_name)
