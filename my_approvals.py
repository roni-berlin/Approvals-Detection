import asyncio
from functools import wraps
from typing import Annotated
from dotenv import load_dotenv
import typer
from web3 import AsyncWeb3
from common.eth import ERC20

load_dotenv()

def async_typer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    
    return wrapper

@async_typer
async def my_approvals(
    address: Annotated[str, typer.Option()],
    web3_http_provider: Annotated[str, typer.Argument(envvar="WEB3_HTTP_PROVIDER")],
):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(web3_http_provider))
    if not await w3.is_connected():
        print("Connection Error")
    else:
        erc20 = ERC20(w3)
        erc20_log_recipients = await erc20.get_approvals_by_owner_address(
            address, from_block="earliest", to_block="latest"
        )
        for erc20_log_recipient in erc20_log_recipients:
            print(f"approval on {erc20_log_recipient.symbol or "UnknownERC20"} for amount of {erc20_log_recipient.decimal_value}")
            
if __name__ == "__main__":
    typer.run(my_approvals)
