import uuid
import re
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.dlp import DLPRuleCreate, DLPRuleResponse, DLPViolationResponse, ScanRequest, ScanResult


class DLPService:
    def __init__(self):
        self._rules: Dict[str, dict] = {}
        self._violations: Dict[str, dict] = {}
        self._seed_rules()

    def _seed_rules(self):
        defaults = [
            ("Credit Card Numbers", "REGEX", r"\b(?:\d[ -]*?){13,16}\b", "HIGH", "ALERT"),
            ("SSN Pattern", "REGEX", r"\b\d{3}-\d{2}-\d{4}\b", "CRITICAL", "BLOCK"),
            ("Email Addresses", "REGEX", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "LOW", "ALERT"),
            ("API Keys", "KEYWORD", "api_key", "HIGH", "ALERT"),
        ]
        for name, rtype, pattern, severity, action in defaults:
            rid = str(uuid.uuid4())
            self._rules[rid] = {"id": uuid.UUID(rid), "name": name, "rule_type": rtype,
                                 "pattern": pattern, "severity": severity, "action": action,
                                 "description": None, "is_active": True, "match_count": 0,
                                 "created_at": datetime.utcnow()}

    async def create_rule(self, payload: DLPRuleCreate) -> DLPRuleResponse:
        rid = str(uuid.uuid4())
        rule = {"id": uuid.UUID(rid), "is_active": True, "match_count": 0,
                "created_at": datetime.utcnow(), **payload.model_dump()}
        self._rules[rid] = rule
        return DLPRuleResponse(**rule)

    async def list_rules(self, rule_type: Optional[str] = None) -> List[DLPRuleResponse]:
        items = [r for r in self._rules.values() if r["is_active"]]
        if rule_type:
            items = [r for r in items if r["rule_type"] == rule_type]
        return [DLPRuleResponse(**r) for r in items]

    async def delete_rule(self, rule_id: str) -> bool:
        if rule_id not in self._rules:
            return False
        self._rules[rule_id]["is_active"] = False
        return True

    async def scan(self, payload: ScanRequest) -> ScanResult:
        start = time.time()
        violations = []
        blocked = False
        for rule in self._rules.values():
            if not rule["is_active"]:
                continue
            try:
                if rule["rule_type"] == "REGEX":
                    matches = re.findall(rule["pattern"], payload.content)
                else:
                    matches = [payload.content] if rule["pattern"].lower() in payload.content.lower() else []
                if matches:
                    rule["match_count"] += 1
                    v_id = str(uuid.uuid4())
                    violation = {
                        "id": uuid.UUID(v_id), "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "content_snippet": payload.content[:100] + "...",
                        "source": payload.source, "severity": rule["severity"],
                        "action_taken": rule["action"], "user_id": payload.user_id,
                        "is_resolved": False, "resolution_notes": None,
                        "detected_at": datetime.utcnow(), "resolved_at": None,
                    }
                    self._violations[v_id] = violation
                    violations.append({"rule": rule["name"], "severity": rule["severity"], "action": rule["action"]})
                    if rule["action"] == "BLOCK":
                        blocked = True
            except re.error:
                pass
        duration = (time.time() - start) * 1000
        return ScanResult(violations_found=len(violations), violations=violations,
                          blocked=blocked, scan_duration_ms=round(duration, 2))

    async def list_violations(self, severity: Optional[str] = None, resolved: Optional[bool] = None) -> List[DLPViolationResponse]:
        items = list(self._violations.values())
        if severity:
            items = [v for v in items if v["severity"] == severity]
        if resolved is not None:
            items = [v for v in items if v["is_resolved"] == resolved]
        return [DLPViolationResponse(**v) for v in items]

    async def resolve_violation(self, violation_id: str) -> Optional[DLPViolationResponse]:
        v = self._violations.get(violation_id)
        if not v:
            return None
        v["is_resolved"] = True
        v["resolved_at"] = datetime.utcnow()
        return DLPViolationResponse(**v)
