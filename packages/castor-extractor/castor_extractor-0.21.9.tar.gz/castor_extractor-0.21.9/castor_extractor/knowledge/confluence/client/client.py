from functools import partial
from http import HTTPStatus
from typing import Iterator, Optional

from ....utils import (
    APIClient,
    BasicAuth,
    RequestSafeMode,
    fetch_all_pages,
)
from ..assets import (
    ConfluenceAsset,
)
from .credentials import ConfluenceCredentials
from .endpoints import ConfluenceEndpointFactory
from .pagination import ConfluencePagination

_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

_MAX_ERROR_IGNORED_COUNT = 10
_IGNORED_ERROR_CODES = (HTTPStatus.BAD_GATEWAY,)
_SAFE_MODE = RequestSafeMode(
    max_errors=_MAX_ERROR_IGNORED_COUNT,
    status_codes=_IGNORED_ERROR_CODES,
)


class ConfluenceClient(APIClient):
    def __init__(
        self,
        credentials: ConfluenceCredentials,
        safe_mode: Optional[RequestSafeMode] = None,
    ):
        self.account_id = credentials.account_id
        auth = BasicAuth(
            username=credentials.username, password=credentials.password
        )
        super().__init__(
            auth=auth,
            host=credentials.base_url,
            headers=_HEADERS,
            safe_mode=safe_mode or _SAFE_MODE,
        )

    def pages(self):
        request = partial(
            self._get,
            endpoint=ConfluenceEndpointFactory.pages(),
            params={"body-format": "atlas_doc_format"},
        )
        yield from fetch_all_pages(request, ConfluencePagination)

    def users(self):
        request_body = {"accountIds": [self.account_id]}
        request = partial(
            self._post,
            endpoint=ConfluenceEndpointFactory.users(),
            data=request_body,
        )
        yield from fetch_all_pages(request, ConfluencePagination)

    def fetch(self, asset: ConfluenceAsset) -> Iterator[dict]:
        """Returns the needed metadata for the queried asset"""
        if asset == ConfluenceAsset.PAGES:
            yield from self.pages()

        elif asset == ConfluenceAsset.USERS:
            yield from self.users()

        else:
            raise ValueError(f"This asset {asset} is unknown")
