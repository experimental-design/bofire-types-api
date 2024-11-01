from pydantic import BaseModel


class ValidationResult(BaseModel):
    valid: bool
    details: str
