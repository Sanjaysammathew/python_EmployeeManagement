from pydantic import BaseModel,EmailStr

class EmployeeCreate(BaseModel) :
    name:str
    email:EmailStr
    department:str
    salary:int

class employeeUpdate(BaseModel) :
    name:str
    email:EmailStr
    department:str
    salary:int
