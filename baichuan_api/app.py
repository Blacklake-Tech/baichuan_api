from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from .api import baichuan_api_req

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/chat")
async def chat(
    msg: Annotated[list[str], Query(title="message")] = [], stream: bool = False
):
    if len(msg) == 0:
        raise HTTPException(status_code=400, detail="message不能为空")
    r = await baichuan_api_req(msg, stream=stream)
    return r
