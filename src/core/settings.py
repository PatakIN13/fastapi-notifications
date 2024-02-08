"""
Settings module for the project.
It uses pydantic_settings to load settings from environment variables and .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    main_url: str = "/"
    db_dsn: str = "sqlite+aiosqlite:///db.sqlite3"
    db_echo: bool = False


settings = Settings()
