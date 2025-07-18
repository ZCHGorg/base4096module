import unicodedata
import importlib.resources

def is_valid_char(c):
    try:
        name = unicodedata.name(c)
        exclude_keywords = ['CONTROL', 'PRIVATE USE', 'SURROGATE', 'UNASSIGNED', 'TAG']
        if any(x in name for x in exclude_keywords):
            return False
        if c.isspace():
            return False
        return True
    except ValueError:
        return False

SEED = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "!@#$%^&*()-_+=[{]};:',\"<>?/"
    + ''.join(chr(i) for i in range(0x20, 0x7F))
)

def generate_base4096_alphabet(seed):
    seen = set()
    base_chars = []

    for ch in seed:
        if ch not in seen:
            seen.add(ch)
            base_chars.append(ch)

    for codepoint in range(0x20, 0x30000):
        c = chr(codepoint)
        if c not in seen and is_valid_char(c):
            base_chars.append(c)
            seen.add(c)
            if len(base_chars) == 4096:
                break

    if len(base_chars) < 4096:
        raise ValueError("Failed to generate 4096 unique characters.")
    return ''.join(base_chars)

def generate_frozen_base4096(seed):
    seen = set()
    base_chars = []

    for ch in seed:
        if ch not in seen and is_valid_char(ch):
            seen.add(ch)
            base_chars.append(ch)

    candidate_range_end = 0x40000
    for codepoint in range(0x20, candidate_range_end):
        c = chr(codepoint)
        if c not in seen and is_valid_char(c):
            base_chars.append(c)
            seen.add(c)
            if len(base_chars) == 4096:
                break

    if len(base_chars) != 4096:
        raise ValueError(f"Could only generate {len(base_chars)} valid characters; need 4096 exactly.")

    return ''.join(base_chars)

def load_frozen_alphabet() -> str:
    try:
        # Adjust __package__ if necessary or use direct path if this fails
        with importlib.resources.files(__package__).joinpath("frozen_base4096_alphabet.txt").open("r", encoding="utf-8") as f:
            alphabet = f.read()
        # Remove any whitespace/newlines just in case
        alphabet = ''.join(alphabet.split())
        if len(alphabet) != 4096:
            raise ValueError("Frozen alphabet length is not 4096 characters after stripping whitespace.")
        return alphabet
    except Exception as e:
        raise RuntimeError("Failed to load frozen_base4096_alphabet.txt") from e

try:
    BASE4096_ALPHABET = load_frozen_alphabet()
except Exception as e:
    print(f"Warning: Could not load frozen alphabet: {e}")
    print("Falling back to internal seed (not recommended).")
    BASE4096_ALPHABET = generate_base4096_alphabet(SEED)

CHAR_TO_INDEX = {ch: idx for idx, ch in enumerate(BASE4096_ALPHABET)}

def encode(data: bytes) -> str:
    num = int.from_bytes(data, byteorder='big')
    result = []
    while num > 0:
        num, rem = divmod(num, 4096)
        result.append(BASE4096_ALPHABET[rem])
    return ''.join(reversed(result)) or BASE4096_ALPHABET[0]

def decode(encoded: str) -> bytes:
    num = 0
    for char in encoded:
        if char not in CHAR_TO_INDEX:
            raise ValueError(f"Invalid character in input: {repr(char)}")
        num = num * 4096 + CHAR_TO_INDEX[char]
    length = (num.bit_length() + 7) // 8
    return num.to_bytes(length, byteorder='big')


if __name__ == "__main__":
    frozen_alphabet = generate_frozen_base4096(SEED)

    # Write no-newline txt file (exactly 4096 chars)
    with open("frozen_base4096_alphabet.txt", "w", encoding="utf-8") as f:
        f.write(frozen_alphabet)

    # Write python constant file for easy import
    with open("frozen_base4096_alphabet.py", "w", encoding="utf-8") as f:
        f.write("# frozen_base4096_alphabet.py\n")
        f.write("# Canonical Base-4096 Alphabet (frozen, deterministic)\n\n")
        f.write("FROZEN_BASE4096_ALPHABET = (\n")
        for i in range(0, 4096, 64):
            chunk = frozen_alphabet[i:i+64]
            f.write(f"    \"{chunk}\"\n")
        f.write(")\n")

    print(f"✅ Frozen Base4096 alphabet generated with length {len(frozen_alphabet)}")
