from pathlib import Path
from typing import List, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sentinel Shield Backend"
    ENVIRONMENT: str = "development"

    # Either set DATABASE_URL directly, or set the POSTGRES_* parts below
    # and the URL is assembled from them.
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "sentinel_db"
    SQL_ECHO: bool = False

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME_MONGO: str = "sentinel_shield_community"
    MONGODB_ENABLED: bool = False

    SECRET_KEY: str = "CHANGE_THIS_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    INCIDENT_HIGH_RISK_THRESHOLD: float = 70.0
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    UPLOAD_DIR: str = str(BACKEND_DIR / "uploads")
    IMAGE_MAX_WIDTH: int = 1280
    IMAGE_MAX_HEIGHT: int = 1280
    IMAGE_QUALITY: int = 82

    SEED_DATA_ON_STARTUP: bool = True

    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
    ]

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )

    @model_validator(mode="after")
    def assemble_derived_settings(self) -> "Settings":
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        # A relative UPLOAD_DIR in .env is resolved against the backend dir,
        # so it doesn't depend on the process working directory.
        upload_path = Path(self.UPLOAD_DIR)
        if not upload_path.is_absolute():
            self.UPLOAD_DIR = str(BACKEND_DIR / upload_path)
        return self


settings = Settings()
