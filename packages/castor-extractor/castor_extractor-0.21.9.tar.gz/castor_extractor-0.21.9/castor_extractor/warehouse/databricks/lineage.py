from typing import Dict, List, Set, Tuple, cast

from .types import Link, Ostr, OTimestampedLink, TimestampedLink


class LineageLinks:
    """
    helper class that handles lineage deduplication and filtering
    """

    def __init__(self):
        self.lineage: Dict[Link, Ostr] = dict()

    def add(self, timestamped_link: TimestampedLink) -> None:
        """
        keep the most recent lineage link, adding to `self.lineage`
        """
        parent, child, timestamp = timestamped_link
        link = (parent, child)
        if not self.lineage.get(link):
            self.lineage[link] = timestamp
            return

        if not timestamp:
            return
        # keep most recent link; cast for mypy
        recent = max(cast(str, self.lineage[link]), cast(str, timestamp))
        self.lineage[link] = recent


def _to_table_path(table: dict) -> Ostr:
    if table.get("name"):
        return f"{table['catalog_name']}.{table['schema_name']}.{table['name']}"
    return None


def _to_column_path(column: dict) -> Ostr:
    if column.get("name"):
        return f"{column['catalog_name']}.{column['schema_name']}.{column['table_name']}.{column['name']}"
    return None


def _link(path_from: Ostr, path_to: Ostr, timestamp: Ostr) -> OTimestampedLink:
    """exclude missing path and self-lineage"""
    if (not path_from) or (not path_to):
        return None
    is_self_lineage = path_from.lower() == path_to.lower()
    if is_self_lineage:
        return None
    return path_from, path_to, timestamp


def single_table_lineage_links(
    table_path: str, single_table_lineage: dict
) -> List[TimestampedLink]:
    """
    process databricks lineage API response for a given table
    returns a list of (parent, child, timestamp)

    Note: in `upstreams` or `downstreams` we only care about `tableInfo`,
    we could also have `notebookInfos` or `fileInfo`
    """
    links: List[OTimestampedLink] = []
    # add parent:
    for link in single_table_lineage.get("upstreams", []):
        parent = link.get("tableInfo", {})
        parent_path = _to_table_path(parent)
        timestamp: Ostr = parent.get("lineage_timestamp")
        links.append(_link(parent_path, table_path, timestamp))

    # add children:
    for link in single_table_lineage.get("downstreams", []):
        child = link.get("tableInfo", {})
        child_path = _to_table_path(child)
        timestamp = child.get("lineage_timestamp")
        links.append(_link(table_path, child_path, timestamp))

    return list(filter(None, links))


def single_column_lineage_links(
    column_path: str, single_column_lineage: dict
) -> List[TimestampedLink]:
    """
    process databricks lineage API response for a given table
    returns a list of (parent, child, timestamp)

    Note: in `upstreams` or `downstreams` we only care about `tableInfo`,
    we could also have `notebookInfos` or `fileInfo`
    """
    links: List[OTimestampedLink] = []
    # add parent:
    for link in single_column_lineage.get("upstream_cols", []):
        parent_path = _to_column_path(link)
        timestamp: Ostr = link.get("lineage_timestamp")
        links.append(_link(parent_path, column_path, timestamp))

    # add children:
    for link in single_column_lineage.get("downstream_cols", []):
        child_path = _to_column_path(link)
        timestamp = link.get("lineage_timestamp")
        links.append(_link(column_path, child_path, timestamp))

    return list(filter(None, links))


def paths_for_column_lineage(
    tables: List[dict], columns: List[dict], table_lineage: List[dict]
) -> List[Tuple[str, str]]:
    """
    helper providing a list of candidate columns to look lineage for:
    we only look for column lineage where there is table lineage
    """
    # mapping between table id and its path db.schema.table
    # table["schema_id"] follows the pattern `db.schema`
    mapping = {
        table["id"]: ".".join([table["schema_id"], table["table_name"]])
        for table in tables
    }

    tables_with_lineage: Set[str] = set()
    for t in table_lineage:
        tables_with_lineage.add(t["parent_path"])
        tables_with_lineage.add(t["child_path"])

    paths_to_return: List[Tuple[str, str]] = []
    for column in columns:
        table_path = mapping[column["table_id"]]
        if table_path not in tables_with_lineage:
            continue
        column_ = (table_path, column["column_name"])
        paths_to_return.append(column_)

    return paths_to_return


def deduplicate_lineage(lineages: List[TimestampedLink]) -> dict:
    deduplicated_lineage = LineageLinks()
    for timestamped_link in lineages:
        deduplicated_lineage.add(timestamped_link)
    return deduplicated_lineage.lineage
