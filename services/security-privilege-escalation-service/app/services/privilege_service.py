import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from app.schemas.privilege import (EscalationRequestCreate, EscalationRequestResponse, EscalationDecision)


class PrivilegeService:
    def __init__(self):
        self._requests: Dict[str, dict] = {}

    async def create_request(self, payload: EscalationRequestCreate, current_user: dict) -> EscalationRequestResponse:
        rid = str(uuid.uuid4())
        now = datetime.utcnow()
        req = {"id": uuid.UUID(rid), "requester_id": current_user.get("sub", "unknown"),
               "requester_email": current_user.get("email"), "target_role": payload.target_role,
               "target_resource": payload.target_resource, "justification": payload.justification,
               "duration_hours": payload.duration_hours, "status": "PENDING",
               "approved_by": None, "approval_notes": None, "requested_at": now,
               "decided_at": None, "expires_at": None, "revoked_at": None, "ticket_id": payload.ticket_id}
        self._requests[rid] = req
        return EscalationRequestResponse(**req)

    async def get_request(self, rid: str) -> Optional[EscalationRequestResponse]:
        r = self._requests.get(rid)
        return EscalationRequestResponse(**r) if r else None

    async def list_requests(self) -> List[EscalationRequestResponse]:
        return [EscalationRequestResponse(**r) for r in self._requests.values()]

    async def decide(self, rid: str, decision: str, payload: EscalationDecision, current_user: dict) -> Optional[EscalationRequestResponse]:
        req = self._requests.get(rid)
        if not req:
            return None
        now = datetime.utcnow()
        req["status"] = decision
        req["approved_by"] = current_user.get("sub", "unknown")
        req["approval_notes"] = payload.notes
        req["decided_at"] = now
        if decision == "APPROVED":
            req["expires_at"] = now + timedelta(hours=req["duration_hours"])
        return EscalationRequestResponse(**req)

    async def revoke(self, rid: str) -> Optional[EscalationRequestResponse]:
        req = self._requests.get(rid)
        if not req:
            return None
        req["status"] = "REVOKED"
        req["revoked_at"] = datetime.utcnow()
        return EscalationRequestResponse(**req)
