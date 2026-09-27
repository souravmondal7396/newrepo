from __future__ import annotations
import hashlib, struct
from pathlib import Path

MAGIC = b"AEGIS-WM1"
class ReferenceWatermark:
    """Dependency-free image reference engine. Use only for demos/tests."""
    def embed(self, source: Path, payload: bytes, target: Path) -> None:
        from PIL import Image
        image = Image.open(source).convert("RGB"); raw = bytearray(image.tobytes())
        packet = MAGIC + struct.pack("!H", len(payload)) + payload + hashlib.sha256(payload).digest()[:4]
        bits = [(byte >> bit) & 1 for byte in packet for bit in range(7, -1, -1)]
        if len(bits) > len(raw): raise ValueError("image too small for watermark")
        for i, bit in enumerate(bits): raw[i] = (raw[i] & 254) | bit
        Image.frombytes("RGB", image.size, bytes(raw)).save(target, format="PNG")
    def extract(self, source: Path) -> bytes:
        from PIL import Image
        raw = Image.open(source).convert("RGB").tobytes(); bits = [x & 1 for x in raw]
        data = bytes(sum(bits[i+j] << (7-j) for j in range(8)) for i in range(0, len(bits)-7, 8))
        if not data.startswith(MAGIC): raise ValueError("watermark not found")
        n = struct.unpack("!H", data[len(MAGIC):len(MAGIC)+2])[0]; start = len(MAGIC)+2; payload=data[start:start+n]
        if data[start+n:start+n+4] != hashlib.sha256(payload).digest()[:4]: raise ValueError("watermark checksum failed")
        return payload
