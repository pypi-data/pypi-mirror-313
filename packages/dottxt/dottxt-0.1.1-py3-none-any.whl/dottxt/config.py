from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    api_key: str = Field(..., exclude=True)
    base_url: str = Field(default="https://api.dottxt.co")

    model_config = SettingsConfigDict(env_prefix="dottxt_")
