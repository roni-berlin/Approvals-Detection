import asyncio
from eth_typing import BlockIdentifier, HexStr
from web3 import AsyncWeb3
from eth_utils.hexadecimal import add_0x_prefix, remove_0x_prefix
from common.eth.enum import EventTopic
from common.eth.model import ERC20LogRecipient


class ERC20:

    def __init__(self, w3: AsyncWeb3) -> None:
        self.w3 = w3

    @classmethod
    def _to_zero_padded_checksum_address(cls, address: HexStr, zero_pad: int) -> str:
        address = AsyncWeb3.to_checksum_address(address)
        return add_0x_prefix(remove_0x_prefix(address).zfill(zero_pad))

    def is_connected(self) -> bool:
        return self.w3.is_connected()

    async def get_approvals_by_owner_address(
        self,
        owner_address: HexStr,
        from_block: BlockIdentifier,
        to_block: BlockIdentifier,
    ) -> list[ERC20LogRecipient]:
        owner_address = ERC20._to_zero_padded_checksum_address(owner_address, 64)
        filter = await self.w3.eth.filter(
            {
                "fromBlock": from_block,
                "toBlock": to_block,
                "topics": [
                    EventTopic.APPROVAL,
                    owner_address,
                ],
            }
        )
        log_receipts = await filter.get_all_entries()
        approvals = {log.address: log for log in log_receipts}
        tasks = [
            ERC20LogRecipient.model_validate(log, context={"web3": self.w3})
            for log in approvals.values()
        ]
        results = await asyncio.gather(*tasks)

        return results
