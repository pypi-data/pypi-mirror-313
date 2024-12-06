from attrs import Attribute, field, frozen

__all__ = ["AttestationType"]


@frozen
class AttestationType:
    @staticmethod
    def _length_validation(
        instance: "AttestationType", attribute: Attribute, value: bytes
    ):
        if len(value) != 32:
            raise ValueError(f"{attribute.name} must have exactly 32 bytes.")

    attestation_type: bytes = field(validator=_length_validation)

    @property
    def representation(self) -> str:
        return self.attestation_type.decode("utf-8").rstrip("\x00").strip()

    @classmethod
    def from_represenation(cls, representaion: str):
        encoded_rep = representaion.encode().ljust(32, b"\x00")

        return cls(encoded_rep)

    @classmethod
    def fromhex(cls, hexstr: str):
        return cls(bytes.fromhex(hexstr))
