# Baichuan API

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
