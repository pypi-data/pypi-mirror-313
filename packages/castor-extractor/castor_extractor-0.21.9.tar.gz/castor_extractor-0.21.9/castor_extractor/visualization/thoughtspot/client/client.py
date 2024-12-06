from typing import Dict, Iterator, Optional

import requests

from ....utils import (
    APIClient,
    BearerAuth,
    RequestSafeMode,
    build_url,
    handle_response,
)
from ..assets import (
    ThoughtspotAsset,
)
from .credentials import (
    ThoughtspotCredentials,
)
from .endpoints import (
    ThoughtspotEndpointFactory,
)
from .utils import (
    usage_liveboard_reader,
)

_AUTH_TIMEOUT_S = 60
_THOUGHTSPOT_HEADERS = {
    "X-Requested-By": "ThoughtSpot",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
_METADATA_BATCH_SIZE = 100
_USAGE_LIVEBOARD_ID = "bea79810-145f-4ad0-a02c-4177a6e7d861"
# By default, no errors are ignored for the moment
THOUGHTSPOT_SAFE_MODE = RequestSafeMode()


class ThoughtspotBearerAuth(BearerAuth):
    def __init__(self, host: str, token_payload: Dict[str, str]):
        auth_endpoint = ThoughtspotEndpointFactory.authentication()
        self.authentication_url = build_url(host, auth_endpoint)
        self.token_payload = token_payload

    def fetch_token(self):
        token_api_path = self.authentication_url
        token_response = requests.post(
            token_api_path, data=self.token_payload, timeout=_AUTH_TIMEOUT_S
        )
        return handle_response(token_response)["token"]


class ThoughtspotClient(APIClient):
    def __init__(
        self,
        credentials: ThoughtspotCredentials,
        safe_mode: Optional[RequestSafeMode] = None,
    ):
        auth = ThoughtspotBearerAuth(
            host=credentials.base_url,
            token_payload=credentials.dict(),
        )
        super().__init__(
            host=credentials.base_url,
            auth=auth,
            headers=_THOUGHTSPOT_HEADERS,
            safe_mode=safe_mode or THOUGHTSPOT_SAFE_MODE,
        )

    def _metadata_search(
        self,
        metadata_type: str,
    ) -> Iterator[dict]:
        offset = 0
        while True:
            metadata = self._post(
                ThoughtspotEndpointFactory.metadata_search(),
                data={
                    "metadata": [{"type": metadata_type}],
                    "include_details": True,
                    "record_size": _METADATA_BATCH_SIZE,
                    "record_offset": offset,
                },
            )
            yield from metadata
            if len(metadata) < _METADATA_BATCH_SIZE:
                break
            offset = offset + _METADATA_BATCH_SIZE

    def _get_all_liveboards(self) -> Iterator[dict]:
        yield from self._metadata_search(metadata_type="LIVEBOARD")

    def _get_all_columns(self) -> Iterator[dict]:
        yield from self._metadata_search(metadata_type="LOGICAL_COLUMN")

    def _get_all_tables(self) -> Iterator[dict]:
        yield from self._metadata_search(metadata_type="LOGICAL_TABLE")

    def _get_liveboards_usages(self) -> Iterator[dict]:
        data = self._post(
            endpoint=ThoughtspotEndpointFactory.liveboard(),
            headers={"Accept": "application/octet-stream"},
            data={
                "metadata_identifier": _USAGE_LIVEBOARD_ID,
                "file_format": "CSV",
                "visualization_identifiers": [
                    "Popular Liveboards Last 30 Days"
                ],
            },
            handler=lambda x: x.text,
        )
        yield from usage_liveboard_reader(data)

    def fetch(self, asset: ThoughtspotAsset):
        if asset == ThoughtspotAsset.LIVEBOARDS:
            yield from self._get_all_liveboards()

        if asset == ThoughtspotAsset.USAGES:
            yield from self._get_liveboards_usages()

        if asset == ThoughtspotAsset.LOGICAL_TABLES:
            yield from self._get_all_tables()
