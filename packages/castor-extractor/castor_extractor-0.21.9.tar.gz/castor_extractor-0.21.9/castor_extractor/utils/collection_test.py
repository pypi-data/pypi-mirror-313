from .collection import deduplicate, mapping_from_rows


def test__mapping_from_rows__basic_mapping():
    rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    result = mapping_from_rows(rows, "id", "name")
    expected = {1: "Alice", 2: "Bob"}
    assert result == expected


def test__mapping_from_rows__missing_key():
    rows = [{"id": 1, "name": "Alice"}, {"name": "Bob"}]
    result = mapping_from_rows(rows, "id", "name")
    expected = {1: "Alice"}
    assert result == expected


def test__mapping_from_rows__missing_value():
    rows = [{"id": 1, "name": "Alice"}, {"id": 2}]
    result = mapping_from_rows(rows, "id", "name")
    expected = {1: "Alice"}
    assert result == expected


def test__mapping_from_rows__empty_list():
    rows = []
    result = mapping_from_rows(rows, "id", "name")
    expected = {}
    assert result == expected


def test__mapping_from_rows__non_existent_key_value():
    rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    result = mapping_from_rows(rows, "nonexistent_key", "nonexistent_value")
    expected = {}
    assert result == expected


def test__mapping_from_rows__none_key_value():
    rows = [
        {"id": 1, "name": "Alice"},
        {"id": None, "name": "Bob"},
        {"id": 2, "name": None},
    ]
    result = mapping_from_rows(rows, "id", "name")
    expected = {1: "Alice"}
    assert result == expected


def test__mapping_from_rows__multiple_valid_rows():
    rows = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]
    result = mapping_from_rows(rows, "id", "name")
    expected = {1: "Alice", 2: "Bob", 3: "Charlie"}
    assert result == expected


def test_deduplicate():
    e1 = {"id": "1", "name": "element_1"}
    e2 = {"id": "2", "name": "element_2"}
    e3 = {"id": "3", "name": "element_3"}

    elements = [
        e1,
        e2,
        e3,
        {"id": "3", "name": "duplicate"},
        {"id": "3", "name": "duplicate"},
        {"id": "2", "name": "duplicate"},
    ]
    assert deduplicate("id", elements) == [e1, e2, e3]
