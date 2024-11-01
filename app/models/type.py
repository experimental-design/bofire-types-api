from typing import Dict, List, Literal, Union, _UnionGenericAlias

from pydantic import BaseModel


class Type(BaseModel):
    group: str
    key: str
    name: str
    description: str
    typeSchema: dict

    @classmethod
    def from_type(
        cls,
        type_,
        group: str,
    ) -> "Type":
        return cls(
            group="feature",
            key=type_.__name__,
            name=type_.__name__,
            description=type_.__doc__ or "",
            typeSchema=type_.schema(),
        )

    @classmethod
    def from_types(
        cls,
        types: list,
        group: str,
    ) -> dict[str, "Type"]:
        types = {}
        for type_ in types:
            type_ = cls.from_type(type_, group)
            types[type_.key] = type_
        return types

    @classmethod
    def from_union(
        cls,
        union: _UnionGenericAlias,
        group: str,
    ) -> dict[str, "Type"]:
        return cls.from_types(union.__args__, group)
