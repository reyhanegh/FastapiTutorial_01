from fastapi import FastAPI, status, HTTPException, Body
from schema import ExpenseSchema, ExpenseCreate, ExpenseUpdate
from typing import List


app = FastAPI()


Expenses: List[ExpenseSchema] = [
    ExpenseSchema(id=1, description="buy", amount=125.6),
    ExpenseSchema(id=2, description="food", amount=50.0)
]


@app.get("/expense/", response_model=List[ExpenseSchema], status_code=status.HTTP_200_OK)
async def root():
    return Expenses


@app.get("/expense/{id}", response_model=ExpenseSchema, status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int):
    for e in Expenses:
        if(e["id"] == id):
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.post("/add_expense/", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate ):
    new_expense = ExpenseSchema(
        id=max((e.id for e in Expenses), default=0) + 1,
        description=expense.description, amount=expense.amount)
    Expenses.append(new_expense)
    return new_expense

@app.put("/edit_expense/", response_model=ExpenseSchema)
async def edit_expense(update_data: ExpenseUpdate ):
    for e in Expenses:
        if e["id"] == update_data.id:
            if update_data.description is not None :
                e['description'] = update_data.description
            if update_data.amount is not None :
                e['amount'] = update_data.amount
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.delete("/delete_expense/{id}")
def delete_expense(id: int):
    for i, n in enumerate(Expenses):
        if n["id"] == id:
            del Expenses[i]
            return {"message": f"Name with ID {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
