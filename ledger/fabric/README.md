# Hyperledger Fabric deployment README

This folder contains artifacts and scripts to deploy a three-organization Hyperledger Fabric network for the Aegis Provenance chaincode.

Prerequisites (build host):
- Docker & Docker Compose
- Hyperledger Fabric binaries in PATH: cryptogen, configtxgen, peer, orderer
- Go toolchain for chaincode build: go >= 1.20
- At least 8GB free disk and 4 CPUs for local test deployment

Quick start (development):

1. Generate crypto material and channel artifacts:
   ledger/fabric/scripts/network.sh

2. Start the fabric containers (orderer + peers):
   docker-compose -f ledger/fabric/docker-compose-fabric.yml up -d

3. Create channel and join peers:
   ledger/fabric/scripts/join-and-deploy.sh

4. Package, install and commit chaincode using peer CLI inside peer containers (see chaincode-deploy-instructions.sh)

Security notes:
- For production, use external CA or Fabric CA; cryptogen is for test only.
- Configure TLS on orderer and peers, enable certificate rotation, and protect private keys.
- Use separate machines or VMs per organization in production, with independent administrators.
