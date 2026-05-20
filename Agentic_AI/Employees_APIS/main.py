# import FastAPI
# FastAPI is the predefined class, used to develop API Calls
from fastapi import FastAPI

# import BaseModel
# BaseModel used to define Schema
from pydantic import BaseModel


# instantiate FastAPI
app = FastAPI()

# Define Schema (Rules & Regulations)
class Employee(BaseModel):
    emp_id:int
    emp_name:str
    department:str
    salary:float
    experience:int
    email:str
    is_active:bool

# DataBase
employees = [{
     "emp_id":111,
     "emp_name":"Emp1",
     "department":"CSE",
     "salary":10000,
     "experience":1,
     "email":"emp1@gmail.com",
     "is_active":True
    }]

@app.get("/")
def home():
    return {"message":"welcome to Fast API !!!"}

@app.get("/employees")
def get_all_employees():
    return {
        "total_employees" : len(employees),
        "data": employees
    }

# req param
@app.get("/employee/{emp_id}")
def get_employee(emp_id:int):
    for emp in employees:
        if emp["emp_id"] == emp_id:
            return emp
    return {"message":"Employee Not Found !!!"}


# POST
@app.post("/add-employee")
def add_employee(employee:Employee):
    employees.append(employee.dict())
    return {"message":"Employee Added Successfully !!!","employee":employee}

# PUT (Update)
@app.put("/update-employee/{emp_id}")
def update_employee(emp_id:int,updated_employee:Employee):
    for index,emp in enumerate(employees):
        if emp["emp_id"] == emp_id:
            employees[index] = updated_employee.dict()
            return {"message":"Employee Updated Successfully !!!","updated_data":updated_employee}
    return {"message":"Employee Not Found !!!"}

# DELETE
@app.delete("/delete-employee/{emp_id}")
def delete_employee(emp_id:int):
    for emp in employees:
        if emp["emp_id"] == emp_id:
            employees.remove(emp)
            return {"message":"Employee Removed Successfully !!!"}
    return {"message":"Employee Not Found !!!"}




