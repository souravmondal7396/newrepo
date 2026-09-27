# Deployment

## Container deployment

```bash
# development/demo deployment
AEGIS_ALLOW_DEV_CRYPTO=1 docker compose up --build
curl http://localhost:8080/healthz
```

The service exposes:

- `GET /healthz`
- `GET /readyz`
- `POST /v1/release?recipient_key_id=...` with a PNG/JPEG multipart field named `file`
- `GET /v1/releases/{event_id}`
- `POST /v1/verify` with JSON `{ "watermark_id": "..." }` and the leaked image as `file`

## Offline deployment

On a connected build station:

```bash
./deploy/build-offline.sh
./deploy/export-offline.sh
```

Transfer `bundle/` through the approved air-gap process. On the isolated host:

```bash
./deploy/install-offline.sh
```

The scripts verify the exported image hash before loading it. Pin the base image digest and sign `SHA256SUMS` with the organization release key before operational use.

## Production requirements

The compose deployment is a complete runnable service, but `AEGIS_ALLOW_DEV_CRYPTO=1` is for demonstration only. For production, build an image containing a pinned, locally audited `liboqs` installation, set `AEGIS_ALLOW_DEV_CRYPTO=0`, provision recipient keys outside the container, and replace the reference watermark with a validated robust engine. The JSONL ledger is single-node; use the Fabric network under `ledger/fabric` for multi-organization consensus and configure backups, private collections, TLS, and endorsement policies before claiming distributed deployment.
