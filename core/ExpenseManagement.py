from fastapi import FastAPI, status, HTTPException, Body
from typing import Optional
app = FastAPI()


Expenses = [
    {"id":1, "description":"buy ", "amount":125.6},
]

@app.get("/expenses", status_code=status.HTTP_200_OK)
async def root():
    return Expenses

@app.post("/expenses", status_code=status.HTTP_200_OK)
async def create_expense(
    description: str = Body(...),
    amount: float = Body(...)
     ):
    Expenses.append({"id":max((e["id"] for e in Expenses), default=0) + 1,"description":description, "amount":amount})
    return Expenses[-1]


@app.get("/expenses/{id}", status_code=status.HTTP_200_OK)
async def get_expense(id:int):
    for e in Expenses:
        if(e["id"] == id):
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.put("/expenses/{id}", status_code=status.HTTP_200_OK)
async def replace_expense(id:int, description: str = Body(...), amount: float  = Body(...)):
    for e in Expenses:
        if(e["id"] == id):
            e["description"] = description
            e["amount"] = amount
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.patch("/expenses/{id}", status_code=status.HTTP_200_OK)
async def update_expense(id:int, description:  Optional[str] = Body(None), amount:  Optional[float] = Body(None) ):
    for e in Expenses:
        if(e["id"] == id):
            if description is not None and description.strip() != "":
                e["description"] = description
            if amount is not None:
                e["amount"] = amount
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int):
    for i, n in enumerate(Expenses):
        if n["id"] == id:
            del Expenses[i]
            return 
        # {"message": f"Name with ID {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
