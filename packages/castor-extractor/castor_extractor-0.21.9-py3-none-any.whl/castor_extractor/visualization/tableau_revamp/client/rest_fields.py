from typing import Dict, Set

from ..assets import TableauRevampAsset

# list of fields to pick in REST API or TSC responses
REST_FIELDS: Dict[TableauRevampAsset, Set[str]] = {
    TableauRevampAsset.DATASOURCE: {
        "id",
        "project_id",
        "webpage_url",
    },
    TableauRevampAsset.METRIC: {
        "id",
        "definition_id",
    },
    TableauRevampAsset.METRIC_DEFINITION: {
        "metadata",
        "specification",
    },
    TableauRevampAsset.PROJECT: {
        "description",
        "id",
        "name",
        "parent_id",
    },
    TableauRevampAsset.SUBSCRIPTION: {
        "follower",
        "id",
        "metric_id",
    },
    TableauRevampAsset.USAGE: {
        "name",
        "total_views",
        "workbook_id",
    },
    TableauRevampAsset.USER: {
        "email",
        "fullname",
        "id",
        "name",
        "site_role",
    },
    TableauRevampAsset.WORKBOOK: {
        "id",
        "project_id",
    },
}
