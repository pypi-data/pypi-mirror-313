from __future__ import annotations

from eth_utils.address import to_checksum_address

from atlantiscore.lib.exceptions import InvalidByteEncoding, InvalidEVMAddress
from atlantiscore.types.evm.base import (
    PREFIX_SIZE,
    ByteEncoding,
    LiteralByteEncoding,
    _encoding_to_bytes,
)

EXAMPLE_ADDRESS_STRING = "0xa8E219Aa773fb12A812B7A3a4671b5B1933a49A8"
PREFIXED_ADDRESS_LENGTH = 42
ADDRESS_BYTE_COUNT = 20


class EVMAddress(ByteEncoding):
    _example: str = EXAMPLE_ADDRESS_STRING
    _byte_count: int = ADDRESS_BYTE_COUNT
    _max_str_length: int = PREFIXED_ADDRESS_LENGTH
    _min_str_length: int = PREFIXED_ADDRESS_LENGTH - PREFIX_SIZE

    def __init__(self, value: EVMAddress | LiteralByteEncoding) -> None:
        self._value = _address_to_bytes(value)

    def _to_checksum(self) -> str:
        return to_checksum_address(self._value)

    def __str__(self) -> str:
        return self._to_checksum()

    def __eq__(self, other: any) -> bool:
        try:
            return hash(self) == hash(EVMAddress(other))
        except InvalidEVMAddress:
            return False

    def __gt__(self, other: any) -> bool:
        return super().__gt__(EVMAddress(other))

    def __lt__(self, other: any) -> bool:
        return super().__lt__(EVMAddress(other))

    def __hash__(self) -> int:
        return int(self)


def _address_to_bytes(value: EVMAddress | LiteralByteEncoding) -> bytes:
    try:
        return _encoding_to_bytes(value, ADDRESS_BYTE_COUNT)
    except InvalidByteEncoding as e:
        raise InvalidEVMAddress(value) from e
