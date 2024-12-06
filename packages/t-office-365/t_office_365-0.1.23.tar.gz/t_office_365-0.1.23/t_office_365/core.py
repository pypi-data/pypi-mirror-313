"""Core module for the Office 365 API."""
from dataclasses import dataclass
from urllib.parse import quote

from O365 import Account

from t_office_365.constants import MS_GRAPH_BASE_URL


@dataclass
class Core:
    """Core class for the Office 365 API."""

    account: Account = None
    base_url: str = MS_GRAPH_BASE_URL

    @property
    def access_token(self):
        """Get the access token from the account."""
        if not self.account.is_authenticated:
            self.account.con.refresh_token()
        return self.account.con.session.access_token

    @property
    def expiration_datetime(self):
        """Get the expiration datetime of the token."""
        return self.account.connection.token_backend.token.expiration_datetime

    def headers(self, add_headers: dict = None) -> dict:
        """Get the headers for the request."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        if add_headers:
            for key, value in add_headers.items():
                headers[key] = value

        return headers

    @staticmethod
    def encode_url(url) -> str:
        """Encode the url."""
        return quote(url)

    def get_url(self, endpoint: str) -> str:
        """Get the URL for the request."""
        return f"{self.base_url}{endpoint}"
