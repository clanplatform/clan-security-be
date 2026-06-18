import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.sox import SOXControlCreate, SOXControlResponse, SOXAssessmentCreate, SOXAssessmentResponse


class SOXService:
    def __init__(self):
        self._controls: Dict[str, dict] = {}
        self._assessments: Dict[str, dict] = {}

    async def create_control(self, payload: SOXControlCreate) -> SOXControlResponse:
        cid = str(uuid.uuid4())
        now = datetime.utcnow()
        ctrl = {"id": uuid.UUID(cid), "status": "ACTIVE", "created_at": now, "updated_at": now,
                **payload.model_dump()}
        self._controls[cid] = ctrl
        return SOXControlResponse(**ctrl)

    async def get_control(self, cid: str) -> Optional[SOXControlResponse]:
        ctrl = self._controls.get(cid)
        return SOXControlResponse(**ctrl) if ctrl else None

    async def list_controls(self, control_type: Optional[str] = None, owner: Optional[str] = None) -> List[SOXControlResponse]:
        items = list(self._controls.values())
        if control_type:
            items = [c for c in items if c["control_type"] == control_type]
        if owner:
            items = [c for c in items if owner.lower() in c["owner"].lower()]
        return [SOXControlResponse(**c) for c in items]

    async def create_assessment(self, payload: SOXAssessmentCreate) -> SOXAssessmentResponse:
        aid = str(uuid.uuid4())
        assessment = {"id": uuid.UUID(aid), "assessed_at": datetime.utcnow(), "next_assessment": None,
                      **payload.model_dump()}
        self._assessments[aid] = assessment
        return SOXAssessmentResponse(**assessment)

    async def list_assessments(self, period: Optional[str] = None, result: Optional[str] = None) -> List[SOXAssessmentResponse]:
        items = list(self._assessments.values())
        if period:
            items = [a for a in items if a["period"] == period]
        if result:
            items = [a for a in items if a["result"] == result]
        return [SOXAssessmentResponse(**a) for a in items]

    async def get_period_report(self, period: str) -> Dict[str, Any]:
        assessments = [a for a in self._assessments.values() if a["period"] == period]
        effective = sum(1 for a in assessments if a["result"] == "EFFECTIVE")
        ineffective = sum(1 for a in assessments if a["result"] == "INEFFECTIVE")
        return {
            "period": period,
            "total_assessments": len(assessments),
            "effective": effective,
            "ineffective": ineffective,
            "not_tested": len(assessments) - effective - ineffective,
            "effectiveness_rate": round(effective / len(assessments) * 100, 2) if assessments else 0,
            "has_deficiencies": any(a.get("deficiencies") for a in assessments),
        }
