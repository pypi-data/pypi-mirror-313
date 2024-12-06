from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    api_key: str = Field(..., exclude=True)
    base_url: str = Field(default="https://api.dottxt.co")

    model_config = SettingsConfigDict(env_prefix="dottxt_")

    @model_validator(mode="before")
    def validate_api_key(cls, values):
        api_key = values.get("api_key")
        if not api_key:
            raise ValueError(
                "An API key is required. Please set the 'DOTTXT_API_KEY' "
                "environment variable or pass 'api_key' directly during "
                "initialization."
            )
        return values
