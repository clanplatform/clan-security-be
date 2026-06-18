import base64
import secrets
from typing import Dict
from cryptography.fernet import Fernet
from app.schemas.encryption import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse, GenerateKeyResponse


class EncryptionService:
    def __init__(self):
        self._keys: Dict[str, bytes] = {}

    async def generate_key(self, algorithm: str = "AES-256") -> GenerateKeyResponse:
        key_id = f"key_{secrets.token_hex(8)}"
        fernet_key = Fernet.generate_key()
        self._keys[key_id] = fernet_key
        return GenerateKeyResponse(
            key_id=key_id,
            algorithm=algorithm,
            key_material=base64.urlsafe_b64encode(fernet_key).decode(),
            key_size=256,
        )

    def _get_or_create_key(self, key_id: str) -> tuple[str, bytes]:
        if key_id and key_id in self._keys:
            return key_id, self._keys[key_id]
        new_id = f"key_{secrets.token_hex(8)}"
        fernet_key = Fernet.generate_key()
        self._keys[new_id] = fernet_key
        return new_id, fernet_key

    async def encrypt(self, payload: EncryptRequest) -> EncryptResponse:
        key_id, key_material = self._get_or_create_key(payload.key_id or "")
        f = Fernet(key_material)
        ciphertext = f.encrypt(payload.plaintext.encode()).decode()
        return EncryptResponse(ciphertext=ciphertext, key_id=key_id, algorithm=payload.algorithm)

    async def decrypt(self, payload: DecryptRequest) -> DecryptResponse:
        key_material = self._keys.get(payload.key_id)
        if not key_material:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Key not found")
        f = Fernet(key_material)
        plaintext = f.decrypt(payload.ciphertext.encode()).decode()
        return DecryptResponse(plaintext=plaintext, key_id=payload.key_id, algorithm=payload.algorithm)
