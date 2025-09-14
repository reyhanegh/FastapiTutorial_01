from fastapi import FastAPI, status, HTTPException, Body, Query, Depends
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from typing import List, Optional
from contextlib import asynccontextmanager
from database import Base, engine, get_db, Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Startup tasks...")
    Base.metadata.create_all(bind = engine)

    yield

    print("Shutdown tasks...")

    


app = FastAPI(lifespan=lifespan)


Expenses: List[ExpenseResponseSchema] = [
    ExpenseResponseSchema(id=1, description="buy", amount=125.6),
    ExpenseResponseSchema(id=2, description="food", amount=50.0)
]


@app.get("/expenses", response_model=List[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
async def retrieve_data(min: Optional[float] = Query(default=None), max:Optional[float] = Query(default=None), db:Session=Depends(get_db)):
    
    q = db.query(Expense)
    if min is not None and max is not None:
        q = q.filter(Expense.amount >= min, Expense.amount <= max)
    elif min is not None:  
        q = q.filter(Expense.amount >= min)
    elif max is not None:  
        q = q.filter(Expense.amount <= max)
   
    results = q.all()
    return results

    
    # if min is not None and max is not None:
    #     return [item for item in Expenses if min <= item.amount <= max]
    # elif min is not None:
    #     return [item for item in Expenses if item.amount >= min]
    # elif max is not None:
    #     return [item for item in Expenses if item.amount <= max]
    # else:
    #     return Expenses


@app.post("/expenses", response_model=ExpenseResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreateSchema, db:Session=Depends(get_db)):
    # new_expense = ExpenseResponseSchema(
    #     id=max((item.id for item in Expenses), default=0) + 1,
    #     description=expense.description, amount=expense.amount)
    # Expenses.append(new_expense)

    new_expense = Expense(description=expense.description, amount=expense.amount)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.get("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int, db:Session=Depends(get_db)):
    # for item in Expenses:
    #     if(item.id == id):
    #         return item

    person = db.query(Expense).filter_by(id=id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.put("/expenses/{id}",response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def replace_expense(id:int, new_data: ExpenseCreateSchema, db:Session=Depends(get_db)):
    # for item in Expenses:
    #     if(item.id == id):
    #         item.description = new_data.description
    #         item.amount = new_data.amount
    #         return item

    person = db.query(Expense).filter_by(id=id).one_or_none()
    if person:
        person.description = new_data.description
        person.amount = new_data.amount
        db.commit()
        db.refresh(person)
        return person
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.patch("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def edit_expense(id:int, update_data: ExpenseUpdateSchema, db:Session=Depends(get_db) ):

    update_data = update_data.model_dump(exclude_unset=True)
    expense = db.query(Expense).filter_by(id=id).one_or_none()

    # for item in Expenses:
    #     if item.id == id:
    #         for key, value in update_data.items():
    #             if isinstance(value, str) and value.strip() == "":
    #                 continue
    #             if value is not None:
    #                 setattr(item, key, value)
    #         return item

    if expense:
        for key, value in update_data.items():
            if isinstance(value, str) and value.strip() == "":
                continue
            if value is not None:
                setattr(expense, key, value)

        db.commit()
        db.refresh(expense)
        return expense
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, db:Session=Depends(get_db)):

    # for i, item in enumerate(Expenses):
    #     if item.id == id:
    #         del Expenses[i]
    #         return 
        # {"message": f"Name with ID {id} deleted successfully"}

    expense = db.query(Expense).filter_by(id=id).one_or_none()
    if(expense):
        if expense:
            db.delete(expense)
            db.commit()
            db.refresh(expense)
            return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
