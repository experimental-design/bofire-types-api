import jsonschema

from tests.conftest import Client
from tests.schemas import TYPE_SCHEMA


def test_get_type_should_reject_invalid_type_key(
    client: Client,
    group_key: str,
    rand_str: str,
):
    response = client.get(f"/types/{group_key}/{rand_str}")
    assert response.status_code == 404


def test_get_type_should_reject_invalid_group_key(
    client: Client,
    type_key: str,
    rand_str: str,
):
    response = client.get(f"/types/{rand_str}/{type_key}")
    assert response.status_code == 404


def test_get_type_should_return_valid_data(
    client: Client,
    group_key: str,
    type_key: str,
):
    response = client.get(f"/types/{group_key}/{type_key}")
    assert response.status_code == 200
    res = response.json()
    jsonschema.validate(res, TYPE_SCHEMA)
