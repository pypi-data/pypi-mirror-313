# Fields which will be use for Tableau GraphQL API
from enum import Enum
from typing import Dict, List, Union

from .assets import TableauAsset, TableauGraphqlAsset

FIELDS = "fields"
OBJECT_TYPE = "object_type"


class GQLQueryFields(Enum):
    BIN_FIELDS: str = """
           datasource {
               ... on PublishedDatasource {
                    name
                    luid
               }
           }
           dataType
           description
           fields {
               id
           }
           folderName
           id
           name
           role
    """

    CALCULATED_FIELDS: str = """
           datasource {
               ... on PublishedDatasource {
                    name
                    luid
               }
           }
           fields {
               id
           }
           dataType
           description
           folderName
           id
           name
           role

    """

    COLUMN_FIELDS: str = """
           columns {
               id
               name
               table {
                   ... on DatabaseTable {
                       id
                       description
                       name
                       fullName
                       schema
                       database {
                           name
                           luid
                       }
                   }
               }

           }
           datasource {
               ... on PublishedDatasource {
                    name
                    luid
               }
           }
           dataType
           description
           folderName
           id
           name
           role
    """

    CUSTOM_SQL_TABLE: str = """
           id
           name
           columns {
               referencedByFields {
                   datasource {
                       ... on PublishedDatasource {
                           luid
                       }

                       ... on EmbeddedDatasource {
                           id
                       }
                   }
               }
           }
    """

    CUSTOM_SQL_QUERY: str = """
           id
           name
           query
           database {
               name
               connectionType
           }
           tables {
               name
           }
    """

    DASHBOARDS: str = """
            id
            name
            path
            tags {
                name
            }
            workbook {
               luid # to retrieve the parent
            }
    """

    DATASOURCE: str = """
           ... on PublishedDatasource {
               luid
           }
           id
           name
           hasExtracts
           upstreamTables {
               id
               schema
               name
               fullName
               database {
                   id
                   name
                   connectionType
               }
           }
    """

    GROUP_FIELDS: str = """
           datasource {
               ... on PublishedDatasource {
                    name
                    luid
               }
           }
           dataType
           description
           fields {
               id
           }
           folderName
           id
           name
           role
    """

    SHEET: str = """
            containedInDashboards {
                id
            }
            id
            index
            name
            upstreamFields{
                name
            }
            workbook {
                luid
            }
    """

    WORKBOOK_TO_DATASOURCE: str = """
           luid
           id
           embeddedDatasources {
               id
               name
           }
           upstreamDatasources {
               luid
               name
           }
    """


QueryInfo = List[Dict[str, Union[GQLQueryFields, TableauGraphqlAsset]]]

QUERY_FIELDS: Dict[TableauAsset, QueryInfo] = {
    TableauAsset.CUSTOM_SQL_TABLE: [
        {
            FIELDS: GQLQueryFields.CUSTOM_SQL_TABLE,
            OBJECT_TYPE: TableauGraphqlAsset.CUSTOM_SQL,
        },
    ],
    TableauAsset.CUSTOM_SQL_QUERY: [
        {
            FIELDS: GQLQueryFields.CUSTOM_SQL_QUERY,
            OBJECT_TYPE: TableauGraphqlAsset.CUSTOM_SQL,
        },
    ],
    TableauAsset.DASHBOARD: [
        {
            FIELDS: GQLQueryFields.DASHBOARDS,
            OBJECT_TYPE: TableauGraphqlAsset.DASHBOARD,
        },
    ],
    TableauAsset.DATASOURCE: [
        {
            FIELDS: GQLQueryFields.DATASOURCE,
            OBJECT_TYPE: TableauGraphqlAsset.DATASOURCE,
        },
    ],
    TableauAsset.FIELD: [
        {
            FIELDS: GQLQueryFields.BIN_FIELDS,
            OBJECT_TYPE: TableauGraphqlAsset.BIN_FIELD,
        },
        {
            FIELDS: GQLQueryFields.CALCULATED_FIELDS,
            OBJECT_TYPE: TableauGraphqlAsset.CALCULATED_FIELD,
        },
        {
            FIELDS: GQLQueryFields.COLUMN_FIELDS,
            OBJECT_TYPE: TableauGraphqlAsset.COLUMN_FIELD,
        },
        {
            FIELDS: GQLQueryFields.GROUP_FIELDS,
            OBJECT_TYPE: TableauGraphqlAsset.GROUP_FIELD,
        },
    ],
    TableauAsset.SHEET: [
        {
            FIELDS: GQLQueryFields.SHEET,
            OBJECT_TYPE: TableauGraphqlAsset.SHEETS,
        },
    ],
    TableauAsset.WORKBOOK_TO_DATASOURCE: [
        {
            FIELDS: GQLQueryFields.WORKBOOK_TO_DATASOURCE,
            OBJECT_TYPE: TableauGraphqlAsset.WORKBOOK_TO_DATASOURCE,
        },
    ],
}
