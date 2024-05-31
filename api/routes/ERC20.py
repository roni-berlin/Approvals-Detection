from typing import Annotated
from eth_typing import HexStr
from fastapi import APIRouter, Depends
import asyncio

from api.config.ERC20 import get_erc20
from common.eth import ERC20

router = APIRouter()


@router.post("/get_approvals")
async def get_approvals(
    addresses: list[str], erc20: Annotated[ERC20, Depends(get_erc20)]
) -> dict[str, tuple]:
    approvals = {}

    tasks = [
        erc20.get_approvals_by_owner_address(
            owner_address=address, from_block="earliest", to_block="latest"
        )
        for address in addresses
    ]
    results = await asyncio.gather(*tasks)
    for address, log_recipients in zip(addresses, results):
        approvals[address] = [(log.symbol, log.decimal_value) for log in log_recipients]
    return approvals
