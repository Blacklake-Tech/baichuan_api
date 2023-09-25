import hashlib
import json
import logging
import os
import time
from functools import cache
from logging.config import dictConfig

import dotenv
import requests
from beartype import beartype
from fastapi import HTTPException
from pydantic import BaseModel
from ulid import ULID

from .models import BaichuanReq, BaichuanResp


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "baichuan-api"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s - %(message)s"
    LOG_LEVEL: str = "INFO"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


dotenv.load_dotenv()
dictConfig(LogConfig())

logger = logging.getLogger("baichuan-api")


@cache
def get_key_and_secret():
    api_key, secret_key = os.getenv("API_KEY"), os.getenv("SECRET_KEY")
    if not api_key or not secret_key:
        raise HTTPException(
            status_code=500, detail="API_KEY or SECRET_KEY not found in environment"
        )
    return api_key, secret_key


@beartype
def calculate_md5(input_string: str) -> str:
    md5 = hashlib.md5()
    md5.update(input_string.encode("utf-8"))
    encrypted = md5.hexdigest()
    return encrypted


@beartype
def generate_header(data: BaichuanReq) -> tuple[dict, str]:
    api_key, secret_key = get_key_and_secret()
    time_stamp = int(time.time())
    data = data.model_dump(exclude_none=True)
    data = json.dumps(data, ensure_ascii=True)
    signature = calculate_md5(secret_key + data + str(time_stamp))
    req_id = str(ULID())
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        "X-BC-Request-Id": req_id,
        "X-BC-Timestamp": str(time_stamp),
        "X-BC-Signature": signature,
        "X-BC-Sign-Algo": "MD5",
    }
    return headers, req_id


@beartype
def baichuan_api_req(messages: list[str]) -> BaichuanResp:
    url = "https://api.baichuan-ai.com/v1/chat"
    data = BaichuanReq(
        model="Baichuan2-53B",
        messages=[{"role": "user", "content": message} for message in messages],
    )
    headers, req_id = generate_header(data)
    logger.info("[%s] %s", req_id, data.model_dump_json(exclude_none=True))
    response = requests.post(
        url, json=data.model_dump(exclude_none=True), headers=headers
    )

    if response.status_code == 200:
        try:
            r = response.json()
            r = BaichuanResp(**r)
        except Exception as e:
            logger.warning("[%s] %s", req_id, "上游返回解析失败")
            raise HTTPException(status_code=500, detail="上游返回解析失败")
        if r.code != 0:
            logger.warning("[%s] %s %s", req_id, r.code, r.msg)
            raise HTTPException(status_code=500, detail=r.code.get_message())
        else:
            logger.info("[%s] %s %s", req_id, r.code, r.msg)
            return r
    else:
        logger.error("请求失败，状态码: %s", response.status_code)
        raise HTTPException(
            status_code=500, detail="请求失败，状态码: %s" % response.status_code
        )
