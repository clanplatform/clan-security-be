import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DataSubjectRequest(Base):
    __tablename__ = "data_subject_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_email = Column(String(255), nullable=False, index=True)
    request_type = Column(String(50), nullable=False)  # access, deletion, portability, rectification
    status = Column(String(50), nullable=False, default="PENDING")
    description = Column(Text, nullable=True)
    handler_notes = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_email = Column(String(255), nullable=False, index=True)
    purpose = Column(String(255), nullable=False)
    granted = Column(Boolean, nullable=False, default=True)
    legal_basis = Column(String(100), nullable=True)
    source = Column(String(255), nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)
