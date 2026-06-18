from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
import uuid


@dataclass
class SecurityEvent:
    event_type: str
    service: str
    payload: Dict[str, Any]
    severity: str = "INFO"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None


@dataclass
class AuditEvent(SecurityEvent):
    action: str = ""
    resource: str = ""
    result: str = "SUCCESS"
    ip_address: Optional[str] = None


@dataclass
class ThreatEvent(SecurityEvent):
    threat_type: str = ""
    confidence: float = 0.0
    indicators: Dict[str, Any] = field(default_factory=dict)
