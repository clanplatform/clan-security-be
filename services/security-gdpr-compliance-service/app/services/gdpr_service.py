import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from app.schemas.gdpr import DSRCreate, DSRResponse, DSRStatusUpdate, ConsentCreate, ConsentResponse


class GDPRService:
    def __init__(self):
        self._dsrs: Dict[str, dict] = {}
        self._consents: Dict[str, dict] = {}

    async def create_dsr(self, payload: DSRCreate) -> DSRResponse:
        dsr_id = str(uuid.uuid4())
        now = datetime.utcnow()
        dsr = {
            "id": uuid.UUID(dsr_id),
            "subject_email": payload.subject_email,
            "request_type": payload.request_type,
            "status": "PENDING",
            "description": payload.description,
            "handler_notes": None,
            "due_date": now + timedelta(days=30),
            "completed_at": None,
            "created_at": now,
            "updated_at": now,
            "tenant_id": payload.tenant_id,
        }
        self._dsrs[dsr_id] = dsr
        return DSRResponse(**dsr)

    async def get_dsr(self, dsr_id: str) -> Optional[DSRResponse]:
        dsr = self._dsrs.get(dsr_id)
        return DSRResponse(**dsr) if dsr else None

    async def list_dsrs(
        self, status_filter: Optional[str] = None, request_type: Optional[str] = None
    ) -> List[DSRResponse]:
        items = list(self._dsrs.values())
        if status_filter:
            items = [d for d in items if d["status"] == status_filter]
        if request_type:
            items = [d for d in items if d["request_type"] == request_type]
        return [DSRResponse(**d) for d in items]

    async def update_dsr_status(self, dsr_id: str, payload: DSRStatusUpdate) -> Optional[DSRResponse]:
        dsr = self._dsrs.get(dsr_id)
        if not dsr:
            return None
        dsr["status"] = payload.status
        dsr["updated_at"] = datetime.utcnow()
        if payload.handler_notes:
            dsr["handler_notes"] = payload.handler_notes
        if payload.status == "COMPLETED":
            dsr["completed_at"] = datetime.utcnow()
        return DSRResponse(**dsr)

    async def record_consent(self, payload: ConsentCreate) -> ConsentResponse:
        consent_id = str(uuid.uuid4())
        consent = {
            "id": uuid.UUID(consent_id),
            "subject_email": payload.subject_email,
            "purpose": payload.purpose,
            "granted": payload.granted,
            "legal_basis": payload.legal_basis,
            "source": payload.source,
            "revoked_at": None,
            "created_at": datetime.utcnow(),
            "tenant_id": payload.tenant_id,
        }
        self._consents[consent_id] = consent
        return ConsentResponse(**consent)

    async def list_consents(
        self, subject_email: Optional[str] = None, purpose: Optional[str] = None
    ) -> List[ConsentResponse]:
        items = [c for c in self._consents.values() if c.get("revoked_at") is None]
        if subject_email:
            items = [c for c in items if c["subject_email"] == subject_email]
        if purpose:
            items = [c for c in items if purpose.lower() in c["purpose"].lower()]
        return [ConsentResponse(**c) for c in items]

    async def revoke_consent(self, consent_id: str) -> bool:
        consent = self._consents.get(consent_id)
        if not consent:
            return False
        consent["granted"] = False
        consent["revoked_at"] = datetime.utcnow()
        return True
