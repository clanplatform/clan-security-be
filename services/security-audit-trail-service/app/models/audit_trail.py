import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    session_id = Column(String(255), nullable=True)
    action = Column(String(255), nullable=False, index=True)
    resource = Column(String(500), nullable=False)
    resource_id = Column(String(255), nullable=True)
    result = Column(String(50), nullable=False, default="SUCCESS")
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    service = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False, default="INFO")
    details = Column(JSON, nullable=True)
    tenant_id = Column(String(255), nullable=True, index=True)
    correlation_id = Column(String(255), nullable=True)
