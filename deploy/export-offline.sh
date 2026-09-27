#!/usr/bin/env bash
set -euo pipefail
mkdir -p bundle/images bundle/wheels
IMAGE="${IMAGE:-aegis-provenance:local}"
docker save "$IMAGE" -o bundle/images/aegis-provenance.tar
sha256sum bundle/images/aegis-provenance.tar > bundle/SHA256SUMS
cp docker-compose.yml bundle/
cp README.md bundle/
printf 'Offline bundle created at %s\n' "$PWD/bundle"
