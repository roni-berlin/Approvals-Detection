from enum import StrEnum

from web3 import Web3


class EventTopic(StrEnum):
    APPROVAL = Web3.keccak(text="Approval(address,address,uint256)").hex()
