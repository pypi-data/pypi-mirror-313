from typing import Generic, TypeVar

from attrs import frozen

__all__ = []

T = TypeVar("T")
U = TypeVar("U")


@frozen
class ParsedPayload(Generic[T]):
    protocol_id: int
    voting_round_id: int
    size: int
    payload: T


@frozen
class ParsedMessage(Generic[T, U]):
    fdc: ParsedPayload[U] | None
    ftso: ParsedPayload[T] | None


@frozen
class FtsoSubmit1:
    commit_hash: bytes


@frozen
class FtsoSubmit2:
    random: int
    values: list[int | None]


@frozen
class FdcSubmit1:
    pass


@frozen
class FdcSubmit2:
    number_of_requests: int
    bit_vector: list[bool]


@frozen
class FtsoMessage:
    protocol_id: int
    random_quality_score: int
    merkle_root: str


@frozen
class FdcMessage:
    protocol_id: int
    random_quality_score: int
    merkle_root: str


@frozen
class Signature:
    v: str
    r: str
    s: str


@frozen
class SubmitSignature(Generic[T]):
    type: int
    message: T
    signature: Signature
