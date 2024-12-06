# TSC for TableauServerClient: basic REST API to extracting core objects
from typing import Dict, Set

from .assets import TableauAsset

# TSC fields extracted per assets
TSC_FIELDS: Dict[TableauAsset, Set[str]] = {
    TableauAsset.PROJECT: {
        "id",
        "name",
        "description",
        "parent_id",
    },
    TableauAsset.PUBLISHED_DATASOURCE: {
        "id",
        "name",
        "description",
        "tags",
        "project_id",
        "created_at",
        "updated_at",
        "owner_id",
        "webpage_url",
    },
    TableauAsset.USAGE: {
        "workbook_id",
        "total_views",
    },
    TableauAsset.USER: {
        "id",
        "name",
        "email",
        "fullname",
        "site_role",
    },
    TableauAsset.WORKBOOK: {
        "id",
        "name",
        "description",
        "tags",
        "project_id",
        "created_at",
        "updated_at",
        "owner_id",
        "webpage_url",
    },
}
