"""
Settings module for the project.
It uses pydantic_settings to load settings from environment variables and .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database settings."""

    model_config = SettingsConfigDict(env_file=".db.env", env_file_encoding="utf-8")

    dsn: str = "sqlite+aiosqlite:///db.sqlite3"
    echo: bool = False


class Settings(BaseSettings):
    """Settings class."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    main_url: str = "/"
    secret_key: str = "secret"
    prefix_api_key: str = ""

    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
