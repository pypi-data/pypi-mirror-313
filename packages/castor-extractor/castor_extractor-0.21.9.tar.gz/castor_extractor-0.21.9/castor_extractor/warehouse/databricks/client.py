import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Set

from ...utils import (
    mapping_from_rows,
)
from ..abstract import TimeFilter
from .api_client import DatabricksAPIClient
from .credentials import DatabricksCredentials
from .format import DatabricksFormatter
from .lineage import deduplicate_lineage, paths_for_column_lineage
from .sql_client import DatabricksSQLClient, TagEntity
from .types import TablesColumns, TimestampedLink

logger = logging.getLogger(__name__)

_THREADS_COLUMN_LINEAGE = 2
_THREADS_TABLE_LINEAGE = 10


class DatabricksClient:
    """Databricks Client"""

    def __init__(
        self,
        credentials: DatabricksCredentials,
        db_allowed: Optional[Set[str]] = None,
        db_blocked: Optional[Set[str]] = None,
        has_table_tags: bool = False,
        has_column_tags: bool = False,
    ):
        self.api_client = DatabricksAPIClient(
            credentials=credentials,
            db_allowed=db_allowed,
            db_blocked=db_blocked,
        )
        self.sql_client = DatabricksSQLClient(
            credentials=credentials,
            has_table_tags=has_table_tags,
            has_column_tags=has_column_tags,
        )

        self.formatter = DatabricksFormatter()

    @staticmethod
    def name() -> str:
        return "Databricks"

    @staticmethod
    def _match_table_with_user(table: dict, user_mapping: dict) -> dict:
        table_owner_email = table.get("owner_email")
        if not table_owner_email:
            return table
        owner_external_id = user_mapping.get(table_owner_email)
        if not owner_external_id:
            return table
        return {**table, "owner_external_id": owner_external_id}

    @staticmethod
    def _get_user_mapping(users: List[dict]) -> dict:
        return {
            **mapping_from_rows(users, "email", "id"),
            **mapping_from_rows(users, "user_name", "id"),
        }

    def schemas(self, databases: List[dict]) -> List[dict]:
        return self.api_client.schemas(databases)

    def databases(self) -> List[dict]:
        return self.api_client.databases()

    def tables_and_columns(
        self, schemas: List[dict], users: List[dict]
    ) -> TablesColumns:
        """
        Get the databricks tables & columns leveraging the unity catalog API
        """
        tables: List[dict] = []
        columns: List[dict] = []
        user_mapping = self._get_user_mapping(users)
        table_tags = self.sql_client.get_tags_mapping(TagEntity.TABLE)
        column_tags = self.sql_client.get_tags_mapping(TagEntity.COLUMN)
        for schema in schemas:
            t_to_add, c_to_add = self.api_client.tables_columns_of_schema(
                schema=schema,
                table_tags=table_tags,
                column_tags=column_tags,
            )
            t_with_owner = [
                self._match_table_with_user(table, user_mapping)
                for table in t_to_add
            ]
            tables.extend(t_with_owner)
            columns.extend(c_to_add)
        return tables, columns

    def table_lineage(self, tables: List[dict]) -> List[dict]:
        """
        Wrapper function that retrieves all table lineage
        """
        # retrieve table lineage
        with ThreadPoolExecutor(max_workers=_THREADS_TABLE_LINEAGE) as executor:
            table_paths = [
                ".".join([table["schema_id"], table["table_name"]])
                for table in tables
            ]
            results = executor.map(
                self.api_client.get_single_table_lineage, table_paths
            )
        lineages = [link for links in results for link in links]
        deduplicated = deduplicate_lineage(lineages)
        return self.formatter.format_lineage(deduplicated)

    def column_lineage(
        self, tables: List[dict], columns: List[dict], table_lineage: List[dict]
    ) -> List[dict]:
        """
        Wrapper function that retrieves all column lineage
        we only try to retrieve column lineage if we found table lineage
        """
        candidate_paths = paths_for_column_lineage(
            tables, columns, table_lineage
        )
        # retrieve column lineage
        with ThreadPoolExecutor(
            max_workers=_THREADS_COLUMN_LINEAGE
        ) as executor:
            results = executor.map(
                self.api_client.get_single_column_lineage, candidate_paths
            )
        lineages: List[TimestampedLink] = [
            link for links in results for link in links
        ]
        deduplicated = deduplicate_lineage(lineages)
        return self.formatter.format_lineage(deduplicated)

    def queries(self, time_filter: Optional[TimeFilter] = None) -> List[dict]:
        return self.api_client.queries(time_filter)

    def users(self) -> List[dict]:
        return self.api_client.users()

    def view_ddl(self, schemas: List[dict]) -> List[dict]:
        return self.api_client.view_ddl(schemas)
