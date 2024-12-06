from .utils import (
    usage_liveboard_reader,
)

VALID_CSV = '''"Data extract produced by Castor on 09/19/2024 06:54"
"Filters applied on data :"
"User Action IN [pinboard_embed_view,pinboard_tspublic_no_runtime_filter,pinboard_tspublic_runtime_filter,pinboard_view]"
"Pinboard NOT IN [mlm - availability pinboard,null]"
"Timestamp >= 20240820 00:00:00 < 20240919 00:00:00"
"Timestamp >= 20240919 00:00:00 < 20240920 00:00:00"
""
"Pinboard","Pinboard Views","Unique Number of User"
"Market Report","559","19"
"Retailer report","204","14"
"Second-hand market","72","6"
"September test","25","2"'''


# Invalid CSV input (missing data rows)
INVALID_CSV = '''"Data extract produced by Castor on 09/19/2024 06:54"
"Filters applied on data :"
"User Action IN [pinboard_embed_view,pinboard_tspublic_no_runtime_filter,pinboard_tspublic_runtime_filter,pinboard_view]"
"Pinboard NOT IN [mlm - availability pinboard,null]"
"Timestamp >= 20240820 00:00:00 < 20240919 00:00:00"
"Timestamp >= 20240919 00:00:00 < 20240920 00:00:00"
""'''


def test_usage_liveboard_reader():
    expected_output = [
        {
            "Pinboard": "Market Report",
            "Pinboard Views": "559",
            "Unique Number of User": "19",
        },
        {
            "Pinboard": "Retailer report",
            "Pinboard Views": "204",
            "Unique Number of User": "14",
        },
        {
            "Pinboard": "Second-hand market",
            "Pinboard Views": "72",
            "Unique Number of User": "6",
        },
        {
            "Pinboard": "September test",
            "Pinboard Views": "25",
            "Unique Number of User": "2",
        },
    ]

    result = list(usage_liveboard_reader(VALID_CSV))
    assert result == expected_output

    result = list(usage_liveboard_reader(INVALID_CSV))
    assert result == []  # Expect an empty result since there is no data
