from typing import Any, Optional

from pydantic import (
    PostgresDsn,
    field_validator,
    model_validator,
    root_validator,
    validator,
)
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "technical-test"
    VERSION: str = "0.2.0"
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def database_uri(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        
        postgres_dsn = PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )
        return str(postgres_dsn)

settings = Settings()