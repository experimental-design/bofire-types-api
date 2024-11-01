# Bofire Types Api



## Running it

### Run locally

Create a venv and install all dependencies:

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn  --reload --port 8000 --app-dir app app:app
```

If you want to run tests, overwrite the `ADD_DUMMY_TYPES` env var:

```bash
export ADD_DUMMY_TYPES=True
uvicorn  --reload --port 8000 --app-dir app app:app
```

### Run containerized

Build the image:

```bash
docker build -f Dockerfile -t bofire-types-api:latest
```

Run a container:

```bash
docker run -d -p 8000:8000 bofire-types-api:latest
```

If you want to run tests, overwrite the `ADD_DUMMY_TYPES` env var:

```bash
docker run -d -p 8000:8000 -e ADD_DUMMY_TYPES=True bofire-types-api:latest
```

### Swagger UI

The Swagger UI should then be accessable [here](http://127.0.0.1:8000/docs).

### Run tests

Install the test dependencies:

```bash
pip install -r requirements-test.txt
```

Run the tests:

```bash
export TYPES_API_PATH="http://localhost:8000"
pytest tests/
```







```
services:
  types:
    build: ./types
    environment:
      ADD_DUMMY_TYPES: "True"
    ports:
      - 5008:80
```

