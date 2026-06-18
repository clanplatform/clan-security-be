import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MaskingConfigCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    field_type: str = Field(..., pattern="^(EMAIL|PHONE|CC_NUMBER|SSN|NAME|ADDRESS|CUSTOM)$")
    mask_type: str = Field(..., pattern="^(REDACT|PARTIAL|TOKENIZE|HASH)$")
    pattern: Optional[str] = None
    replacement: str = "***"
    preserve_length: bool = False
    preserve_format: bool = False


class MaskingConfigResponse(BaseModel):
    id: uuid.UUID
    name: str
    field_type: str
    mask_type: str
    pattern: Optional[str]
    replacement: str
    preserve_length: bool
    preserve_format: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MaskRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Key-value pairs to mask")
    config_ids: Optional[List[uuid.UUID]] = None


class MaskResponse(BaseModel):
    masked_data: Dict[str, Any]
    fields_masked: int
    tokens: Dict[str, str] = {}


class UnmaskRequest(BaseModel):
    tokens: Dict[str, str] = Field(..., description="field -> token mapping")
