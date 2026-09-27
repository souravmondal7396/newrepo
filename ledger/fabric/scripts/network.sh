#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

# pre-reqs: cryptogen, configtxgen, peer, docker, docker-compose
which cryptogen > /dev/null || { echo "cryptogen not found in PATH"; exit 1; }
which configtxgen > /dev/null || { echo "configtxgen not found in PATH"; exit 1; }

ARTIFACTS_DIR=channel-artifacts
CRYPTO_CONFIG=crypto-config.yaml

# generate crypto material
rm -rf crypto-config $ARTIFACTS_DIR
cryptogen generate --config=$CRYPTO_CONFIG

# generate genesis block
mkdir -p $ARTIFACTS_DIR
export FABRIC_CFG_PATH=$BASE_DIR
configtxgen -profile ThreeOrgsOrdererGenesis -channelID system-channel -outputBlock $ARTIFACTS_DIR/orderer.genesis.block

# create channel tx
configtxgen -profile ThreeOrgsChannel -outputCreateChannelTx $ARTIFACTS_DIR/channel.tx -channelID aegischannel

# organizations anchor peers
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate $ARTIFACTS_DIR/Org1MSPanchors.tx -channelID aegischannel -asOrg Org1MSP
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate $ARTIFACTS_DIR/Org2MSPanchors.tx -channelID aegischannel -asOrg Org2MSP
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate $ARTIFACTS_DIR/Org3MSPanchors.tx -channelID aegischannel -asOrg Org3MSP

# bring up fabric components
docker-compose -f docker-compose-fabric.yml up -d orderer.example.com peer0.org1.example.com peer0.org2.example.com peer0.org3.example.com

# wait for containers
sleep 5

echo "Fabric network started. Next: create channel and join peers using the peer CLI inside peer containers."
