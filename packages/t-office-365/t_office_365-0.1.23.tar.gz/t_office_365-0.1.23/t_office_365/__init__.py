"""Top-level package for t-office-365."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "0.1.23"

from .drive.excel import Excel
from .drive.onedrive import Onedrive, OnedriveSite
from .drive.sharepoint import Sharepoint, SharepointSite
from .office import OfficeAccount
from .outlook import Outlook

__all__ = ["OfficeAccount", "Outlook", "Onedrive", "Sharepoint", "OnedriveSite", "SharepointSite", "Excel"]
