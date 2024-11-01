FROM python:3.11-bookworm

RUN apt-get update &&\
    apt-get install -y libopenblas-dev

COPY requirements.txt .

RUN pip install --upgrade pip &&\
    pip install torch --index-url https://download.pytorch.org/whl/cpu &&\
    pip install -r requirements.txt

COPY app /src

WORKDIR /src

EXPOSE 8000

CMD uvicorn --host 0.0.0.0 --port 8000 app:app 
