import os
import random
import uuid
from typing import Dict, List, Tuple

import requests
from pytest import fixture


class Client:
    def __init__(self, base_url: str, requests=requests):
        self.base_url = base_url
        self.requests = requests

    def get(self, path: str) -> requests.Response:
        return self.requests.get(f"{self.base_url}{path}")

    def post(self, path: str, request_body: dict) -> requests.Response:
        return self.requests.post(f"{self.base_url}{path}", json=request_body)


@fixture
def client() -> Client:
    return Client(base_url=os.getenv("TYPES_URL", "http://localhost:8000"))


@fixture
def rand_str() -> str:
    return str(uuid.uuid4())[:6]


@fixture
def all_keys(client) -> Dict[str, List[str]]:
    return client.get(f"/keys").json()


@fixture
def group_key(all_keys) -> str:
    return random.choice(list(all_keys.keys()))


@fixture
def type_key(all_keys, group_key) -> str:
    return random.choice(all_keys[group_key])
