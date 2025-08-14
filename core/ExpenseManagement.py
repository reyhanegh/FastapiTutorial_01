from fastapi import FastAPI, status, HTTPException

app = FastAPI()


Expenses = [
    {"id":1, "description":"buy ", "amount":125.6},
]


@app.get("/expense/")
async def root():
    return Expenses


@app.get("/expense/{id}")
async def get_expense_byId(id:int):
    for e in Expenses:
        if(e["id"] == id):
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.post("/add_expense/", status_code=status.HTTP_201_CREATED)
async def create_expense(description:str, amount:float ):
    Expenses.append({"id":len(Expenses)+1,"description":description, "amount":amount})
    return Expenses[-1]



@app.put("/edit_expense/{id}")
async def edit_expense(id:int, description:str, amount:float):
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
