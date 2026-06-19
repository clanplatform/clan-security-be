import uuid
import re
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.ids import (SignatureCreate, SignatureResponse, IntrusionEventCreate,
                              IntrusionEventResponse, AnalyzeRequest, AnalyzeResponse)

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


class IDSService:
    def __init__(self):
        self._sigs: Dict[str, dict] = {}
        self._events: Dict[str, dict] = {}
        self._seed_signatures()

    def _seed_signatures(self):
        defaults = [
            ("SQL Injection Attempt", "2001", "EXPLOIT", "CRITICAL", r"(?:UNION|SELECT|INSERT|DROP|DELETE|UPDATE)\s+", "ALERT"),
            ("Port Scan Detection", "2002", "SCAN", "MEDIUM", r"nmap|masscan|zmap", "ALERT"),
            ("XSS Attempt", "2003", "EXPLOIT", "HIGH", r"<script[\s>]|javascript:", "ALERT"),
            ("Command Injection", "2004", "EXPLOIT", "CRITICAL", r"(?:;|\||&&)\s*(?:cat|ls|id|whoami|wget|curl)", "DROP"),
        ]
        for name, sid, cat, sev, pattern, action in defaults:
            pid = str(uuid.uuid4())
            self._sigs[pid] = {"id": uuid.UUID(pid), "name": name, "sid": sid, "category": cat,
                                "severity": sev, "pattern": pattern, "action": action, "protocol": None,
                                "description": None, "is_active": True, "match_count": 0,
                                "created_at": datetime.utcnow()}

    async def create_signature(self, payload: SignatureCreate) -> SignatureResponse:
        sid = str(uuid.uuid4())
        s = {"id": uuid.UUID(sid), "is_active": True, "match_count": 0,
             "created_at": datetime.utcnow(), **payload.model_dump()}
        self._sigs[sid] = s
        return SignatureResponse(**s)

    async def list_signatures(self) -> List[SignatureResponse]:
        return [SignatureResponse(**s) for s in self._sigs.values() if s["is_active"]]

    async def record_event(self, payload: IntrusionEventCreate) -> IntrusionEventResponse:
        eid = str(uuid.uuid4())
        e = {"id": uuid.UUID(eid), "status": "OPEN", "detected_at": datetime.utcnow(), **payload.model_dump()}
        self._events[eid] = e
        return IntrusionEventResponse(**e)

    async def list_events(self) -> List[IntrusionEventResponse]:
        return [IntrusionEventResponse(**e) for e in sorted(self._events.values(), key=lambda x: x["detected_at"], reverse=True)]

    async def analyze(self, payload: AnalyzeRequest) -> AnalyzeResponse:
        matched = []
        max_sev = None
        for s in self._sigs.values():
            if not s["is_active"]:
                continue
            try:
                if re.search(s["pattern"], payload.payload, re.IGNORECASE):
                    matched.append(s["name"])
                    s["match_count"] += 1
                    if max_sev is None or SEVERITY_ORDER.get(s["severity"], 0) > SEVERITY_ORDER.get(max_sev, 0):
                        max_sev = s["severity"]
            except re.error:
                pass
        action = "BLOCK" if matched and max_sev in ("HIGH", "CRITICAL") else ("ALERT" if matched else "ALLOW")
        return AnalyzeResponse(source_ip=payload.source_ip, threat_detected=bool(matched),
                                matched_signatures=matched, severity=max_sev, recommended_action=action)

    async def get_stats(self) -> Dict[str, Any]:
        by_sev = Counter(e["severity"] for e in self._events.values())
        by_status = Counter(e["status"] for e in self._events.values())
        return {"total_signatures": len(self._sigs), "active_signatures": sum(1 for s in self._sigs.values() if s["is_active"]),
                "total_events": len(self._events), "events_by_severity": dict(by_sev), "events_by_status": dict(by_status)}
