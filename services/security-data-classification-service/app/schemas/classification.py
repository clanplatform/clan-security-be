import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClassificationLabelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: int = Field(..., ge=1, le=5)
    color: Optional[str] = None
    description: Optional[str] = None
    handling_requirements: Optional[str] = None


class ClassificationLabelResponse(BaseModel):
    id: uuid.UUID
    name: str
    level: int
    color: Optional[str]
    description: Optional[str]
    handling_requirements: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ClassificationRuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    pattern: str = Field(..., min_length=1)
    rule_type: str = Field(..., pattern="^(REGEX|KEYWORD|ML_MODEL)$")
    label_id: uuid.UUID
    confidence_threshold: int = Field(default=80, ge=0, le=100)


class ClassificationRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    pattern: str
    rule_type: str
    label_id: uuid.UUID
    confidence_threshold: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ClassifyRequest(BaseModel):
    content: str = Field(..., min_length=1)
    content_type: Optional[str] = "text"
    source: Optional[str] = None
