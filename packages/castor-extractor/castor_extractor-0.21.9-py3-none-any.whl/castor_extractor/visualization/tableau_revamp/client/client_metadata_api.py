from typing import Dict, Iterator, Optional

import tableauserverclient as TSC  # type: ignore

from ....utils import SerializedAsset, retry
from ..assets import TableauRevampAsset
from ..constants import DEFAULT_PAGE_SIZE
from .errors import TableauApiError, TableauApiTimeout
from .gql_queries import FIELDS_QUERIES, GQL_QUERIES, QUERY_TEMPLATE

# increase the value when extraction is too slow
# decrease the value when timeouts arise
_CUSTOM_PAGE_SIZE: Dict[TableauRevampAsset, int] = {
    # for some clients, extraction of columns tend to hit the node limit
    # https://community.tableau.com/s/question/0D54T00000YuK60SAF/metadata-query-nodelimitexceeded-error
    # the workaround is to reduce pagination
    TableauRevampAsset.COLUMN: 50,
    # fields are light but volumes are bigger
    TableauRevampAsset.FIELD: 1000,
    TableauRevampAsset.TABLE: 50,
}

_TIMEOUT_MESSAGE = (
    "Execution canceled because timeout of 30000 millis was reached"
)

_RETRY_BASE_MS = 10_000
_RETRY_COUNT = 4


def _check_errors(answer: dict) -> None:
    """
    handle errors in graphql response:
    - return None when there's no errors in the answer
    - TableauApiTimeout if any of the errors is a timeout
    - TableauApiError (generic) otherwise
    """
    if "errors" not in answer:
        return

    errors = answer["errors"]

    for error in errors:
        if error.get("message") == _TIMEOUT_MESSAGE:
            # we need specific handling for timeout issues (retry strategy)
            raise TableauApiTimeout(errors)

    raise TableauApiError(answer["errors"])


def gql_query_scroll(
    server,
    query: str,
    resource: str,
) -> Iterator[SerializedAsset]:
    """
    Iterate over GQL query results, handling pagination and cursor

    We have a retry strategy when timeout issues arise.
    It's a known issue on Tableau side, still waiting for their fix:
    https://issues.salesforce.com/issue/a028c00000zKahoAAC/undefined
    """

    @retry(
        exceptions=(TableauApiTimeout,),
        max_retries=_RETRY_COUNT,
        base_ms=_RETRY_BASE_MS,
    )
    def _call(cursor: Optional[str]) -> dict:
        # If cursor is defined it must be quoted else use null token
        token = "null" if cursor is None else f'"{cursor}"'
        query_ = query.replace("AFTER_TOKEN_SIGNAL", token)
        answer = server.metadata.query(query_)
        _check_errors(answer)
        return answer["data"][f"{resource}Connection"]

    cursor = None
    while True:
        payload = _call(cursor)
        yield payload["nodes"]

        page_info = payload["pageInfo"]
        if page_info["hasNextPage"]:
            cursor = page_info["endCursor"]
        else:
            break


class TableauClientMetadataApi:
    """
    Calls the MetadataAPI, using graphQL
    https://help.tableau.com/current/api/metadata_api/en-us/reference/index.html
    """

    def __init__(
        self,
        server: TSC.Server,
        override_page_size: Optional[int] = None,
    ):
        self._server = server
        self._forced_page_size = override_page_size

    def _call(
        self,
        resource: str,
        fields: str,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> SerializedAsset:
        query = QUERY_TEMPLATE.format(
            resource=resource,
            fields=fields,
            page_size=page_size,
        )
        result_pages = gql_query_scroll(self._server, query, resource)
        return [asset for page in result_pages for asset in page]

    def _page_size(self, asset: TableauRevampAsset) -> int:
        return (
            self._forced_page_size
            or _CUSTOM_PAGE_SIZE.get(asset)
            or DEFAULT_PAGE_SIZE
        )

    def _fetch_fields(self) -> SerializedAsset:
        result: SerializedAsset = []
        page_size = self._page_size(TableauRevampAsset.FIELD)
        for resource, fields in FIELDS_QUERIES:
            current = self._call(resource, fields, page_size)
            result.extend(current)
        return result

    def fetch(
        self,
        asset: TableauRevampAsset,
    ) -> SerializedAsset:
        if asset == TableauRevampAsset.FIELD:
            return self._fetch_fields()

        page_size = self._page_size(asset)
        resource, fields = GQL_QUERIES[asset]
        return self._call(resource, fields, page_size)
