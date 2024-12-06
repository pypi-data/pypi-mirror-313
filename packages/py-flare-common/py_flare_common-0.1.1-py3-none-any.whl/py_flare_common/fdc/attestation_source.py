from attrs import Attribute, field, frozen

__all__ = ["AttestationSource"]


@frozen
class AttestationSource:
    @staticmethod
    def _length_validation(
        instance: "AttestationSource", attribute: Attribute, value: bytes
    ):
        if len(value) != 32:
            raise ValueError(f"{attribute.name} must have exactly 32 bytes.")

    source_id: bytes = field(validator=_length_validation)

    @property
    def representation(self) -> str:
        return self.source_id.decode("utf-8").rstrip("\x00").strip()

    @classmethod
    def from_represenation(cls, representaion: str):
        encoded_rep = representaion.encode().ljust(32, b"\x00")

        return cls(encoded_rep)

    @classmethod
    def fromhex(cls, hexstr: str):
        return cls(bytes.fromhex(hexstr))
