from __future__ import annotations
import argparse, json, os
from pathlib import Path
from .ledger import AppendOnlyLedger, create_event
from .model import b64, digest, unb64
from .pq import PQIdentity

def demo(workdir: Path):
    workdir.mkdir(parents=True, exist_ok=True); identity=PQIdentity.generate(); document=b"SIH confidential document demo"
    event=create_event(document, document, "recipient-demo", os.urandom(16).hex(), identity)
    ledger=AppendOnlyLedger(workdir/"ledger.jsonl"); ledger.append(event)
    assert ledger.verify_chain(); record=ledger.find(event.watermark_id)
    assert record and identity.verify(event.bytes_to_sign(), unb64(event.signature))
    (workdir/"event.json").write_text(json.dumps(record, indent=2)); print(json.dumps({"status":"verified","watermark_id":event.watermark_id,"ledger":str(ledger.path)}, indent=2))

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="command", required=True); d=sub.add_parser("demo"); d.add_argument("--workdir", type=Path, default=Path("demo")); args=p.parse_args()
    if args.command == "demo": demo(args.workdir)
if __name__ == "__main__": main()
