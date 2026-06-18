import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.audit_trail import AuditEntryCreate, AuditEntryResponse, AuditSearchParams


class AuditTrailService:
    """In-memory implementation. Replace storage with async SQLAlchemy in production."""

    def __init__(self):
        self._store: Dict[str, dict] = {}

    async def create_entry(self, payload: AuditEntryCreate) -> AuditEntryResponse:
        entry_id = str(uuid.uuid4())
        entry = {
            "id": uuid.UUID(entry_id),
            "timestamp": datetime.utcnow(),
            **payload.model_dump(),
        }
        self._store[entry_id] = entry
        return AuditEntryResponse(**entry)

    async def get_entry(self, entry_id: str) -> Optional[AuditEntryResponse]:
        entry = self._store.get(entry_id)
        if not entry:
            return None
        return AuditEntryResponse(**entry)

    async def search_entries(self, params: AuditSearchParams) -> List[AuditEntryResponse]:
        results = list(self._store.values())

        if params.user_id:
            results = [e for e in results if e.get("user_id") == params.user_id]
        if params.action:
            results = [e for e in results if params.action.lower() in (e.get("action") or "").lower()]
        if params.resource:
            results = [e for e in results if params.resource.lower() in (e.get("resource") or "").lower()]
        if params.from_date:
            results = [e for e in results if e["timestamp"] >= params.from_date]
        if params.to_date:
            results = [e for e in results if e["timestamp"] <= params.to_date]

        results.sort(key=lambda e: e["timestamp"], reverse=True)
        start = (params.page - 1) * params.page_size
        return [AuditEntryResponse(**e) for e in results[start : start + params.page_size]]

    async def get_stats(
        self, from_date: Optional[datetime], to_date: Optional[datetime]
    ) -> Dict[str, Any]:
        entries = list(self._store.values())
        if from_date:
            entries = [e for e in entries if e["timestamp"] >= from_date]
        if to_date:
            entries = [e for e in entries if e["timestamp"] <= to_date]

        by_result: Dict[str, int] = {}
        by_severity: Dict[str, int] = {}
        by_service: Dict[str, int] = {}
        for e in entries:
            by_result[e["result"]] = by_result.get(e["result"], 0) + 1
            by_severity[e["severity"]] = by_severity.get(e["severity"], 0) + 1
            by_service[e["service"]] = by_service.get(e["service"], 0) + 1

        return {
            "total": len(entries),
            "by_result": by_result,
            "by_severity": by_severity,
            "by_service": by_service,
        }
