from fastapi import APIRouter

from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeCreatedResponse,
    EmployeeResponse,
)
from services import employee_service

router = APIRouter(prefix="/employees", tags=["Employee Details"])


@router.get("/", response_model=list[EmployeeResponse])
def get_employee():
    return employee_service.get_all_employees()


@router.post("/", response_model=EmployeeCreatedResponse)
def create_employee(employee: EmployeeCreate):
    return employee_service.create_employee(employee)
