from functools import cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from web3 import AsyncWeb3, Web3
from common.eth import ERC20


class ERC20Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WEB3_")
    http_provider: str


@cache
def get_erc20() -> ERC20:
    erc20_settings = ERC20Settings()
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(erc20_settings.http_provider))
    erc20 = ERC20(w3)
    return erc20
