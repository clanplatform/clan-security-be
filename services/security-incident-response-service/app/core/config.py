from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    SERVICE_NAME: str = "Security Incident Response Service"
    SERVICE_DESCRIPTION: str = "Security incident lifecycle management, escalation, and playbooks"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8026
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["*"]
    SLA_CRITICAL_MINUTES: int = 15
    SLA_HIGH_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
