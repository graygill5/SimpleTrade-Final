from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SimpleTrade"
    debug: bool = True
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg2://simpletrade:simpletrade@localhost:5432/simpletrade"

    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
