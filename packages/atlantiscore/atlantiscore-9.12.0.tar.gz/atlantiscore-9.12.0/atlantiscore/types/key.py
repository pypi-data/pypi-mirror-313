from typing import Self

from coincurve import GLOBAL_CONTEXT, Context, PrivateKey as CoinCurvePrivateKey
from coincurve.utils import hex_to_bytes
from eth_utils import keccak

from atlantiscore.types.evm import EVMAddress

NUMBER_OF_BYTES_IN_ADDRESS = 20


class PrivateKey(CoinCurvePrivateKey):
    @property
    def public_address(self) -> EVMAddress:
        public_key = self.public_key.format(compressed=False)[1:]
        return EVMAddress(keccak(public_key)[-NUMBER_OF_BYTES_IN_ADDRESS:])

    @classmethod
    def from_der(cls, *args, **kwargs) -> Self:
        return cls.from_hex(CoinCurvePrivateKey.from_der(*args, **kwargs).to_hex())

    @classmethod
    def from_hex(cls, hexed: str, context: Context = GLOBAL_CONTEXT) -> Self:
        return PrivateKey(hex_to_bytes(hexed), context)

    @classmethod
    def from_int(cls, *args, **kwargs) -> Self:
        return cls.from_hex(CoinCurvePrivateKey.from_int(*args, **kwargs).to_hex())

    @classmethod
    def from_pem(cls, *args, **kwargs) -> Self:
        return cls.from_hex(CoinCurvePrivateKey.from_pem(*args, **kwargs).to_hex())
