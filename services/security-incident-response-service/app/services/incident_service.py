import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.schemas.incident import (IncidentCreate, IncidentResponse, IncidentUpdate,
                                   TimelineEntryCreate, TimelineEntryResponse)


class IncidentService:
    def __init__(self):
        self._incidents: Dict[str, dict] = {}
        self._timelines: Dict[str, list] = {}
        self._counter = 0

    def _next_number(self) -> str:
        self._counter += 1
        return f"INC-{datetime.utcnow().year}-{self._counter:06d}"

    async def create_incident(self, payload: IncidentCreate, current_user: dict) -> IncidentResponse:
        iid = str(uuid.uuid4())
        now = datetime.utcnow()
        inc = {"id": uuid.UUID(iid), "incident_number": self._next_number(), "status": "OPEN",
               "reporter_id": current_user.get("sub"), "assignee_id": None, "resolution_notes": None,
               "created_at": now, "updated_at": now, "resolved_at": None, **payload.model_dump()}
        self._incidents[iid] = inc
        self._timelines[iid] = [{"id": uuid.uuid4(), "incident_id": iid, "action": "Incident created",
                                   "details": payload.description, "entry_type": "NOTE",
                                   "actor_id": current_user.get("sub", "system"), "occurred_at": now}]
        return IncidentResponse(**inc)

    async def get_incident(self, iid: str) -> Optional[IncidentResponse]:
        i = self._incidents.get(iid)
        return IncidentResponse(**i) if i else None

    async def list_incidents(self, status_filter: Optional[str] = None, severity: Optional[str] = None) -> List[IncidentResponse]:
        items = list(self._incidents.values())
        if status_filter:
            items = [i for i in items if i["status"] == status_filter]
        if severity:
            items = [i for i in items if i["severity"] == severity]
        return [IncidentResponse(**i) for i in sorted(items, key=lambda x: x["created_at"], reverse=True)]

    async def update_incident(self, iid: str, payload: IncidentUpdate) -> Optional[IncidentResponse]:
        inc = self._incidents.get(iid)
        if not inc:
            return None
        update = {k: v for k, v in payload.model_dump().items() if v is not None}
        inc.update(update)
        inc["updated_at"] = datetime.utcnow()
        if payload.status in ("RESOLVED", "CLOSED"):
            inc["resolved_at"] = datetime.utcnow()
        return IncidentResponse(**inc)

    async def add_timeline(self, iid: str, payload: TimelineEntryCreate, current_user: dict) -> Optional[TimelineEntryResponse]:
        if iid not in self._incidents:
            return None
        now = datetime.utcnow()
        entry = {"id": uuid.uuid4(), "incident_id": iid, "actor_id": current_user.get("sub", "system"),
                 "occurred_at": now, **payload.model_dump()}
        self._timelines[iid].append(entry)
        return TimelineEntryResponse(**entry)

    async def get_timeline(self, iid: str) -> List[TimelineEntryResponse]:
        return [TimelineEntryResponse(**e) for e in self._timelines.get(iid, [])]
