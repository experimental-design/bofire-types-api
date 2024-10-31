from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from models.type import AllTypes, GroupTypes, Type, ValidationResult
from mytypes.all import ALL_CLASSES, ALL_TYPES

router = APIRouter(prefix="", tags=["types"])

@router.get("/keys", response_model=Dict[str, List[str]])
def get_all_keys() -> Dict[str, List[str]]:
    return {
        group_key: [
            type_key
            for type_key in types
        ]
        for group_key, types in ALL_TYPES.items()
    }

@router.get("/types", response_model=AllTypes)
def get_all_types() -> AllTypes:
    return ALL_TYPES

@router.get("/types/{groupKey}", response_model=GroupTypes)
def get_group_types(groupKey: str) -> GroupTypes:
    try:
        return ALL_TYPES[groupKey]
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"No group {groupKey} exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"A server error occurred. Details: {e}")

@router.get("/types/{groupKey}/{typeKey}", response_model=Type)
def get_type(groupKey: str, typeKey: str) -> Type:
    try:
        return ALL_TYPES[groupKey][typeKey]
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"No type {typeKey} for group {groupKey} exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"A server error occurred. Details: {e}")


@router.post("/types/{groupKey}/{typeKey}/validate-type-schema", response_model=ValidationResult)
def validate_type_schema(groupKey: str, typeKey: str, schema: dict,) -> ValidationResult:
    try:
        cls_ = ALL_CLASSES[groupKey][typeKey]
        try:
            res = cls_(**schema)
            return ValidationResult(valid=True, details=f"OK {res}")
        except ValidationError as e:
            # this is to get a more verbose exception message from pydantic than the standard (truncated) one
            return ValidationResult(valid=False, details=str(e.errors()))
        except Exception as e:
            return ValidationResult(valid=False, details=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No type {typeKey} for group {groupKey} exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"A server error occurred. Details: {e}")


