from fastapi import FastAPI, status, HTTPException, Body, Query, Depends
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from schemas import UserResponseSchema, UserCreateSchema, UserUpdateSchema
from typing import List, Optional
from contextlib import asynccontextmanager
from database import Base, engine, get_db, Expense,User
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Startup tasks...")
    Base.metadata.create_all(bind = engine)

    yield

    print("Shutdown tasks...")

    


app = FastAPI(lifespan=lifespan)


# Expenses: List[ExpenseResponseSchema] = [
#     ExpenseResponseSchema(id=1, description="buy", amount=125.6),
#     ExpenseResponseSchema(id=2, description="food", amount=50.0)
# ]


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


    user = db.query(User).filter_by(id=expense.user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {expense.user_id} not found")

    new_expense = Expense(user_id=expense.user_id, description=expense.description, amount=expense.amount)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.get("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int, db:Session=Depends(get_db)):
    # for item in Expenses:
    #     if(item.id == id):
    #         return item

    query = db.query(Expense).filter_by(id=id)
    expense = get_or_404(query, "expense")
    return expense


@app.get("/expenses/{id}/user", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def get_expense_byId(id:int, db:Session=Depends(get_db)):

    query = db.query(Expense).filter_by(id=id)
    expense = get_or_404(query, "expense")
    return expense.user


@app.put("/expenses/{id}",response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def replace_expense(id:int, new_data: ExpenseCreateSchema, db:Session=Depends(get_db)):
    # for item in Expenses:
    #     if(item.id == id):
    #         item.description = new_data.description
    #         item.amount = new_data.amount
    #         return item

    query = db.query(Expense).filter_by(id=id)
    expense = get_or_404(query, "expense")

    expense.description = new_data.description
    expense.amount = new_data.amount
    db.commit()
    db.refresh(expense)
    return expense



@app.patch("/expenses/{id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
async def edit_expense(id:int, update_data: ExpenseUpdateSchema, db:Session=Depends(get_db) ):

    update_data = update_data.model_dump(exclude_unset=True)
    query = db.query(Expense).filter_by(id=id)
    expense = get_or_404(query, "expense")

    # for item in Expenses:
    #     if item.id == id:
    #         for key, value in update_data.items():
    #             if isinstance(value, str) and value.strip() == "":
    #                 continue
    #             if value is not None:
    #                 setattr(item, key, value)
    #         return item

    for key, value in update_data.items():
        if isinstance(value, str) and value.strip() == "":
            continue
        if value is not None:
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, db:Session=Depends(get_db)):

    # for i, item in enumerate(Expenses):
    #     if item.id == id:
    #         del Expenses[i]
    #         return 
        # {"message": f"Name with ID {id} deleted successfully"}

    query = db.query(Expense).filter_by(id=id)
    expense = get_or_404(query, "expense")
    db.delete(expense)
    db.commit()
    return
   

# *************************************** user endpoints ***************************************
@app.get("/users", response_model=List[UserResponseSchema], status_code=status.HTTP_200_OK)
async def retrieve_data(start_by:Optional[str] = Query(default=None, description="Filter users with name starts with start_by")
                        , db:Session=Depends(get_db)):
    
    q = db.query(User)
    if start_by is not None:
        q = q.filter(User.name.ilike(f"{start_by}%")).order_by(User.name.asc())
    
    results = q.all()
    if not results:
        return []
    return results


@app.post("/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema, db:Session=Depends(get_db)):

    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def get_user_byId(id:int, db:Session=Depends(get_db)):

    query = db.query(User).filter_by(id=id)
    user = get_or_404(query, "user")
    return user

@app.get("/users/{id}/expenses", response_model=List[ExpenseResponseSchema])
def get_user_expenses(id: int, db: Session = Depends(get_db)):
    query = db.query(User).filter_by(id=id)
    user = get_or_404(query, "user")
    return user.expenses



@app.put("/users/{id}",response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def replace_user(id:int, new_data: UserCreateSchema, db:Session=Depends(get_db)):

    query = db.query(User).filter_by(id=id)
    user = get_or_404(query, "user")
    user.name = new_data.name
    db.commit()
    db.refresh(user)
    return user



@app.patch("/users/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def edit_user(id:int, update_data: UserUpdateSchema, db:Session=Depends(get_db) ):

    update_data = update_data.model_dump(exclude_unset=True)
    query = db.query(User).filter_by(id=id)

    user = get_or_404(query, "user")
    for key, value in update_data.items():
        if isinstance(value, str) and value.strip() == "":
            continue
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
   

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db:Session=Depends(get_db)):

    query = db.query(User).filter_by(id=id)
    user = get_or_404(query, "user")
    db.delete(user)
    db.commit()
    return
    

def get_or_404(query, model_name="Object"):
    obj = query.one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    return obj