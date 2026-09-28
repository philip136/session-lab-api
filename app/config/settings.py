from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    app_host: str = "127.0.0.1"
    app_port: int = 8000

    database_url: str = "sqlite:///data/sessionlab.db"

    raw_data_dir: str = "data/raw"

    cors_origin: str = "http://localhost:4200"

    logging: LoggingSettings = LoggingSettings()


settings = Settings()