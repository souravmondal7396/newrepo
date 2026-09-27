# Aegis Provenance

Runnable offline reference implementation for SIH26237. It performs AES-256-GCM encryption, per-decryption event creation, signed event verification, invisible PNG watermark embedding/extraction, and hash-chained append-only audit storage.

## Run

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev,image]'
python -m aegis demo --workdir demo
pytest
```

The demo is fully runnable without liboqs using a clearly labelled development HMAC provider. Production mode requires `liboqs-python` and ML-DSA-65; the development provider is not post-quantum and must never be used for evidence.

## Production PQ setup

Install a locally built, pinned Open Quantum Safe distribution and run:

```bash
pip install -e '.[pq,image]'
```

The code invokes ML-DSA-65 for signatures and provides ML-KEM-768 encapsulation/decapsulation APIs. The Fabric chaincode under `ledger/fabric` is the distributed-ledger adapter; the JSONL ledger is only a deterministic local test implementation.

## Current boundary

The reference watermark is intentionally runnable and testable but is not robust against a determined remover. Replace it with a validated DWT-DCT-SVD/VideoSeal engine for operational deployment, benchmark it against the target document formats, and use a trusted viewer with hardware-backed keys. A watermark is an index; cryptographic signature and independent ledger evidence establish verification.
