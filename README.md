# BoFire Types API

[![Test](https://github.com/experimental-design/bofire-types-api/workflows/Tests/badge.svg)](https://github.com/experimental-design/bofire-types-api/actions?query=workflow%3ATests)
[![Lint](https://github.com/experimental-design/bofire-types-api/workflows/Lint/badge.svg)](https://github.com/experimental-design/bofire-types-api/actions?query=workflow%3ALint)


In BoFire, all data model entities have a type assigned to them. This type directly impacts the properties required / allowed for these entities. For example, a feature can be of type `CategoricalInput` or `ContinuousOutput` (among others). Each of these types has a different json schema which describes the properties required in the entity's spec (a json string).

This API can be used to:

1. get lists of available types (of available type groups)
2. validate if entities comply with its schema


## Types

Every type, provided / managed by this API, has the following structure / properties:

```
{
  "group": "group_key",
  "key": "type_key",
  "name": "Name of this type",
  "description": "Description of this type",
  "typeSchema": {
  	"json schema": "provided by the underlying pydantic model",
  	"this": "can be disregarded by the frontend (for now)."
  },
}
```

## Group and type keys

All types are grouped into **type groups** (valid `group_keys`), e.g., feature, variable, constraint, objective. To obtain a list of all valid group and type keys, simply send a GET request to the `/keys` endpoint. The (potentially outdated) result is:

```json
{
  "feature": [
    "DiscreteInput",
    "CategoricalInput",
    "ContinuousOutput",
    "ContinuousInput",
    "ContinuousDescriptorInput",
    "CategoricalDescriptorInput",
    "MolecularInput"
  ],
  "constraint": [
    "LinearEqualityConstraint",
    "LinearInequalityConstraint",
    "NonlinearEqualityConstraint",
    "NonlinearInequalityConstraint",
    "NChooseKConstraint"
  ],
  "objective": [
    "MaximizeObjective",
    "MinimizeObjective",
    "MaximizeSigmoidObjective",
    "MinimizeSigmoidObjective",
    "TargetObjective",
    "CloseToTargetObjective"
  ],
  "variable": [
    "NumericalInput",
    "NumericalOutput",
    "CategoricalInput",
    "CategoricalOutput",
    "MolecularInput",
    "MolecularOutput"
  ],
  "acquisition-function": [
    "qNEI",
    "qEI",
    "qSR",
    "qUCB",
    "qPI"
  ],
  "kernel": [
    "AdditiveKernel",
    "MultiplicativeKernel",
    "ScaleKernel",
    "HammondDistanceKernel",
    "LinearKernel",
    "MaternKernel",
    "RBFKernel"
  ],
  "prior": [
    "GammaPrior",
    "NormalPrior"
  ],
  "sampler": [
    "PolytopeSampler",
    "RejectionSampler"
  ],
  "strategy": [
    "SoboStrategy",
    "AdditiveSoboStrategy",
    "MultiplicativeSoboStrategy",
    "QehviStrategy",
    "QnehviStrategy",
    "QparegoStrategy",
    "PolytopeSampler",
    "RejectionSampler",
    "RandomStrategy"
  ],
  "surrogate": [
    "EmpiricalSurrogate",
    "RandomForestSurrogate",
    "SingleTaskGPSurrogate",
    "MixedSingleTaskGPSurrogate",
    "MLPEnsemble"
  ]
}
```


## Endpoints

The types API provides the following endpoints:

### GET `/keys`

Returns the keys of all known types, separated into groups.

### GET `/types`

Returns a dictionary of all known types, separated into groups.

### GET `/types/{group_key}`

Return all types of the specified group with status code 200.

If an invalid `group_key` is provided, an error message with status code 404 is returned.

### GET `/types/{group_key}/{type_key}`

Return all types of the specified group with status code 200.

If an invalid `group_key` or `type_key` is provided, an error message with status code 404 is returned.

### POST `/types/{group_key}/{type_key}/validate-type-schema`

The data to validate against the `typeSchema` must be specified in the request body, e.g.:

```json
{
  "name": "my feature"
}
```

If the data is valid according to the `typeSchema`, the following result is returned:

```json
{
  "valid": true,
  "details": "OK key='qwe' type='DiscreteInput' values=[1.0, 2.0, 3.0]"
}
```

If the data is invalid, the following result is returned:

```json
{
  "valid": false,
  "details": "2 validation errors for DiscreteInput\nkey\n  field required (type=value_error.missing)\nvalues\n  field required (type=value_error.missing)"
}
```

If an invalid `group_key` or `type_key` is provided, an error message with status code 404 is returned.

```json
{
  "detail": "No type DiscreteInput_ for group feature exists."
}
```

### POST `/types/{group_key}/{type_key}/validate-db-schema`

The data to validate against the `dbSchema` must be specified in the request body, e.g.:

```json
{
  "name": "my variable"
}
```

If the data is valid according to the `typeSchema`, the following result is returned:

```json
{
  "valid": true,
  "details": "OK"
}
```

If the data is invalid, the following result is returned:

```json
{
  "valid": false,
  "details": "[] is too short\n\nFailed validating 'minItems' in schema['properties']['categories']:\n    {'items': {'$ref': '#/definitions/Category'},\n     'minItems': 1,\n     'title': 'Categories',\n     'type': 'array'}\n\nOn instance['categories']:\n    []"
}
```

If an invalid `group_key` or `type_key` is provided, an error message with status code 404 is returned.

```json
{
  "detail": "No type CategoricalInput_ for group variable exists."
}
```



## Env

The following environment variables can be used:

- `ADD_DUMMY_TYPES` (default: False)
  - set to True to add dummy types
  - this is used / required for testing

## Local dev setup

Use the following command to set and run the API locally as well as run the unit tests.

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
export ADD_DUMMY_TYPES=True
uvicorn --app-dir app:app --reload
```

### Run unit tests

```bash
pytest
```
