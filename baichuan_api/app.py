from functools import cache
from logging.config import dictConfig
from typing import Annotated

from fastapi import FastAPI, Query
from ulid import ULID

from .api import baichuan_api_req
from .models import BaichuanData

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/chat")
async def chat(msg: Annotated[list[str] | None, Query()]) -> BaichuanData:
    resp = baichuan_api_req(msg)
    return resp.data
