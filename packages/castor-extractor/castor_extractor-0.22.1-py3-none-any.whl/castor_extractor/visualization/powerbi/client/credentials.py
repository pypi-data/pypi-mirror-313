from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SCOPE = "https://analysis.windows.net/powerbi/api/.default"
POWERBI_ENV_PREFIX = "CASTOR_POWERBI_"


class PowerbiCredentials(BaseSettings):
    """Class to handle PowerBI rest API permissions"""

    model_config = SettingsConfigDict(
        env_prefix=POWERBI_ENV_PREFIX,
        extra="ignore",
        populate_by_name=True,
    )

    client_id: str
    tenant_id: str
    secret: str = Field(repr=False)
    scopes: list[str] = [DEFAULT_SCOPE]

    @field_validator("scopes", mode="before")
    @classmethod
    def _check_scopes(cls, scopes: Optional[list[str]]) -> list[str]:
        return scopes if scopes is not None else [DEFAULT_SCOPE]
