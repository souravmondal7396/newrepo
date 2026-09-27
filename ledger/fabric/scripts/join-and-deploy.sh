#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# helper to exec peer CLI in peer0.org1
peer_exec(){
  docker exec -e CORE_PEER_LOCALMSPID=Org1MSP -e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp peer0.org1.example.com "$@"
}

# create channel
docker exec peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c aegischannel -f /var/hyperledger/orderer/channel.tx --outputBlock /var/hyperledger/orderer/aegischannel.block

# join peers
docker exec peer0.org1.example.com peer channel join -b /var/hyperledger/orderer/aegischannel.block

# copy block to other peers and join
docker cp peer0.org1.example.com:/var/hyperledger/orderer/aegischannel.block .
docker cp aegischannel.block peer0.org2.example.com:/var/hyperledger/orderer/aegischannel.block
docker cp aegischannel.block peer0.org3.example.com:/var/hyperledger/orderer/aegischannel.block

docker exec peer0.org2.example.com peer channel join -b /var/hyperledger/orderer/aegischannel.block
docker exec peer0.org3.example.com peer channel join -b /var/hyperledger/orderer/aegischannel.block

echo "Peers joined channel aegischannel"

# install chaincode placeholder - user must package and install chaincode image, then approve and commit
