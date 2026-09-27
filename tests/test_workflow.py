from pathlib import Path
from aegis.ledger import AppendOnlyLedger, create_event
from aegis.pq import PQIdentity

def test_signed_event_and_chain(tmp_path: Path):
    identity=PQIdentity.generate(); ledger=AppendOnlyLedger(tmp_path/"ledger.jsonl")
    event=create_event(b"doc",b"version","r1","wm-1",identity,ledger.last_hash()); ledger.append(event)
    assert ledger.verify_chain(); assert ledger.find("wm-1")["event_id"]==event.event_id

def test_tamper_is_detected(tmp_path: Path):
    identity=PQIdentity.generate(); ledger=AppendOnlyLedger(tmp_path/"ledger.jsonl")
    ledger.append(create_event(b"doc",b"v","r1","wm-1",identity,ledger.last_hash()))
    content=ledger.path.read_text().replace('"r1"','"attacker"'); ledger.path.write_text(content)
    assert not ledger.verify_chain()
