from enum import Enum

from ..utils import RetryStrategy

# url of the gcs proxy
INGEST_URL = "https://ingest.castordoc.com"

RETRY_BASE_MS = 10_000
RETRY_JITTER_MS = 1_000
RETRY_STRATEGY = RetryStrategy.LINEAR


class FileType(Enum):
    """type of file to load"""

    DBT = "DBT"
    QUALITY = "QUALITY"
    VIZ = "VIZ"
    WAREHOUSE = "WAREHOUSE"


PATH_TEMPLATES = {
    FileType.DBT: "transformation-{source_id}/{timestamp}-manifest.json",
    FileType.QUALITY: "quality-{source_id}/{timestamp}-{filename}",
    FileType.VIZ: "visualization-{source_id}/{filename}",
    FileType.WAREHOUSE: "warehouse-{source_id}/{filename}",
}


"""
The default request timeout in seconds for the upload
"""
DEFAULT_TIMEOUT = 60.0
ENVIRON_TIMEOUT = "CASTOR_TIMEOUT_OVERRIDE"

"""
The default retry for the upload
"""
DEFAULT_RETRY = 1
ENVIRON_RETRY = "CASTOR_RETRY_OVERRIDE"
