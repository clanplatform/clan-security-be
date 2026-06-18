import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class EscalationRequest(Base):
    __tablename__ = "escalation_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(String(255), nullable=False, index=True)
    requester_email = Column(String(255), nullable=True)
    target_role = Column(String(100), nullable=False)
    target_resource = Column(String(255), nullable=True)
    justification = Column(Text, nullable=False)
    duration_hours = Column(Integer, nullable=False, default=1)
    status = Column(String(30), nullable=False, default="PENDING")
    approved_by = Column(String(255), nullable=True)
    approval_notes = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    ticket_id = Column(String(100), nullable=True)
