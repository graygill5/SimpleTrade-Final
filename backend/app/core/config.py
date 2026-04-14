from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SimpleTrade"
    api_prefix: str = "/api/v1"
    debug: bool = True

    database_url: str = "postgresql+psycopg2://simpletrade:simpletrade@localhost:5432/simpletrade"

    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    openai_api_key: str = ""
    initial_virtual_cash: float = 100000.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
