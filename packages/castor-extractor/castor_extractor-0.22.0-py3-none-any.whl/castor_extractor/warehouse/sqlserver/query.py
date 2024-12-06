from typing import Optional

from ..abstract import (
    AbstractQueryBuilder,
    ExtractionQuery,
    TimeFilter,
    WarehouseAsset,
)


class MSSQLQueryBuilder(AbstractQueryBuilder):
    """
    Builds queries to extract assets from SQL Server.
    """

    def __init__(
        self,
        time_filter: Optional[TimeFilter] = None,
    ):
        super().__init__(time_filter=time_filter)

    def build(self, asset: WarehouseAsset) -> list[ExtractionQuery]:
        query = self.build_default(asset)
        return [query]
