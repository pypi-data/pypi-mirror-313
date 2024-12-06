from unittest.mock import Mock, patch

from .client import (
    DatabricksClient,
)
from .test_constants import (
    CLOSER_DATE,
    MOCK_TABLES_FOR_TABLE_LINEAGE,
    OLDER_DATE,
    TABLE_LINEAGE_SIDE_EFFECT,
)


class MockDatabricksClient(DatabricksClient):
    def __init__(self):
        self._db_allowed = ["prd", "staging"]
        self._db_blocked = ["dev"]


def test_DatabricksClient__get_user_mapping():
    client = MockDatabricksClient()
    users = [
        {"id": "both", "email": "hello@world.com", "user_name": "hello world"},
        {"id": "no_email", "email": "", "user_name": "no email"},
        {"id": "no_name", "email": "no@name.fr", "user_name": ""},
        {"id": "no_both", "email": "", "user_name": ""},
        {"id": "", "email": "no@id.com", "user_name": "no id"},
    ]
    expected = {
        "hello@world.com": "both",
        "hello world": "both",
        "no@name.fr": "no_name",
        "no email": "no_email",
    }
    mapping = client._get_user_mapping(users)
    assert mapping == expected


def test_DatabricksClient__match_table_with_user():
    client = MockDatabricksClient()
    user_mapping = {"bob@castordoc.com": 3}

    table = {"id": 1, "owner_email": "bob@castordoc.com"}
    table_with_owner = client._match_table_with_user(table, user_mapping)

    assert table_with_owner == {**table, "owner_external_id": 3}

    table_without_owner = {"id": 1, "owner_email": None}
    actual = client._match_table_with_user(table_without_owner, user_mapping)
    assert actual == table_without_owner


@patch(
    "source.packages.extractor.castor_extractor.warehouse.databricks.client.DatabricksAPIClient._get",
    side_effect=TABLE_LINEAGE_SIDE_EFFECT,
)
def test_DatabricksClient_table_lineage(mock_get):
    client = DatabricksClient(Mock())

    lineage = client.table_lineage(MOCK_TABLES_FOR_TABLE_LINEAGE)
    assert len(lineage) == 2

    expected_link_1 = {
        "parent_path": "dev.silver.pre_analytics",
        "child_path": "dev.silver.analytics",
        "timestamp": OLDER_DATE,
    }
    expected_link_2 = {
        "parent_path": "dev.bronze.analytics",
        "child_path": "dev.silver.analytics",
        "timestamp": CLOSER_DATE,
    }
    assert expected_link_1 in lineage
    assert expected_link_2 in lineage
