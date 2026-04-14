from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SimpleTrade"
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg2://simpletrade:simpletrade@localhost:5432/simpletrade"
    jwt_secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 10080

    frontend_url: str = "http://localhost:3000"
    backend_cors_origins: str = "http://localhost:3000"

    openai_api_key: str = ""
    news_api_key: str = ""

    initial_virtual_cash: float = 100000.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]


settings = Settings()
