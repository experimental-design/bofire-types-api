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
    ) -> List["Type"]:
        return [cls.from_type(type_, group) for type_ in types]

    @classmethod
    def from_union(
        cls,
        union: _UnionGenericAlias,
        group: str,
    ) -> List["Type"]:
        types = []
        for type_ in union.__args__:
            types.append(cls.from_type(type_, group))
        return types
