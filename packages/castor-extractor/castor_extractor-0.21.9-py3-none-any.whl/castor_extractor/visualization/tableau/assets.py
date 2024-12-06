from enum import Enum
from typing import Set

from ...types import ExternalAsset, classproperty


class TableauAsset(ExternalAsset):
    """
    Tableau assets
    """

    CUSTOM_SQL_TABLE = "custom_sql_tables"
    CUSTOM_SQL_QUERY = "custom_sql_queries"
    DASHBOARD = "dashboards"
    DASHBOARD_SHEET = "dashboards_sheets"
    DATASOURCE = "datasources"
    FIELD = "fields"
    PROJECT = "projects"
    PUBLISHED_DATASOURCE = "published_datasources"
    SHEET = "sheets"
    USAGE = "views"
    USER = "users"
    WORKBOOK = "workbooks"
    WORKBOOK_TO_DATASOURCE = "workbooks_to_datasource"

    @classproperty
    def optional(cls) -> Set["TableauAsset"]:
        return {
            TableauAsset.DASHBOARD,
            TableauAsset.DASHBOARD_SHEET,
            TableauAsset.FIELD,
            TableauAsset.SHEET,
            TableauAsset.PUBLISHED_DATASOURCE,
        }


class TableauGraphqlAsset(Enum):
    """
    Assets which can be fetched from Tableau
    """

    BIN_FIELD = "binFields"
    CALCULATED_FIELD = "calculatedFields"
    COLUMN_FIELD = "columnFields"
    CUSTOM_SQL = "customSQLTables"
    DASHBOARD = "dashboards"
    DATASOURCE = "datasources"
    GROUP_FIELD = "groupFields"
    SHEETS = "sheets"
    WORKBOOK_TO_DATASOURCE = "workbooks"
