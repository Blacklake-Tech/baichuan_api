from functools import cache
from logging.config import dictConfig

from fastapi import FastAPI
from ulid import ULID

from .api import baichuan_api_req
from .models import BaichuanData

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/chat")
async def chat(message: str) -> BaichuanData:
    resp = baichuan_api_req([message])
    return resp.data
