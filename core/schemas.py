from pydantic import BaseModel, field_validator, Field, field_serializer
from typing import Optional
import re

# *************************************** expense schema ***************************************

class baseExpenseSchema(BaseModel):
    description: str = Field(..., description="Purpose of expense", max_length=50)
    amount : float = Field(..., description="Expense amount", gt=0)

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)
    
    @field_validator("description",  mode = 'after' )    
    @classmethod
    def validate_description(cls,value: str):
        if len(value)>50:
            raise ValueError("description must not exceed 50 characters")
        if not re.match(r"^[A-Za-z0-9\s.,-]+$", value):
            raise ValueError("Description can only contain letters, numbers, spaces, and basic punctuation")
        return value
    


class ExpenseResponseSchema(baseExpenseSchema):
    id: int = Field( description="Expense Identification")
    user_id : int =  Field(..., description="user id")
    

class ExpenseCreateSchema(baseExpenseSchema):
    user_id : int =  Field(..., description="user id")

   

class ExpenseUpdateSchema(BaseModel):
    description: Optional[str] =Field(None, max_length=50)
    amount : Optional[float] = Field(None, gt=0)

    @field_serializer("amount")
    def serialize_float(self, value: float):
        return round(value, 2)
    
    @field_validator("description" )
    @classmethod
    def validate_description(cls,value: str):
        if len(value)>50:
            raise ValueError("description must not exceed 50 characters")
        if not re.match(r"^[A-Za-z0-9\s.,-]+$", value):
            raise ValueError("Description can only contain letters, numbers, spaces, and basic punctuation")
        return value

# *************************************** user schema ***************************************
class baseUserSchema(BaseModel):
    name: str =Field(..., max_length=30)

    
    @field_validator("name",  mode = 'after' )    
    @classmethod
    def validate_name(cls,value: str):
        if len(value)>30:
            raise ValueError("name must not exceed 30 characters")
        if not re.match(r"^[\w\s.,-]+$", value):
            raise ValueError("name can only contain letters, spaces, and basic punctuation")
        return value
    


class UserResponseSchema(baseUserSchema):
    id: int = Field( description="User Identification")
    expenses: list[ExpenseResponseSchema] = Field(default_factory=list)
    
    

class UserCreateSchema(baseUserSchema):
    pass
   

class UserUpdateSchema(BaseModel):
    name: Optional[str] =Field(None, max_length=30)

    
    @field_validator("name" )
    @classmethod
    def validate_name(cls,value: str):
        if len(value)>30:
            raise ValueError("name must not exceed 30 characters")
        if not re.match(r"^[\w\s.,-]+$", value):
            raise ValueError("name can only contain letters, spaces, and basic punctuation")
        return value