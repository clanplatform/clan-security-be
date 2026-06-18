import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False, index=True)
    cert_type = Column(String(50), nullable=False)  # DV, OV, EV, WILDCARD, SAN
    status = Column(String(50), nullable=False, default="PENDING")
    issuer = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=True)
    fingerprint = Column(String(255), nullable=True, unique=True)
    serial_number = Column(String(255), nullable=True)
    key_algorithm = Column(String(50), nullable=False, default="RSA")
    key_size = Column(Integer, nullable=False, default=2048)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    auto_renew = Column(String(10), nullable=False, default="true")
    san_domains = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tenant_id = Column(String(255), nullable=True)
