import uuid
import re
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.masking import MaskingConfigCreate, MaskingConfigResponse, MaskRequest, MaskResponse, UnmaskRequest


class MaskingService:
    def __init__(self):
        self._configs: Dict[str, dict] = {}
        self._tokens: Dict[str, str] = {}  # token -> original value
        self._seed_configs()

    def _seed_configs(self):
        defaults = [
            ("Email Masker", "EMAIL", "PARTIAL", None, "***@***.***"),
            ("Phone Masker", "PHONE", "PARTIAL", None, "***-***-****"),
            ("CC Masker", "CC_NUMBER", "REDACT", None, "****-****-****-****"),
            ("SSN Masker", "SSN", "REDACT", None, "***-**-****"),
            ("Name Masker", "NAME", "REDACT", None, "[REDACTED]"),
        ]
        for name, ftype, mtype, pattern, replacement in defaults:
            cid = str(uuid.uuid4())
            self._configs[cid] = {"id": uuid.UUID(cid), "name": name, "field_type": ftype,
                                   "mask_type": mtype, "pattern": pattern, "replacement": replacement,
                                   "preserve_length": False, "preserve_format": True,
                                   "is_active": True, "created_at": datetime.utcnow()}

    async def create_config(self, payload: MaskingConfigCreate) -> MaskingConfigResponse:
        cid = str(uuid.uuid4())
        cfg = {"id": uuid.UUID(cid), "is_active": True, "created_at": datetime.utcnow(), **payload.model_dump()}
        self._configs[cid] = cfg
        return MaskingConfigResponse(**cfg)

    async def get_config(self, cid: str) -> Optional[MaskingConfigResponse]:
        cfg = self._configs.get(cid)
        return MaskingConfigResponse(**cfg) if cfg else None

    async def list_configs(self) -> List[MaskingConfigResponse]:
        return [MaskingConfigResponse(**c) for c in self._configs.values() if c["is_active"]]

    def _mask_value(self, value: str, config: dict) -> tuple[str, Optional[str]]:
        if config["mask_type"] == "REDACT":
            return config["replacement"], None
        elif config["mask_type"] == "HASH":
            return hashlib.sha256(value.encode()).hexdigest()[:16], None
        elif config["mask_type"] == "TOKENIZE":
            token = f"TOKEN_{secrets.token_hex(8).upper()}"
            self._tokens[token] = value
            return token, token
        elif config["mask_type"] == "PARTIAL":
            if len(value) <= 4:
                return config["replacement"], None
            return value[:2] + "*" * (len(value) - 4) + value[-2:], None
        return config["replacement"], None

    async def mask(self, payload: MaskRequest) -> MaskResponse:
        masked = {}
        tokens = {}
        fields_masked = 0
        configs = list(self._configs.values()) if not payload.config_ids else [
            self._configs[str(cid)] for cid in payload.config_ids
            if str(cid) in self._configs
        ]
        active_configs = {c["field_type"]: c for c in configs if c["is_active"]}
        for key, value in payload.data.items():
            if not isinstance(value, str):
                masked[key] = value
                continue
            matched = False
            for ftype, cfg in active_configs.items():
                if ftype.lower() in key.lower() or key.lower() in ftype.lower():
                    masked_val, token = self._mask_value(value, cfg)
                    masked[key] = masked_val
                    if token:
                        tokens[key] = token
                    fields_masked += 1
                    matched = True
                    break
            if not matched:
                masked[key] = value
        return MaskResponse(masked_data=masked, fields_masked=fields_masked, tokens=tokens)

    async def unmask(self, payload: UnmaskRequest) -> Dict[str, Any]:
        result = {}
        for field, token in payload.tokens.items():
            original = self._tokens.get(token)
            result[field] = original if original else "[TOKEN_NOT_FOUND]"
        return result
