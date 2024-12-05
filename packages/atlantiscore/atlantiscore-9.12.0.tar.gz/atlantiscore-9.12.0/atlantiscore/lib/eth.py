import asyncio

from web3.eth import Eth
from web3.exceptions import TimeExhausted, TransactionNotFound


async def wait_for_transaction_receipt(
    eth: Eth,
    transaction_hash: str,
    timeout_in_seconds: int = 120,
    poll_latency: float = 0.1,
) -> dict:
    try:
        return await asyncio.wait_for(
            _wait_for_transaction_receipt_indefinetly(
                eth, transaction_hash, poll_latency
            ),
            timeout_in_seconds,
        )
    except asyncio.TimeoutError:
        raise TimeExhausted("Transaction receipt not found within the given time limit")


async def _wait_for_transaction_receipt_indefinetly(
    eth: Eth,
    transaction_hash: str,
    poll_latency: float = 0.1,
) -> dict:
    while True:
        try:
            return eth.get_transaction_receipt(transaction_hash)
        except TransactionNotFound:
            await asyncio.sleep(poll_latency)
