from __future__ import annotations
import json, os
from dataclasses import replace
from pathlib import Path
from .model import DecryptionEvent, b64, digest, utc_now
from .pq import PQIdentity

class AppendOnlyLedger:
    def __init__(self, path: Path): self.path=path; self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, event: DecryptionEvent) -> str:
        previous = ""
        if self.path.exists():
            lines=self.path.read_text().splitlines(); previous=json.loads(lines[-1])["record_hash"] if lines else ""
        event=replace(event, previous_record_hash=previous); record=event.to_dict(); record["record_hash"]=digest(json.dumps(record, sort_keys=True).encode())
        with self.path.open("a") as f: f.write(json.dumps(record, sort_keys=True)+"\n")
        return record["record_hash"]
    def find(self, watermark_id: str) -> dict | None:
        if not self.path.exists(): return None
        for line in self.path.read_text().splitlines():
            record=json.loads(line)
            if record["watermark_id"] == watermark_id: return record
        return None
    def verify_chain(self) -> bool:
        previous=""
        if not self.path.exists(): return True
        for line in self.path.read_text().splitlines():
            record=json.loads(line); supplied=record.pop("record_hash"); expected=digest(json.dumps(record, sort_keys=True).encode())
            if supplied != expected or record["previous_record_hash"] != previous: return False
            previous=supplied
        return True

def create_event(document: bytes, version: bytes, recipient_key_id: str, watermark_id: str, identity: PQIdentity) -> DecryptionEvent:
    event=DecryptionEvent(1, os.urandom(16).hex(), digest(document), digest(version), recipient_key_id, os.urandom(16).hex(), watermark_id, utc_now(), digest(watermark_id.encode()), identity.algorithm, b64(identity.public))
    return replace(event, signature=b64(identity.sign(event.bytes_to_sign())))
