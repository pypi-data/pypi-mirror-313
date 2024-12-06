from collections.abc import Callable

from py_flare_common._hexstr.hexstr import to_bytes

from .byte_parser import ByteParser, ParseError
from .types import (
    FdcMessage,
    FdcSubmit1,
    FdcSubmit2,
    FtsoMessage,
    FtsoSubmit1,
    FtsoSubmit2,
    ParsedMessage,
    ParsedPayload,
    Signature,
    SubmitSignature,
    T,
    U,
)

__all__ = [
    "parse_generic_tx",
    "parse_submit1_tx",
    "parse_submit2_tx",
    "parse_submit_signature_tx",
]


def _default_parse(b: bytes) -> bytes:
    return b


def parse_generic_tx(
    message: bytes | str,
    pid_100_parse: Callable[[bytes], T] = _default_parse,
    pid_200_parse: Callable[[bytes], U] = _default_parse,
) -> ParsedMessage[T, U]:
    kwargs: dict[str, ParsedPayload | None] = {"ftso": None, "fdc": None}
    message = to_bytes(message)
    bp = ByteParser(message)

    while not bp.is_empty():
        protocol_id = bp.uint8()
        voting_round_id = bp.uint32()
        payload_length = bp.uint16()
        payload = bp.next_n(payload_length)

        if protocol_id == 100:
            parsed = pid_100_parse(payload)
            kwargs["ftso"] = ParsedPayload(
                protocol_id, voting_round_id, payload_length, parsed
            )

        if protocol_id == 200:
            parsed = pid_200_parse(payload)
            kwargs["fdc"] = ParsedPayload(
                protocol_id, voting_round_id, payload_length, parsed
            )

    return ParsedMessage(**kwargs)


def parse_submit1_tx(message: bytes | str) -> ParsedMessage[FtsoSubmit1, FdcSubmit1]:
    return parse_generic_tx(message, ftso_submit1, fdc_submit1)


def parse_submit2_tx(message: bytes | str) -> ParsedMessage[FtsoSubmit2, FdcSubmit2]:
    return parse_generic_tx(message, ftso_submit2, fdc_submit2)


def parse_submit_signature_tx(
    message: bytes | str,
) -> ParsedMessage[SubmitSignature[FtsoMessage], SubmitSignature[FdcMessage]]:
    return parse_generic_tx(message, ftso_submit_signature, fdc_submit_signature)


def ftso_submit1(payload: bytes) -> FtsoSubmit1:
    if len(payload) != 32:
        raise ParseError("Invalid payload length: expected 32 bytes.")
    return FtsoSubmit1(payload)


def fdc_submit1(payload: bytes) -> FdcSubmit1:
    if payload:
        raise ParseError("Invalid payload length: expected 0 bytes.")
    return FdcSubmit1()


def ftso_submit2(payload: bytes) -> FtsoSubmit2:
    EMPTY_FEED_VALUE = "0" * 8

    bp = ByteParser(payload)
    random = bp.uint256()
    values: list[int | None] = []

    while not bp.is_empty():
        raw_value = bp.next_n(4).hex()
        value = int(raw_value, 16) - 2**31 if raw_value != EMPTY_FEED_VALUE else None
        values.append(value)

    return FtsoSubmit2(random=random, values=values)


def fdc_submit2(payload: bytes) -> FdcSubmit2:
    bp = ByteParser(payload)
    n_requests = bp.uint16()

    votes = bp.drain()
    bit_vector = [False for _ in range(n_requests)]

    for j, byte in enumerate(reversed(votes)):
        for shift in range(8):
            i = n_requests - 1 - j * 8 - shift
            if i < 0 and (byte >> shift) & 1 == 1:
                raise ParseError("Invalid payload length.")
            elif i >= 0:
                bit_vector[i] = (byte >> shift) & 1 == 1

    return FdcSubmit2(
        number_of_requests=n_requests,
        bit_vector=bit_vector,
    )


def _submit_signature(payload: bytes) -> tuple[int, bytes, Signature]:
    payload_bp = ByteParser(payload)

    type = payload_bp.uint8()
    message_to_parse = payload_bp.next_n(38)
    signature_to_parse = payload_bp.next_n(65)
    if not payload_bp.is_empty():
        raise ParseError("Invalid payload length: expected 104 bytes.")

    signature_bp = ByteParser(signature_to_parse)
    v = signature_bp.next_n(1).hex()
    r = signature_bp.next_n(32).hex()
    s = signature_bp.next_n(32).hex()
    if not signature_bp.is_empty():
        raise ParseError("Invalid payload length: expected 65 bytes.")

    signature = Signature(v=v, r=r, s=s)

    return type, message_to_parse, signature


def ftso_submit_signature(payload: bytes) -> SubmitSignature[FtsoMessage]:
    type, message_to_parse, signature = _submit_signature(payload)

    message_bp = ByteParser(message_to_parse)
    protocol_id = message_bp.uint8()
    message_bp.next_n(4)
    random_quality_score = message_bp.uint8()
    merkle_root = message_bp.drain().hex()

    message = FtsoMessage(
        protocol_id=protocol_id,
        random_quality_score=random_quality_score,
        merkle_root=merkle_root,
    )

    return SubmitSignature(
        type=type,
        message=message,
        signature=signature,
    )


def fdc_submit_signature(payload: bytes) -> SubmitSignature[FdcMessage]:
    type, message_to_parse, signature = _submit_signature(payload)

    message_bp = ByteParser(message_to_parse)
    protocol_id = message_bp.uint8()
    message_bp.next_n(4)
    random_quality_score = message_bp.uint8()
    merkle_root = message_bp.drain().hex()

    message = FdcMessage(
        protocol_id=protocol_id,
        random_quality_score=random_quality_score,
        merkle_root=merkle_root,
    )

    return SubmitSignature(
        type=type,
        message=message,
        signature=signature,
    )
