import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class SecurityPolicy(Base):
    __tablename__ = "security_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="DRAFT")
    owner = Column(String(255), nullable=True)
    effective_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    review_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)


class PolicyViolation(Base):
    __tablename__ = "policy_violations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="MEDIUM")
    reporter = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="OPEN")
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
