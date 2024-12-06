from functools import partial
from http import HTTPStatus
from typing import Callable, Dict, Iterator, List, Optional, Tuple

import requests

from ....utils import (
    APIClient,
    BearerAuth,
    RequestSafeMode,
    build_url,
    fetch_all_pages,
    handle_response,
)
from ..assets import SigmaAsset
from .credentials import SigmaCredentials
from .endpoints import SigmaEndpointFactory
from .pagination import SIGMA_API_LIMIT, SigmaPagination

_CONTENT_TYPE = "application/x-www-form-urlencoded"

_DATA_ELEMENTS: Tuple[str, ...] = (
    "input-table",
    "pivot-table",
    "table",
    "visualization",
    "viz",
)

_AUTH_TIMEOUT_S = 60
_SIGMA_TIMEOUT = 120

_SIGMA_HEADERS = {
    "Content-Type": _CONTENT_TYPE,
}

_VOLUME_IGNORED = 10_000
_IGNORED_ERROR_CODES = (
    HTTPStatus.BAD_REQUEST,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.CONFLICT,
    HTTPStatus.NOT_FOUND,
)
SIGMA_SAFE_MODE = RequestSafeMode(
    max_errors=_VOLUME_IGNORED,
    status_codes=_IGNORED_ERROR_CODES,
)


class SigmaBearerAuth(BearerAuth):
    def __init__(self, host: str, token_payload: Dict[str, str]):
        auth_endpoint = SigmaEndpointFactory.authentication()
        self.authentication_url = build_url(host, auth_endpoint)
        self.token_payload = token_payload

    def fetch_token(self):
        token_api_path = self.authentication_url
        token_response = requests.post(
            token_api_path, data=self.token_payload, timeout=_AUTH_TIMEOUT_S
        )
        return handle_response(token_response)["access_token"]


class SigmaClient(APIClient):
    def __init__(
        self,
        credentials: SigmaCredentials,
        safe_mode: Optional[RequestSafeMode] = None,
    ):
        auth = SigmaBearerAuth(
            host=credentials.host,
            token_payload=credentials.token_payload,
        )
        super().__init__(
            host=credentials.host,
            auth=auth,
            headers=_SIGMA_HEADERS,
            timeout=_SIGMA_TIMEOUT,
            safe_mode=safe_mode or SIGMA_SAFE_MODE,
        )

    def _get_paginated(self, endpoint: str) -> Callable:
        return partial(
            self._get, endpoint=endpoint, params={"limit": SIGMA_API_LIMIT}
        )

    def _get_all_datasets(self) -> Iterator[dict]:
        request = self._get_paginated(endpoint=SigmaEndpointFactory.datasets())
        yield from fetch_all_pages(request, SigmaPagination)

    def _get_all_files(self) -> Iterator[dict]:
        request = self._get_paginated(endpoint=SigmaEndpointFactory.files())
        yield from fetch_all_pages(request, SigmaPagination)

    def _get_all_members(self) -> Iterator[dict]:
        request = self._get_paginated(endpoint=SigmaEndpointFactory.members())
        yield from fetch_all_pages(request, SigmaPagination)

    def _get_all_workbooks(self) -> Iterator[dict]:
        request = self._get_paginated(endpoint=SigmaEndpointFactory.workbooks())
        yield from fetch_all_pages(request, SigmaPagination)

    def _get_elements_per_page(
        self, page: dict, workbook_id: str
    ) -> Iterator[dict]:
        page_id = page["pageId"]
        request = self._get_paginated(
            SigmaEndpointFactory.elements(workbook_id, page_id)
        )
        elements = fetch_all_pages(request, SigmaPagination)
        for element in elements:
            if element.get("type") not in _DATA_ELEMENTS:
                continue
            yield {
                **element,
                "workbook_id": workbook_id,
                "page_id": page_id,
            }

    def _get_all_elements(self, workbooks: List[dict]) -> Iterator[dict]:
        for workbook in workbooks:
            workbook_id = workbook["workbookId"]

            request = self._get_paginated(
                SigmaEndpointFactory.pages(workbook_id)
            )
            pages = fetch_all_pages(request, SigmaPagination)

            for page in pages:
                yield from self._get_elements_per_page(
                    page=page, workbook_id=workbook_id
                )

    def _get_all_lineages(self, elements: List[dict]) -> Iterator[dict]:
        for element in elements:
            workbook_id = element["workbook_id"]
            element_id = element["elementId"]
            lineage = self._get(
                endpoint=SigmaEndpointFactory.lineage(workbook_id, element_id)
            )
            yield {
                **lineage,
                "workbook_id": workbook_id,
                "element_id": element_id,
            }

    def _get_all_queries(self, workbooks: List[dict]) -> Iterator[dict]:
        for workbook in workbooks:
            workbook_id = workbook["workbookId"]
            request = self._get_paginated(
                SigmaEndpointFactory.queries(workbook_id)
            )
            queries = fetch_all_pages(request, SigmaPagination)

            for query in queries:
                yield {**query, "workbook_id": workbook_id}

    def fetch(
        self,
        asset: SigmaAsset,
        workbooks: Optional[List[dict]] = None,
        elements: Optional[List[dict]] = None,
    ) -> Iterator[dict]:
        """Returns the needed metadata for the queried asset"""
        if asset == SigmaAsset.DATASETS:
            yield from self._get_all_datasets()

        elif asset == SigmaAsset.ELEMENTS:
            if not workbooks:
                raise ValueError("Missing workbooks to extract elements")

            yield from self._get_all_elements(workbooks)

        elif asset == SigmaAsset.FILES:
            yield from self._get_all_files()

        elif asset == SigmaAsset.LINEAGES:
            if not elements:
                raise ValueError("Missing elements to extract lineage")
            yield from self._get_all_lineages(elements)

        elif asset == SigmaAsset.MEMBERS:
            yield from self._get_all_members()

        elif asset == SigmaAsset.QUERIES:
            if not workbooks:
                raise ValueError("Missing workbooks to extract queries")

            yield from self._get_all_queries(workbooks)

        elif asset == SigmaAsset.WORKBOOKS:
            yield from self._get_all_workbooks()

        else:
            raise ValueError(f"This asset {asset} is unknown")
