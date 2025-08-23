from pydantic import BaseModel, field_validator, Field, field_serializer
from typing import Optional, List

class baseExpenseShema(BaseModel):
    description: str = Field(..., description="Purpose of expense", max_length=100)
    amount : float = Field(..., description="Expense amount", gt=0)

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)
    
    @field_validator("description")
    def validate_description(self,value: str):
        if len(value)>100:
            raise ValueError("description must not exceed 100 characters")
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
    
    @field_validator("description")
    def validate_description(self,value: str):
        if len(value)>100:
            raise ValueError("description must not exceed 100 characters")
        return value


