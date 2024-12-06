import logging
from collections import defaultdict
from enum import Enum
from typing import Optional

from databricks import sql  # type: ignore

from .credentials import DatabricksCredentials
from .format import TagMapping
from .utils import build_path, tag_label

logger = logging.getLogger(__name__)

_INFORMATION_SCHEMA_SQL = "SELECT * FROM system.information_schema"


class TagEntity(Enum):
    """Entities that can be tagged in Databricks"""

    COLUMN = "COLUMN"
    TABLE = "TABLE"


class DatabricksSQLClient:
    def __init__(
        self,
        credentials: DatabricksCredentials,
        has_table_tags: bool = False,
        has_column_tags: bool = False,
    ):
        self._http_path = credentials.http_path
        self._has_table_tags = has_table_tags
        self._has_column_tags = has_column_tags
        self._host = credentials.host
        self._token = credentials.token

    def execute_sql(
        self,
        query: str,
        params: Optional[dict] = None,
    ):
        """
        Execute a SQL query on Databricks system tables and return the results.
        https://docs.databricks.com/en/dev-tools/python-sql-connector.html

        //!\\ credentials.http_path is required in order to run SQL queries
        """
        assert self._http_path, "HTTP_PATH is required to run SQL queries"
        with sql.connect(
            server_hostname=self._host,
            http_path=self._http_path,
            access_token=self._token,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def _needs_extraction(self, entity: TagEntity) -> bool:
        if entity == TagEntity.TABLE:
            return self._has_table_tags
        if entity == TagEntity.COLUMN:
            return self._has_column_tags
        raise AssertionError(f"Entity not supported: {entity}")

    def get_tags_mapping(self, entity: TagEntity) -> TagMapping:
        """
        Fetch tags of the given entity and build a mapping:
        { path: list[tags] }

        https://docs.databricks.com/en/sql/language-manual/information-schema/table_tags.html
        https://docs.databricks.com/en/sql/language-manual/information-schema/column_tags.html
        """
        if not self._needs_extraction(entity):
            # extracting tags require additional credentials (http_path)
            return dict()

        table = f"{entity.value.lower()}_tags"
        query = f"{_INFORMATION_SCHEMA_SQL}.{table}"
        result = self.execute_sql(query)
        mapping = defaultdict(list)
        for row in result:
            dict_row = row.asDict()
            keys = ["catalog_name", "schema_name", "table_name"]
            if entity == TagEntity.COLUMN:
                keys.append("column_name")
            path = build_path(dict_row, keys)
            label = tag_label(dict_row)
            mapping[path].append(label)

        return mapping
