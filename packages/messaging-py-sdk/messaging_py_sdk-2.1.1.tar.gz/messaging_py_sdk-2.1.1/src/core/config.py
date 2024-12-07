import os

from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings
from src.core.logger import logger


class Settings(BaseSettings):
    BASE_URL: str = Field(default="http://localhost:3000", json_schema_extra={"env": "BASE_URL"})
    API_KEY: str = Field(json_schema_extra={"env": "API_KEY"})
    WEBHOOK_SECRET: str = Field(json_schema_extra={"env": "WEBHOOK_SECRET"})

    @field_validator("BASE_URL")
    def validate_base_url(cls, value):
        if not value.startswith("http"):
            raise ValueError("BASE_URL must start with 'http'")
        logger.info(f"Validated BASE_URL: {value}")
        return value

    @field_validator("API_KEY", "WEBHOOK_SECRET")
    def validate_non_empty(cls, value, info):
        field_name = info.field_name  # Get the name of the field being validated
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        logger.info(f"Validated {field_name}: {value}")
        return value

    model_config = ConfigDict(env_file=os.path.join(os.path.dirname(__file__), "../../.env"), env_file_encoding="utf-8")


settings = Settings()
