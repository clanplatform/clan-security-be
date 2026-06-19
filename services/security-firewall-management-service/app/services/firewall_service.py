import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.schemas.firewall import (FirewallRuleCreate, FirewallRuleResponse,
                                   PacketCheckRequest, PacketCheckResponse)


class FirewallService:
    def __init__(self):
        self._rules: Dict[str, dict] = {}
        self._seed_rules()

    def _seed_rules(self):
        defaults = [
            ("Block All Inbound Telnet", "INBOUND", "DENY", "TCP", None, None, None, "23", 10),
            ("Allow HTTP", "INBOUND", "ALLOW", "TCP", None, None, None, "80", 100),
            ("Allow HTTPS", "INBOUND", "ALLOW", "TCP", None, None, None, "443", 100),
            ("Block RFC1918 Outbound", "OUTBOUND", "DENY", "ANY", None, None, "10.0.0.0/8", None, 50),
        ]
        for name, direction, action, proto, sip, sport, dip, dport, prio in defaults:
            rid = str(uuid.uuid4())
            self._rules[rid] = {"id": uuid.UUID(rid), "name": name, "direction": direction,
                                 "action": action, "protocol": proto, "source_ip": sip,
                                 "source_port": sport, "destination_ip": dip, "destination_port": dport,
                                 "priority": prio, "description": None, "is_active": True,
                                 "hit_count": 0, "created_at": datetime.utcnow()}

    async def create_rule(self, payload: FirewallRuleCreate) -> FirewallRuleResponse:
        rid = str(uuid.uuid4())
        r = {"id": uuid.UUID(rid), "is_active": True, "hit_count": 0,
             "created_at": datetime.utcnow(), **payload.model_dump()}
        self._rules[rid] = r
        return FirewallRuleResponse(**r)

    async def get_rule(self, rid: str) -> Optional[FirewallRuleResponse]:
        r = self._rules.get(rid)
        return FirewallRuleResponse(**r) if r else None

    async def list_rules(self) -> List[FirewallRuleResponse]:
        return [FirewallRuleResponse(**r) for r in sorted(self._rules.values(), key=lambda x: x["priority"])]

    async def toggle(self, rid: str) -> Optional[FirewallRuleResponse]:
        r = self._rules.get(rid)
        if not r:
            return None
        r["is_active"] = not r["is_active"]
        return FirewallRuleResponse(**r)

    async def delete_rule(self, rid: str) -> bool:
        return bool(self._rules.pop(rid, None))

    async def check_packet(self, payload: PacketCheckRequest) -> PacketCheckResponse:
        active = sorted([r for r in self._rules.values() if r["is_active"]], key=lambda x: x["priority"])
        for rule in active:
            if rule["direction"] not in (payload.direction, "BOTH"):
                continue
            if rule["protocol"] not in (payload.protocol, "ANY"):
                continue
            if rule["destination_port"] and str(payload.destination_port) != rule["destination_port"]:
                continue
            if rule["destination_ip"] and not payload.destination_ip.startswith(rule["destination_ip"][:5]):
                continue
            rule["hit_count"] += 1
            allowed = rule["action"] in ("ALLOW", "LOG")
            return PacketCheckResponse(allowed=allowed, action=rule["action"],
                                        matched_rule_id=str(rule["id"]), matched_rule_name=rule["name"],
                                        reason=f"Matched rule '{rule['name']}'")
        return PacketCheckResponse(allowed=False, action="DENY", matched_rule_id=None,
                                    matched_rule_name=None, reason="Default deny — no matching rule")
