"""Thoughtful Office 365 Integration Module.

This module provides a convenient interface, 'OfficeAccount', for interacting with Microsoft Office 365 services
including Outlook, Sharepoint, OneDrive and Excel (with Sharepoint) using the O365 library.

Classes:
- OfficeAccount: A class for initializing and accessing various Microsoft Office services.
"""
from O365 import Account

from t_office_365.drive.onedrive import Onedrive
from t_office_365.drive.sharepoint import Sharepoint
from t_office_365.exceptions import AuthenticationGraphError
from t_office_365.outlook import Outlook


class OfficeAccount:
    """OfficeAccount class is used for initializing and accessing various Microsoft Office services."""

    def __init__(self, client_id: str, client_secret: str, tenant_id: str, main_resource: str = None, **kwargs) -> None:
        """Initializes OfficeAccount with the provided authentication credentials.

        :param:
        - client_id (str): The client ID for authentication.
        - client_secret (str): The client secret for authentication.
        - tenant_id (str): The ID of the Azure AD tenant.
        - main_resource (str): The main resource for authentication.

        :return: None
        """
        self.account = Account(
            (client_id, client_secret),
            auth_flow_type="credentials",
            tenant_id=tenant_id,
            main_resource=main_resource,
            **kwargs
        )
        self.account.authenticate()
        if not self.account.is_authenticated:
            raise AuthenticationGraphError

        # Initialize instances of services
        self.__outlook_instance = None
        self.__sharepoint_instance = None
        self.__onedrive_instance = None

    @property
    def outlook(self) -> Outlook:
        """Property for accessing the Outlook service.

        :return:
        Outlook: An instance of the Outlook class for managing Outlook-related operations.
        """
        if self.__outlook_instance is None:
            self.__outlook_instance = Outlook(self.account)
        return self.__outlook_instance

    @property
    def sharepoint(self) -> Sharepoint:
        """Property for accessing the Sharepoint service.

        :return:
        Sharepoint: An instance of the Sharepoint class for managing Sharepoint-related operations.
        """
        if self.__sharepoint_instance is None:
            self.__sharepoint_instance = Sharepoint(self.account)
        return self.__sharepoint_instance

    @property
    def onedrive(self) -> Onedrive:
        """Property for accessing the Onedrive service.

        :return:
        Onedrive: An instance of the Onedrive class for managing Onedrive-related operations.
        """
        if self.__onedrive_instance is None:
            self.__onedrive_instance = Onedrive(self.account)
        return self.__onedrive_instance
