from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SERVICE_NAME: str = "Security Certificate Management Service"
    SERVICE_DESCRIPTION: str = "SSL/TLS certificate lifecycle management and monitoring"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8010
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6386/0"
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["*"]
    CERT_EXPIRY_WARNING_DAYS: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
