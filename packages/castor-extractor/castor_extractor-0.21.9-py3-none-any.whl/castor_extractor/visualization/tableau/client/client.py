import logging
from typing import List

import tableauserverclient as TSC  # type: ignore

from ....utils import SerializedAsset
from ..assets import TableauAsset
from ..constants import PAGE_SIZE, TABLEAU_SERVER_VERSION
from ..usage import compute_usage_views
from .client_utils import extract_asset, get_paginated_objects
from .credentials import CredentialsApi, CredentialsKey, get_value
from .project import compute_project_path
from .safe_mode import safe_mode_fetch_usage

logger = logging.getLogger(__name__)


class ApiClient:
    """
    Connect to Tableau REST API and fetch main assets.
    Superuser credentials are required.
    https://tableau.github.io/server-client-python/docs/
    """

    def __init__(
        self,
        **kwargs,
    ):
        self._credentials = CredentialsApi(
            user=get_value(CredentialsKey.TABLEAU_USER, kwargs, True),
            password=get_value(CredentialsKey.TABLEAU_PASSWORD, kwargs, True),
            token_name=get_value(
                CredentialsKey.TABLEAU_TOKEN_NAME,
                kwargs,
                True,
            ),
            token=get_value(CredentialsKey.TABLEAU_TOKEN, kwargs, True),
            server_url=get_value(CredentialsKey.TABLEAU_SERVER_URL, kwargs),
            site_id=get_value(CredentialsKey.TABLEAU_SITE_ID, kwargs, True),
        )
        self._server = TSC.Server(self._credentials.server_url)
        self._server.add_http_options({"verify": True})
        self._page_size = PAGE_SIZE
        self._server.version = TABLEAU_SERVER_VERSION
        self._safe_mode = bool(kwargs.get("safe_mode"))
        self.errors: List[str] = []

    @staticmethod
    def name() -> str:
        return "Tableau/API"

    def _user_password_login(self) -> None:
        """Login into Tableau using user and password"""
        self._server.auth.sign_in(
            TSC.TableauAuth(
                self._credentials.user,
                self._credentials.password,
                site_id=self._credentials.site_id,
            ),
        )

    def _pat_login(self) -> None:
        """Login into Tableau using personal authentication token"""
        self._server.auth.sign_in(
            TSC.PersonalAccessTokenAuth(
                self._credentials.token_name,
                self._credentials.token,
                site_id=self._credentials.site_id,
            ),
        )

    def login(self) -> None:
        """Login into Tableau"""

        if self._credentials.user and self._credentials.password:
            logger.info("Logging in using user and password authentication")
            return self._user_password_login()

        if self._credentials.token_name and self._credentials.token:
            logger.info("Logging in using token authentication")
            return self._pat_login()

        raise ValueError(
            """Wrong authentication: you should provide either user and password
             or personal access token""",
        )

    def base_url(self) -> str:
        return self._credentials.server_url

    def _fetch_users(self) -> SerializedAsset:
        """Fetches list of User"""
        return [
            extract_asset(user, TableauAsset.USER)
            for user in TSC.Pager(self._server.users)
        ]

    def _fetch_workbooks(self) -> SerializedAsset:
        """Fetches list of Workbooks"""

        return [
            extract_asset(workbook, TableauAsset.WORKBOOK)
            for workbook in TSC.Pager(self._server.workbooks)
        ]

    def _fetch_usages(self, safe_mode: bool) -> SerializedAsset:
        """Fetches list of Usages"""
        if not safe_mode:
            usages = [
                extract_asset(usage, TableauAsset.USAGE)
                for usage in TSC.Pager(self._server.views, usage=True)
            ]

            return compute_usage_views(usages)

        return safe_mode_fetch_usage(self)

    def _fetch_projects(self) -> SerializedAsset:
        """Fetches list of Projects"""
        return compute_project_path(
            [
                extract_asset(project, TableauAsset.PROJECT)
                for project in TSC.Pager(self._server.projects)
            ],
        )

    def _fetch_workbooks_to_datasource(self) -> SerializedAsset:
        """Fetches workbooks to datasource"""

        return self._fetch_paginated_objects(
            TableauAsset.WORKBOOK_TO_DATASOURCE,
        )

    def _fetch_published_datasources(self) -> SerializedAsset:
        """Fetches list of published datasources"""

        return [
            extract_asset(datasource, TableauAsset.PUBLISHED_DATASOURCE)
            for datasource in TSC.Pager(self._server.datasources)
        ]

    def _fetch_datasources(self) -> SerializedAsset:
        """Fetches both embedded and published datasource"""

        return self._fetch_paginated_objects(
            TableauAsset.DATASOURCE,
        )

    def _fetch_fields(self) -> SerializedAsset:
        """Fetches fields"""
        return self._fetch_paginated_objects(
            TableauAsset.FIELD,
        )

    def _fetch_custom_sql_queries(self) -> SerializedAsset:
        """Fetches custom sql queries"""

        return self._fetch_paginated_objects(
            TableauAsset.CUSTOM_SQL_QUERY,
        )

    def _fetch_custom_sql_tables(self) -> SerializedAsset:
        """Fetches custom sql tables"""

        return self._fetch_paginated_objects(
            TableauAsset.CUSTOM_SQL_TABLE,
        )

    def _fetch_dashboards(self) -> SerializedAsset:
        """Fetches dashboards"""

        return self._fetch_paginated_objects(
            TableauAsset.DASHBOARD,
        )

    def _fetch_sheets(self) -> SerializedAsset:
        """Fetches sheets"""

        return self._fetch_paginated_objects(
            TableauAsset.SHEET,
        )

    def _fetch_paginated_objects(self, asset: TableauAsset) -> SerializedAsset:
        """Fetches paginated objects"""

        return get_paginated_objects(self._server, asset, self._page_size)

    def fetch(self, asset: TableauAsset) -> SerializedAsset:
        """Fetches the given asset"""
        logger.info(f"Fetching {asset.name}")

        if asset == TableauAsset.CUSTOM_SQL_QUERY:
            assets = self._fetch_custom_sql_queries()

        if asset == TableauAsset.CUSTOM_SQL_TABLE:
            assets = self._fetch_custom_sql_tables()

        if asset == TableauAsset.DASHBOARD:
            assets = self._fetch_dashboards()

        if asset == TableauAsset.DATASOURCE:
            assets = self._fetch_datasources()

        if asset == TableauAsset.FIELD:
            assets = self._fetch_fields()

        if asset == TableauAsset.PROJECT:
            assets = self._fetch_projects()

        if asset == TableauAsset.PUBLISHED_DATASOURCE:
            assets = self._fetch_published_datasources()

        if asset == TableauAsset.SHEET:
            assets = self._fetch_sheets()

        if asset == TableauAsset.USAGE:
            assets = self._fetch_usages(self._safe_mode)

        if asset == TableauAsset.USER:
            assets = self._fetch_users()

        if asset == TableauAsset.WORKBOOK:
            assets = self._fetch_workbooks()

        if asset == TableauAsset.WORKBOOK_TO_DATASOURCE:
            assets = self._fetch_workbooks_to_datasource()

        logger.info(f"Fetched {asset.name} ({len(assets)} results)")

        return assets
