# Baichuan API

[![Python CI](https://github.com/Blacklake-Tech/baichuan_api/actions/workflows/CI.yaml/badge.svg)](https://github.com/Blacklake-Tech/baichuan_api/actions/workflows/CI.yaml)

百川大语言模型 53B API版本wrapper - Wrapper around Baichuan API

## Running locally in dev mode

```bash
# install dependencies
poetry install
# run
uvicorn baichuan_api.app:app --reload
```

## Running with docker

```bash
# building image
docker build -t baichuan_api .
# run
docker run -it --rm -v $(pwd):/app -p 8000:8000 baichuan_api
```
