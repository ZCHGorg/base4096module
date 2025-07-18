from .core import encode, decode
from .frozen_alphabet import load_frozen_alphabet, BASE4096_ALPHABET
from .freeze_alphabet import generate_base4096_alphabet
from .hkdf_seal import hkdf_seal, hkdf_open  # if present
from .signer import sign_alphabet, verify_signature  # if present

__all__ = [
    "encode", "decode",
    "load_frozen_alphabet", "generate_base4096_alphabet",
    "BASE4096_ALPHABET",
    "hkdf_seal", "hkdf_open",
    "sign_alphabet", "verify_signature"
]
