from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/polywatch"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    llm_enabled: bool = True
    llm_daily_budget_cents: int = 500


settings = Settings()
