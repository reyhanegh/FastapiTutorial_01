from fastapi import FastAPI, status, HTTPException, Body

app = FastAPI()


Expenses = [
    {"id":1, "description":"buy ", "amount":125.6},
]


@app.get("/expense/", status_code=status.HTTP_200_OK)
async def root():
    return Expenses


@app.get("/expense/{id}", status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int):
    for e in Expenses:
        if(e["id"] == id):
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.post("/add_expense/", status_code=status.HTTP_201_CREATED)
async def create_expense(
    description: str = Body(...),
    amount: float = Body(...)
     ):
    Expenses.append({"id":len(Expenses)+1,"description":description, "amount":amount})
    return Expenses[-1]



@app.put("/edit_expense/")
async def edit_expense(
    id:int = Body(...),
    description: str | None = Body(None),
    amount: float | None = Body(None)
    ):
    for e in Expenses:
        if e["id"] == id:
            e['description'] = description
            e['amount'] = amount
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.delete("/delete_expense/{id}")
def delete_expense(id: int):
    for i, n in enumerate(Expenses):
        if n["id"] == id:
            del Expenses[i]
            return {"message": f"Name with ID {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
