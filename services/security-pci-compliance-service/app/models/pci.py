import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PCIControl(Base):
    __tablename__ = "pci_controls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requirement_id = Column(String(50), nullable=False, unique=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")
    last_assessed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    result = Column(String(50), nullable=False)  # PASS, FAIL, NOT_APPLICABLE
    evidence = Column(Text, nullable=True)
    assessor = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    assessed_at = Column(DateTime, default=datetime.utcnow)
    next_review = Column(DateTime, nullable=True)
