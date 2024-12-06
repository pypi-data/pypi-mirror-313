from eth_abi.abi import encode
from eth_hash.auto import keccak

__all__ = ["commit_hash"]


def commit_hash(
    submit_address: str, voting_round: int, random: int, feed_values: bytes
) -> str:
    types = ["address", "uint32", "uint256", "bytes"]
    values = [submit_address, voting_round, random, feed_values]
    encoded = encode(types, values)
    return keccak(encoded).hex()
