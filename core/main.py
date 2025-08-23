from fastapi import FastAPI, status, HTTPException, Body, Query
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from typing import List, Optional


app = FastAPI()


Expenses: List[ExpenseResponseSchema] = [
    ExpenseResponseSchema(id=1, description="buy", amount=125.6),
    ExpenseResponseSchema(id=2, description="food", amount=50.0)
]


@app.get("/expenses", response_model=List[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
async def retrieve_data(min: Optional[float] = Query(default=None), max:Optional[float] = Query(default=None)):
    if min is not None and max is not None:
        return [item for item in Expenses if min <= item.amount <= max]
    elif min is not None:
        return [item for item in Expenses if item.amount >= min]
    elif max is not None:
        return [item for item in Expenses if item.amount <= max]
    else:
        return Expenses


@app.post("/expenses", response_model=ExpenseResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreateSchema ):
    new_expense = ExpenseResponseSchema(
        id=max((item.id for item in Expenses), default=0) + 1,
        description=expense.description, amount=expense.amount)
    Expenses.append(new_expense)
    return new_expense

@app.get("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int):
    for item in Expenses:
        if(item.id == id):
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.put("/expenses/{id}",response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def replace_expense(id:int, new_data: ExpenseCreateSchema):
    for item in Expenses:
        if(item.id == id):
            item.description = new_data.description
            item.amount = new_data.amount
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.patch("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def edit_expense(id:int, update_data: ExpenseUpdateSchema ):

    update_data = update_data.model_dump(exclude_unset=True)

    for item in Expenses:
        if item.id == id:
            for key, value in update_data.items():
                if isinstance(value, str) and value.strip() == "":
                    continue
                if value is not None:
                    setattr(item, key, value)
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int):
    for i, item in enumerate(Expenses):
        if item.id == id:
            del Expenses[i]
            return 
        # {"message": f"Name with ID {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
