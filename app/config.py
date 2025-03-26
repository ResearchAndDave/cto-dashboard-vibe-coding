from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    # Base settings
    APP_NAME: str = "CTO Dashboard"
    DEBUG: bool = True

    # Database settings
    DB_FILE: str = "dashboard.duckdb"

    # Path settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings object
settings = Settings()
