from fastapi import APIRouter

from schemas.employee_schema import EmployeeCreate
from services import employee_service

router = APIRouter(prefix="/employees")


@router.get("/")
def get_employees():
    return employee_service.get_all_employees()


@router.get("/{employee_id}")
def get_employee_by_id(employee_id: int):
    return employee_service.get_employee_by_id(employee_id)


@router.post("/")
def create_employee(employee: EmployeeCreate):
    return employee_service.create_employee(employee)


@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeCreate):
    return employee_service.update_employee(employee_id, employee)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    return employee_service.delete_employee(employee_id)
