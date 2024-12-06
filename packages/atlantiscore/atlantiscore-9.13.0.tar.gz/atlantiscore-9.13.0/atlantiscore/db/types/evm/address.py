from sqlalchemy.types import LargeBinary

from atlantiscore.db.types.evm.base import ByteEncoding
from atlantiscore.types.evm import EVMAddress as PythonEVMAddress, LiteralByteEncoding

BYTE_COUNT = 20


class EVMAddress(ByteEncoding):
    _default_type: LargeBinary = LargeBinary(BYTE_COUNT)
    cache_ok: bool = True

    @staticmethod
    def _parse(value: PythonEVMAddress | LiteralByteEncoding) -> PythonEVMAddress:
        return PythonEVMAddress(value)
