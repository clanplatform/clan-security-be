from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SERVICE_NAME: str = "Security Audit Trail Service"
    SERVICE_DESCRIPTION: str = "Immutable audit trail for all security events across the platform"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8001
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["*"]
    RETENTION_DAYS: int = 2555  # 7 years for compliance

    class Config:
        env_file = ".env"


settings = Settings()
