from __future__ import annotations
import hashlib, hmac, os
try:
    import oqs
except ImportError: oqs = None

class PQIdentity:
    """ML-DSA-65 identity. The HMAC provider is development-only and must not ship."""
    def __init__(self, public: bytes, secret: bytes, algorithm: str): self.public, self.secret, self.algorithm = public, secret, algorithm
    @classmethod
    def generate(cls, algorithm="ML-DSA-65"):
        if oqs:
            s = oqs.Signature(algorithm); public, secret = s.generate_keypair(); return cls(public, secret, algorithm)
        return cls(os.urandom(32), os.urandom(32), "DEV-HMAC-NOT-PQ")
    def sign(self, message: bytes) -> bytes:
        if self.algorithm == "DEV-HMAC-NOT-PQ": return hmac.new(self.secret, message, hashlib.sha256).digest()
        return oqs.Signature(self.algorithm, self.secret).sign(message)
    def verify(self, message: bytes, signature: bytes) -> bool:
        if self.algorithm == "DEV-HMAC-NOT-PQ": return hmac.compare_digest(hmac.new(self.secret, message, hashlib.sha256).digest(), signature)
        return oqs.Signature(self.algorithm).verify(message, signature, self.public)

class PQKEM:
    """ML-KEM-768 adapter. It is intentionally separate from document encryption."""
    algorithm = "ML-KEM-768"
    @staticmethod
    def available() -> bool: return oqs is not None
