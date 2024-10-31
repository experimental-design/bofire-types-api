import pytest

from tests.conftest import Client


def test_type_schema_validation_should_reject_invalid_group_key(
    client: Client,
    type_key: str,
    rand_str: str,
):
    response = client.post(f"/types/{rand_str}/{type_key}/validate-type-schema", {})
    assert response.status_code == 404


def test_type_schema_validation_should_reject_invalid_type_key(
    client: Client,
    group_key: str,
    rand_str: str,
):
    response = client.post(f"/types/{group_key}/{rand_str}/validate-type-schema", {})
    assert response.status_code == 404


def test_type_schema_validation_should_reject_missing_body(
    client: Client,
    group_key: str,
    type_key: str,
):
    response = client.post(f"/types/{group_key}/{type_key}/validate-type-schema", None)
    assert response.status_code == 422


def test_type_schema_validation_should_accept_valid_body(
    client: Client,
    group_key: str,
    type_key: str,
):
    response = client.post(f"/types/{group_key}/{type_key}/validate-type-schema", {})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "group_key, type_key, valid, spec",
    [
        ("dummy_category", "DummyCategory", True, {"name": "qwe"}),
        ("dummy_category", "DummyCategory", False, {}),
        ("dummy", "DummyA", True, {"a": 123, "category": {"name": "cat"}}),
        ("dummy", "DummyA", False, {"a": 123, "category": {}}),
        ("dummy", "DummyA", False, {"a": 123}),
        ("dummy", "DummyA", False, {"category": {"name": "cat"}}),
        ("dummy", "DummyB", True, {"b": 123, "category": {"name": "cat"}}),
        ("dummy", "DummyB", False, {"b": 123, "category": {}}),
        ("dummy", "DummyB", False, {"b": 123}),
        ("dummy", "DummyB", False, {"category": {"name": "cat"}}),
    ],
)
def test_type_schema_validation_should_validate_spec(
    client: Client,
    group_key: str,
    type_key: str,
    valid: bool,
    spec: dict,
):
    response = client.post(f"/types/{group_key}/{type_key}/validate-type-schema", spec)
    assert response.status_code == 200
    res = response.json()
    assert res["valid"] == valid
