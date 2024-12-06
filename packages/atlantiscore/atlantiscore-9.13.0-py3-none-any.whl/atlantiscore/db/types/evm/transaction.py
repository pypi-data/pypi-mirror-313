from sqlalchemy.types import LargeBinary

from atlantiscore.db.types.evm.base import ByteEncoding
from atlantiscore.types.evm import (
    EVMTransactionHash as PythonTransactionHash,
    LiteralByteEncoding,
)

BYTE_COUNT = 32


class EVMTransactionHash(ByteEncoding):
    _default_type: LargeBinary = LargeBinary(BYTE_COUNT)
    cache_ok: bool = True

    @staticmethod
    def _parse(
        value: PythonTransactionHash | LiteralByteEncoding,
    ) -> PythonTransactionHash:
        return PythonTransactionHash(value)
