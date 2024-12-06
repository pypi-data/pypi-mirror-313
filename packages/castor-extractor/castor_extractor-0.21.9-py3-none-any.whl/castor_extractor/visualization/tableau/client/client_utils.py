from typing import Dict, Iterator, Optional

from ....utils import SerializedAsset
from ..assets import TableauAsset
from ..gql_fields import QUERY_FIELDS
from ..tsc_fields import TSC_FIELDS

QUERY_TEMPLATE = """
{{
  {object_type}Connection(first: {page_size}, after: AFTER_TOKEN_SIGNAL) {{
    nodes {{ {query_fields}
    }}
    pageInfo {{
      hasNextPage
      endCursor
    }}
    totalCount
  }}
}}
"""

RESOURCE_TEMPLATE = "{resource}Connection"


def get_paginated_objects(
    server,
    asset: TableauAsset,
    page_size: int,
) -> SerializedAsset:
    assets: SerializedAsset = []
    for query in QUERY_FIELDS[asset]:
        fields = query["fields"].value
        object_type = query["object_type"].value
        query_formatted = QUERY_TEMPLATE.format(
            object_type=object_type,
            page_size=page_size,
            query_fields=fields,
        )
        resource = RESOURCE_TEMPLATE.format(resource=object_type)
        result_pages = query_scroll(server, query_formatted, resource)
        queried_assets = [asset for page in result_pages for asset in page]
        assets.extend(queried_assets)
    return assets


def query_scroll(
    server,
    query: str,
    resource: str,
) -> Iterator[SerializedAsset]:
    """build a tableau query iterator handling pagination and cursor"""

    def _call(cursor: Optional[str]) -> dict:
        # If cursor is defined it must be quoted else use null token
        token = "null" if cursor is None else f'"{cursor}"'
        query_ = query.replace("AFTER_TOKEN_SIGNAL", token)

        return server.metadata.query(query_)["data"][resource]

    cursor = None
    while True:
        payload = _call(cursor)
        yield payload["nodes"]

        page_info = payload["pageInfo"]
        if page_info["hasNextPage"]:
            cursor = page_info["endCursor"]
        else:
            break


def extract_asset(asset: Dict, asset_type: TableauAsset) -> Dict:
    """Agnostic function extracting dedicated attributes with define asset"""
    return {key: getattr(asset, key) for key in TSC_FIELDS[asset_type]}
