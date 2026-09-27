#!/usr/bin/env bash
set -euo pipefail
: "${IMAGE:=aegis-provenance:local}"
docker build --pull=false -t "$IMAGE" .
docker image inspect "$IMAGE" --format '{{.Id}}'
printf 'Built %s\n' "$IMAGE"
