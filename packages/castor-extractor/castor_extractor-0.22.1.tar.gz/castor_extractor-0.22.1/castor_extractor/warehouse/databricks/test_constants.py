OLDER_DATE = "2024-04-18 20:20:20.0"
CLOSER_DATE = "2024-04-19 20:20:20.0"

MOCK_TABLES_FOR_TABLE_LINEAGE = [
    {
        "id": "f51ba2ca-8cc3-4de6-8f8b-730359e8f40f",
        "schema_id": "dev.silver",
        "table_name": "analytics",
    },
    {
        "id": "4e140bdc-a67c-4b68-8a07-c684657d8b44",
        "schema_id": "dev.silver",
        "table_name": "pre_analytics",
    },
    {
        "id": "7d403198-55ea-4a40-9995-6ee2f4c79dfa",
        "schema_id": "dev.bronze",
        "table_name": "analytics",
    },
]

_RAW_LINEAGE_DEV_SILVER_ANALYTICS = {
    "upstreams": [
        {  # there could be other keys: jobInfos, notebookInfos, queryInfos
            "tableInfo": {
                "name": "pre_analytics",
                "catalog_name": "dev",
                "schema_name": "silver",
                "table_type": "PERSISTED_VIEW",  # not used
                "lineage_timestamp": OLDER_DATE,
            }
        },
        {
            "tableInfo": {
                "name": "analytics",
                "catalog_name": "dev",
                "schema_name": "bronze",
                "table_type": "PERSISTED_VIEW",  # not used
                "lineage_timestamp": CLOSER_DATE,
            }
        },
    ],
    "downstreams": [],
}
_RAW_LINEAGE_DEV_SILVER_PRE_ANALYTICS = {
    "upstreams": [],
    "downstreams": [
        {
            "tableInfo": {
                "name": "analytics",
                "catalog_name": "dev",
                "schema_name": "silver",
                "table_type": "PERSISTED_VIEW",  # not used
                "lineage_timestamp": OLDER_DATE,
            }
        },
    ],
}
_RAW_LINEAGE_DEV_BRONZE_ANALYTICS = {
    "upstreams": [],
    "downstreams": [
        {
            "tableInfo": {
                "name": "analytics",
                "catalog_name": "dev",
                "schema_name": "silver",
                "table_type": "PERSISTED_VIEW",  # not used
                "lineage_timestamp": OLDER_DATE,
            }
        },
    ],
}

# should be in the same order as MOCK_TABLES_FOR_TABLE_LINEAGE
TABLE_LINEAGE_SIDE_EFFECT: tuple = (
    _RAW_LINEAGE_DEV_SILVER_ANALYTICS,
    _RAW_LINEAGE_DEV_SILVER_PRE_ANALYTICS,
    _RAW_LINEAGE_DEV_BRONZE_ANALYTICS,
)
