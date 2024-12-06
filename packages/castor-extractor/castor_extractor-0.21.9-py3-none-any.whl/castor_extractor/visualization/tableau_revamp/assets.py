from ...types import ExternalAsset


class TableauRevampAsset(ExternalAsset):
    """
    Tableau assets
    """

    COLUMN = "columns"
    DASHBOARD = "dashboards"
    DATASOURCE = "datasources"
    FIELD = "fields"
    METRIC = "metrics"
    METRIC_DEFINITION = "metrics_definitions"
    PROJECT = "projects"
    SHEET = "sheets"
    SUBSCRIPTION = "subscriptions"
    TABLE = "tables"
    USAGE = "usage"
    USER = "users"
    WORKBOOK = "workbooks"


# assets that are only available for clients using Tableau Pulse
TABLEAU_PULSE_ASSETS = (
    TableauRevampAsset.METRIC,
    TableauRevampAsset.METRIC_DEFINITION,
    TableauRevampAsset.SUBSCRIPTION,
)
