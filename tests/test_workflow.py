import json
from pathlib import Path
from aegis.ledger import AppendOnlyLedger, create_event
from aegis.pq import PQIdentity

def test_signed_event_and_chain(tmp_path: Path):
    identity=PQIdentity.generate(); event=create_event(b"doc", b"version", "r1", "wm-1", identity)
    ledger=AppendOnlyLedger(tmp_path/"ledger.jsonl"); ledger.append(event)
    assert ledger.verify_chain(); assert ledger.find("wm-1")["event_id"] == event.event_id
    assert identity.verify(event.bytes_to_sign(), __import__('base64').urlsafe_b64decode(event.signature + "=" * (-len(event.signature)%4)))
