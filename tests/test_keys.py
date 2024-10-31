import jsonschema

from tests.conftest import Client
from tests.schemas import KEYS_SCHEMA


def test_get_keys_should_return_valid_data(client: Client):
    response = client.get("/keys")
    assert response.status_code == 200
    res = response.json()
    jsonschema.validate(res, KEYS_SCHEMA)


def test_get_keys_should_return_valid_group_keys(client: Client):
    res = client.get("/keys").json()
    for group_key in res.keys():
        response = client.get(f"/types/{group_key}")
        assert response.status_code == 200


def test_get_keys_should_return_valid_type_keys(client: Client):
    res = client.get("/keys").json()
    for group_key, type_keys in res.items():
        for type_key in type_keys:
            response = client.get(f"/types/{group_key}/{type_key}")
            assert response.status_code == 200


def test_get_keys_should_return_same_types_as_get_group(client: Client):
    res = client.get("/keys").json()
    for group_key, type_keys in res.items():
        res_ = client.get(f"/types/{group_key}").json()
        type_keys_ = list(res_.keys())
        assert type_keys == type_keys_
