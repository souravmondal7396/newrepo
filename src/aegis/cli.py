from __future__ import annotations
import argparse, json, os
from pathlib import Path
from .crypto import EnvelopeCrypto
from .ledger import AppendOnlyLedger, create_event
from .model import canonical, digest, unb64
from .pq import PQIdentity
from .watermark import ReferenceWatermark

def demo(workdir: Path):
    workdir.mkdir(parents=True,exist_ok=True); source=workdir/"original.png"; encrypted=workdir/"document.bin"; output=workdir/"released.png"
    from PIL import Image
    if not source.exists(): Image.new("RGB",(256,256),(80,120,160)).save(source)
    plaintext=source.read_bytes(); crypto=EnvelopeCrypto(); key=crypto.generate_key(); encrypted.write_bytes(crypto.encrypt(key,plaintext,digest(plaintext).encode()))
    recovered=crypto.decrypt(key,encrypted.read_bytes(),digest(plaintext).encode()); assert recovered==plaintext
    identity=PQIdentity.generate(); ledger=AppendOnlyLedger(workdir/"ledger.jsonl"); watermark_id=os.urandom(16).hex()
    event=create_event(recovered,recovered,"recipient-demo",watermark_id,identity,ledger.last_hash()); ReferenceWatermark().embed(source,watermark_id.encode(),output); ledger.append(event)
    extracted=ReferenceWatermark().extract(output).decode(); record=ledger.find(extracted)
    assert record and ledger.verify_chain() and digest(extracted.encode())==record["watermark_digest"]
    (workdir/"event.json").write_text(json.dumps(record,indent=2)); print(json.dumps({"status":"verified","watermark_id":extracted,"output":str(output)},indent=2))

def main():
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest="command",required=True); command=sub.add_parser("demo"); command.add_argument("--workdir",type=Path,default=Path("demo")); args=parser.parse_args(); demo(args.workdir)
if __name__=="__main__": main()
