import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ClassificationLabel(Base):
    __tablename__ = "classification_labels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    level = Column(Integer, nullable=False)  # 1=Public, 2=Internal, 3=Confidential, 4=Restricted, 5=Top Secret
    color = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    handling_requirements = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClassificationRule(Base):
    __tablename__ = "classification_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    pattern = Column(Text, nullable=False)
    rule_type = Column(String(50), nullable=False)  # REGEX, KEYWORD, ML_MODEL
    label_id = Column(UUID(as_uuid=True), nullable=False)
    confidence_threshold = Column(Integer, nullable=False, default=80)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
