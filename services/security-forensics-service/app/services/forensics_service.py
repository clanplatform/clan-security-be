import uuid
import secrets
from datetime import datetime
from typing import Optional, List, Dict
from app.schemas.forensics import (CaseCreate, CaseResponse, EvidenceCreate, EvidenceResponse, ChainOfCustodyEntry)


class ForensicsService:
    def __init__(self):
        self._cases: Dict[str, dict] = {}
        self._evidence: Dict[str, list] = {}  # case_id -> [evidence]
        self._chain: Dict[str, list] = {}     # case_id -> [entries]
        self._case_counter = 0

    def _next_case_number(self) -> str:
        self._case_counter += 1
        return f"FOR-{datetime.utcnow().year}-{self._case_counter:05d}"

    async def create_case(self, payload: CaseCreate, current_user: dict) -> CaseResponse:
        cid = str(uuid.uuid4())
        now = datetime.utcnow()
        case = {"id": uuid.UUID(cid), "case_number": self._next_case_number(),
                "status": "OPEN", "investigator_id": current_user.get("sub"),
                "created_at": now, "updated_at": now, "evidence_count": 0, **payload.model_dump()}
        self._cases[cid] = case
        self._evidence[cid] = []
        self._chain[cid] = [{"id": uuid.uuid4(), "case_id": cid, "evidence_id": None,
                              "action": "CASE_OPENED", "actor_id": current_user.get("sub", "system"),
                              "notes": "Case created", "timestamp": now}]
        return CaseResponse(**case)

    async def get_case(self, cid: str) -> Optional[CaseResponse]:
        c = self._cases.get(cid)
        if not c:
            return None
        c["evidence_count"] = len(self._evidence.get(cid, []))
        return CaseResponse(**c)

    async def list_cases(self) -> List[CaseResponse]:
        result = []
        for cid, c in self._cases.items():
            c["evidence_count"] = len(self._evidence.get(cid, []))
            result.append(CaseResponse(**c))
        return result

    async def add_evidence(self, case_id: str, payload: EvidenceCreate, current_user: dict) -> Optional[EvidenceResponse]:
        if case_id not in self._cases:
            return None
        eid = str(uuid.uuid4())
        now = datetime.utcnow()
        ev = {"id": uuid.UUID(eid), "case_id": case_id, "collected_by": current_user.get("sub"),
              "collected_at": now, **payload.model_dump()}
        self._evidence[case_id].append(ev)
        self._chain[case_id].append({"id": uuid.uuid4(), "case_id": case_id, "evidence_id": eid,
                                      "action": "EVIDENCE_COLLECTED", "actor_id": current_user.get("sub", "system"),
                                      "notes": f"Evidence '{payload.name}' added", "timestamp": now})
        return EvidenceResponse(**ev)

    async def list_evidence(self, case_id: str) -> List[EvidenceResponse]:
        return [EvidenceResponse(**e) for e in self._evidence.get(case_id, [])]

    async def get_chain(self, case_id: str) -> List[ChainOfCustodyEntry]:
        return [ChainOfCustodyEntry(**e) for e in self._chain.get(case_id, [])]
