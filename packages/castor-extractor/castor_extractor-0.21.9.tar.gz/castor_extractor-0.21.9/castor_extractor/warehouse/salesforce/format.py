from typing import Any, Dict, Iterator, List

from ...utils import group_by
from .constants import SCHEMA_NAME

_HAS_DUPLICATE_KEY = "#has_duplicate"


def _clean(raw: str) -> str:
    return raw.strip('"')


def _name(sobject: dict) -> str:
    """
    compute name for table and columns
    - when unique: label
    - when label is empty or has duplicate: label (api_name)
    """
    label = sobject["Label"]
    api_name = sobject["QualifiedApiName"]
    if not label:
        return api_name
    if not sobject[_HAS_DUPLICATE_KEY]:
        return label
    return f"{label} ({api_name})"


def _field_description(field: Dict[str, Any]) -> str:
    context: Dict[str, str] = {}

    field_definition: Dict[str, str] = field.get("FieldDefinition") or {}
    if description := field_definition.get("Description"):
        context["Description"] = _clean(description)
    if help_text := field.get("InlineHelpText"):
        context["Help Text"] = _clean(help_text)
    if compliance_group := field_definition.get("ComplianceGroup"):
        context["Compliance Categorization"] = _clean(compliance_group)
    if security_level := field_definition.get("SecurityClassification"):
        context["Data Sensitivity Level"] = _clean(security_level)

    return "\n".join([f"- {k}: {v}" for k, v in context.items()])


def _to_column_payload(field: dict, position: int, table_name: str) -> dict:
    field_name = _name(field)
    return {
        "column_name": field_name,
        "data_type": field.get("DataType"),
        "description": _field_description(field),
        "id": f"{table_name}.{field_name}",
        "ordinal_position": position,
        "salesforce_developer_name": field.get("DeveloperName"),
        "salesforce_tooling_url": field.get("attributes", {}).get("url"),
        "table_id": table_name,
    }


def _to_table_payload(sobject: dict) -> dict:
    name = _name(sobject)
    return {
        "id": name,
        "api_name": sobject["QualifiedApiName"],
        "label": sobject["Label"],
        "schema_id": SCHEMA_NAME,
        "table_name": name,
        "description": sobject.get("Description"),
        "tags": [],
        "type": "TABLE",
    }


def _detect_duplicates(sobjects: List[dict]) -> List[dict]:
    """
    enrich the given data with "has_duplicate" flag:
    - True when another asset has the same Label in the list
    - False otherwise
    """
    by_label = group_by("Label", sobjects)
    for sobject in sobjects:
        label = sobject["Label"]
        sobject[_HAS_DUPLICATE_KEY] = len(by_label[label]) > 1
    return sobjects


class SalesforceFormatter:
    """
    Helper functions that format the response in the format to be exported as
    csv.
    """

    @staticmethod
    def tables(sobjects: List[dict]) -> Iterator[dict]:
        """
        formats the raw list of sobjects to tables
        """
        sobjects = _detect_duplicates(sobjects)
        for sobject in sobjects:
            yield _to_table_payload(sobject)

    @staticmethod
    def columns(sobject_fields: Dict[str, List[dict]]) -> Iterator[dict]:
        """formats the raw list of sobject fields to columns"""
        for table_name, fields in sobject_fields.items():
            fields = _detect_duplicates(fields)
            for index, field in enumerate(fields):
                yield _to_column_payload(field, index, table_name)
