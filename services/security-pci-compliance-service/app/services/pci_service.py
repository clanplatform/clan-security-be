import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.pci import PCIControlCreate, PCIControlResponse, ComplianceCheckCreate, ComplianceCheckResponse


class PCIService:
    def __init__(self):
        self._controls: Dict[str, dict] = {}
        self._checks: Dict[str, dict] = {}
        self._seed_controls()

    def _seed_controls(self):
        requirements = [
            ("1.1", "Install and maintain a firewall configuration", "Network Security"),
            ("2.1", "Do not use vendor-supplied defaults for passwords", "Secure Configuration"),
            ("3.1", "Keep cardholder data storage to a minimum", "Data Protection"),
            ("4.1", "Use strong cryptography for cardholder data transmission", "Encryption"),
            ("6.1", "Protect all systems against malware", "Vulnerability Management"),
            ("7.1", "Limit access to system components to only those individuals whose job requires access", "Access Control"),
            ("8.1", "Identify and authenticate access to system components", "Identity Management"),
            ("10.1", "Implement audit trails to link all access to system components", "Audit Logging"),
            ("11.1", "Test security of systems and networks regularly", "Security Testing"),
            ("12.1", "Establish, publish, maintain, and disseminate a security policy", "Policy Management"),
        ]
        for req_id, title, category in requirements:
            ctrl_id = str(uuid.uuid4())
            self._controls[ctrl_id] = {
                "id": uuid.UUID(ctrl_id),
                "requirement_id": req_id,
                "title": title,
                "description": f"PCI DSS Requirement {req_id}",
                "category": category,
                "status": "ACTIVE",
                "last_assessed": None,
                "created_at": datetime.utcnow(),
            }

    async def create_control(self, payload: PCIControlCreate) -> PCIControlResponse:
        ctrl_id = str(uuid.uuid4())
        ctrl = {"id": uuid.UUID(ctrl_id), "status": "ACTIVE", "last_assessed": None,
                "created_at": datetime.utcnow(), **payload.model_dump()}
        self._controls[ctrl_id] = ctrl
        return PCIControlResponse(**ctrl)

    async def get_control(self, ctrl_id: str) -> Optional[PCIControlResponse]:
        ctrl = self._controls.get(ctrl_id)
        return PCIControlResponse(**ctrl) if ctrl else None

    async def list_controls(self, category: Optional[str] = None, status_filter: Optional[str] = None) -> List[PCIControlResponse]:
        items = list(self._controls.values())
        if category:
            items = [c for c in items if category.lower() in c["category"].lower()]
        if status_filter:
            items = [c for c in items if c["status"] == status_filter]
        return [PCIControlResponse(**c) for c in items]

    async def create_check(self, payload: ComplianceCheckCreate) -> ComplianceCheckResponse:
        check_id = str(uuid.uuid4())
        check = {"id": uuid.UUID(check_id), "assessed_at": datetime.utcnow(),
                 "next_review": None, **payload.model_dump()}
        self._checks[check_id] = check
        ctrl = next((c for c in self._controls.values() if c["id"] == payload.control_id), None)
        if ctrl:
            ctrl["last_assessed"] = datetime.utcnow()
        return ComplianceCheckResponse(**check)

    async def list_checks(self, control_id: Optional[str] = None, result: Optional[str] = None) -> List[ComplianceCheckResponse]:
        items = list(self._checks.values())
        if control_id:
            items = [c for c in items if str(c["control_id"]) == control_id]
        if result:
            items = [c for c in items if c["result"] == result]
        return [ComplianceCheckResponse(**c) for c in items]

    async def get_summary(self) -> Dict[str, Any]:
        checks = list(self._checks.values())
        passed = sum(1 for c in checks if c["result"] == "PASS")
        failed = sum(1 for c in checks if c["result"] == "FAIL")
        total_controls = len(self._controls)
        return {
            "total_controls": total_controls,
            "total_checks": len(checks),
            "passed": passed,
            "failed": failed,
            "compliance_percentage": round((passed / len(checks) * 100) if checks else 0, 2),
        }
