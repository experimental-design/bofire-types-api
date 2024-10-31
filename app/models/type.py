from typing import Dict

from pydantic import BaseModel


class Type(BaseModel):
    group: str
    key: str
    name: str
    description: str
    typeSchema: dict


GroupTypes = Dict[str, Type]
AllTypes = Dict[str, GroupTypes]


class ValidationResult(BaseModel):
    valid: bool
    details: str
