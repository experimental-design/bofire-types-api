# BASE
FROM python:3.11-bookworm as base

RUN apt-get update &&\
    apt-get install -y libopenblas-dev

RUN python3 -m venv /venv &&\
    /venv/bin/pip install --upgrade pip

COPY requirements.txt .

RUN /venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu &&\
    /venv/bin/pip install --disable-pip-version-check -r requirements.txt


## TEST
FROM python:3.11-slim-bookworm as test

COPY --from=base venv venv
COPY src ./src
COPY tests ./tests

RUN /venv/bin/pip install pytest

RUN export USE_DUMMY_COMPUTATIONS=True;\
    /venv/bin/python3 -m pytest ./tests
RUN export USE_DUMMY_COMPUTATIONS=False;\
    /venv/bin/python3 -m pytest ./tests


# BUILD
FROM python:3.11-slim-bookworm as run

COPY --from=test /src ./src
COPY --from=test venv venv

ENV PATH="/venv/bin:$PATH"
WORKDIR /src

EXPOSE 8000

CMD uvicorn --host 0.0.0.0 --port 8000 app:app 
