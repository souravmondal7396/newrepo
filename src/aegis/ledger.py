from __future__ import annotations
import json, os
from dataclasses import replace
from pathlib import Path
from .model import DecryptionEvent, b64, canonical, digest, unb64, utc_now
from .pq import verify_signature, PQIdentity

class AppendOnlyLedger:
    def __init__(self, path: Path): self.path=path; self.path.parent.mkdir(parents=True, exist_ok=True)
    def last_hash(self) -> str:
        if not self.path.exists(): return ""
        lines=self.path.read_text().splitlines(); return json.loads(lines[-1])["record_hash"] if lines else ""
    def append(self, event: DecryptionEvent) -> str:
        if event.previous_record_hash != self.last_hash(): raise ValueError("ledger head changed; rebuild and re-sign event")
        if not verify_signature(event.signature_algorithm, unb64(event.signer_public_key), event.bytes_to_sign(), unb64(event.signature)):
            raise ValueError("invalid event signature")
        if self.find(event.watermark_id): raise ValueError("watermark already exists")
        record=event.to_dict(); record["record_hash"]=digest(canonical(record))
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps(record, sort_keys=True)+"\n")
        return record["record_hash"]
    def find(self, watermark_id: str) -> dict | None:
        if not self.path.exists(): return None
        for line in self.path.read_text().splitlines():
            record=json.loads(line)
            if record.get("watermark_id") == watermark_id: return record
        return None
    def verify_chain(self) -> bool:
        previous=""
        if not self.path.exists(): return True
        for line in self.path.read_text().splitlines():
            record=json.loads(line); supplied=record.pop("record_hash", None)
            if supplied != digest(canonical(record)) or record.get("previous_record_hash") != previous: return False
            if not verify_signature(record["signature_algorithm"], unb64(record["signer_public_key"]), canonical({k:v for k,v in record.items() if k != "signature"}), unb64(record["signature"])): return False
            previous=supplied
        return True

def create_event(document: bytes, version: bytes, recipient_key_id: str, watermark_id: str, identity: PQIdentity, previous_record_hash="") -> DecryptionEvent:
    event=DecryptionEvent(1, os.urandom(16).hex(), digest(document), digest(version), recipient_key_id, os.urandom(16).hex(), watermark_id, utc_now(), digest(watermark_id.encode()), identity.algorithm, identity.export_public(), "", previous_record_hash)
    return replace(event, signature=b64(identity.sign(event.bytes_to_sign())))
