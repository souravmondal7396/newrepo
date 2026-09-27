from __future__ import annotations
import hashlib, hmac, os
from pathlib import Path
from .model import b64, unb64
try:
    import oqs
except ImportError:
    oqs = None

class PQIdentity:
    """ML-DSA-65 identity. DEV-HMAC is only for tests and is rejected by strict mode."""
    def __init__(self, public: bytes, secret: bytes | None, algorithm: str):
        self.public, self.secret, self.algorithm = public, secret, algorithm
    @classmethod
    def generate(cls, algorithm="ML-DSA-65", allow_dev=True):
        if oqs is not None:
            signer = oqs.Signature(algorithm)
            public, secret = signer.generate_keypair()
            return cls(public, secret, algorithm)
        if not allow_dev: raise RuntimeError("liboqs is required for production PQ signatures")
        secret = os.urandom(32)
        return cls(secret, secret, "DEV-HMAC-NOT-PQ")
    def sign(self, message: bytes) -> bytes:
        if self.algorithm == "DEV-HMAC-NOT-PQ":
            if self.secret is None: raise ValueError("secret key unavailable")
            return hmac.new(self.secret, message, hashlib.sha256).digest()
        if oqs is None or self.secret is None: raise RuntimeError("liboqs/private key unavailable")
        try: return oqs.Signature(self.algorithm, secret_key=self.secret).sign(message)
        except TypeError: return oqs.Signature(self.algorithm, self.secret).sign(message)
    def verify(self, message: bytes, signature: bytes) -> bool:
        return verify_signature(self.algorithm, self.public, message, signature)
    def export_public(self) -> str: return b64(self.public)
    def save(self, path: Path) -> None:
        if self.secret is None: raise ValueError("private key unavailable")
        path.write_text('{"algorithm":"%s","public":"%s","secret":"%s"}' % (self.algorithm, b64(self.public), b64(self.secret)))
    @classmethod
    def load(cls, path: Path):
        import json
        value=json.loads(path.read_text()); return cls(unb64(value["public"]), unb64(value["secret"]), value["algorithm"])

def verify_signature(algorithm: str, public: bytes, message: bytes, signature: bytes) -> bool:
    if algorithm == "DEV-HMAC-NOT-PQ": return hmac.compare_digest(hmac.new(public, message, hashlib.sha256).digest(), signature)
    if oqs is None: return False
    return bool(oqs.Signature(algorithm).verify(message, signature, public))

class PQKEM:
    algorithm = "ML-KEM-768"
    @staticmethod
    def generate_keypair():
        if oqs is None: raise RuntimeError("liboqs is required for ML-KEM-768")
        return oqs.KeyEncapsulation(PQKEM.algorithm).generate_keypair()
    @staticmethod
    def encapsulate(public_key: bytes):
        if oqs is None: raise RuntimeError("liboqs is required for ML-KEM-768")
        return oqs.KeyEncapsulation(PQKEM.algorithm).encap_secret(public_key)
    @staticmethod
    def decapsulate(secret_key: bytes, ciphertext: bytes):
        if oqs is None: raise RuntimeError("liboqs is required for ML-KEM-768")
        try: return oqs.KeyEncapsulation(PQKEM.algorithm, secret_key=secret_key).decap_secret(ciphertext)
        except TypeError: return oqs.KeyEncapsulation(PQKEM.algorithm, secret_key).decap_secret(ciphertext)
