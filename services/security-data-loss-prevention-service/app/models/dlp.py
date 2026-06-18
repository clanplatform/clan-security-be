import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DLPRule(Base):
    __tablename__ = "dlp_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    rule_type = Column(String(50), nullable=False)  # REGEX, KEYWORD, ML_MODEL
    pattern = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="MEDIUM")
    action = Column(String(50), nullable=False, default="ALERT")  # ALERT, BLOCK, ENCRYPT
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    match_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class DLPViolation(Base):
    __tablename__ = "dlp_violations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), nullable=False)
    rule_name = Column(String(255), nullable=False)
    content_snippet = Column(Text, nullable=True)
    source = Column(String(255), nullable=True)
    severity = Column(String(20), nullable=False)
    action_taken = Column(String(50), nullable=False)
    user_id = Column(String(255), nullable=True)
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
