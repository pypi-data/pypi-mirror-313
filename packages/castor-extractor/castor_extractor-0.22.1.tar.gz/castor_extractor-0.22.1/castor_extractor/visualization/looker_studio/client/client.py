from typing import Iterator

from .. import LookerStudioAsset
from .admin_sdk_client import USER_EMAIL_FIELD, AdminSDKClient
from .credentials import LookerStudioCredentials
from .looker_studio_api_client import LookerStudioAPIClient


class LookerStudioClient:
    """
    Acts as a wrapper class to fetch Looker Studio assets, which requires
    coordinating calls between the Admin SDK API and the Looker Studio API.
    """

    def __init__(self, credentials: LookerStudioCredentials):
        self.admin_sdk_client = AdminSDKClient(credentials)
        self.looker_studio_client = LookerStudioAPIClient(credentials)

    def _get_assets(self) -> Iterator[dict]:
        """
        Extracts reports and data sources user by user.
        """
        users = self.admin_sdk_client.list_users()

        for user in users:
            email = user[USER_EMAIL_FIELD]
            yield from self.looker_studio_client.fetch_user_assets(email)

    def fetch(self, asset: LookerStudioAsset) -> Iterator[dict]:
        if asset == LookerStudioAsset.VIEW_ACTIVITY:
            yield from self.admin_sdk_client.list_view_events()

        elif asset == LookerStudioAsset.ASSETS:
            yield from self._get_assets()

        else:
            raise ValueError(f"The asset {asset}, is not supported")
