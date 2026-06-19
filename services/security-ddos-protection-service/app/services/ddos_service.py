import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.core.config import settings
from app.schemas.ddos import (RateLimitRuleCreate, RateLimitRuleResponse, BlockedIPCreate,
                                BlockedIPResponse, AttackEventCreate, AttackEventResponse,
                                TrafficAnalysisRequest, TrafficAnalysisResponse)


class DDoSService:
    def __init__(self):
        self._rules: Dict[str, dict] = {}
        self._blocked: Dict[str, dict] = {}
        self._attacks: Dict[str, dict] = {}

    async def create_rule(self, payload: RateLimitRuleCreate) -> RateLimitRuleResponse:
        rid = str(uuid.uuid4())
        r = {"id": uuid.UUID(rid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._rules[rid] = r
        return RateLimitRuleResponse(**r)

    async def list_rules(self) -> List[RateLimitRuleResponse]:
        return [RateLimitRuleResponse(**r) for r in self._rules.values()]

    async def block_ip(self, payload: BlockedIPCreate) -> BlockedIPResponse:
        bid = str(uuid.uuid4())
        b = {"id": uuid.UUID(bid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._blocked[bid] = b
        return BlockedIPResponse(**b)

    async def list_blocked(self) -> List[BlockedIPResponse]:
        return [BlockedIPResponse(**b) for b in self._blocked.values() if b["is_active"]]

    async def unblock_ip(self, bid: str) -> bool:
        b = self._blocked.get(bid)
        if not b:
            return False
        b["is_active"] = False
        return True

    async def record_attack(self, payload: AttackEventCreate) -> AttackEventResponse:
        aid = str(uuid.uuid4())
        a = {"id": uuid.UUID(aid), "detected_at": datetime.utcnow(), **payload.model_dump()}
        self._attacks[aid] = a
        return AttackEventResponse(**a)

    async def list_attacks(self) -> List[AttackEventResponse]:
        return [AttackEventResponse(**a) for a in sorted(self._attacks.values(), key=lambda x: x["detected_at"], reverse=True)]

    async def analyze(self, payload: TrafficAnalysisRequest) -> TrafficAnalysisResponse:
        is_blocked = any(b["ip_address"] == payload.source_ip and b["is_active"] for b in self._blocked.values())
        risk = 0
        if payload.requests_per_second > settings.BLOCK_THRESHOLD_RPS:
            risk = 90
        elif payload.requests_per_second > settings.DEFAULT_RATE_LIMIT_RPS:
            risk = 50
        is_suspicious = risk >= 50
        action = "BLOCK" if risk >= 90 else ("THROTTLE" if risk >= 50 else "ALLOW")
        reason = f"RPS={payload.requests_per_second:.0f} threshold={settings.DEFAULT_RATE_LIMIT_RPS}"
        if is_blocked:
            action = "BLOCK"
            risk = 100
            reason = "IP is in blocklist"
        return TrafficAnalysisResponse(source_ip=payload.source_ip, is_suspicious=is_suspicious,
                                        is_blocked=is_blocked, risk_score=risk,
                                        recommended_action=action, reason=reason)
