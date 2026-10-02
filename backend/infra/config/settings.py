from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    cors_origin: str = "http://localhost:4200"
    data_dir: Path = PROJECT_ROOT / "data"

    model_config = SettingsConfigDict(
        env_file=".env",
    )

    @property
    def db_path(self) -> Path:
        return self.data_dir / "session_lab.db"
    
    @property
    def raw_data_path(self):
        return self.data_dir / "raw"


settings = Settings()