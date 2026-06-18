import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class SOXControl(Base):
    __tablename__ = "sox_controls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(String(50), nullable=False, unique=True)
    objective = Column(Text, nullable=False)
    control_type = Column(String(50), nullable=False)  # PREVENTIVE, DETECTIVE, CORRECTIVE
    frequency = Column(String(50), nullable=False)  # DAILY, WEEKLY, MONTHLY, QUARTERLY, ANNUAL
    owner = Column(String(255), nullable=False)
    process = Column(String(255), nullable=True)
    risk_level = Column(String(20), nullable=False, default="MEDIUM")
    status = Column(String(50), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SOXAssessment(Base):
    __tablename__ = "sox_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    period = Column(String(20), nullable=False)  # e.g., "2024-Q1"
    result = Column(String(50), nullable=False)  # EFFECTIVE, INEFFECTIVE, NOT_TESTED
    evidence = Column(Text, nullable=True)
    assessor = Column(String(255), nullable=True)
    deficiencies = Column(Text, nullable=True)
    remediation_plan = Column(Text, nullable=True)
    assessed_at = Column(DateTime, default=datetime.utcnow)
    next_assessment = Column(DateTime, nullable=True)
