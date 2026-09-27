# Verification checklist

- [ ] Verify document hash against the claimed source.
- [ ] Extract watermark and validate its checksum.
- [ ] Resolve watermark ID to exactly one ledger record.
- [ ] Reconstruct the canonical unsigned event bytes.
- [ ] Verify the ML-DSA signature against the enrolled public key.
- [ ] Verify Fabric transaction ID, block inclusion, endorsement policy, and ledger history.
- [ ] Verify key status at event time and trusted time evidence.
- [ ] Preserve the original leaked artifact and compute its hash before analysis.
- [ ] Produce a signed evidence report with tool version and configuration.
