from atlantiscore.lib.abi import read_abi
from atlantiscore.middleware.blockchain.evm import EVMContractMiddleware
from atlantiscore.types import EVMAddress


class ERC20Middleware(EVMContractMiddleware):
    address: EVMAddress

    @staticmethod
    async def get_abi() -> dict:
        return await read_abi("erc20")

    async def transfer(
        self,
        recipient: EVMAddress,
        amount: int,
        additional_transaction_data: dict = {},
    ) -> str:
        contract = await self.get_contract()
        transfer = contract.functions.transfer(str(recipient), amount)
        tx = transfer.build_transaction(
            await self.create_transaction_data(additional_transaction_data),
        )
        return (await self.send_unsigned_transaction(tx)).hex()

    async def get_decimals(self):
        contract = await self.get_contract()
        return contract.functions.decimals().call()

    async def approve(
        self,
        spender: EVMAddress,
        amount: int,
        additional_transaction_data: dict = {},
    ) -> str:
        contract = await self.get_contract()
        approve = contract.functions.approve(str(spender), amount)
        tx = approve.build_transaction(
            await self.create_transaction_data(additional_transaction_data),
        )
        return (await self.send_unsigned_transaction(tx)).hex()
