import logging
from functools import partial
from http import HTTPStatus
from typing import Iterator, List, Optional, Set, Tuple

import requests

from ...utils import (
    APIClient,
    BearerAuth,
    SafeMode,
    build_url,
    fetch_all_pages,
    handle_response,
    retry,
    retry_request,
    safe_mode,
)
from ..abstract import TimeFilter
from .credentials import DatabricksCredentials
from .endpoints import DatabricksEndpointFactory
from .format import DatabricksFormatter, TagMapping
from .lineage import single_column_lineage_links, single_table_lineage_links
from .pagination import DATABRICKS_PAGE_SIZE, DatabricksPagination
from .types import TablesColumns, TimestampedLink
from .utils import hourly_time_filters

logger = logging.getLogger(__name__)

_DATABRICKS_CLIENT_TIMEOUT_S = 90
_MAX_NUMBER_OF_LINEAGE_ERRORS = 1000
_MAX_NUMBER_OF_QUERY_ERRORS = 1000
_RETRY_ATTEMPTS = 3
_RETRY_BASE_MS = 1000
_RETRY_EXCEPTIONS = [
    requests.exceptions.ConnectTimeout,
]
_WORKSPACE_ID_HEADER = "X-Databricks-Org-Id"

safe_lineage_params = SafeMode((BaseException,), _MAX_NUMBER_OF_LINEAGE_ERRORS)
safe_query_params = SafeMode((BaseException,), _MAX_NUMBER_OF_QUERY_ERRORS)


class DatabricksAuth(BearerAuth):
    def __init__(self, credentials: DatabricksCredentials):
        self.token = credentials.token

    def fetch_token(self) -> Optional[str]:
        return self.token


