from __future__ import annotations
import json, os, tempfile
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .ledger import AppendOnlyLedger, create_event
from .model import digest, unb64
from .pq import PQIdentity
from .watermark import ReferenceWatermark

DATA_DIR = Path(os.getenv("AEGIS_DATA_DIR", "/var/lib/aegis"))
LEDGER = AppendOnlyLedger(DATA_DIR / "ledger.jsonl")
app = FastAPI(title="Aegis Provenance", version="0.2.0")

class VerifyRequest(BaseModel):
    watermark_id: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "ledger_chain_valid": LEDGER.verify_chain()}

@app.get("/readyz")
def readyz():
    if not LEDGER.verify_chain(): raise HTTPException(503, "ledger integrity check failed")
    return {"status": "ready"}

@app.post("/v1/release")
async def release(recipient_key_id: str, file: UploadFile = File(...)):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw = await file.read()
    if not raw: raise HTTPException(400, "empty document")
    identity = PQIdentity.generate(allow_dev=os.getenv("AEGIS_ALLOW_DEV_CRYPTO", "0") == "1")
    watermark_id = os.urandom(16).hex()
    event = create_event(raw, raw, recipient_key_id, watermark_id, identity, LEDGER.last_hash())
    suffix = Path(file.filename or "document.png").suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg"}: raise HTTPException(415, "reference release supports PNG/JPEG only")
    source = DATA_DIR / (event.event_id + "-source.png")
    output = DATA_DIR / (event.event_id + "-released.png")
    source.write_bytes(raw)
    try: ReferenceWatermark().embed(source, watermark_id.encode(), output)
    except Exception as exc: raise HTTPException(422, str(exc)) from exc
    LEDGER.append(event)
    (DATA_DIR / (event.event_id + ".json")).write_text(json.dumps(event.to_dict(), indent=2))
    return {"event_id": event.event_id, "watermark_id": watermark_id, "download": f"/v1/releases/{event.event_id}"}

@app.get("/v1/releases/{event_id}")
def download_release(event_id: str):
    matches = list(DATA_DIR.glob(event_id + "-released.png"))
    if not matches: raise HTTPException(404, "release not found")
    return FileResponse(matches[0], media_type="image/png", filename="released.png")

@app.post("/v1/verify")
async def verify(request: VerifyRequest, file: UploadFile = File(...)):
    temp = Path(tempfile.mkstemp(suffix=".png")[1])
    try:
        temp.write_bytes(await file.read()); extracted = ReferenceWatermark().extract(temp).decode()
        if extracted != request.watermark_id: raise HTTPException(400, "watermark mismatch")
        record = LEDGER.find(extracted)
        if not record: raise HTTPException(404, "no ledger record")
        valid = LEDGER.verify_chain() and digest(extracted.encode()) == record["watermark_digest"]
        if not valid: raise HTTPException(422, "evidence verification failed")
        return {"verified": True, "record": record}
    finally: temp.unlink(missing_ok=True)
