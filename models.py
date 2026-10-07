from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    id: int
    name: str
    salary: int
    experience: int
