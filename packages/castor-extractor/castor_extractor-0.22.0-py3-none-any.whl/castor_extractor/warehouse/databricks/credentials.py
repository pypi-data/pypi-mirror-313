from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic_settings import SettingsConfigDict

DATABRICKS_ENV_PREFIX = "CASTOR_DATABRICKS_"


@dataclass
class DatabricksCredentials:
    """
    Credentials needed by Databricks client
    Requires:
    - host
    - token
    """

    host: str
    token: str = field(metadata={"sensitive": True})
    http_path: Optional[str] = field(default=None)

    model_config = SettingsConfigDict(
        env_prefix=DATABRICKS_ENV_PREFIX,
        extra="ignore",
        populate_by_name=True,
    )
