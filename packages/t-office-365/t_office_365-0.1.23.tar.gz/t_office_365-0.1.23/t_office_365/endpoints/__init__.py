"""This module for t_office_365 package api endpoints."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "0.1.23"

from t_office_365.endpoints import drive_api, mail_api, workbook_api

__all__ = [
    "drive_api",
    "workbook_api",
    "mail_api",
]
