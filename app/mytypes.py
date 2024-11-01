import os
from typing import Dict, List, Literal, Union, _UnionGenericAlias

from bofire.data_models.api import (
    AnyAcquisitionFunction,
    AnyConstraint,
    AnyFeature,
    AnyKernel,
    AnyObjective,
    AnyPrior,
    AnyStrategy,
    AnySurrogate,
    Domain,
    Inputs,
    Outputs,
)
from models import Type
from pydantic import BaseModel


def get_type(type) -> dict:
    return {
        "key": type.__name__,
        "class": type,
        "name": type.__name__,
        # FIXME: fix handling of missing docstrings
        "description": type.__doc__ or "",
    }


def get_types_from_union(union: _UnionGenericAlias) -> List[dict]:
    types = []
    for type_ in union.__args__:
        types.append(get_type(type_))
    return types


def to_type_models(types: List[dict], group: str) -> Dict[str, Type]:
    return {
        type_["key"]: Type(
            group=group,
            key=type_["key"],
            name=type_["name"],
            description=type_["description"],
            typeSchema=type_["class"].schema(),
        )
        for type_ in types
    }


feature_types = Type.from_union(AnyFeature, "feature")
constraint_types = Type.from_union(AnyConstraint, "constraint")
objective_types = Type.from_union(AnyObjective, "objective")
acquisition_function_types = Type.from_union(
    AnyAcquisitionFunction, "acquisition-function"
)
kernel_types = Type.from_union(AnyKernel, "kernel")
prior_types = Type.from_union(AnyPrior, "prior")
strategy_types = Type.from_union(AnyStrategy, "strategy")
surrogate_types = Type.from_union(AnySurrogate, "surrogate")
domain_types = Type.from_types([Domain, Inputs, Outputs], "domain")

ALL_TYPES = {
    "feature": feature_types,
    "constraint": constraint_types,
    "objective": objective_types,
    "acquisition-function": acquisition_function_types,
    "kernel": kernel_types,
    "prior": prior_types,
    "strategy": strategy_types,
    "surrogate": surrogate_types,
    "domain": domain_types,
}

# TODO: update this
ALL_CLASSES = {
    "feature": {x.__name__: x for x in AnyFeature.__args__},
    "constraint": {x.__name__: x for x in AnyConstraint.__args__},
    "objective": {x.__name__: x for x in AnyObjective.__args__},
    "acquisition-function": {x.__name__: x for x in AnyAcquisitionFunction.__args__},
    "kernel": {x.__name__: x for x in AnyKernel.__args__},
    "prior": {x.__name__: x for x in AnyPrior.__args__},
    "strategy": {x.__name__: x for x in AnyStrategy.__args__},
    "surrogate": {x.__name__: x for x in AnySurrogate.__args__},
    "domain": {x.__name__: x for x in [Domain, Inputs, Outputs]},
}

ALL_CLASSES = {}

if os.getenv("ADD_DUMMY_TYPES", "False").lower() == "true":

    class DummyCategory(BaseModel):
        name: str

    class Dummy(BaseModel):
        category: DummyCategory
        type: str

    class DummyA(Dummy):
        type: Literal["DummyA"] = "DummyA"
        a: int

    class DummyB(Dummy):
        type: Literal["DummyB"] = "DummyB"
        b: int

    AnyDummyCategory = DummyCategory
    AnyDummy = Union[DummyA, DummyB]

    ALL_TYPES["dummy_category"] = to_type_models(
        [
            {
                "key": DummyCategory.__name__,
                "class": DummyCategory,
                "name": DummyCategory.__name__,
                "description": "",
            }
        ],
        "dummy_category",
    )
    ALL_TYPES["dummy"] = to_type_models(get_types_from_union(AnyDummy), "dummy")

    ALL_CLASSES["dummy_category"] = {DummyCategory.__name__: DummyCategory}
    ALL_CLASSES["dummy"] = {x.__name__: x for x in AnyDummy.__args__}
    ALL_CLASSES["dummy"] = {x.__name__: x for x in AnyDummy.__args__}
    ALL_CLASSES["dummy"] = {x.__name__: x for x in AnyDummy.__args__}
    ALL_CLASSES["dummy"] = {x.__name__: x for x in AnyDummy.__args__}
    ALL_CLASSES["dummy"] = {x.__name__: x for x in AnyDummy.__args__}
