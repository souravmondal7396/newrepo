# Threat model and acceptance gates

## Threats

- Recipient edits the viewer or exports plaintext before watermarking.
- Image transformation, cropping, recompression, or watermark removal.
- Ledger administrator modifies an audit record.
- Compromised recipient key or stolen workstation.
- Clock rollback and offline evidence replay.

## Required gates before operational use

- ML-KEM-768 and ML-DSA-65 exercised through a maintained, reviewed liboqs build.
- Watermark benchmark across target PDF/image formats and attack corpus; measure false positives/negatives.
- Trusted viewer prevents unwatermarked export and releases plaintext only after ledger commit.
- Multi-organization Fabric endorsement policy tested with one unavailable or malicious peer.
- Key generation, rotation, revocation, backup, destruction, and incident response tested offline.
- Independent security review, dependency/SBOM review, and legal evidence review.

No prototype result alone establishes attribution in court; the report must include limitations and verification inputs.
