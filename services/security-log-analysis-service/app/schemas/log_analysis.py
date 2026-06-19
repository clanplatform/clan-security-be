import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class LogEntryIngest(BaseModel):
    source: str = Field(..., min_length=1, max_length=255)
    log_level: str = Field(..., pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    message: str = Field(..., min_length=1)
    timestamp: Optional[datetime] = None
    host: Optional[str] = None
    service: Optional[str] = None
    trace_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None


class LogEntryResponse(BaseModel):
    id: uuid.UUID
    source: str
    log_level: str
    message: str
    timestamp: datetime
    host: Optional[str]
    service: Optional[str]
    trace_id: Optional[str]
    fields: Optional[Dict[str, Any]]
    ingested_at: datetime

    model_config = {"from_attributes": True}


class LogQueryRequest(BaseModel):
    query: Optional[str] = None  # keyword search
    source: Optional[str] = None
    log_level: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)


class LogQueryResponse(BaseModel):
    total: int
    entries: List[LogEntryResponse]
    query_time_ms: float


class LogAnomalyResponse(BaseModel):
    id: uuid.UUID
    source: str
    anomaly_type: str
    description: str
    severity: str
    log_count: int
    detected_at: datetime
