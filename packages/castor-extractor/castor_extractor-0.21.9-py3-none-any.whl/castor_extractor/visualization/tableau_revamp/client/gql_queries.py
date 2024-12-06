from typing import Dict, Tuple

from ..assets import TableauRevampAsset

QUERY_TEMPLATE = """
{{
  {resource}Connection(first: {page_size}, after: AFTER_TOKEN_SIGNAL) {{
    nodes {{ {fields}
    }}
    pageInfo {{
      hasNextPage
      endCursor
    }}
    totalCount
  }}
}}
"""

_COLUMNS_QUERY = """
downstreamDashboards { id }
downstreamFields {
    id
    __typename
    datasource { id }
}
downstreamWorkbooks { id }
id
name
table { id }
"""

_DASHBOARDS_QUERY = """
createdAt
id
name
path
tags { name }
updatedAt
workbook { id }
"""

_DATASOURCES_QUERY = """
__typename
downstreamDashboards { id }
downstreamWorkbooks { id }
id
name
... on PublishedDatasource {
    description
    luid
    owner { luid }
    site { name }
    tags { name }
    uri
}
"""

_TABLES_QUERY = """
__typename
downstreamDashboards { id }
downstreamDatasources { id }
downstreamWorkbooks { id }
id
name
... on DatabaseTable {
    fullName
    schema
    database {
        connectionType
        id
        name
    }
}
... on CustomSQLTable {
    query
    database {
        connectionType
        id
        name
    }
}
"""


_WORKBOOKS_QUERY = """
createdAt
description
embeddedDatasources { id }
id
luid
name
owner { luid }
site { name }
tags { name }
updatedAt
uri
"""

_FIELDS_QUERY = """
__typename
datasource { id }
description
downstreamDashboards { id }
downstreamWorkbooks { id }
folderName
id
name
dataType
role
"""


_FIELDS_QUERY_WITH_COLUMNS = f"""
{_FIELDS_QUERY}
columns {{
    name
   table {{ name }}
}}
"""

_SHEETS_QUERY = """
containedInDashboards { id }
createdAt
id
index
name
updatedAt
upstreamFields { name }
workbook { id }
"""


GQL_QUERIES: Dict[TableauRevampAsset, Tuple[str, str]] = {
    TableauRevampAsset.COLUMN: ("columns", _COLUMNS_QUERY),
    TableauRevampAsset.DASHBOARD: ("dashboards", _DASHBOARDS_QUERY),
    TableauRevampAsset.DATASOURCE: ("datasources", _DATASOURCES_QUERY),
    TableauRevampAsset.SHEET: ("sheets", _SHEETS_QUERY),
    TableauRevampAsset.TABLE: ("tables", _TABLES_QUERY),
    TableauRevampAsset.WORKBOOK: ("workbooks", _WORKBOOKS_QUERY),
}

FIELDS_QUERIES = (
    ("binFields", _FIELDS_QUERY),
    ("calculatedFields", _FIELDS_QUERY),
    ("columnFields", _FIELDS_QUERY_WITH_COLUMNS),
    ("groupFields", _FIELDS_QUERY),
)
