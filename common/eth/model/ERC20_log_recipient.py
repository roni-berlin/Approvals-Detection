from contextvars import Context
from functools import cache
from typing import Any, Sequence, cast
from eth_typing import BlockNumber, ChecksumAddress
from hexbytes import HexBytes
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    computed_field,
    model_validator,
)
from web3 import AsyncWeb3, Web3
from common.eth.consts import ERC20_ABI


class ERC20LogRecipient(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    address: ChecksumAddress
    blockHash: HexBytes
    blockNumber: BlockNumber
    data: HexBytes
    logIndex: int
    topics: Sequence[HexBytes]
    transactionHash: HexBytes
    transactionIndex: int
    removed: bool
    symbol: str = None

    @model_validator(mode="after")
    async def compute_field(self, info: ValidationInfo):
        context = cast(Context, info.context)
        w3: AsyncWeb3 = context.get("web3")
        contract = w3.eth.contract(address=self.address, abi=ERC20_ABI)
        try:
            self.symbol = await contract.functions.symbol().call()
        except:
            pass

        return self

    @computed_field
    @property
    def decimal_value(self) -> int:
        return Web3.to_int(self.data)
