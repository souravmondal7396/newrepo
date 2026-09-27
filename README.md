# Aegis Provenance

Enterprise-oriented reference implementation for SIH26237: cryptographic attribution and immutable decryption provenance for multi-recipient document distribution.

> **Status:** four-phase engineering baseline. The local ledger and watermark engine are runnable; the Fabric adapter, controlled viewer, and offline deployment artifacts are included as integration foundations. This is not a claim of legal-grade non-repudiation without a trusted endpoint and hardware-backed keys.

## Four phases

1. **Local cryptographic PoC** – envelope encryption, per-session watermark IDs, signed canonical records, extraction and verification.
2. **Permissioned ledger** – append-only local ledger plus Hyperledger Fabric chaincode and deployment contract.
3. **Document/viewer** – PNG/JPEG blind watermark adapter, PDF rendering boundary, controlled-release policy and evidence reports.
4. **Enterprise hardening** – offline build manifest, key rotation/revocation model, SBOM/security controls, backup and operational guidance.

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
python -m aegis demo --workdir ./demo
pytest
```

The default demo uses a deterministic, dependency-free LSB reference watermark so the workflow works in an air-gapped Python installation. It is intentionally a test engine, not a production forensic watermark. Install the optional extras for Open Quantum Safe and image processing:

```bash
pip install -e '.[pq,image]'
```

For production, configure `liboqs`/`liboqs-python` and replace the reference watermark with a validated robust implementation such as a DWT-DCT-SVD or VideoSeal adapter. Never use the fallback signature provider for real evidence.

## Architecture

`aegis.crypto` uses AES-GCM when `cryptography` is installed and refuses to silently downgrade. `aegis.pq` exposes ML-KEM-768 and ML-DSA-65 through liboqs when available, with a clearly marked development provider for tests. `aegis.watermark` embeds a signed-looking opaque watermark reference, never a plaintext identity. `aegis.ledger` is append-only locally and verifies hash chaining. `aegis.workflow` coordinates release, extraction, signature verification, and evidence reports.

The Fabric contract in `ledger/fabric/chaincode.go` stores the event digest, watermark ID, recipient key ID, signature, and previous digest. Sensitive identity attributes belong in a private collection, not public ledger state.

## Security boundaries

- A recipient-controlled endpoint can remove or suppress a watermark; strong attribution requires a trusted viewer, secure boot, hardware-backed keys, and release only after ledger commit.
- A watermark is an index, not proof. The verifier must validate the canonical event, ML-DSA signature, document digest, and independent ledger evidence.
- ML-KEM and ML-DSA parameters are configurable only through policy. The enterprise profile defaults to ML-KEM-768 and ML-DSA-65.
- No cloud KMS, public blockchain, network time, or external service is required at runtime.

## Repository layout

```text
src/aegis/                 Python implementation and CLI
ledger/fabric/             Fabric chaincode skeleton and endorsement policy
infra/airgap/              offline deployment/checklist artifacts
docs/                      threat model, operations, and integration guide
tests/                     unit and end-to-end tests
```

## License

MIT. Review third-party licenses before redistributing optional dependencies.
