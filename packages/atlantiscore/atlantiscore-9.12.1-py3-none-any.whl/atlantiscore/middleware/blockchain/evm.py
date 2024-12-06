from abc import ABCMeta, abstractmethod

from web3 import HTTPProvider, Web3
from web3.contract import Contract
from web3.eth import Eth

from atlantiscore.types import EVMAddress, PrivateKey

ETHEREUM_MAINNET_CHAIN_ID = 1
SEPOLIA_CHAIN_ID = 11155111


class EVMMiddleware:
    web3: Web3
    private_key: PrivateKey
    chain_id: int
    compatible_chain_ids: tuple[int] = (ETHEREUM_MAINNET_CHAIN_ID, SEPOLIA_CHAIN_ID)

    def __init__(
        self,
        http_node_provider_url: str,
        chain_id: int,
        private_key: PrivateKey,
    ) -> None:
        if chain_id not in self.compatible_chain_ids:
            raise ValueError("Unsupported chain_id")

        self.chain_id = chain_id
        self.web3 = Web3(HTTPProvider(http_node_provider_url))
        self.private_key = private_key

    @property
    def eth(self) -> Eth:
        return self.web3.eth

    async def create_transaction_data(self, additional_data: dict = {}) -> dict:
        nonce = await self.get_nonce()
        return {
            "chainId": self.chain_id,
            "nonce": nonce,
            "from": str(self.private_key.public_address),
            **additional_data,
        }

    async def send_unsigned_transaction(self, transaction: dict) -> str:
        signed_transaction = self.eth.account.sign_transaction(
            transaction,
            private_key=self.private_key.to_hex(),
        )
        return self.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()

    async def get_nonce(self) -> int:
        return self.eth.get_transaction_count(str(self.private_key.public_address))

    async def get_balance(self) -> int:
        return self.eth.get_balance(str(self.private_key.public_address))


class EVMContractMiddleware(EVMMiddleware, metaclass=ABCMeta):
    address: EVMAddress

    def __init__(self, address: EVMAddress, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.address = address

    @staticmethod
    @abstractmethod
    async def get_abi() -> dict:
        """Returns abi for associated contract."""

    async def get_contract(self) -> Contract:
        abi = await self.get_abi()
        return self.eth.contract(address=str(self.address), abi=abi)
