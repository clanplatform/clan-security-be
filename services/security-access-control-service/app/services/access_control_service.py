import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.access_control import (RoleCreate, RoleResponse, PermissionCreate, PermissionResponse,
                                          RolePermissionAssign, AccessCheckRequest, AccessCheckResponse)


class AccessControlService:
    def __init__(self):
        self._roles: Dict[str, dict] = {}
        self._permissions: Dict[str, dict] = {}
        self._role_permissions: Dict[str, List[str]] = {}  # role_id -> [permission_ids]
        self._seed_defaults()

    def _seed_defaults(self):
        for pname, resource, action in [
            ("admin:*", "*", "ADMIN"), ("user:read", "user", "READ"),
            ("user:write", "user", "CREATE"), ("user:update", "user", "UPDATE"),
            ("audit:read", "audit", "READ"), ("report:read", "report", "READ"),
        ]:
            pid = str(uuid.uuid4())
            self._permissions[pid] = {"id": uuid.UUID(pid), "name": pname, "resource": resource,
                                       "action": action, "description": None, "created_at": datetime.utcnow()}
        for rname, is_sys in [("admin", True), ("viewer", False), ("operator", False)]:
            rid = str(uuid.uuid4())
            self._roles[rid] = {"id": uuid.UUID(rid), "name": rname, "description": f"{rname} role",
                                 "is_system_role": is_sys, "is_active": True,
                                 "created_at": datetime.utcnow(), "tenant_id": None}
            self._role_permissions[rid] = []

    async def create_role(self, payload: RoleCreate) -> RoleResponse:
        rid = str(uuid.uuid4())
        role = {"id": uuid.UUID(rid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._roles[rid] = role
        self._role_permissions[rid] = []
        return RoleResponse(**role, permissions=[])

    async def list_roles(self) -> List[RoleResponse]:
        result = []
        for rid, r in self._roles.items():
            perm_names = [self._permissions[pid]["name"] for pid in self._role_permissions.get(rid, []) if pid in self._permissions]
            result.append(RoleResponse(**r, permissions=perm_names))
        return result

    async def create_permission(self, payload: PermissionCreate) -> PermissionResponse:
        pid = str(uuid.uuid4())
        perm = {"id": uuid.UUID(pid), "created_at": datetime.utcnow(), **payload.model_dump()}
        self._permissions[pid] = perm
        return PermissionResponse(**perm)

    async def list_permissions(self) -> List[PermissionResponse]:
        return [PermissionResponse(**p) for p in self._permissions.values()]

    async def assign_permission(self, role_id: str, payload: RolePermissionAssign) -> Optional[RoleResponse]:
        role = self._roles.get(role_id)
        if not role:
            return None
        perm_id = str(payload.permission_id)
        if role_id not in self._role_permissions:
            self._role_permissions[role_id] = []
        if perm_id not in self._role_permissions[role_id]:
            self._role_permissions[role_id].append(perm_id)
        perm_names = [self._permissions[pid]["name"] for pid in self._role_permissions[role_id] if pid in self._permissions]
        return RoleResponse(**role, permissions=perm_names)

    async def check_access(self, payload: AccessCheckRequest) -> AccessCheckResponse:
        for rid, role in self._roles.items():
            if role["name"] in payload.roles and role["is_active"]:
                for pid in self._role_permissions.get(rid, []):
                    perm = self._permissions.get(pid)
                    if perm and (perm["resource"] in (payload.resource, "*")) and perm["action"] in (payload.action, "ADMIN"):
                        return AccessCheckResponse(allowed=True, subject=payload.subject,
                                                    resource=payload.resource, action=payload.action,
                                                    matched_permission=perm["name"], reason="Permission matched via role")
        return AccessCheckResponse(allowed=False, subject=payload.subject, resource=payload.resource,
                                    action=payload.action, reason="No matching permission found")
