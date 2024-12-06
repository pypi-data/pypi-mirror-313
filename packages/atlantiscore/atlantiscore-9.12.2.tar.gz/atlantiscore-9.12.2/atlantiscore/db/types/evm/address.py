from sqlalchemy.types import LargeBinary

from atlantiscore.db.types.evm.base import ByteEncoding
from atlantiscore.types.evm import EVMAddress as PythonEVMAddress, LiteralByteEncoding

BYTE_COUNT = 20


class EVMAddress(ByteEncoding):
    _default_type: LargeBinary = LargeBinary(BYTE_COUNT)
    cache_ok: bool = True
    padding: bool = False

    def __init__(self, *args, padding: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.padding = padding

    def _parse(self, value: PythonEVMAddress | LiteralByteEncoding) -> PythonEVMAddress:
        return PythonEVMAddress(value, self.padding)
