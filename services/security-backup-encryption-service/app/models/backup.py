import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BackupKey(Base):
    __tablename__ = "backup_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    algorithm = Column(String(50), nullable=False, default="AES-256-GCM")
    key_version = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="ACTIVE")
    description = Column(String(500), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    rotated_at = Column(DateTime, nullable=True)
    tenant_id = Column(String(255), nullable=True)


class BackupJob(Base):
    __tablename__ = "backup_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    key_id = Column(UUID(as_uuid=True), nullable=False)
    source = Column(String(500), nullable=False)
    destination = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False, default="SCHEDULED")
    schedule = Column(String(100), nullable=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    checksum = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
