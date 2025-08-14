from fastapi import FastAPI, status, HTTPException

app = FastAPI()


students = [
    {"id":1, "name":"narges"},
    {"id":2, "name":"mina"},
    {"id":3, "name":"sara"},
    {"id":4, "name":"mahsa"},
    {"id":5, "name":"raha"}
]


@app.get("/")
async def root():
    return students


@app.get("/students/{id}")
async def get_stuname_byId(id:int):
    for stu in students:
        if(stu["id"] == id):
            return stu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

# create object 201 code
# @app.post("/students")
@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_stu(stu_name:str):
    students.append({"id":len(students)+1,"name":stu_name})
    return students[-1]


@app.put("/students/{id}")
async def update_name(id:int, name:str):
    for stu in students:
        if stu["id"] == id:
            stu['name'] = name
            return stu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")




@app.delete("/students/{item_id}")
def names_delete(item_id: int):
    for i, n in enumerate(students):
        if n["id"] == item_id:
            del students[i]
            return {"message": f"Name with ID {item_id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
