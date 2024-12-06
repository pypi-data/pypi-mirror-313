from typing import Any, Dict, Iterable, Iterator

import tableauserverclient as TSC  # type: ignore

from ....utils import JsonType, SerializedAsset
from ..assets import TableauRevampAsset
from .rest_fields import REST_FIELDS


def _pick(element: Any, key: str) -> JsonType:
    if isinstance(element, dict):
        return element[key]
    else:
        return getattr(element, key)


class TableauClientTSC:
    """
    Extract Tableau Assets using TableauServerClient (TSC)
    https://tableau.github.io/server-client-python/docs/api-ref
    """

    def __init__(
        self,
        server: TSC.Server,
    ):
        self._server = server

    def _pick_fields(
        self,
        data: Iterable,
        asset: TableauRevampAsset,
    ) -> Iterator[Dict]:
        keys = REST_FIELDS[asset]

        for row in data:
            fields = {key: _pick(row, key) for key in keys}
            if asset == TableauRevampAsset.USER:
                self._server.users.populate_groups(row)
                fields["group_ids"] = [group.id for group in row.groups]

            yield fields

    def fetch(
        self,
        asset: TableauRevampAsset,
    ) -> SerializedAsset:
        if asset == TableauRevampAsset.DATASOURCE:
            data = TSC.Pager(self._server.datasources)

        elif asset == TableauRevampAsset.PROJECT:
            data = TSC.Pager(self._server.projects)

        elif asset == TableauRevampAsset.USAGE:
            data = TSC.Pager(self._server.views, usage=True)

        elif asset == TableauRevampAsset.USER:
            data = TSC.Pager(self._server.users)

        elif asset == TableauRevampAsset.WORKBOOK:
            data = TSC.Pager(self._server.workbooks)

        else:
            raise AssertionError(f"Fetching from TSC not supported for {asset}")

        return list(self._pick_fields(data, asset))