class DatabricksAPIClient(APIClient):
    """Databricks Client"""

    def __init__(
        self,
        credentials: DatabricksCredentials,
        db_allowed: Optional[Set[str]] = None,
        db_blocked: Optional[Set[str]] = None,
    ):
        auth = DatabricksAuth(credentials)
        super().__init__(
            host=credentials.host,
            auth=auth,
            timeout=_DATABRICKS_CLIENT_TIMEOUT_S,
        )
        self._http_path = credentials.http_path
        self._db_allowed = db_allowed
        self._db_blocked = db_blocked

        self.formatter = DatabricksFormatter()

    def _keep_catalog(self, catalog: str) -> bool:
        """
        Helper function to determine if we should keep the Databricks catalog
        which is a CastorDoc database
        """
        if self._db_allowed and catalog not in self._db_allowed:
            return False
        if self._db_blocked and catalog in self._db_blocked:
            return False
        return True

    def databases(self) -> List[dict]:
        content = self._get(DatabricksEndpointFactory.databases())
        _databases = self.formatter.format_database(content.get("catalogs", []))
        return [d for d in _databases if self._keep_catalog(d["database_name"])]

    def _schemas_of_database(self, database: dict) -> List[dict]:
        payload = {"catalog_name": database["database_name"]}
        content = self._get(DatabricksEndpointFactory.schemas(), params=payload)
        schemas = content.get("schemas", [])
        return self.formatter.format_schema(schemas, database)

    def schemas(self, databases: List[dict]) -> List[dict]:
        """
        Get the databricks schemas (also sometimes called databases)
        (which correspond to the schemas in Castor)
        leveraging the unity catalog API
        """
        return [
            schema
            for database in databases
            for schema in self._schemas_of_database(database)
        ]

    def tables_columns_of_schema(
        self,
        schema: dict,
        table_tags: TagMapping,
        column_tags: TagMapping,
    ) -> TablesColumns:
        payload = {
            "catalog_name": schema["database_id"],
            "schema_name": schema["schema_name"],
        }
        response = self._call(
            method="GET",
            endpoint=DatabricksEndpointFactory.tables(),
            params=payload,
        )
        workspace_id = response.headers[_WORKSPACE_ID_HEADER]
        content = handle_response(response)
        host = build_url(self._host, endpoint="")
        return self.formatter.format_table_column(
            raw_tables=content.get("tables", []),
            schema=schema,
            host=host,
            workspace_id=workspace_id,
            table_tags=table_tags,
            column_tags=column_tags,
        )

    @safe_mode(safe_lineage_params, lambda: [])
    @retry(
        exceptions=_RETRY_EXCEPTIONS,
        max_retries=_RETRY_ATTEMPTS,
        base_ms=_RETRY_BASE_MS,
    )
    @retry_request(
        status_codes=(HTTPStatus.TOO_MANY_REQUESTS,),
        max_retries=_RETRY_ATTEMPTS,
    )
    def get_single_column_lineage(
        self,
        names: Tuple[str, str],
    ) -> List[TimestampedLink]:
        """
        Helper function used in get_lineage_links.
        Call data lineage API and return the content of the result

        eg table_path: broward_prd.bronze.account_adjustments
        FYI: Maximum rate of 10 requests per SECOND
        """
        table_path, column_name = names
        payload = {
            "table_name": table_path,
            "column_name": column_name,
            "include_entity_lineage": True,
        }
        content = self._get(
            DatabricksEndpointFactory.column_lineage(), params=payload
        )
        column_path = f"{table_path}.{column_name}"
        return single_column_lineage_links(column_path, content)

    @safe_mode(safe_lineage_params, lambda: [])
    @retry(
        exceptions=_RETRY_EXCEPTIONS,
        max_retries=_RETRY_ATTEMPTS,
        base_ms=_RETRY_BASE_MS,
    )
    def get_single_table_lineage(
        self, table_path: str
    ) -> List[TimestampedLink]:
        """
        Helper function used in get_lineage_links.
        Call data lineage API and return the content of the result
        eg table_path: broward_prd.bronze.account_adjustments
        FYI: Maximum rate of 50 requests per SECOND
        """
        payload = {"table_name": table_path, "include_entity_lineage": True}
        content = self._get(
            DatabricksEndpointFactory.table_lineage(), params=payload
        )
        return single_table_lineage_links(table_path, content)

    @safe_mode(safe_query_params, lambda: [])
    @retry(
        exceptions=_RETRY_EXCEPTIONS,
        max_retries=_RETRY_ATTEMPTS,
        base_ms=_RETRY_BASE_MS,
    )
    def _queries(
        self,
        filter_: dict,
    ) -> Iterator[dict]:
        """
        Callback to scroll the queries api
        https://docs.databricks.com/api/workspace/queryhistory/list
        max_results: Limit the number of results returned in one page.
            The default is 100. (both on our side and Databricks')
        """
        payload = {**filter_, "max_results": DATABRICKS_PAGE_SIZE}
        request = partial(
            self._get,
            endpoint=DatabricksEndpointFactory.queries(),
            data=payload,
        )
        queries = fetch_all_pages(request, DatabricksPagination)
        return queries

    def queries(self, time_filter: Optional[TimeFilter] = None) -> List[dict]:
        """get all queries, hour per hour"""
        time_range_filters = hourly_time_filters(time_filter)
        raw_queries = []
        for _filter in time_range_filters:
            logger.info(f"Fetching queries for time filter {_filter}")
            hourly = self._queries(_filter)
            raw_queries.extend(hourly)
        return self.formatter.format_query(raw_queries)

    def users(self) -> List[dict]:
        """
        retrieve user from api
        """
        content = self._get(DatabricksEndpointFactory.users())
        return self.formatter.format_user(content.get("Resources", []))

    def _view_ddl_per_schema(self, schema: dict) -> List[dict]:
        payload = {
            "catalog_name": schema["database_id"],
            "schema_name": schema["schema_name"],
            "omit_columns": True,
        }
        content = self._get(DatabricksEndpointFactory.tables(), params=payload)
        return self.formatter.format_view_ddl(content.get("tables", []), schema)

    def view_ddl(self, schemas: List[dict]) -> List[dict]:
        """retrieve view ddl"""
        view_ddl: List[dict] = []
        for schema in schemas:
            v_to_add = self._view_ddl_per_schema(schema)
            view_ddl.extend(v_to_add)
        return view_ddl
