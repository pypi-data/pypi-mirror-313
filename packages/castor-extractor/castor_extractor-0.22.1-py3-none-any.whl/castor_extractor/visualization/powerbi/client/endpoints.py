from datetime import date, datetime
from typing import Optional

from ....utils import at_midnight, format_date, yesterday

_CLIENT_APP_BASE = "https://login.microsoftonline.com"
_REST_API_BASE_PATH = "https://api.powerbi.com/v1.0/myorg"


def _time_filter(day: Optional[date]) -> tuple[datetime, datetime]:
    target_day = day or yesterday()
    start = at_midnight(target_day)
    end = datetime.combine(target_day, datetime.max.time())
    return start, end


class PowerBiEndpointFactory:
    @classmethod
    def activity_events(cls, day: Optional[date]) -> str:
        start, end = _time_filter(day)
        url = f"{_REST_API_BASE_PATH}/admin/activityevents"
        url += "?$filter=Activity eq 'viewreport'"
        url += f"&startDateTime='{format_date(start)}'"
        url += f"&endDateTime='{format_date(end)}'"
        return url

    @classmethod
    def authority(cls, tenant_id: str) -> str:
        return f"{_CLIENT_APP_BASE}/{tenant_id}"

    @classmethod
    def dashboards(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/dashboards"

    @classmethod
    def datasets(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/datasets"

    @classmethod
    def groups(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/groups"

    @classmethod
    def metadata_create_scan(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/workspaces/getInfo"

    @classmethod
    def metadata_scan_result(cls, scan_id: int) -> str:
        return f"{_REST_API_BASE_PATH}/admin/workspaces/scanResult/{scan_id}"

    @classmethod
    def metadata_scan_status(cls, scan_id: int) -> str:
        return f"{_REST_API_BASE_PATH}/admin/workspaces/scanStatus/{scan_id}"

    @classmethod
    def pages(cls, report_id: str) -> str:
        return f"{_REST_API_BASE_PATH}/admin/reports/{report_id}/pages"

    @classmethod
    def reports(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/reports"

    @classmethod
    def workspace_ids(cls) -> str:
        return f"{_REST_API_BASE_PATH}/admin/workspaces/modified"
