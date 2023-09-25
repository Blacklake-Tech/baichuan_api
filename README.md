# Baichuan API

[![Python CI](https://github.com/Blacklake-Tech/baichuan_api/actions/workflows/CI.yaml/badge.svg)](https://github.com/Blacklake-Tech/baichuan_api/actions/workflows/CI.yaml)

百川大语言模型 53B 版本 [API][api] wrapper / Wrapper around Baichuan 53B [API][api]

## Running locally in dev mode

```bash
# install dependencies
poetry install
# run
uvicorn baichuan_api.app:app --reload
# open in browser http://localhost:8000/chat?msg=Somos+Banditos
# you can use multiple msg query params to send multiple messages
```

## Running with docker

```bash
# building image
docker build -t baichuan_api .
# run
docker run -it --rm -v $(pwd):/app -p 8000:8000 baichuan_api
# open in browser http://localhost:8000/chat?msg=Somos+Banditos
# you can use multiple msg query params to send multiple messages
```

[api]: https://platform.baichuan-ai.com/docs/api
