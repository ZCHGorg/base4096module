"""
base4096 v2.0.0

Core public API:
- encode(data: bytes) -> str
- decode(encoded: str) -> bytes
- BASE4096_ALPHABET: str
"""

from .core import encode, decode, BASE4096_ALPHABET

__all__ = [
    "encode",
    "decode",
    "BASE4096_ALPHABET",
]
