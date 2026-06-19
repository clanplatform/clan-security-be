import uuid
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.monitoring import MetricCreate, MetricResponse, AlertCreate, AlertResponse, DashboardResponse


class MonitoringService:
    def __init__(self):
        self._metrics: Dict[str, dict] = {}
        self._alerts: Dict[str, dict] = {}

    async def record_metric(self, payload: MetricCreate) -> MetricResponse:
        mid = str(uuid.uuid4())
        m = {"id": uuid.UUID(mid), "recorded_at": datetime.utcnow(), **payload.model_dump()}
        self._metrics[mid] = m
        return MetricResponse(**m)

    async def list_metrics(self, name: Optional[str] = None) -> List[MetricResponse]:
        items = list(self._metrics.values())
        if name:
            items = [m for m in items if m["name"] == name]
        items.sort(key=lambda x: x["recorded_at"], reverse=True)
        return [MetricResponse(**m) for m in items[:200]]

    async def create_alert(self, payload: AlertCreate) -> AlertResponse:
        aid = str(uuid.uuid4())
        a = {"id": uuid.UUID(aid), "status": "ACTIVE", "acknowledged_by": None,
             "acknowledged_at": None, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._alerts[aid] = a
        return AlertResponse(**a)

    async def list_alerts(self, active_only: bool = True) -> List[AlertResponse]:
        items = list(self._alerts.values())
        if active_only:
            items = [a for a in items if a["status"] == "ACTIVE"]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return [AlertResponse(**a) for a in items]

    async def acknowledge_alert(self, aid: str, current_user: dict) -> Optional[AlertResponse]:
        a = self._alerts.get(aid)
        if not a:
            return None
        a["status"] = "ACKNOWLEDGED"
        a["acknowledged_by"] = current_user.get("sub", "unknown")
        a["acknowledged_at"] = datetime.utcnow()
        return AlertResponse(**a)

    async def get_dashboard(self) -> DashboardResponse:
        active = [a for a in self._alerts.values() if a["status"] == "ACTIVE"]
        by_sev = Counter(a["severity"] for a in active)
        recent = sorted(active, key=lambda x: x["created_at"], reverse=True)[:5]
        return DashboardResponse(total_metrics=len(self._metrics), active_alerts=len(active),
                                  alerts_by_severity=dict(by_sev),
                                  recent_alerts=[AlertResponse(**a) for a in recent],
                                  generated_at=datetime.utcnow())
