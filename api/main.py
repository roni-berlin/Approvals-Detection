from fastapi import FastAPI
from api.routes.ERC20 import router as erc20_router

app = FastAPI()

app.include_router(erc20_router, prefix="/ERC20")
