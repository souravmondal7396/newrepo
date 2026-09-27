# Air-gapped deployment profile

1. Build and scan all wheels, container images, and the Fabric binaries on a connected build station.
2. Export an SBOM, hashes, signatures, and license inventory to `manifest.json`.
3. Transfer only the signed bundle through approved removable media.
4. Verify signatures and SHA3-256 hashes before installation.
5. Run Fabric peers/orderers as separate organizations; require at least two endorsers for production records.
6. Keep private collections for recipient identity and never publish names or private keys to the ledger.
7. Use an offline trusted time source or signed time attestations; record clock uncertainty in evidence reports.
8. Back up ledger snapshots and encrypted key material separately, with dual control.

The included Python ledger is a deterministic development substitute for Fabric and must not be represented as distributed consensus.
