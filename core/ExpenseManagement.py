from fastapi import FastAPI, status, HTTPException, Body, Query
from typing import Optional
from fastapi.responses import JSONResponse


app = FastAPI()


Expenses = [
    {"id":1, "description":"buy ", "amount":125.6},
]

@app.get("/expenses", status_code=status.HTTP_200_OK)
async def retrieve_data(min: Optional[float] = Query(default=None), max:Optional[float] = Query(default=None)):
    if min is not None and max is not None:
        return [item for item in Expenses if min <= item["amount"] <= max]
    elif min is not None:
        return [item for item in Expenses if item["amount"] >= min]
    elif max is not None:
        return [item for item in Expenses if item["amount"] <= max]
    else:
        return Expenses

@app.get("/expenses/{id}", status_code=status.HTTP_200_OK)
async def get_expense(id:int):
    for e in Expenses:
        if(e["id"] == id):
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
async def create_expense(
    description: str = Body(...),
    amount: float = Body(...)
     ):
    Expenses.append({"id":max((e["id"] for e in Expenses), default=0) + 1,"description":description, "amount":amount})
    return Expenses[-1]


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
            return  {"message": f"Name with ID {id} deleted successfully"}
            # return JSONResponse(content = {"message": f"Name with ID {id} deleted successfully"}, status_code=status.HTTP_200_ok)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
