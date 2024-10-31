import jsonschema

from tests.conftest import Client
from tests.schemas import GROUPS_SCHEMA


def test_get_groups_should_return_valid_data(client: Client):
    response = client.get("/types")
    assert response.status_code == 200
    res = response.json()
    jsonschema.validate(res, GROUPS_SCHEMA)


def test_get_groups_should_return_same_data_as_get_group(client: Client):
    response = client.get("/types")
    assert response.status_code == 200
    res = response.json()
    for k, v in res.items():
        response_ = client.get(f"/types/{k}")
        res_ = response_.json()
        assert v == res_
