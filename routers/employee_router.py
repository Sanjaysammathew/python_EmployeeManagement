from fastapi import APIRouter
from models import EmployeeCreate

from crud.employee_crud import (
    get_students,
    post_students
)

router = APIRouter(
    prefix="/employees",
    tags=["Employee Details"]
)


@router.get("/")
def get_employee():
    return get_students()


@router.post("/")
def create_employee(employee: EmployeeCreate):
    return post_students(employee)