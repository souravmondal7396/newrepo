#!/usr/bin/env bash
set -euo pipefail
if [[ ! -f bundle/SHA256SUMS ]]; then echo 'bundle/SHA256SUMS missing' >&2; exit 1; fi
(cd bundle && sha256sum -c SHA256SUMS)
docker load -i bundle/images/aegis-provenance.tar
docker compose -f bundle/docker-compose.yml up -d --no-build
curl --fail http://127.0.0.1:8080/healthz
