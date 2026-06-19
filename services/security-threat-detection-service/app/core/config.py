from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SERVICE_NAME: str = "Security Threat Detection Service"
    SERVICE_DESCRIPTION: str = "Real-time threat detection rules, IOCs, and behavioral analytics"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8028
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
