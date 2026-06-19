import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MetricCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    value: float
    unit: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    source: Optional[str] = None


class MetricResponse(BaseModel):
    id: uuid.UUID
    name: str
    value: float
    unit: Optional[str]
    labels: Optional[Dict[str, str]]
    source: Optional[str]
    recorded_at: datetime

    model_config = {"from_attributes": True}


class AlertCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    severity: str = Field(..., pattern="^(INFO|LOW|MEDIUM|HIGH|CRITICAL)$")
    source: Optional[str] = None
    metric_name: Optional[str] = None
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None


class AlertResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    severity: str
    status: str
    source: Optional[str]
    metric_name: Optional[str]
    threshold_value: Optional[float]
    current_value: Optional[float]
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    total_metrics: int
    active_alerts: int
    alerts_by_severity: Dict[str, int]
    recent_alerts: List[AlertResponse]
    generated_at: datetime
