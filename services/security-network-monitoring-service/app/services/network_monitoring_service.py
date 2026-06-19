import uuid
from collections import Counter
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.network_monitoring import (DeviceCreate, DeviceResponse, FlowCreate, FlowResponse, NetworkStatsResponse)


class NetworkMonitoringService:
    def __init__(self):
        self._devices: Dict[str, dict] = {}
        self._flows: Dict[str, dict] = {}

    async def register_device(self, payload: DeviceCreate) -> DeviceResponse:
        did = str(uuid.uuid4())
        now = datetime.utcnow()
        d = {"id": uuid.UUID(did), "status": "ONLINE", "last_seen": now,
             "registered_at": now, **payload.model_dump()}
        self._devices[did] = d
        return DeviceResponse(**d)

    async def get_device(self, did: str) -> Optional[DeviceResponse]:
        d = self._devices.get(did)
        return DeviceResponse(**d) if d else None

    async def list_devices(self) -> List[DeviceResponse]:
        return [DeviceResponse(**d) for d in self._devices.values()]

    async def record_flow(self, payload: FlowCreate) -> FlowResponse:
        fid = str(uuid.uuid4())
        f = {"id": uuid.UUID(fid), "recorded_at": datetime.utcnow(), **payload.model_dump()}
        self._flows[fid] = f
        return FlowResponse(**f)

    async def list_flows(self, source_ip: Optional[str] = None) -> List[FlowResponse]:
        flows = list(self._flows.values())
        if source_ip:
            flows = [f for f in flows if f["source_ip"] == source_ip]
        return [FlowResponse(**f) for f in sorted(flows, key=lambda x: x["recorded_at"], reverse=True)[:200]]

    async def get_stats(self) -> NetworkStatsResponse:
        online = sum(1 for d in self._devices.values() if d["status"] == "ONLINE")
        total_in = sum(f["bytes_received"] for f in self._flows.values())
        total_out = sum(f["bytes_sent"] for f in self._flows.values())
        talker_counts = Counter(f["source_ip"] for f in self._flows.values())
        top_talkers = [{"ip": ip, "flows": cnt} for ip, cnt in talker_counts.most_common(10)]
        return NetworkStatsResponse(total_devices=len(self._devices), online_devices=online,
                                     total_flows=len(self._flows), total_bytes_in=total_in,
                                     total_bytes_out=total_out, top_talkers=top_talkers,
                                     generated_at=datetime.utcnow())
