from __future__ import annotations
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .model import b64, unb64

class EnvelopeCrypto:
    """AES-256-GCM document encryption; recipient KEM wrapping is a policy layer."""
    def generate_key(self) -> bytes: return AESGCM.generate_key(bit_length=256)
    def encrypt(self, key: bytes, plaintext: bytes, aad: bytes = b"") -> bytes:
        nonce = os.urandom(12); return nonce + AESGCM(key).encrypt(nonce, plaintext, aad)
    def decrypt(self, key: bytes, ciphertext: bytes, aad: bytes = b"") -> bytes:
        if len(ciphertext) < 28: raise ValueError("invalid envelope")
        return AESGCM(key).decrypt(ciphertext[:12], ciphertext[12:], aad)
    def export(self, key: bytes) -> str: return b64(key)
    def import_key(self, value: str) -> bytes: return unb64(value)
