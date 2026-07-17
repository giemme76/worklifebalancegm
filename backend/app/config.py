"""Configurazione applicazione, letta da variabili d'ambiente / file .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"

    # SQLite in sviluppo, MySQL in produzione (impostare DATABASE_URL su cPanel).
    database_url: str = "sqlite:///./officepresence.db"

    session_cookie_name: str = "officepresence_session"
    session_cookie_max_age_days: int = 365

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def session_cookie_max_age_seconds(self) -> int:
        return self.session_cookie_max_age_days * 24 * 60 * 60

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()
