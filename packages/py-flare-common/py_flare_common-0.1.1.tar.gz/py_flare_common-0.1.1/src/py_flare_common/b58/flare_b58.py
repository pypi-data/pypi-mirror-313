from hashlib import sha256

from base58 import BITCOIN_ALPHABET, b58decode, b58encode, scrub_input

__all__ = [
    "flare_b58_encode_check",
    "flare_b58_decode_check",
]


def flare_b58_encode_check(
    v: str | bytes,
    alphabet: bytes = BITCOIN_ALPHABET,
) -> bytes:
    """
    Encode a string using Base58 with a 4 character checksum like in avalanche
    and not like in spec
    https://github.com/flare-foundation/go-flare/blob/93fd844b1e85366ee9c1c4a3fb9e9399220534cc/avalanchego/utils/hashing/hashing.go#L78-L81
    """
    v = scrub_input(v)

    digest = sha256(v).digest()
    return b58encode(v + digest[-4:], alphabet=alphabet)


def flare_b58_decode_check(
    v: str | bytes, alphabet: bytes = BITCOIN_ALPHABET, *, autofix: bool = False
) -> bytes:
    """
    Encode a string using Base58 with a 4 character checksum like in avalanche
    and not like in spec
    https://github.com/flare-foundation/go-flare/blob/93fd844b1e85366ee9c1c4a3fb9e9399220534cc/avalanchego/utils/hashing/hashing.go#L78-L81
    """
    result = b58decode(v, alphabet=alphabet, autofix=autofix)
    result, check = result[:-4], result[-4:]
    digest = sha256(result).digest()

    if check != digest[-4:]:
        raise ValueError("Invalid checksum")

    return result
