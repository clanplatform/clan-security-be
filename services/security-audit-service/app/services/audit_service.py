import uuid
import secrets
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.audit import AuditEventCreate, AuditEventResponse, AuditReportRequest, AuditReportResponse


class AuditService:
    def __init__(self):
        self._events: Dict[str, dict] = {}

    async def record_event(self, payload: AuditEventCreate) -> AuditEventResponse:
        eid = str(uuid.uuid4())
        event = {"id": uuid.UUID(eid), "occurred_at": datetime.utcnow(), **payload.model_dump()}
        self._events[eid] = event
        return AuditEventResponse(**event)

    async def get_event(self, eid: str) -> Optional[AuditEventResponse]:
        e = self._events.get(eid)
        return AuditEventResponse(**e) if e else None

    async def list_events(self, actor_id: Optional[str] = None, event_type: Optional[str] = None,
                           severity: Optional[str] = None, limit: int = 50) -> List[AuditEventResponse]:
        items = list(self._events.values())
        if actor_id:
            items = [e for e in items if e.get("actor_id") == actor_id]
        if event_type:
            items = [e for e in items if e["event_type"] == event_type]
        if severity:
            items = [e for e in items if e["severity"] == severity]
        items.sort(key=lambda x: x["occurred_at"], reverse=True)
        return [AuditEventResponse(**e) for e in items[:limit]]

    async def generate_report(self, payload: AuditReportRequest) -> AuditReportResponse:
        in_range = [e for e in self._events.values()
                    if payload.start_date <= e["occurred_at"] <= payload.end_date]
        if payload.event_types:
            in_range = [e for e in in_range if e["event_type"] in payload.event_types]
        if payload.severity_filter:
            in_range = [e for e in in_range if e["severity"] == payload.severity_filter]

        by_severity = Counter(e["severity"] for e in in_range)
        by_outcome = Counter(e["outcome"] for e in in_range)
        actor_counts = Counter(e.get("actor_id") for e in in_range if e.get("actor_id"))
        top_actors = [{"actor_id": a, "count": c} for a, c in actor_counts.most_common(10)]

        return AuditReportResponse(
            report_id=secrets.token_hex(8), title=payload.report_title,
            period_start=payload.start_date, period_end=payload.end_date,
            total_events=len(in_range), events_by_severity=dict(by_severity),
            events_by_outcome=dict(by_outcome), top_actors=top_actors, generated_at=datetime.utcnow(),
        )

    async def get_summary(self) -> Dict[str, Any]:
        by_sev = Counter(e["severity"] for e in self._events.values())
        by_out = Counter(e["outcome"] for e in self._events.values())
        return {"total_events": len(self._events), "by_severity": dict(by_sev), "by_outcome": dict(by_out)}
