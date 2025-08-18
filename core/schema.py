from pydantic import BaseModel, field_validator, Field, field_serializer
from typing import Optional, List


Expenses = [
    {"id":1, "description":"buy ", "amount":125.6},
]


class ExpenseSchema(BaseModel):
    id: int
    description: str
    amount : float

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)


class ExpenseCreate(BaseModel):
    description: str 
    amount : float = Field(gt=0)

    


class ExpenseUpdate(BaseModel):
    id: int = Field(...)
    description: Optional[str] 
    amount : Optional[float] = Field(gt=0)


