import uuid
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.threat_detection import (RuleCreate, RuleResponse, IOCCreate, IOCResponse, DetectRequest, DetectResponse)

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


class ThreatDetectionService:
    def __init__(self):
        self._rules: Dict[str, dict] = {}
        self._iocs: Dict[str, dict] = {}
        self._seed()

    def _seed(self):
        seed_iocs = [
            ("IP", "198.51.100.1", "CRITICAL", "Known C2 server"),
            ("DOMAIN", "malware.example.com", "HIGH", "Known malware distribution"),
            ("HASH_MD5", "d41d8cd98f00b204e9800998ecf8427e", "CRITICAL", "Known ransomware hash"),
        ]
        for ioc_type, value, sev, desc in seed_iocs:
            iid = str(uuid.uuid4())
            self._iocs[iid] = {"id": uuid.UUID(iid), "ioc_type": ioc_type, "value": value,
                                "confidence": 95, "severity": sev, "source": "SEED", "description": desc,
                                "is_active": True, "created_at": datetime.utcnow()}

    async def create_rule(self, payload: RuleCreate) -> RuleResponse:
        rid = str(uuid.uuid4())
        r = {"id": uuid.UUID(rid), "is_active": True, "hit_count": 0,
             "created_at": datetime.utcnow(), **payload.model_dump()}
        self._rules[rid] = r
        return RuleResponse(**r)

    async def list_rules(self) -> List[RuleResponse]:
        return [RuleResponse(**r) for r in self._rules.values() if r["is_active"]]

    async def add_ioc(self, payload: IOCCreate) -> IOCResponse:
        iid = str(uuid.uuid4())
        i = {"id": uuid.UUID(iid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._iocs[iid] = i
        return IOCResponse(**i)

    async def list_iocs(self) -> List[IOCResponse]:
        return [IOCResponse(**i) for i in self._iocs.values() if i["is_active"]]

    async def detect(self, payload: DetectRequest) -> DetectResponse:
        matched_iocs = []
        max_sev = None
        for ioc in self._iocs.values():
            if not ioc["is_active"]:
                continue
            match_val = None
            if ioc["ioc_type"] == "IP" and payload.source_ip == ioc["value"]:
                match_val = ioc["value"]
            elif ioc["ioc_type"] == "DOMAIN" and payload.domain == ioc["value"]:
                match_val = ioc["value"]
            elif ioc["ioc_type"].startswith("HASH_") and payload.file_hash == ioc["value"]:
                match_val = ioc["value"]
            elif ioc["ioc_type"] == "URL" and payload.url == ioc["value"]:
                match_val = ioc["value"]
            if match_val:
                matched_iocs.append(f"{ioc['ioc_type']}:{match_val}")
                if max_sev is None or SEVERITY_ORDER.get(ioc["severity"], 0) > SEVERITY_ORDER.get(max_sev, 0):
                    max_sev = ioc["severity"]
        detected = bool(matched_iocs)
        action = "BLOCK" if detected and max_sev in ("HIGH", "CRITICAL") else ("ALERT" if detected else "ALLOW")
        return DetectResponse(threat_detected=detected, matched_rules=[], matched_iocs=matched_iocs,
                               overall_severity=max_sev, recommended_action=action, analyzed_at=datetime.utcnow())

    async def get_stats(self) -> Dict[str, Any]:
        by_type = Counter(i["ioc_type"] for i in self._iocs.values())
        return {"total_rules": len(self._rules), "active_rules": sum(1 for r in self._rules.values() if r["is_active"]),
                "total_iocs": len(self._iocs), "iocs_by_type": dict(by_type)}
