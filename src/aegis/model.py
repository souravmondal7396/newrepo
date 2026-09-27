from __future__ import annotations
import base64, hashlib, json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


def b64(value: bytes) -> str: return base64.urlsafe_b64encode(value).decode().rstrip("=")
def unb64(value: str) -> bytes: return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
def digest(value: bytes) -> str: return hashlib.sha3_256(value).hexdigest()
def canonical(value: dict) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
def utc_now() -> str: return datetime.now(timezone.utc).isoformat()

@dataclass
class DecryptionEvent:
    schema_version: int
    event_id: str
    document_id: str
    document_version: str
    recipient_key_id: str
    session_id: str
    watermark_id: str
    decryption_time: str
    watermark_digest: str
    signature_algorithm: str
    signer_public_key: str
    signature: str = ""
    previous_record_hash: str = ""

    def unsigned(self) -> dict:
        value = asdict(self); value.pop("signature"); return value
    def bytes_to_sign(self) -> bytes: return canonical(self.unsigned())
    def to_dict(self) -> dict: return asdict(self)
