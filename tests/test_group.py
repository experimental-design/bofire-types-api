import jsonschema

from tests.conftest import Client
from tests.schemas import GROUP_SCHEMA


def test_get_group_should_reject_invalid_group_key(client: Client, rand_str: str):
    response = client.get(f"/types/{rand_str}")
    assert response.status_code == 404


def test_get_group_should_return_valid_data(client: Client, group_key: str):
    response = client.get(f"/types/{group_key}")
    assert response.status_code == 200
    res = response.json()
    jsonschema.validate(res, GROUP_SCHEMA)
    for k, v in res.items():
        assert v["key"] == k
        assert v["group"] == group_key


def test_get_group_should_return_same_data_as_get_type(client: Client, group_key: str):
    response = client.get(f"/types/{group_key}")
    assert response.status_code == 200
    res = response.json()
    for k, v in res.items():
        response_ = client.get(f"/types/{group_key}/{k}")
        res_ = response_.json()
        assert v == res_
