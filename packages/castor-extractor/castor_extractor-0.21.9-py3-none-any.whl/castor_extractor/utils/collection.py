from collections import defaultdict
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Sequence,
    Set,
    TypeVar,
)

from .object import getproperty
from .type import Getter

T = TypeVar("T")


def group_by(identifier: Getter, elements: Sequence) -> Dict[Any, List]:
    """Groups the elements by the given key"""
    groups: Dict[Any, List] = defaultdict(list)
    for element in elements:
        key = getproperty(element, identifier)
        groups[key].append(element)

    return groups


def mapping_from_rows(rows: List[Dict], key: Any, value: Any) -> Dict:
    """
    Create a dictionary mapping from a list of dictionaries using specified keys for mapping.

    Args:
        rows (list[dict]): A list of dictionaries from which to create the mapping.
        key (Any): The key to use for the keys of the resulting dictionary.
        value (Any): The key to use for the values of the resulting dictionary.

    Returns:
        dict: A dictionary where each key-value pair corresponds to the specified key and value
              from each dictionary in the input list. Only dictionaries with both specified key
              and value present are included in the result.

    Example:
        rows = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
        mapping = mapping_from_rows(rows, 'id', 'name')
        # mapping will be {1: 'Alice', 2: 'Bob'}
    """
    mapping = {}

    for row in rows:
        mapping_key = row.get(key)
        mapping_value = row.get(value)

        if not mapping_key or not mapping_value:
            continue
        mapping[mapping_key] = mapping_value

    return mapping


def empty_iterator():
    """
    Utils to return empty iterator, mainly used for viz transformers
    Remark: missing return type is on purpose, it breaks the typing
    """
    return iter([])


def deduplicate(
    identifier: Getter,
    elements: Iterable[T],
) -> List[T]:
    """
    Remove duplicates in the given elements, using the specified identifier
    Only the first occurrence is kept.
    """
    deduplicated: List[T] = []
    processed: Set[Any] = set()

    for element in elements:
        key = getproperty(element, identifier)
        if key in processed:
            continue
        processed.add(key)
        deduplicated.append(element)

    return deduplicated
