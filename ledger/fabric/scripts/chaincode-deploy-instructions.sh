#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CHAINCODE_LABEL=${1:-aegis_chaincode_v1}
CHAINCODE_PACKAGE=${CHAINCODE_LABEL}.tar.gz

# this script shows packaging pattern using peer lifecycle (calls must run inside peer CLI context)
cat <<'EOF'
# Example steps to run inside peer0.org1 container or using peer CLI with env vars:
# peer lifecycle chaincode package ${CHAINCODE_PACKAGE} --path /opt/chaincode --lang golang --label ${CHAINCODE_LABEL}
# peer lifecycle chaincode install ${CHAINCODE_PACKAGE}
# peer lifecycle chaincode approveformyorg --channelID aegischannel --name aegiscc --version 1.0 --package-id <pkg-id> --sequence 1 --orderer orderer.example.com:7050
# peer lifecycle chaincode commit -o orderer.example.com:7050 --channelID aegischannel --name aegiscc --version 1.0 --sequence 1 --peerAddresses peer0.org1.example.com:7051 --peerAddresses peer0.org2.example.com:8051 --peerAddresses peer0.org3.example.com:9051
EOF
