__all__ = []


class ParseError(Exception):
    pass


class ByteParser:
    def __init__(self, b: bytes) -> None:
        self._b = b
        self._pointer = 0

    def _move_pointer(self, n: int) -> int:
        p = self._pointer
        self._pointer += n
        if self._pointer > len(self._b):
            raise ParseError("Tried to parse bytes out of range.")
        return p

    def _consume(self, n: int) -> bytes:
        p = self._move_pointer(n)
        return self._b[p : self._pointer]

    def _parse_int(self, size: int, signed: bool) -> int:
        return int.from_bytes(self._consume(size), signed=signed)

    def uint8(self) -> int:
        return self._parse_int(1, False)

    def int8(self) -> int:
        return self._parse_int(1, True)

    def uint16(self) -> int:
        return self._parse_int(2, False)

    def int16(self) -> int:
        return self._parse_int(2, True)

    def uint32(self) -> int:
        return self._parse_int(4, False)

    def int32(self) -> int:
        return self._parse_int(4, True)

    def uint64(self) -> int:
        return self._parse_int(8, False)

    def int64(self) -> int:
        return self._parse_int(8, True)

    def uint128(self) -> int:
        return self._parse_int(16, False)

    def int128(self) -> int:
        return self._parse_int(16, True)

    def uint256(self) -> int:
        return self._parse_int(32, False)

    def int256(self) -> int:
        return self._parse_int(32, True)

    def next_n(self, n) -> bytes:
        return self._consume(n)

    def is_empty(self) -> bool:
        return self._pointer == len(self._b)

    def drain(self) -> bytes:
        return self._consume(len(self) - self._pointer)

    def __len__(self) -> int:
        return len(self._b)
