import string

__all__ = []


def un_prefix_0x(s: str) -> str:
    return s.removeprefix("0x")


def prefix_0x(s: str) -> str:
    return "0x" + un_prefix_0x(s)


def is_hex_str(s: str):
    s = un_prefix_0x(s)
    return all(c in string.hexdigits for c in s)


def to_bytes(s: str | bytes) -> bytes:
    if isinstance(s, str):
        if not is_hex_str(s):
            raise ValueError("Invalid hex string")
        s = bytes.fromhex(s)
    return s
