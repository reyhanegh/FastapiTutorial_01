from pydantic import BaseModel, field_validator, Field, field_serializer
from typing import Optional, List


class ExpenseSchema(BaseModel):
    id: int
    description: str
    amount : float

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)


class ExpenseCreate(BaseModel):
    description: str = Field( max_length=100)
    amount : float = Field(ge=0)
   


class ExpenseUpdate(BaseModel):
    description: Optional[str] =Field(max_length=100)
    amount : Optional[float] = Field(ge=0)


