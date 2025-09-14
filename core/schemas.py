from pydantic import BaseModel, field_validator, Field, field_serializer
from typing import Optional
import re

class baseExpenseShema(BaseModel):
    description: str = Field(..., description="Purpose of expense", max_length=100)
    amount : float = Field(..., description="Expense amount", gt=0)

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)
    
    @field_validator("description",  mode = 'after' )    
    @classmethod
    def validate_description(cls,value: str):
        if len(value)>100:
            raise ValueError("description must not exceed 100 characters")
        if not re.match(r"^[A-Za-z0-9\s.,-]+$", value):
            raise ValueError("Description can only contain letters, numbers, spaces, and basic punctuation")
        return value
    


class ExpenseResponseSchema(baseExpenseShema):
    id: int = Field( description="Expense Identification")
    

class ExpenseCreateSchema(baseExpenseShema):
    pass
   

class ExpenseUpdateSchema(BaseModel):
    description: Optional[str] =Field(None, max_length=100)
    amount : Optional[float] = Field(None, gt=0)

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)
    
    @field_validator("description" )
    @classmethod
    def validate_description(cls,value: str):
        if len(value)>100:
            raise ValueError("description must not exceed 100 characters")
        if not re.match(r"^[A-Za-z0-9\s.,-]+$", value):
            raise ValueError("Description can only contain letters, numbers, spaces, and basic punctuation")
        return value


