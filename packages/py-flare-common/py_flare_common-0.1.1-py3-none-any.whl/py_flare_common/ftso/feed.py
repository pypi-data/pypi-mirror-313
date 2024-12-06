from attrs import Attribute, field, frozen

__all__ = ["FtsoFeed"]


@frozen
class FtsoFeed:
    @staticmethod
    def _length_validation(instance: "FtsoFeed", attribute: Attribute, value: bytes):
        if len(value) != 21:
            raise ValueError(f"{attribute.name} must have exactly 21 bytes.")

    feed_id: bytes = field(validator=_length_validation)

    @property
    def representation(self) -> str:
        return self.feed_id[1:].decode("utf-8").rstrip("\x00").strip()

    @property
    def type(self) -> int:
        return int(hex(self.feed_id[0]), 16)

    @classmethod
    def from_represenation_and_type(cls, type: int, representaion: str):
        encoded_type = type.to_bytes()
        encoded_rep = representaion.encode().ljust(20, b"\x00")

        return cls(encoded_type + encoded_rep)

    @classmethod
    def fromhex(cls, hexstr: str):
        return cls(bytes.fromhex(hexstr))
