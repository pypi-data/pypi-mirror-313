import logging
from collections.abc import Iterator
from typing import Optional

from ....utils import build_url
from ....utils.salesforce import SalesforceBaseClient
from ..assets import SalesforceReportingAsset
from .soql import queries

logger = logging.getLogger(__name__)

REQUIRING_URL_ASSETS = (
    SalesforceReportingAsset.REPORTS,
    SalesforceReportingAsset.DASHBOARDS,
    SalesforceReportingAsset.FOLDERS,
)


class SalesforceReportingClient(SalesforceBaseClient):
    """
    Salesforce Reporting API client
    """

    def _get_asset_url(
        self, asset_type: SalesforceReportingAsset, asset: dict
    ) -> Optional[str]:
        """
        Fetch the given Asset + add the corresponding URL.
        """

        if asset_type == SalesforceReportingAsset.DASHBOARDS:
            path = f"lightning/r/Dashboard/{asset['Id']}/view"
            return build_url(self._host, path)

        if asset_type == SalesforceReportingAsset.FOLDERS:
            path = asset["attributes"]["url"].lstrip("/")
            return build_url(self._host, path)

        if asset_type == SalesforceReportingAsset.REPORTS:
            path = f"lightning/r/Report/{asset['Id']}/view"
            return build_url(self._host, path)

        return None

    def _fetch_and_add_url(
        self, asset_type: SalesforceReportingAsset
    ) -> Iterator[dict]:
        assets = self._query_all(queries[asset_type])
        for asset in assets:
            url = self._get_asset_url(asset_type, asset)
            yield {**asset, "Url": url}

    def fetch(self, asset: SalesforceReportingAsset) -> list[dict]:
        """
        Fetch Salesforce Reporting assets
        """
        logger.info(f"Starting extraction of {asset}")

        if asset in REQUIRING_URL_ASSETS:
            return list(self._fetch_and_add_url(asset))

        return list(self._query_all(queries[asset]))
