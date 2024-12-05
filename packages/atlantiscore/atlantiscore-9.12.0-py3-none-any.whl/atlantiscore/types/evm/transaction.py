from __future__ import annotations

from atlantiscore.lib.exceptions import InvalidByteEncoding, InvalidEVMTransactionHash
from atlantiscore.types.evm.base import (
    PREFIX_SIZE,
    ByteEncoding,
    LiteralByteEncoding,
    _encoding_to_bytes,
)

TRANSACTION_HASH_BYTE_COUNT = 32
EXAMPLE_TRANSACTION_HASH_STRING = (
    "0xd4fe60962208702e0e5915e0268847709610d7b3b8be39b2af57ccca6809951a"
)


class EVMTransactionHash(ByteEncoding):
    _example: str = EXAMPLE_TRANSACTION_HASH_STRING
    _byte_count: int = TRANSACTION_HASH_BYTE_COUNT
    _min_str_length: int = _byte_count * 2
    _max_str_length: int = _min_str_length + PREFIX_SIZE

    def __init__(self, value: EVMTransactionHash | LiteralByteEncoding) -> None:
        self._value = _transaction_hash_to_bytes(value)

    def __eq__(self, other: any) -> bool:
        try:
            return hash(self) == hash(EVMTransactionHash(other))
        except InvalidByteEncoding:
            return False

    def __gt__(self, other: any) -> bool:
        return super().__gt__(EVMTransactionHash(other))

    def __lt__(self, other: any) -> bool:
        return super().__lt__(EVMTransactionHash(other))

    def __hash__(self) -> int:
        return int(self)


def _transaction_hash_to_bytes(
    value: EVMTransactionHash | LiteralByteEncoding,
) -> bytes:
    try:
        return _encoding_to_bytes(value, TRANSACTION_HASH_BYTE_COUNT)
    except InvalidByteEncoding as e:
        raise InvalidEVMTransactionHash(value) from e
