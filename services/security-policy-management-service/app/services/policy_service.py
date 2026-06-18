import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.schemas.policy import PolicyCreate, PolicyResponse, PolicyUpdate, PolicyViolationCreate, PolicyViolationResponse


class PolicyService:
    def __init__(self):
        self._policies: Dict[str, dict] = {}
        self._violations: Dict[str, dict] = {}

    async def create_policy(self, payload: PolicyCreate) -> PolicyResponse:
        pid = str(uuid.uuid4())
        now = datetime.utcnow()
        policy = {"id": uuid.UUID(pid), "version": 1, "status": "DRAFT",
                  "review_date": None, "created_at": now, "updated_at": now,
                  **payload.model_dump()}
        self._policies[pid] = policy
        return PolicyResponse(**policy)

    async def get_policy(self, policy_id: str) -> Optional[PolicyResponse]:
        p = self._policies.get(policy_id)
        return PolicyResponse(**p) if p else None

    async def list_policies(self, category: Optional[str] = None, policy_status: Optional[str] = None) -> List[PolicyResponse]:
        items = [p for p in self._policies.values() if p["status"] != "DELETED"]
        if category:
            items = [p for p in items if category.lower() in p["category"].lower()]
        if policy_status:
            items = [p for p in items if p["status"] == policy_status]
        return [PolicyResponse(**p) for p in items]

    async def update_policy(self, policy_id: str, payload: PolicyUpdate) -> Optional[PolicyResponse]:
        policy = self._policies.get(policy_id)
        if not policy:
            return None
        updates = {k: v for k, v in payload.model_dump().items() if v is not None}
        if "content" in updates:
            policy["version"] += 1
        policy.update(updates)
        policy["updated_at"] = datetime.utcnow()
        return PolicyResponse(**policy)

    async def set_policy_status(self, policy_id: str, new_status: str) -> Optional[PolicyResponse]:
        policy = self._policies.get(policy_id)
        if not policy:
            return None
        policy["status"] = new_status
        policy["updated_at"] = datetime.utcnow()
        return PolicyResponse(**policy)

    async def delete_policy(self, policy_id: str) -> bool:
        if policy_id not in self._policies:
            return False
        self._policies[policy_id]["status"] = "DELETED"
        return True

    async def report_violation(self, policy_id: str, payload: PolicyViolationCreate) -> PolicyViolationResponse:
        vid = str(uuid.uuid4())
        violation = {"id": uuid.UUID(vid), "policy_id": uuid.UUID(policy_id),
                     "status": "OPEN", "resolution": None,
                     "created_at": datetime.utcnow(), "resolved_at": None,
                     **payload.model_dump()}
        self._violations[vid] = violation
        return PolicyViolationResponse(**violation)

    async def get_violations(self, policy_id: str) -> List[PolicyViolationResponse]:
        items = [v for v in self._violations.values() if str(v["policy_id"]) == policy_id]
        return [PolicyViolationResponse(**v) for v in items]
